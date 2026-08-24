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

from app.services.cover_letter_service import (
    CoverLetterService
)


class CoverLettersPage(QWidget):

    def __init__(self, main_window):

        super().__init__()

        self.main_window = main_window

        self.setup_ui()

        self.refresh_cover_letters()

    # ========================================================
    # UI
    # ========================================================

    def setup_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            50,
            40,
            50,
            40
        )

        layout.setSpacing(20)

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        header = QHBoxLayout()

        title_area = QVBoxLayout()

        title = QLabel(
            "Cover Letters"
        )

        title.setObjectName(
            "pageTitle"
        )

        subtitle = QLabel(
            "Create and manage personalized cover letters."
        )

        subtitle.setObjectName(
            "pageSubtitle"
        )

        title_area.addWidget(title)
        title_area.addWidget(subtitle)

        header.addLayout(title_area)

        header.addStretch()

        create_button = QPushButton(
            "New Cover Letter"
        )

        create_button.setObjectName(
            "primaryButton"
        )

        create_button.setIcon(
            qta.icon(
                "fa5s.plus",
                color="white"
            )
        )

        create_button.clicked.connect(
            self.create_cover_letter
        )

        header.addWidget(
            create_button
        )

        layout.addLayout(header)

        # ----------------------------------------------------
        # SEARCH AND SORT
        # ----------------------------------------------------

        controls = QHBoxLayout()

        self.search_input = QLineEdit()

        self.search_input.setPlaceholderText(
            "Search cover letters..."
        )

        self.search_input.setClearButtonEnabled(
            True
        )

        self.search_input.textChanged.connect(
            self.refresh_cover_letters
        )

        controls.addWidget(
            self.search_input,
            1
        )

        self.sort_combo = QComboBox()

        self.sort_combo.addItems([
            "Recently Edited",
            "Oldest",
            "Name A-Z"
        ])

        self.sort_combo.currentTextChanged.connect(
            self.refresh_cover_letters
        )

        controls.addWidget(
            self.sort_combo
        )

        layout.addLayout(controls)

        # ----------------------------------------------------
        # COVER LETTER LIST
        # ----------------------------------------------------

        self.scroll_area = QScrollArea()

        self.scroll_area.setWidgetResizable(
            True
        )

        self.scroll_area.setObjectName(
            "resumeScrollArea"
        )

        self.cards_container = QWidget()

        self.cards_layout = QGridLayout(
            self.cards_container
        )

        self.cards_layout.setContentsMargins(
            5,
            5,
            5,
            5
        )

        self.cards_layout.setSpacing(20)

        self.scroll_area.setWidget(
            self.cards_container
        )

        layout.addWidget(
            self.scroll_area,
            1
        )

    # ========================================================
    # REFRESH
    # ========================================================

    def clear_cards(self):

        while self.cards_layout.count():

            item = self.cards_layout.takeAt(0)

            widget = item.widget()

            if widget:
                widget.deleteLater()

    def refresh_cover_letters(self):

        self.clear_cards()

        cover_letters = (
            CoverLetterService.get_all_cover_letters(

                self.search_input.text(),

                self.sort_combo.currentText()
            )
        )

        if not cover_letters:

            empty = QLabel(
                "No cover letters yet.\n\n"
                "Create your first cover letter to get started."
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

        for index, cover_letter in enumerate(
            cover_letters
        ):

            card = self.create_cover_letter_card(
                cover_letter
            )

            row = index // 2

            column = index % 2

            self.cards_layout.addWidget(
                card,
                row,
                column
            )

    # ========================================================
    # CARD
    # ========================================================

    def create_cover_letter_card(
        self,
        cover_letter
    ):

        card = QFrame()

        card.setObjectName(
            "resumeCard"
        )

        layout = QVBoxLayout(card)

        layout.setContentsMargins(
            22,
            20,
            22,
            20
        )

        layout.setSpacing(12)

        # TOP

        top = QHBoxLayout()

        icon_label = QLabel()

        icon_label.setPixmap(
            qta.icon(
                "fa5s.envelope",
                color="#2D6CDF"
            ).pixmap(
                30,
                30
            )
        )

        top.addWidget(icon_label)

        top.addStretch()

        menu_button = QPushButton()

        menu_button.setObjectName(
            "cardMenuButton"
        )

        menu_button.setFixedSize(
            34,
            34
        )

        menu_button.setIcon(
            qta.icon(
                "fa5s.ellipsis-v"
            )
        )

        menu_button.clicked.connect(

            lambda checked=False,
            c=cover_letter,
            b=menu_button:

            self.show_cover_letter_menu(
                c,
                b
            )
        )

        top.addWidget(
            menu_button
        )

        layout.addLayout(top)

        # TITLE

        title = QLabel(
            cover_letter.title
        )

        title.setObjectName(
            "resumeCardTitle"
        )

        title.setWordWrap(True)

        layout.addWidget(title)

        # COMPANY

        company_text = (
            cover_letter.company_name
            or
            "No company specified"
        )

        company = QLabel(
            company_text
        )

        company.setObjectName(
            "resumeCardMeta"
        )

        layout.addWidget(
            company
        )

        # JOB POSITION

        position_text = (
            cover_letter.job_position
            or
            "No position specified"
        )

        position = QLabel(
            position_text
        )

        position.setObjectName(
            "resumeCardMeta"
        )

        layout.addWidget(
            position
        )

        # DATE

        updated = QLabel(
            "Last edited: "
            +
            cover_letter.updated_at.strftime(
                "%d %b %Y"
            )
        )

        updated.setObjectName(
            "resumeCardMeta"
        )

        layout.addWidget(
            updated
        )

        layout.addStretch()

        # OPEN BUTTON

        open_button = QPushButton(
            "Open Cover Letter"
        )

        open_button.setObjectName(
            "primaryButton"
        )

        open_button.clicked.connect(

            lambda:

            self.main_window.open_cover_letter_editor(
                cover_letter.id
            )
        )

        layout.addWidget(
            open_button
        )

        return card

    # ========================================================
    # MENU
    # ========================================================

    def show_cover_letter_menu(
        self,
        cover_letter,
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

            self.rename_cover_letter(
                cover_letter
            )

        elif action == duplicate_action:

            CoverLetterService.duplicate_cover_letter(
                cover_letter.id
            )

            self.refresh_cover_letters()

        elif action == delete_action:

            self.delete_cover_letter(
                cover_letter
            )

    # ========================================================
    # CREATE
    # ========================================================

    def create_cover_letter(self):

        dialog = QDialog(self)

        dialog.setWindowTitle(
            "Create Cover Letter"
        )

        dialog.setMinimumWidth(
            420
        )

        layout = QVBoxLayout(
            dialog
        )

        form = QFormLayout()

        title_input = QLineEdit()

        title_input.setPlaceholderText(
            "Example: Python Developer - Google"
        )

        form.addRow(
            "Cover Letter Name:",
            title_input
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

        layout.addWidget(
            buttons
        )

        if (
            dialog.exec()
            ==
            QDialog.DialogCode.Accepted
        ):

            title = (
                title_input.text().strip()
            )

            if not title:

                QMessageBox.warning(
                    self,
                    "Required",
                    "Please enter a cover letter name."
                )

                return

            cover_letter = (
                CoverLetterService.create_cover_letter(
                    title
                )
            )

            self.refresh_cover_letters()

            self.main_window.open_cover_letter_editor(
                cover_letter.id
            )

    # ========================================================
    # RENAME
    # ========================================================

    def rename_cover_letter(
        self,
        cover_letter
    ):

        dialog = QDialog(self)

        dialog.setWindowTitle(
            "Rename Cover Letter"
        )

        layout = QVBoxLayout(
            dialog
        )

        title_input = QLineEdit(
            cover_letter.title
        )

        layout.addWidget(
            title_input
        )

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

        layout.addWidget(
            buttons
        )

        if (
            dialog.exec()
            ==
            QDialog.DialogCode.Accepted
        ):

            new_title = (
                title_input.text().strip()
            )

            if new_title:

                CoverLetterService.rename_cover_letter(
                    cover_letter.id,
                    new_title
                )

                self.refresh_cover_letters()

    # ========================================================
    # DELETE
    # ========================================================

    def delete_cover_letter(
        self,
        cover_letter
    ):

        answer = QMessageBox.question(

            self,

            "Delete Cover Letter",

            f"Delete '{cover_letter.title}'?",

            QMessageBox.StandardButton.Yes
            |
            QMessageBox.StandardButton.No
        )

        if (
            answer
            ==
            QMessageBox.StandardButton.Yes
        ):

            CoverLetterService.delete_cover_letter(
                cover_letter.id
            )

            self.refresh_cover_letters()