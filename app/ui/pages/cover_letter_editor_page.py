from html import escape

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QTextEdit,
    QScrollArea,
    QSplitter,
    QFormLayout,
    QMessageBox,
)

from app.services.cover_letter_service import (
    CoverLetterService
)


class CoverLetterEditorPage(QWidget):

    def __init__(
        self,
        cover_letter_id,
        back_callback
    ):
        super().__init__()

        self.cover_letter_id = (
            cover_letter_id
        )

        self.back_callback = (
            back_callback
        )

        self.cover_letter = None

        self.setup_ui()
        self.load_cover_letter()
        self.connect_live_preview()

    # ========================================================
    # UI SETUP
    # ========================================================

    def setup_ui(self):

        main_layout = QVBoxLayout(
            self
        )

        main_layout.setContentsMargins(
            25,
            20,
            25,
            25
        )

        main_layout.setSpacing(
            15
        )

        self.create_top_bar(
            main_layout
        )

        splitter = QSplitter(
            Qt.Orientation.Horizontal
        )

        splitter.addWidget(
            self.create_editor_area()
        )

        splitter.addWidget(
            self.create_preview_area()
        )

        splitter.setSizes([
            620,
            500
        ])

        main_layout.addWidget(
            splitter,
            1
        )

    # ========================================================
    # TOP BAR
    # ========================================================

    def create_top_bar(
        self,
        layout
    ):

        top_bar = QHBoxLayout()

        back_button = QPushButton(
            "← Back"
        )

        back_button.clicked.connect(
            self.back_callback
        )

        top_bar.addWidget(
            back_button
        )

        self.editor_title = QLabel(
            "Cover Letter Editor"
        )

        self.editor_title.setObjectName(
            "editorTitle"
        )

        top_bar.addWidget(
            self.editor_title
        )

        top_bar.addStretch()

        self.save_button = QPushButton(
            "Save Changes"
        )

        self.save_button.setObjectName(
            "primaryButton"
        )

        self.save_button.clicked.connect(
            self.save_cover_letter
        )

        top_bar.addWidget(
            self.save_button
        )

        layout.addLayout(
            top_bar
        )

    # ========================================================
    # EDITOR AREA
    # ========================================================

    def create_editor_area(self):

        scroll = QScrollArea()

        scroll.setWidgetResizable(
            True
        )

        content = QWidget()

        layout = QVBoxLayout(
            content
        )

        layout.setContentsMargins(
            25,
            20,
            25,
            25
        )

        layout.setSpacing(
            15
        )

        title = QLabel(
            "Cover Letter Details"
        )

        title.setObjectName(
            "sectionEditorTitle"
        )

        subtitle = QLabel(
            "Add the recipient details and write your cover letter."
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

        form = QFormLayout()

        self.title_input = QLineEdit()

        self.title_input.setPlaceholderText(
            "e.g. Software Developer Application"
        )

        self.recipient_input = QLineEdit()

        self.recipient_input.setPlaceholderText(
            "Hiring Manager"
        )

        self.company_input = QLineEdit()

        self.company_input.setPlaceholderText(
            "Company name"
        )

        self.job_position_input = QLineEdit()

        self.job_position_input.setPlaceholderText(
            "Job position"
        )

        self.date_input = QLineEdit()

        self.date_input.setPlaceholderText(
            "e.g. 23 August 2026"
        )

        self.salutation_input = QLineEdit()

        self.salutation_input.setPlaceholderText(
            "Dear Hiring Manager,"
        )

        form.addRow(
            "Title:",
            self.title_input
        )

        form.addRow(
            "Recipient:",
            self.recipient_input
        )

        form.addRow(
            "Company:",
            self.company_input
        )

        form.addRow(
            "Job Position:",
            self.job_position_input
        )

        form.addRow(
            "Date:",
            self.date_input
        )

        form.addRow(
            "Salutation:",
            self.salutation_input
        )

        layout.addLayout(
            form
        )

        content_title = QLabel(
            "Letter Content"
        )

        content_title.setObjectName(
            "sectionEditorTitle"
        )

        layout.addSpacing(
            10
        )

        layout.addWidget(
            content_title
        )

        self.content_input = QTextEdit()

        self.content_input.setMinimumHeight(
            300
        )

        self.content_input.setPlaceholderText(
            "Write the main body of your cover letter here..."
        )

        layout.addWidget(
            self.content_input
        )

        closing_form = QFormLayout()

        self.closing_input = QLineEdit()

        self.closing_input.setPlaceholderText(
            "Sincerely,"
        )

        self.signature_input = QLineEdit()

        self.signature_input.setPlaceholderText(
            "Your full name"
        )

        closing_form.addRow(
            "Closing:",
            self.closing_input
        )

        closing_form.addRow(
            "Signature:",
            self.signature_input
        )

        layout.addLayout(
            closing_form
        )

        layout.addStretch()

        scroll.setWidget(
            content
        )

        return scroll

    # ========================================================
    # PREVIEW AREA
    # ========================================================

    def create_preview_area(self):

        scroll = QScrollArea()

        scroll.setWidgetResizable(
            True
        )

        preview_container = QWidget()

        preview_layout = QVBoxLayout(
            preview_container
        )

        preview_layout.setContentsMargins(
            25,
            20,
            25,
            25
        )

        preview_title = QLabel(
            "Live Preview"
        )

        preview_title.setObjectName(
            "sectionEditorTitle"
        )

        preview_layout.addWidget(
            preview_title
        )

        self.preview_content = QLabel()

        self.preview_content.setObjectName(
            "resumePreview"
        )

        self.preview_content.setTextFormat(
            Qt.TextFormat.RichText
        )

        self.preview_content.setWordWrap(
            True
        )

        self.preview_content.setAlignment(
            Qt.AlignmentFlag.AlignTop
            |
            Qt.AlignmentFlag.AlignLeft
        )

        self.preview_content.setContentsMargins(
            30,
            30,
            30,
            30
        )

        self.preview_content.setMinimumWidth(
            420
        )

        preview_layout.addWidget(
            self.preview_content
        )

        preview_layout.addStretch()

        scroll.setWidget(
            preview_container
        )

        return scroll

    # ========================================================
    # LOAD COVER LETTER
    # ========================================================

    def load_cover_letter(self):

        self.cover_letter = (
            CoverLetterService.get_cover_letter(
                self.cover_letter_id
            )
        )

        if not self.cover_letter:

            QMessageBox.warning(
                self,
                "Not Found",
                "Cover letter could not be found."
            )

            return

        self.editor_title.setText(
            self.cover_letter.title
        )

        self.title_input.setText(
            self.cover_letter.title
            or ""
        )

        self.recipient_input.setText(
            self.cover_letter.recipient_name
            or ""
        )

        self.company_input.setText(
            self.cover_letter.company_name
            or ""
        )

        self.job_position_input.setText(
            self.cover_letter.job_position
            or ""
        )

        self.date_input.setText(
            self.cover_letter.letter_date
            or ""
        )

        self.salutation_input.setText(
            self.cover_letter.salutation
            or ""
        )

        self.content_input.setPlainText(
            self.cover_letter.content
            or ""
        )

        self.closing_input.setText(
            self.cover_letter.closing
            or ""
        )

        self.signature_input.setText(
            self.cover_letter.signature_name
            or ""
        )

        self.update_preview()

    # ========================================================
    # LIVE PREVIEW CONNECTIONS
    # ========================================================

    def connect_live_preview(self):

        self.title_input.textChanged.connect(
            self.update_preview
        )

        self.recipient_input.textChanged.connect(
            self.update_preview
        )

        self.company_input.textChanged.connect(
            self.update_preview
        )

        self.job_position_input.textChanged.connect(
            self.update_preview
        )

        self.date_input.textChanged.connect(
            self.update_preview
        )

        self.salutation_input.textChanged.connect(
            self.update_preview
        )

        self.content_input.textChanged.connect(
            self.update_preview
        )

        self.closing_input.textChanged.connect(
            self.update_preview
        )

        self.signature_input.textChanged.connect(
            self.update_preview
        )

    # ========================================================
    # CURRENT DATA
    # ========================================================

    def get_current_data(self):

        return {

            "title":
                self.title_input
                .text()
                .strip(),

            "recipient_name":
                self.recipient_input
                .text()
                .strip(),

            "company_name":
                self.company_input
                .text()
                .strip(),

            "job_position":
                self.job_position_input
                .text()
                .strip(),

            "letter_date":
                self.date_input
                .text()
                .strip(),

            "salutation":
                self.salutation_input
                .text()
                .strip(),

            "content":
                self.content_input
                .toPlainText()
                .strip(),

            "closing":
                self.closing_input
                .text()
                .strip(),

            "signature_name":
                self.signature_input
                .text()
                .strip(),
        }

    # ========================================================
    # SAVE
    # ========================================================

    def save_cover_letter(self):

        data = (
            self.get_current_data()
        )

        if not data["title"]:

            QMessageBox.warning(
                self,
                "Required",
                "Please enter a title for the cover letter."
            )

            return

        success = (
            CoverLetterService
            .update_cover_letter(
                self.cover_letter_id,
                data
            )
        )

        if success:

            self.editor_title.setText(
                data["title"]
            )

            self.update_preview()

            QMessageBox.information(
                self,
                "Saved",
                "Your cover letter has been saved successfully."
            )

        else:

            QMessageBox.warning(
                self,
                "Error",
                "Could not save the cover letter."
            )

    # ========================================================
    # LIVE PREVIEW
    # ========================================================

    def update_preview(self):

        title = escape(
            self.title_input
            .text()
            .strip()
            or "Cover Letter"
        )

        recipient = escape(
            self.recipient_input
            .text()
            .strip()
        )

        company = escape(
            self.company_input
            .text()
            .strip()
        )

        job_position = escape(
            self.job_position_input
            .text()
            .strip()
        )

        letter_date = escape(
            self.date_input
            .text()
            .strip()
        )

        salutation = escape(
            self.salutation_input
            .text()
            .strip()
            or "Dear Hiring Manager,"
        )

        content = escape(
            self.content_input
            .toPlainText()
            .strip()
        ).replace(
            "\n",
            "<br>"
        )

        closing = escape(
            self.closing_input
            .text()
            .strip()
            or "Sincerely,"
        )

        signature = escape(
            self.signature_input
            .text()
            .strip()
        )

        header_html = ""

        if letter_date:

            header_html += (
                f"<p>{letter_date}</p>"
            )

        if recipient:

            header_html += (
                f"<p>{recipient}"
            )

            if company:

                header_html += (
                    f"<br>{company}"
                )

            header_html += (
                "</p>"
            )

        position_html = ""

        if job_position:

            position_html = (
                "<p>"
                "<b>Application for: "
                f"{job_position}"
                "</b>"
                "</p>"
            )

        content_html = ""

        if content:

            content_html = (
                f"<p>{content}</p>"
            )

        signature_html = ""

        if signature:

            signature_html = (
                f"<br>{signature}"
            )

        html = f"""
        <div style="
            background-color: white;
            padding: 35px;
            color: #222;
            font-family: Arial;
            line-height: 1.6;
        ">

            <div style="
                text-align: center;
                margin-bottom: 25px;
            ">
                <h2>{title}</h2>
            </div>

            {header_html}

            {position_html}

            <p>{salutation}</p>

            {content_html}

            <p>
                {closing}
                {signature_html}
            </p>

        </div>
        """

        self.preview_content.setText(
            html
        )