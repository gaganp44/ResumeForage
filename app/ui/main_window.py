from PySide6.QtCore import (
    Qt,
    QPropertyAnimation,
    QEasingCurve,
)

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QStackedWidget,
)

import qtawesome as qta

from app.ui.pages.home_page import HomePage
from app.ui.pages.resumes_page import ResumesPage
from app.ui.pages.cover_letters_page import CoverLettersPage
from app.ui.pages.job_match_page import JobMatchPage
from app.ui.pages.settings_page import SettingsPage


class MainWindow(QMainWindow):

    EXPANDED_WIDTH = 230
    COLLAPSED_WIDTH = 72

    def __init__(
        self,
        app
    ):

        super().__init__()

        # Save QApplication instance
        self.app = app

        self.setWindowTitle(
            "ResumeForge"
        )

        self.resize(
            1280,
            800
        )

        self.setMinimumSize(
            950,
            600
        )

        self.sidebar_expanded = True

        self.nav_buttons = []

        self.setup_ui()

    # ========================================================
    # MAIN UI
    # ========================================================

    def setup_ui(self):

        central_widget = QWidget()

        self.setCentralWidget(
            central_widget
        )

        main_layout = QHBoxLayout(
            central_widget
        )

        main_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        main_layout.setSpacing(
            0
        )

        # SIDEBAR

        self.sidebar = self.create_sidebar()

        self.sidebar.setFixedWidth(
            self.EXPANDED_WIDTH
        )

        main_layout.addWidget(
            self.sidebar
        )

        # CONTENT STACK

        self.stack = QStackedWidget()

        main_layout.addWidget(
            self.stack,
            1
        )

        # ====================================================
        # PAGES
        # ====================================================

        self.home_page = HomePage(
            self
        )

        self.resumes_page = ResumesPage(
            self
        )

        self.cover_letters_page = (
            CoverLettersPage(
                self
            )
        )

        self.job_match_page = (
            JobMatchPage()
        )

        # IMPORTANT:
        # Pass the change_theme method as callback
        self.settings_page = (
            SettingsPage(
                self.change_theme
            )
        )

        # ====================================================
        # ADD PAGES
        # ====================================================

        self.stack.addWidget(
            self.home_page
        )

        self.stack.addWidget(
            self.resumes_page
        )

        self.stack.addWidget(
            self.cover_letters_page
        )

        self.stack.addWidget(
            self.job_match_page
        )

        self.stack.addWidget(
            self.settings_page
        )

        self.set_page(
            0
        )

    # ========================================================
    # CREATE SIDEBAR
    # ========================================================

    def create_sidebar(self):

        sidebar = QWidget()

        sidebar.setObjectName(
            "sidebar"
        )

        self.sidebar_layout = QVBoxLayout(
            sidebar
        )

        self.sidebar_layout.setContentsMargins(
            12,
            18,
            12,
            18
        )

        self.sidebar_layout.setSpacing(
            8
        )

        # TOP AREA

        top_layout = QHBoxLayout()

        self.brand_label = QLabel(
            "ResumeForge"
        )

        self.brand_label.setObjectName(
            "appName"
        )

        self.toggle_button = QPushButton()

        self.toggle_button.setObjectName(
            "sidebarToggle"
        )

        self.toggle_button.setFixedSize(
            34,
            34
        )

        self.toggle_button.setToolTip(
            "Collapse sidebar"
        )

        self.toggle_button.setIcon(
            qta.icon(
                "fa5s.bars",
                color="#6B7280"
            )
        )

        self.toggle_button.clicked.connect(
            self.toggle_sidebar
        )

        top_layout.addWidget(
            self.brand_label
        )

        top_layout.addStretch()

        top_layout.addWidget(
            self.toggle_button
        )

        self.sidebar_layout.addLayout(
            top_layout
        )

        # TAGLINE

        self.tagline_label = QLabel(
            "Build. Tailor. Apply."
        )

        self.tagline_label.setObjectName(
            "sidebarTagline"
        )

        self.sidebar_layout.addWidget(
            self.tagline_label
        )

        self.sidebar_layout.addSpacing(
            25
        )

        # NAVIGATION

        self.create_nav_button(
            "Home",
            "fa5s.home",
            0
        )

        self.create_nav_button(
            "Resumes",
            "fa5s.file-alt",
            1
        )

        self.create_nav_button(
            "Cover Letters",
            "fa5s.envelope",
            2
        )

        self.create_nav_button(
            "Job Match",
            "fa5s.bullseye",
            3
        )

        self.sidebar_layout.addStretch()

        self.create_nav_button(
            "Settings",
            "fa5s.cog",
            4
        )

        return sidebar

    # ========================================================
    # CREATE NAV BUTTON
    # ========================================================

    def create_nav_button(
        self,
        text,
        icon_name,
        page_index
    ):

        button = QPushButton(
            text
        )

        button.setObjectName(
            "navButton"
        )

        button.setCheckable(
            True
        )

        button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        button.setToolTip(
            text
        )

        button.setProperty(
            "nav_text",
            text
        )

        button.setIcon(
            qta.icon(
                icon_name,
                color="#6B7280"
            )
        )

        button.clicked.connect(
            lambda checked=False,
            index=page_index:
            self.set_page(
                index
            )
        )

        self.sidebar_layout.addWidget(
            button
        )

        self.nav_buttons.append(
            button
        )

    # ========================================================
    # CHANGE THEME
    # ========================================================

    def change_theme(
        self,
        theme_name
    ):

        try:

            from main import apply_theme

            apply_theme(
                self.app,
                theme_name
            )

            print(
                f"Theme changed successfully: {theme_name}"
            )

        except Exception as error:

            print(
                "Theme change error:"
            )

            print(
                error
            )

    # ========================================================
    # TOGGLE SIDEBAR
    # ========================================================

    def toggle_sidebar(self):

        current_width = self.sidebar.width()

        if self.sidebar_expanded:

            target_width = (
                self.COLLAPSED_WIDTH
            )

            for button in self.nav_buttons:

                button.setText(
                    ""
                )

            self.brand_label.hide()

            self.tagline_label.hide()

            self.toggle_button.setToolTip(
                "Expand sidebar"
            )

            self.sidebar_expanded = False

        else:

            target_width = (
                self.EXPANDED_WIDTH
            )

            for button in self.nav_buttons:

                text = button.property(
                    "nav_text"
                )

                button.setText(
                    text
                )

            self.brand_label.show()

            self.tagline_label.show()

            self.toggle_button.setToolTip(
                "Collapse sidebar"
            )

            self.sidebar_expanded = True

        self.min_animation = QPropertyAnimation(
            self.sidebar,
            b"minimumWidth"
        )

        self.min_animation.setDuration(
            250
        )

        self.min_animation.setStartValue(
            current_width
        )

        self.min_animation.setEndValue(
            target_width
        )

        self.min_animation.setEasingCurve(
            QEasingCurve.Type.InOutCubic
        )

        self.max_animation = QPropertyAnimation(
            self.sidebar,
            b"maximumWidth"
        )

        self.max_animation.setDuration(
            250
        )

        self.max_animation.setStartValue(
            current_width
        )

        self.max_animation.setEndValue(
            target_width
        )

        self.max_animation.setEasingCurve(
            QEasingCurve.Type.InOutCubic
        )

        self.min_animation.start()

        self.max_animation.start()

    # ========================================================
    # CHANGE PAGE
    # ========================================================

    def set_page(
        self,
        page_index
    ):

        self.stack.setCurrentIndex(
            page_index
        )

        self.update_navigation(
            page_index
        )

        if page_index == 0:

            self.home_page.refresh_home()

        elif page_index == 1:

            self.resumes_page.refresh_resumes()

        elif page_index == 2:

            self.cover_letters_page.refresh_cover_letters()

    # ========================================================
    # CREATE NEW RESUME
    # ========================================================

    def create_new_resume(self):

        self.resumes_page.create_resume()

    # ========================================================
    # OPEN RESUME EDITOR
    # ========================================================

    def open_resume_editor(
        self,
        resume_id
    ):

        from app.ui.pages.resume_editor_page import (
            ResumeEditorPage
        )

        editor = ResumeEditorPage(
            resume_id,
            self.show_resume_library
        )

        self.stack.addWidget(
            editor
        )

        self.stack.setCurrentWidget(
            editor
        )

        self.update_navigation(
            1
        )

    # ========================================================
    # SHOW RESUME LIBRARY
    # ========================================================

    def show_resume_library(self):

        self.stack.setCurrentWidget(
            self.resumes_page
        )

        self.resumes_page.refresh_resumes()

        self.home_page.refresh_home()

        self.update_navigation(
            1
        )

    # ========================================================
    # OPEN COVER LETTER EDITOR
    # ========================================================

    def open_cover_letter_editor(
        self,
        cover_letter_id
    ):

        from app.ui.pages.cover_letter_editor_page import (
            CoverLetterEditorPage
        )

        editor = CoverLetterEditorPage(
            cover_letter_id,
            self.show_cover_letter_library
        )

        self.stack.addWidget(
            editor
        )

        self.stack.setCurrentWidget(
            editor
        )

        self.update_navigation(
            2
        )

    # ========================================================
    # SHOW COVER LETTER LIBRARY
    # ========================================================

    def show_cover_letter_library(self):

        self.stack.setCurrentWidget(
            self.cover_letters_page
        )

        self.cover_letters_page.refresh_cover_letters()

        self.update_navigation(
            2
        )

    # ========================================================
    # ACTIVE NAVIGATION
    # ========================================================

    def update_navigation(
        self,
        active_index
    ):

        for index, button in enumerate(
            self.nav_buttons
        ):

            button.setChecked(
                index == active_index
            )