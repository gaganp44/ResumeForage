from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QScrollArea,
    QMessageBox,
)

from app.services.resume_service import ResumeService


class HomePage(QWidget):

    def __init__(self, main_window):

        super().__init__()

        self.main_window = main_window

        self.setup_ui()

    # ========================================================
    # UI SETUP
    # ========================================================

    def setup_ui(self):

        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(
            35, 30, 35, 30
        )

        main_layout.setSpacing(20)

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        title = QLabel("RESUMEFORGE")
        title.setObjectName("dashboardBrand")

        subtitle = QLabel("Build. Tailor. Apply.")
        subtitle.setObjectName("dashboardSubtitle")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        main_layout.addSpacing(20)

        # ----------------------------------------------------
        # CREATE RESUME CARD
        # ----------------------------------------------------

        create_card = QFrame()
        create_card.setObjectName("createResumeCard")

        create_layout = QVBoxLayout(create_card)

        create_layout.setContentsMargins(
            22, 18, 22, 18
        )

        create_title = QLabel("+ Create New Resume")
        create_title.setObjectName("createCardTitle")

        create_text = QLabel(
            "Start building a professional resume"
        )
        create_text.setObjectName("createCardText")

        create_button = QPushButton(
            "Create Resume"
        )
        create_button.setObjectName("primaryButton")

        create_button.clicked.connect(
            self.create_new_resume
        )

        create_layout.addWidget(create_title)
        create_layout.addWidget(create_text)
        create_layout.addSpacing(8)
        create_layout.addWidget(create_button)

        main_layout.addWidget(create_card)

        # ----------------------------------------------------
        # YOUR RESUMES
        # ----------------------------------------------------

        resumes_title = QLabel("YOUR RESUMES")
        resumes_title.setObjectName(
            "dashboardSectionTitle"
        )

        main_layout.addWidget(resumes_title)

        # ----------------------------------------------------
        # RESUME LIST
        # ----------------------------------------------------

        self.scroll_area = QScrollArea()

        self.scroll_area.setWidgetResizable(True)

        self.scroll_area.setFrameShape(
            QFrame.Shape.NoFrame
        )

        self.resumes_container = QWidget()

        self.resumes_layout = QVBoxLayout(
            self.resumes_container
        )

        self.resumes_layout.setSpacing(12)

        self.resumes_layout.setContentsMargins(
            0, 0, 0, 0
        )

        self.resumes_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop
        )

        self.scroll_area.setWidget(
            self.resumes_container
        )

        main_layout.addWidget(
            self.scroll_area,
            1
        )

        self.refresh_home()

    # ========================================================
    # CREATE NEW RESUME
    # ========================================================

    def create_new_resume(self):

        # Use the existing create method from ResumesPage
        self.main_window.resumes_page.create_resume()

    # ========================================================
    # REFRESH DASHBOARD
    # ========================================================

    def refresh_home(self):

        self.clear_resume_cards()

        resumes = ResumeService.get_all_resumes()

        if not resumes:

            empty = QLabel(
                "No resumes created yet.\n\n"
                "Create your first resume to get started."
            )

            empty.setObjectName(
                "emptyResumeMessage"
            )

            empty.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            self.resumes_layout.addWidget(empty)

            return

        for resume in resumes:

            card = self.create_resume_card(
                resume
            )

            self.resumes_layout.addWidget(card)

        self.resumes_layout.addStretch()

    # ========================================================
    # CREATE RESUME CARD
    # ========================================================

    def create_resume_card(self, resume):

        card = QFrame()

        card.setObjectName(
            "dashboardResumeCard"
        )

        layout = QHBoxLayout(card)

        layout.setContentsMargins(
            18, 14, 18, 14
        )

        layout.setSpacing(15)

        # ----------------------------------------------------
        # RESUME INFORMATION
        # ----------------------------------------------------

        info_layout = QVBoxLayout()

        resume_title = (
            resume.title
            if resume.title
            else "Untitled Resume"
        )

        title = QLabel(resume_title)

        title.setObjectName(
            "dashboardResumeTitle"
        )

        template_name = (
            getattr(
                resume,
                "template_name",
                None
            )
            or "Modern"
        )

        template = QLabel(
            f"{template_name} Template"
        )

        template.setObjectName(
            "dashboardResumeMeta"
        )

        info_layout.addWidget(title)
        info_layout.addWidget(template)

        layout.addLayout(
            info_layout,
            1
        )

        # ----------------------------------------------------
        # OPEN BUTTON
        # ----------------------------------------------------

        open_button = QPushButton("Open")

        open_button.setObjectName(
            "secondaryButton"
        )

        open_button.clicked.connect(
            lambda checked=False,
            resume_id=resume.id:
            self.open_resume(resume_id)
        )

        layout.addWidget(open_button)

        # ----------------------------------------------------
        # DELETE BUTTON
        # ----------------------------------------------------

        delete_button = QPushButton("Delete")

        delete_button.setObjectName(
            "deleteButton"
        )

        delete_button.clicked.connect(
            lambda checked=False,
            resume_id=resume.id,
            title=resume_title:
            self.delete_resume(
                resume_id,
                title
            )
        )

        layout.addWidget(delete_button)

        return card

    # ========================================================
    # OPEN RESUME
    # ========================================================

    def open_resume(self, resume_id):

        self.main_window.open_resume_editor(
            resume_id
        )

    # ========================================================
    # DELETE RESUME
    # ========================================================

    def delete_resume(
        self,
        resume_id,
        title
    ):

        answer = QMessageBox.question(
            self,
            "Delete Resume",
            (
                f"Are you sure you want to delete "
                f"'{title}'?"
            ),
            QMessageBox.StandardButton.Yes
            |
            QMessageBox.StandardButton.No
        )

        if (
            answer
            != QMessageBox.StandardButton.Yes
        ):
            return

        success = ResumeService.delete_resume(
            resume_id
        )

        if success:

            self.refresh_home()

            # Refresh resume library if available
            if hasattr(
                self.main_window,
                "resumes_page"
            ):

                self.main_window.resumes_page.refresh_resumes()

    # ========================================================
    # CLEAR RESUME CARDS
    # ========================================================

    def clear_resume_cards(self):

        while self.resumes_layout.count() > 0:

            item = self.resumes_layout.takeAt(0)

            if item is None:
                continue

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

    # ========================================================
    # SHOW EVENT
    # ========================================================

    def showEvent(self, event):

        super().showEvent(event)

        self.refresh_home()