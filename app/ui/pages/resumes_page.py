from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QScrollArea,
    QGridLayout,
    QFrame,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QMessageBox,
    QMenu,
)

import qtawesome as qta

from app.services.resume_service import ResumeService


class ResumesPage(QWidget):

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        self.setup_ui()
        self.refresh_resumes()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        layout.setContentsMargins(50, 40, 50, 40)
        layout.setSpacing(20)

        header = QHBoxLayout()

        title_area = QVBoxLayout()

        title = QLabel("My Resumes")
        title.setObjectName("pageTitle")

        subtitle = QLabel(
            "Create, organize and manage different versions of your resume."
        )
        subtitle.setObjectName("pageSubtitle")

        title_area.addWidget(title)
        title_area.addWidget(subtitle)

        header.addLayout(title_area)
        header.addStretch()

        create_button = QPushButton("New Resume")
        create_button.setObjectName("primaryButton")

        create_button.setIcon(
            qta.icon(
                "fa5s.plus",
                color="white"
            )
        )

        create_button.clicked.connect(
            self.create_resume
        )

        header.addWidget(create_button)

        layout.addLayout(header)

        controls = QHBoxLayout()

        self.search_input = QLineEdit()

        self.search_input.setPlaceholderText(
            "Search resumes..."
        )

        self.search_input.setClearButtonEnabled(True)

        self.search_input.textChanged.connect(
            self.refresh_resumes
        )

        controls.addWidget(
            self.search_input,
            1
        )

        self.sort_combo = QComboBox()

        self.sort_combo.addItems([
            "Recently Edited",
            "Oldest",
            "Name A-Z",
        ])

        self.sort_combo.currentTextChanged.connect(
            self.refresh_resumes
        )

        controls.addWidget(self.sort_combo)

        layout.addLayout(controls)

        self.scroll_area = QScrollArea()

        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("resumeScrollArea")

        self.cards_container = QWidget()

        self.cards_layout = QGridLayout(
            self.cards_container
        )

        self.cards_layout.setContentsMargins(
            5, 5, 5, 5
        )

        self.cards_layout.setSpacing(20)

        self.scroll_area.setWidget(
            self.cards_container
        )

        layout.addWidget(
            self.scroll_area,
            1
        )

    def clear_cards(self):
        while self.cards_layout.count():

            item = self.cards_layout.takeAt(0)

            widget = item.widget()

            if widget:
                widget.deleteLater()

    def refresh_resumes(self):
        self.clear_cards()

        resumes = ResumeService.get_all_resumes(
            self.search_input.text(),
            self.sort_combo.currentText()
        )

        if not resumes:

            empty = QLabel(
                "No resumes yet.\n\n"
                "Create your first resume to get started."
            )

            empty.setObjectName(
                "emptyResumeMessage"
            )

            empty.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            self.cards_layout.addWidget(
                empty,
                0,
                0
            )

            return

        for index, resume in enumerate(resumes):

            card = self.create_resume_card(resume)

            row = index // 2
            column = index % 2

            self.cards_layout.addWidget(
                card,
                row,
                column
            )

    def create_resume_card(self, resume):
        card = QFrame()

        card.setObjectName("resumeCard")

        layout = QVBoxLayout(card)

        layout.setContentsMargins(
            22, 20, 22, 20
        )

        layout.setSpacing(12)

        top = QHBoxLayout()

        icon_label = QLabel()

        icon_label.setPixmap(
            qta.icon(
                "fa5s.file-alt",
                color="#2D6CDF"
            ).pixmap(30, 30)
        )

        top.addWidget(icon_label)
        top.addStretch()

        menu_button = QPushButton()

        menu_button.setObjectName(
            "cardMenuButton"
        )

        menu_button.setFixedSize(34, 34)

        menu_button.setIcon(
            qta.icon("fa5s.ellipsis-v")
        )

        menu_button.clicked.connect(
            lambda checked=False,
            r=resume,
            b=menu_button:
            self.show_resume_menu(r, b)
        )

        top.addWidget(menu_button)

        layout.addLayout(top)

        title = QLabel(resume.title)

        title.setObjectName(
            "resumeCardTitle"
        )

        title.setWordWrap(True)

        layout.addWidget(title)

        template = QLabel(
            f"{resume.template_name} Template"
        )

        template.setObjectName(
            "resumeCardMeta"
        )

        layout.addWidget(template)

        updated = QLabel(
            "Last edited: "
            + resume.updated_at.strftime(
                "%d %b %Y"
            )
        )

        updated.setObjectName(
            "resumeCardMeta"
        )

        layout.addWidget(updated)

        layout.addStretch()

        open_button = QPushButton(
            "Open Resume"
        )

        open_button.setObjectName(
            "primaryButton"
        )

        open_button.clicked.connect(
            lambda:
            self.main_window.open_resume_editor(
                resume.id
            )
        )

        layout.addWidget(open_button)

        return card

    def show_resume_menu(
        self,
        resume,
        button
    ):
        menu = QMenu(self)

        rename_action = menu.addAction(
            "Rename"
        )

        duplicate_action = menu.addAction(
            "Duplicate"
        )

        menu.addSeparator()

        delete_action = menu.addAction(
            "Delete"
        )

        action = menu.exec(
            button.mapToGlobal(
                button.rect().bottomLeft()
            )
        )

        if action == rename_action:

            self.rename_resume(resume)

        elif action == duplicate_action:

            ResumeService.duplicate_resume(
                resume.id
            )

            self.refresh_resumes()

        elif action == delete_action:

            self.delete_resume(resume)

    def create_resume(self):
        dialog = QDialog(self)

        dialog.setWindowTitle(
            "Create New Resume"
        )

        dialog.setMinimumWidth(400)

        layout = QVBoxLayout(dialog)

        form = QFormLayout()

        name_input = QLineEdit()

        name_input.setPlaceholderText(
            "Example: Software Developer Resume"
        )

        template_combo = QComboBox()

        template_combo.addItems([
            "Modern",
            "Classic",
            "Minimal",
        ])

        form.addRow(
            "Resume Name:",
            name_input
        )

        form.addRow(
            "Template:",
            template_combo
        )

        layout.addLayout(form)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            |
            QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(
            dialog.accept
        )

        buttons.rejected.connect(
            dialog.reject
        )

        layout.addWidget(buttons)

        if dialog.exec() == QDialog.DialogCode.Accepted:

            title = name_input.text().strip()

            if not title:

                QMessageBox.warning(
                    self,
                    "Required",
                    "Please enter a resume name."
                )

                return

            resume = ResumeService.create_resume(
                title,
                template_combo.currentText()
            )

            self.refresh_resumes()

            self.main_window.open_resume_editor(
                resume.id
            )

    def rename_resume(self, resume):
        dialog = QDialog(self)

        dialog.setWindowTitle(
            "Rename Resume"
        )

        layout = QVBoxLayout(dialog)

        name_input = QLineEdit(
            resume.title
        )

        layout.addWidget(name_input)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            |
            QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(
            dialog.accept
        )

        buttons.rejected.connect(
            dialog.reject
        )

        layout.addWidget(buttons)

        if dialog.exec() == QDialog.DialogCode.Accepted:

            new_title = name_input.text().strip()

            if new_title:

                ResumeService.rename_resume(
                    resume.id,
                    new_title
                )

                self.refresh_resumes()

    def delete_resume(self, resume):
        answer = QMessageBox.question(
            self,
            "Delete Resume",
            f"Delete '{resume.title}'?",
            QMessageBox.StandardButton.Yes
            |
            QMessageBox.StandardButton.No
        )

        if answer == QMessageBox.StandardButton.Yes:

            ResumeService.delete_resume(
                resume.id
            )

            self.refresh_resumes()