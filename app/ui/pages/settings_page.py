from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QFrame,
)


class SettingsPage(QWidget):

    def __init__(
        self,
        change_theme_callback
    ):

        super().__init__()

        self.change_theme_callback = (
            change_theme_callback
        )

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            50,
            40,
            50,
            40
        )

        layout.setSpacing(
            20
        )

        # PAGE HEADER

        title = QLabel(
            "Settings"
        )

        title.setObjectName(
            "pageTitle"
        )

        subtitle = QLabel(
            "Customize your ResumeForge experience."
        )

        subtitle.setObjectName(
            "pageSubtitle"
        )

        layout.addWidget(
            title
        )

        layout.addWidget(
            subtitle
        )

        # THEME CARD

        theme_card = QFrame()

        theme_card.setObjectName(
            "workspaceCard"
        )

        card_layout = QVBoxLayout(
            theme_card
        )

        theme_title = QLabel(
            "Application Theme"
        )

        theme_title.setObjectName(
            "cardTitle"
        )

        theme_text = QLabel(
            "Choose between light and dark mode."
        )

        theme_text.setObjectName(
            "cardSubtitle"
        )

        # THEME COMBOBOX

        self.theme_combo = QComboBox()

        self.theme_combo.addItems(
            [
                "Dark",
                "Light",
            ]
        )

        self.theme_combo.currentTextChanged.connect(
            self.change_theme
        )

        card_layout.addWidget(
            theme_title
        )

        card_layout.addWidget(
            theme_text
        )

        card_layout.addSpacing(
            10
        )

        card_layout.addWidget(
            self.theme_combo
        )

        layout.addWidget(
            theme_card
        )

        layout.addStretch()

    # ========================================================
    # CHANGE THEME
    # ========================================================

    def change_theme(
        self,
        theme_name
    ):

        theme_name = (
            theme_name
            .lower()
            .strip()
        )

        print(
            f"Theme selected: {theme_name}"
        )

        self.change_theme_callback(
            theme_name
        )