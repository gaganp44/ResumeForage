import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from app.ui.main_window import MainWindow


# ============================================================
# THEME COLORS
# ============================================================

THEMES = {

    "dark": {

        "BACKGROUND": "#171717",
        "SIDEBAR_BG": "#202020",
        "CARD_BG": "#262626",
        "CARD_HOVER": "#2D2D2D",

        "TEXT_PRIMARY": "#F5F5F5",
        "TEXT_SECONDARY": "#C5C5C5",
        "TEXT_MUTED": "#8F8F8F",

        "BORDER": "#3A3A3A",
        "BORDER_LIGHT": "#4A4A4A",

        "HOVER_BG": "#303030",
        "ACTIVE_BG": "#3A2A1B",

        "ACCENT": "#E69A3A",
        "ACCENT_HOVER": "#F0AA4D",

        "INPUT_BG": "#242424",

        "BUTTON_TEXT": "#FFFFFF",

        "SCROLLBAR_BG": "#202020",
        "SCROLLBAR_HANDLE": "#555555",

        "DANGER": "#E05252",
        "DANGER_BG": "#3A2020",

        "SUCCESS": "#4CAF7D",
    },

    "light": {

        "BACKGROUND": "#F6F7F9",
        "SIDEBAR_BG": "#FFFFFF",
        "CARD_BG": "#FFFFFF",
        "CARD_HOVER": "#FAFAFA",

        "TEXT_PRIMARY": "#1F2937",
        "TEXT_SECONDARY": "#4B5563",
        "TEXT_MUTED": "#6B7280",

        "BORDER": "#E2E5E9",
        "BORDER_LIGHT": "#D1D5DB",

        "HOVER_BG": "#F1F3F5",
        "ACTIVE_BG": "#FFF3E0",

        "ACCENT": "#E69A3A",
        "ACCENT_HOVER": "#D88725",

        "INPUT_BG": "#FFFFFF",

        "BUTTON_TEXT": "#FFFFFF",

        "SCROLLBAR_BG": "#F1F3F5",
        "SCROLLBAR_HANDLE": "#B0B5BD",

        "DANGER": "#D32F2F",
        "DANGER_BG": "#FFF0F0",

        "SUCCESS": "#2E7D5B",
    }
}


# ============================================================
# APPLY THEME
# ============================================================

def apply_theme(app, theme_name):

    project_root = Path(__file__).resolve().parent

    stylesheet_path = (
        project_root
        / "resources"
        / "styles"
        / "main.qss"
    )

    if not stylesheet_path.exists():

        print(
            "WARNING: Stylesheet not found:"
        )

        print(stylesheet_path)

        return

    try:

        stylesheet = stylesheet_path.read_text(
            encoding="utf-8"
        )

        theme = THEMES.get(
            theme_name,
            THEMES["dark"]
        )

        for name, value in theme.items():

            placeholder = (
                "{{"
                + name
                + "}}"
            )

            stylesheet = stylesheet.replace(
                placeholder,
                value
            )

        app.setStyleSheet(
            stylesheet
        )

        print(
            f"Theme applied successfully: {theme_name}"
        )

    except Exception as error:

        print(
            "Theme error:"
        )

        print(error)


# ============================================================
# MAIN APPLICATION
# ============================================================

def main():

    app = QApplication(
        sys.argv
    )

    app.setApplicationName(
        "ResumeForge"
    )

    # Start application in dark mode
    apply_theme(
        app,
        "dark"
    )

    # Pass QApplication to MainWindow
    window = MainWindow(
        app
    )

    window.show()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":

    main()