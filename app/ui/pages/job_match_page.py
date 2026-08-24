from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
)


class JobMatchPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        layout.setContentsMargins(50, 40, 50, 40)

        title = QLabel("Job Match")
        title.setObjectName("pageTitle")

        subtitle = QLabel(
            "A simple resume and job-description comparison feature can be added later."
        )
        subtitle.setObjectName("pageSubtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        layout.addStretch()

        message = QLabel(
            "Job Match will be developed as a simple keyword comparison feature."
        )

        message.setObjectName("emptyResumeMessage")
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(message)