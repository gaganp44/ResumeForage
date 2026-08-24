import json

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
    QStackedWidget,
    QFormLayout,
    QFrame,
    QMessageBox,
    QDialog,
    QDialogButtonBox,
    QSplitter,
    QFileDialog,
)

from app.services.resume_service import ResumeService
from app.services.export_service import ExportService
from app.templates.renderers import ResumeRenderer


class ResumeEditorPage(QWidget):

    def __init__(
        self,
        resume_id,
        back_callback
    ):
        super().__init__()

        self.resume_id = resume_id
        self.back_callback = back_callback

        self.resume = None

        self.experience_data = []
        self.education_data = []
        self.projects_data = []
        self.certifications_data = []

        self.setup_ui()
        self.connect_live_preview()
        self.load_resume()

    # =========================================================
    # UI SETUP
    # =========================================================

    def setup_ui(self):

        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(
            25,
            20,
            25,
            25
        )

        main_layout.setSpacing(15)

        self.create_top_bar(
            main_layout
        )

        splitter = QSplitter(
            Qt.Orientation.Horizontal
        )

        editor_area = (
            self.create_editor_area()
        )

        preview_area = (
            self.create_preview_area()
        )

        splitter.addWidget(
            editor_area
        )

        splitter.addWidget(
            preview_area
        )

        splitter.setSizes([
            620,
            500
        ])

        main_layout.addWidget(
            splitter,
            1
        )

    # =========================================================
    # TOP BAR
    # =========================================================

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

        self.resume_title = QLabel(
            "Resume Editor"
        )

        self.resume_title.setObjectName(
            "editorTitle"
        )

        top_bar.addWidget(
            self.resume_title
        )

        top_bar.addStretch()

        self.template_label = QLabel(
            "Template: Modern"
        )

        self.template_label.setObjectName(
            "templateLabel"
        )

        top_bar.addWidget(
            self.template_label
        )

        self.export_pdf_button = QPushButton(
            "Export PDF"
        )

        self.export_pdf_button.clicked.connect(
            self.export_pdf
        )

        top_bar.addWidget(
            self.export_pdf_button
        )

        self.export_docx_button = QPushButton(
            "Export DOCX"
        )

        self.export_docx_button.clicked.connect(
            self.export_docx
        )

        top_bar.addWidget(
            self.export_docx_button
        )

        self.save_button = QPushButton(
            "Save Changes"
        )

        self.save_button.setObjectName(
            "primaryButton"
        )

        self.save_button.clicked.connect(
            self.save_resume
        )

        top_bar.addWidget(
            self.save_button
        )

        layout.addLayout(
            top_bar
        )

    # =========================================================
    # EDITOR AREA
    # =========================================================

    def create_editor_area(self):

        container = QWidget()

        layout = QHBoxLayout(
            container
        )

        layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        section_menu = QVBoxLayout()

        section_menu.setSpacing(6)

        sections = [
            ("Personal Info", 0),
            ("Summary", 1),
            ("Experience", 2),
            ("Education", 3),
            ("Skills", 4),
            ("Projects", 5),
            ("Certifications", 6),
            ("Languages", 7),
        ]

        for text, index in sections:

            button = QPushButton(
                text
            )

            button.setObjectName(
                "editorNavButton"
            )

            button.clicked.connect(
                lambda checked=False,
                i=index:
                self.editor_stack.setCurrentIndex(
                    i
                )
            )

            section_menu.addWidget(
                button
            )

        section_menu.addStretch()

        layout.addLayout(
            section_menu
        )

        self.editor_stack = QStackedWidget()

        self.editor_stack.addWidget(
            self.create_personal_page()
        )

        self.editor_stack.addWidget(
            self.create_summary_page()
        )

        self.editor_stack.addWidget(
            self.create_experience_page()
        )

        self.editor_stack.addWidget(
            self.create_education_page()
        )

        self.editor_stack.addWidget(
            self.create_skills_page()
        )

        self.editor_stack.addWidget(
            self.create_projects_page()
        )

        self.editor_stack.addWidget(
            self.create_certifications_page()
        )

        self.editor_stack.addWidget(
            self.create_languages_page()
        )

        layout.addWidget(
            self.editor_stack,
            1
        )

        return container

    # =========================================================
    # COMMON SCROLL PAGE
    # =========================================================

    def create_scroll_page(self):

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
            15,
            25,
            25
        )

        layout.setSpacing(15)

        scroll.setWidget(
            content
        )

        return scroll, layout

    # =========================================================
    # SECTION TITLE
    # =========================================================

    def create_section_title(
        self,
        layout,
        title,
        subtitle
    ):

        title_label = QLabel(
            title
        )

        title_label.setObjectName(
            "sectionEditorTitle"
        )

        subtitle_label = QLabel(
            subtitle
        )

        subtitle_label.setObjectName(
            "pageSubtitle"
        )

        subtitle_label.setWordWrap(
            True
        )

        layout.addWidget(
            title_label
        )

        layout.addWidget(
            subtitle_label
        )

    # =========================================================
    # PERSONAL INFORMATION
    # =========================================================

    def create_personal_page(self):

        page, layout = (
            self.create_scroll_page()
        )

        self.create_section_title(
            layout,
            "Personal Information",
            "Add your contact and professional profile details."
        )

        form = QFormLayout()

        self.full_name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.location_input = QLineEdit()
        self.linkedin_input = QLineEdit()
        self.github_input = QLineEdit()
        self.website_input = QLineEdit()

        form.addRow(
            "Full Name",
            self.full_name_input
        )

        form.addRow(
            "Email",
            self.email_input
        )

        form.addRow(
            "Phone",
            self.phone_input
        )

        form.addRow(
            "Location",
            self.location_input
        )

        form.addRow(
            "LinkedIn",
            self.linkedin_input
        )

        form.addRow(
            "GitHub",
            self.github_input
        )

        form.addRow(
            "Website",
            self.website_input
        )

        layout.addLayout(
            form
        )

        layout.addStretch()

        return page

    # =========================================================
    # SUMMARY
    # =========================================================

    def create_summary_page(self):

        page, layout = (
            self.create_scroll_page()
        )

        self.create_section_title(
            layout,
            "Professional Summary",
            "Write a concise summary of your professional profile."
        )

        self.summary_input = QTextEdit()

        self.summary_input.setPlaceholderText(
            "Example: Software developer with experience building applications..."
        )

        self.summary_input.setMinimumHeight(
            250
        )

        layout.addWidget(
            self.summary_input
        )

        layout.addStretch()

        return page

    # =========================================================
    # EXPERIENCE
    # =========================================================

    def create_experience_page(self):

        page, layout = (
            self.create_scroll_page()
        )

        self.create_section_title(
            layout,
            "Work Experience",
            "Add jobs, internships, and relevant professional experience."
        )

        self.experience_list_layout = (
            QVBoxLayout()
        )

        layout.addLayout(
            self.experience_list_layout
        )

        add_button = QPushButton(
            "+ Add Experience"
        )

        add_button.setObjectName(
            "primaryButton"
        )

        add_button.clicked.connect(
            self.add_experience
        )

        layout.addWidget(
            add_button
        )

        layout.addStretch()

        return page

    # =========================================================
    # EDUCATION
    # =========================================================

    def create_education_page(self):

        page, layout = (
            self.create_scroll_page()
        )

        self.create_section_title(
            layout,
            "Education",
            "Add your academic qualifications."
        )

        self.education_list_layout = (
            QVBoxLayout()
        )

        layout.addLayout(
            self.education_list_layout
        )

        add_button = QPushButton(
            "+ Add Education"
        )

        add_button.setObjectName(
            "primaryButton"
        )

        add_button.clicked.connect(
            self.add_education
        )

        layout.addWidget(
            add_button
        )

        layout.addStretch()

        return page

    # =========================================================
    # SKILLS
    # =========================================================

    def create_skills_page(self):

        page, layout = (
            self.create_scroll_page()
        )

        self.create_section_title(
            layout,
            "Skills",
            "Add your technical and professional skills."
        )

        self.skills_input = QTextEdit()

        self.skills_input.setPlaceholderText(
            "Python, Django, SQL, Git, REST APIs"
        )

        self.skills_input.setMinimumHeight(
            200
        )

        layout.addWidget(
            self.skills_input
        )

        layout.addStretch()

        return page

    # =========================================================
    # PROJECTS
    # =========================================================

    def create_projects_page(self):

        page, layout = (
            self.create_scroll_page()
        )

        self.create_section_title(
            layout,
            "Projects",
            "Add your important academic or professional projects."
        )

        self.projects_list_layout = (
            QVBoxLayout()
        )

        layout.addLayout(
            self.projects_list_layout
        )

        add_button = QPushButton(
            "+ Add Project"
        )

        add_button.setObjectName(
            "primaryButton"
        )

        add_button.clicked.connect(
            self.add_project
        )

        layout.addWidget(
            add_button
        )

        layout.addStretch()

        return page

    # =========================================================
    # CERTIFICATIONS
    # =========================================================

    def create_certifications_page(self):

        page, layout = (
            self.create_scroll_page()
        )

        self.create_section_title(
            layout,
            "Certifications",
            "Add completed certifications and relevant courses."
        )

        self.certifications_list_layout = (
            QVBoxLayout()
        )

        layout.addLayout(
            self.certifications_list_layout
        )

        add_button = QPushButton(
            "+ Add Certification"
        )

        add_button.setObjectName(
            "primaryButton"
        )

        add_button.clicked.connect(
            self.add_certification
        )

        layout.addWidget(
            add_button
        )

        layout.addStretch()

        return page

    # =========================================================
    # LANGUAGES
    # =========================================================

    def create_languages_page(self):

        page, layout = (
            self.create_scroll_page()
        )

        self.create_section_title(
            layout,
            "Languages",
            "Add languages and proficiency levels."
        )

        self.languages_input = QTextEdit()

        self.languages_input.setPlaceholderText(
            "English - Fluent\nHindi - Native"
        )

        self.languages_input.setMinimumHeight(
            180
        )

        layout.addWidget(
            self.languages_input
        )

        layout.addStretch()

        return page

    # =========================================================
    # PREVIEW AREA
    # =========================================================

    def create_preview_area(self):

        scroll = QScrollArea()

        scroll.setWidgetResizable(
            True
        )

        self.preview_content = QLabel()

        self.preview_content.setObjectName(
            "resumePreview"
        )

        self.preview_content.setAlignment(
            Qt.AlignmentFlag.AlignTop
        )

        self.preview_content.setTextFormat(
            Qt.TextFormat.RichText
        )

        self.preview_content.setWordWrap(
            True
        )

        self.preview_content.setOpenExternalLinks(
            True
        )

        self.preview_content.setContentsMargins(
            20,
            20,
            20,
            20
        )

        scroll.setWidget(
            self.preview_content
        )

        return scroll

    # =========================================================
    # LIVE PREVIEW CONNECTIONS
    # =========================================================

    def connect_live_preview(self):

        inputs = [
            self.full_name_input,
            self.email_input,
            self.phone_input,
            self.location_input,
            self.linkedin_input,
            self.github_input,
            self.website_input,
        ]

        for input_field in inputs:

            input_field.textChanged.connect(
                self.update_preview
            )

        self.summary_input.textChanged.connect(
            self.update_preview
        )

        self.skills_input.textChanged.connect(
            self.update_preview
        )

        self.languages_input.textChanged.connect(
            self.update_preview
        )

    # =========================================================
    # LOAD RESUME
    # =========================================================

    def load_resume(self):

        self.resume = (
            ResumeService.get_resume(
                self.resume_id
            )
        )

        if not self.resume:

            QMessageBox.warning(
                self,
                "Resume Not Found",
                "The requested resume could not be found."
            )

            return

        self.resume_title.setText(
            self.resume.title
        )

        template_name = (
            self.resume.template_name
            or "Modern"
        )

        self.template_label.setText(
            f"Template: {template_name}"
        )

        self.full_name_input.setText(
            self.resume.full_name or ""
        )

        self.email_input.setText(
            self.resume.email or ""
        )

        self.phone_input.setText(
            self.resume.phone or ""
        )

        self.location_input.setText(
            self.resume.location or ""
        )

        self.linkedin_input.setText(
            self.resume.linkedin or ""
        )

        self.github_input.setText(
            self.resume.github or ""
        )

        self.website_input.setText(
            self.resume.website or ""
        )

        self.summary_input.setPlainText(
            self.resume.professional_summary
            or ""
        )

        self.skills_input.setPlainText(
            self.resume.skills
            or ""
        )

        self.languages_input.setPlainText(
            self.resume.languages
            or ""
        )

        self.experience_data = (
            ResumeService.load_list_data(
                self.resume.experience
            )
        )

        self.education_data = (
            ResumeService.load_list_data(
                self.resume.education
            )
        )

        self.projects_data = (
            ResumeService.load_list_data(
                self.resume.projects
            )
        )

        self.certifications_data = (
            ResumeService.load_list_data(
                self.resume.certifications
            )
        )

        self.refresh_dynamic_sections()

        self.update_preview()

    # =========================================================
    # REFRESH DYNAMIC SECTIONS
    # =========================================================

    def refresh_dynamic_sections(self):

        self.refresh_entry_layout(
            self.experience_list_layout,
            self.experience_data,
            "experience"
        )

        self.refresh_entry_layout(
            self.education_list_layout,
            self.education_data,
            "education"
        )

        self.refresh_entry_layout(
            self.projects_list_layout,
            self.projects_data,
            "projects"
        )

        self.refresh_entry_layout(
            self.certifications_list_layout,
            self.certifications_data,
            "certifications"
        )

    def refresh_entry_layout(
        self,
        layout,
        data,
        section
    ):

        while layout.count():

            item = layout.takeAt(
                0
            )

            widget = item.widget()

            if widget:
                widget.deleteLater()

        for index, entry in enumerate(
            data
        ):

            card = QFrame()

            card.setObjectName(
                "entryCard"
            )

            card_layout = QHBoxLayout(
                card
            )

            title = (
                entry.get(
                    "title",
                    "Untitled Entry"
                )
            )

            text = QLabel(
                title
            )

            card_layout.addWidget(
                text
            )

            card_layout.addStretch()

            edit_button = QPushButton(
                "Edit"
            )

            edit_button.clicked.connect(
                lambda checked=False,
                i=index,
                s=section:
                self.edit_entry(
                    i,
                    s
                )
            )

            delete_button = QPushButton(
                "Delete"
            )

            delete_button.clicked.connect(
                lambda checked=False,
                i=index,
                s=section:
                self.delete_entry(
                    i,
                    s
                )
            )

            card_layout.addWidget(
                edit_button
            )

            card_layout.addWidget(
                delete_button
            )

            layout.addWidget(
                card
            )

    # =========================================================
    # ADD ENTRY METHODS
    # =========================================================

    def add_experience(self):

        self.open_entry_dialog(
            "Add Experience",
            "experience"
        )

    def add_education(self):

        self.open_entry_dialog(
            "Add Education",
            "education"
        )

    def add_project(self):

        self.open_entry_dialog(
            "Add Project",
            "projects"
        )

    def add_certification(self):

        self.open_entry_dialog(
            "Add Certification",
            "certifications"
        )

    # =========================================================
    # EDIT / DELETE ENTRY
    # =========================================================

    def edit_entry(
        self,
        index,
        section
    ):

        self.open_entry_dialog(
            f"Edit {section.title()}",
            section,
            index
        )

    def delete_entry(
        self,
        index,
        section
    ):

        data = getattr(
            self,
            f"{section}_data"
        )

        if 0 <= index < len(data):

            del data[index]

        self.refresh_dynamic_sections()

        self.update_preview()

    # =========================================================
    # ENTRY DIALOG
    # =========================================================

    def open_entry_dialog(
        self,
        title,
        section,
        edit_index=None
    ):

        dialog = QDialog(
            self
        )

        dialog.setWindowTitle(
            title
        )

        dialog.setMinimumWidth(
            450
        )

        layout = QVBoxLayout(
            dialog
        )

        form = QFormLayout()

        title_input = QLineEdit()
        subtitle_input = QLineEdit()
        date_input = QLineEdit()

        description_input = QTextEdit()

        description_input.setMinimumHeight(
            120
        )

        if edit_index is not None:

            data = getattr(
                self,
                f"{section}_data"
            )

            if 0 <= edit_index < len(data):

                entry = data[edit_index]

                title_input.setText(
                    entry.get(
                        "title",
                        ""
                    )
                )

                subtitle_input.setText(
                    entry.get(
                        "subtitle",
                        ""
                    )
                )

                date_input.setText(
                    entry.get(
                        "date",
                        ""
                    )
                )

                description_input.setPlainText(
                    entry.get(
                        "description",
                        ""
                    )
                )

        if section == "experience":

            form.addRow(
                "Job Title:",
                title_input
            )

            form.addRow(
                "Company:",
                subtitle_input
            )

        elif section == "education":

            form.addRow(
                "Degree:",
                title_input
            )

            form.addRow(
                "Institution:",
                subtitle_input
            )

        elif section == "projects":

            form.addRow(
                "Project Name:",
                title_input
            )

            form.addRow(
                "Technologies:",
                subtitle_input
            )

        else:

            form.addRow(
                "Certification:",
                title_input
            )

            form.addRow(
                "Issuer:",
                subtitle_input
            )

        form.addRow(
            "Date:",
            date_input
        )

        form.addRow(
            "Description:",
            description_input
        )

        layout.addLayout(
            form
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

            entry_title = (
                title_input.text().strip()
            )

            if not entry_title:

                QMessageBox.warning(
                    self,
                    "Required",
                    "Please enter a title."
                )

                return

            entry = {
                "title": entry_title,
                "subtitle":
                    subtitle_input.text().strip(),
                "date":
                    date_input.text().strip(),
                "description":
                    description_input
                    .toPlainText()
                    .strip(),
            }

            data = getattr(
                self,
                f"{section}_data"
            )

            if edit_index is None:

                data.append(
                    entry
                )

            else:

                data[edit_index] = entry

            self.refresh_dynamic_sections()

            self.update_preview()

    # =========================================================
    # CURRENT DATA
    # =========================================================

    def get_current_data(self):

        return {
            "full_name":
                self.full_name_input.text().strip(),

            "email":
                self.email_input.text().strip(),

            "phone":
                self.phone_input.text().strip(),

            "location":
                self.location_input.text().strip(),

            "linkedin":
                self.linkedin_input.text().strip(),

            "github":
                self.github_input.text().strip(),

            "website":
                self.website_input.text().strip(),

            "professional_summary":
                self.summary_input
                .toPlainText()
                .strip(),

            "skills":
                self.skills_input
                .toPlainText()
                .strip(),

            "languages":
                self.languages_input
                .toPlainText()
                .strip(),

            "experience":
                json.dumps(
                    self.experience_data
                ),

            "education":
                json.dumps(
                    self.education_data
                ),

            "projects":
                json.dumps(
                    self.projects_data
                ),

            "certifications":
                json.dumps(
                    self.certifications_data
                ),
        }

    # =========================================================
    # CURRENT PREVIEW DATA
    # =========================================================

    def get_preview_data(self):

        return {
            "full_name":
                self.full_name_input.text().strip(),

            "email":
                self.email_input.text().strip(),

            "phone":
                self.phone_input.text().strip(),

            "location":
                self.location_input.text().strip(),

            "linkedin":
                self.linkedin_input.text().strip(),

            "github":
                self.github_input.text().strip(),

            "website":
                self.website_input.text().strip(),

            "professional_summary":
                self.summary_input
                .toPlainText()
                .strip(),

            "skills":
                self.skills_input
                .toPlainText()
                .strip(),

            "languages":
                self.languages_input
                .toPlainText()
                .strip(),

            "experience":
                self.experience_data,

            "education":
                self.education_data,

            "projects":
                self.projects_data,

            "certifications":
                self.certifications_data,
        }

    # =========================================================
    # SAVE
    # =========================================================

    def save_current_data_silently(self):

        data = self.get_current_data()

        return ResumeService.update_resume(
            self.resume_id,
            data
        )

    def save_resume(self):

        success = (
            self.save_current_data_silently()
        )

        if success:

            self.resume = (
                ResumeService.get_resume(
                    self.resume_id
                )
            )

            self.update_preview()

            QMessageBox.information(
                self,
                "Saved",
                "Your resume has been saved successfully."
            )

        else:

            QMessageBox.warning(
                self,
                "Save Failed",
                "Could not save the resume."
            )

    # =========================================================
    # EXPORT PDF
    # =========================================================

    def export_pdf(self):

        success = (
            self.save_current_data_silently()
        )

        if not success:

            QMessageBox.warning(
                self,
                "Export Failed",
                "Could not save the resume before exporting."
            )

            return

        resume = (
            ResumeService.get_resume(
                self.resume_id
            )
        )

        default_name = (
            f"{resume.title}.pdf"
            if resume
            else "resume.pdf"
        )

        file_path, _ = (
            QFileDialog.getSaveFileName(
                self,
                "Export Resume as PDF",
                default_name,
                "PDF Files (*.pdf)"
            )
        )

        if not file_path:
            return

        if not file_path.lower().endswith(
            ".pdf"
        ):
            file_path += ".pdf"

        try:

            ExportService.export_pdf(
                self.resume_id,
                file_path
            )

            QMessageBox.information(
                self,
                "Export Successful",
                "Your resume was exported as PDF."
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Export Failed",
                f"Could not export PDF.\n\n{error}"
            )

    # =========================================================
    # EXPORT DOCX
    # =========================================================

    def export_docx(self):

        success = (
            self.save_current_data_silently()
        )

        if not success:

            QMessageBox.warning(
                self,
                "Export Failed",
                "Could not save the resume before exporting."
            )

            return

        resume = (
            ResumeService.get_resume(
                self.resume_id
            )
        )

        default_name = (
            f"{resume.title}.docx"
            if resume
            else "resume.docx"
        )

        file_path, _ = (
            QFileDialog.getSaveFileName(
                self,
                "Export Resume as DOCX",
                default_name,
                "Word Documents (*.docx)"
            )
        )

        if not file_path:
            return

        if not file_path.lower().endswith(
            ".docx"
        ):
            file_path += ".docx"

        try:

            ExportService.export_docx(
                self.resume_id,
                file_path
            )

            QMessageBox.information(
                self,
                "Export Successful",
                "Your resume was exported as DOCX."
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Export Failed",
                f"Could not export DOCX.\n\n{error}"
            )

    # =========================================================
    # UPDATE LIVE PREVIEW
    # =========================================================

    def update_preview(self):

        if not self.resume:
            return

        preview_data = (
            self.get_preview_data()
        )

        template_name = (
            self.resume.template_name
            or "Modern"
        )

        html = ResumeRenderer.render(
            preview_data,
            template_name
        )

        self.preview_content.setText(
            html
        )