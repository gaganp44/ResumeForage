from html import escape


class ResumeRenderer:

    @staticmethod
    def render(resume_data, template_name="Modern"):
        """
        Main template router.
        """

        template_name = (
            template_name or "Modern"
        ).strip().lower()

        if template_name == "classic":
            return ResumeRenderer.render_classic(
                resume_data
            )

        if template_name == "minimal":
            return ResumeRenderer.render_minimal(
                resume_data
            )

        return ResumeRenderer.render_modern(
            resume_data
        )

    # =========================================================
    # COMMON HELPERS
    # =========================================================

    @staticmethod
    def clean(value):
        return escape(
            str(value or "").strip()
        )

    @staticmethod
    def get_contact(resume_data):

        contacts = []

        fields = [
            "email",
            "phone",
            "location",
            "linkedin",
            "github",
            "website",
        ]

        for field in fields:

            value = (
                resume_data.get(
                    field,
                    ""
                )
            )

            if value:
                contacts.append(
                    ResumeRenderer.clean(
                        value
                    )
                )

        return " • ".join(
            contacts
        )

    @staticmethod
    def render_entries(
        title,
        entries,
        accent="#2563eb"
    ):

        if not entries:
            return ""

        html = f"""
        <div style="
            margin-top: 18px;
        ">
            <div style="
                font-size: 15px;
                font-weight: bold;
                color: {accent};
                border-bottom: 2px solid {accent};
                padding-bottom: 4px;
                margin-bottom: 8px;
            ">
                {ResumeRenderer.clean(title)}
            </div>
        """

        for entry in entries:

            entry_title = (
                ResumeRenderer.clean(
                    entry.get(
                        "title",
                        ""
                    )
                )
            )

            subtitle = (
                ResumeRenderer.clean(
                    entry.get(
                        "subtitle",
                        ""
                    )
                )
            )

            date = (
                ResumeRenderer.clean(
                    entry.get(
                        "date",
                        ""
                    )
                )
            )

            description = (
                ResumeRenderer.clean(
                    entry.get(
                        "description",
                        ""
                    )
                ).replace(
                    "\n",
                    "<br>"
                )
            )

            html += """
            <div style="
                margin-bottom: 12px;
            ">
            """

            if entry_title:

                html += f"""
                <div style="
                    font-weight: bold;
                    font-size: 13px;
                ">
                    {entry_title}
                </div>
                """

            if subtitle:

                html += f"""
                <div style="
                    font-size: 11px;
                    color: #555;
                ">
                    {subtitle}
                </div>
                """

            if date:

                html += f"""
                <div style="
                    font-size: 10px;
                    color: #777;
                    margin-bottom: 3px;
                ">
                    {date}
                </div>
                """

            if description:

                html += f"""
                <div style="
                    font-size: 11px;
                    line-height: 1.4;
                ">
                    {description}
                </div>
                """

            html += "</div>"

        html += "</div>"

        return html

    @staticmethod
    def render_text_section(
        title,
        content,
        accent="#2563eb"
    ):

        content = (
            ResumeRenderer.clean(
                content
            )
            .replace(
                "\n",
                "<br>"
            )
        )

        if not content:
            return ""

        return f"""
        <div style="
            margin-top: 18px;
        ">
            <div style="
                font-size: 15px;
                font-weight: bold;
                color: {accent};
                border-bottom: 2px solid {accent};
                padding-bottom: 4px;
                margin-bottom: 8px;
            ">
                {ResumeRenderer.clean(title)}
            </div>

            <div style="
                font-size: 11px;
                line-height: 1.5;
            ">
                {content}
            </div>
        </div>
        """

    # =========================================================
    # MODERN TEMPLATE
    # =========================================================

    @staticmethod
    def render_modern(resume_data):

        name = (
            ResumeRenderer.clean(
                resume_data.get(
                    "full_name",
                    ""
                )
            )
            or "Your Name"
        )

        contact = (
            ResumeRenderer.get_contact(
                resume_data
            )
        )

        html = f"""
        <div style="
            background: white;
            padding: 35px;
            font-family: Arial, sans-serif;
            color: #222;
        ">

            <div style="
                background: #2563eb;
                color: white;
                padding: 22px;
                margin-bottom: 20px;
            ">

                <div style="
                    font-size: 28px;
                    font-weight: bold;
                ">
                    {name}
                </div>

                <div style="
                    font-size: 10px;
                    margin-top: 8px;
                ">
                    {contact}
                </div>

            </div>
        """

        html += (
            ResumeRenderer.render_text_section(
                "PROFESSIONAL SUMMARY",
                resume_data.get(
                    "professional_summary",
                    ""
                ),
                "#2563eb"
            )
        )

        html += (
            ResumeRenderer.render_entries(
                "EXPERIENCE",
                resume_data.get(
                    "experience",
                    []
                ),
                "#2563eb"
            )
        )

        html += (
            ResumeRenderer.render_entries(
                "EDUCATION",
                resume_data.get(
                    "education",
                    []
                ),
                "#2563eb"
            )
        )

        html += (
            ResumeRenderer.render_text_section(
                "SKILLS",
                resume_data.get(
                    "skills",
                    ""
                ),
                "#2563eb"
            )
        )

        html += (
            ResumeRenderer.render_entries(
                "PROJECTS",
                resume_data.get(
                    "projects",
                    []
                ),
                "#2563eb"
            )
        )

        html += (
            ResumeRenderer.render_entries(
                "CERTIFICATIONS",
                resume_data.get(
                    "certifications",
                    []
                ),
                "#2563eb"
            )
        )

        html += (
            ResumeRenderer.render_text_section(
                "LANGUAGES",
                resume_data.get(
                    "languages",
                    ""
                ),
                "#2563eb"
            )
        )

        html += "</div>"

        return html

    # =========================================================
    # CLASSIC TEMPLATE
    # =========================================================

    @staticmethod
    def render_classic(resume_data):

        name = (
            ResumeRenderer.clean(
                resume_data.get(
                    "full_name",
                    ""
                )
            )
            or "Your Name"
        )

        contact = (
            ResumeRenderer.get_contact(
                resume_data
            )
        )

        html = f"""
        <div style="
            background: white;
            padding: 40px;
            font-family: 'Times New Roman';
            color: #111;
        ">

            <div style="
                text-align: center;
                border-bottom: 2px solid black;
                padding-bottom: 12px;
                margin-bottom: 18px;
            ">

                <div style="
                    font-size: 26px;
                    font-weight: bold;
                    text-transform: uppercase;
                ">
                    {name}
                </div>

                <div style="
                    font-size: 10px;
                    margin-top: 6px;
                ">
                    {contact}
                </div>

            </div>
        """

        html += (
            ResumeRenderer.render_text_section(
                "PROFESSIONAL SUMMARY",
                resume_data.get(
                    "professional_summary",
                    ""
                ),
                "#111111"
            )
        )

        html += (
            ResumeRenderer.render_entries(
                "EXPERIENCE",
                resume_data.get(
                    "experience",
                    []
                ),
                "#111111"
            )
        )

        html += (
            ResumeRenderer.render_entries(
                "EDUCATION",
                resume_data.get(
                    "education",
                    []
                ),
                "#111111"
            )
        )

        html += (
            ResumeRenderer.render_text_section(
                "SKILLS",
                resume_data.get(
                    "skills",
                    ""
                ),
                "#111111"
            )
        )

        html += (
            ResumeRenderer.render_entries(
                "PROJECTS",
                resume_data.get(
                    "projects",
                    []
                ),
                "#111111"
            )
        )

        html += (
            ResumeRenderer.render_entries(
                "CERTIFICATIONS",
                resume_data.get(
                    "certifications",
                    []
                ),
                "#111111"
            )
        )

        html += (
            ResumeRenderer.render_text_section(
                "LANGUAGES",
                resume_data.get(
                    "languages",
                    ""
                ),
                "#111111"
            )
        )

        html += "</div>"

        return html

    # =========================================================
    # MINIMAL TEMPLATE
    # =========================================================

    @staticmethod
    def render_minimal(resume_data):

        name = (
            ResumeRenderer.clean(
                resume_data.get(
                    "full_name",
                    ""
                )
            )
            or "Your Name"
        )

        contact = (
            ResumeRenderer.get_contact(
                resume_data
            )
        )

        html = f"""
        <div style="
            background: white;
            padding: 30px;
            font-family: Arial, sans-serif;
            color: #333;
        ">

            <div style="
                margin-bottom: 18px;
            ">

                <div style="
                    font-size: 25px;
                    font-weight: bold;
                ">
                    {name}
                </div>

                <div style="
                    font-size: 9px;
                    color: #666;
                    margin-top: 5px;
                ">
                    {contact}
                </div>

            </div>
        """

        html += (
            ResumeRenderer.render_text_section(
                "Summary",
                resume_data.get(
                    "professional_summary",
                    ""
                ),
                "#666666"
            )
        )

        html += (
            ResumeRenderer.render_entries(
                "Experience",
                resume_data.get(
                    "experience",
                    []
                ),
                "#666666"
            )
        )

        html += (
            ResumeRenderer.render_entries(
                "Education",
                resume_data.get(
                    "education",
                    []
                ),
                "#666666"
            )
        )

        html += (
            ResumeRenderer.render_text_section(
                "Skills",
                resume_data.get(
                    "skills",
                    ""
                ),
                "#666666"
            )
        )

        html += (
            ResumeRenderer.render_entries(
                "Projects",
                resume_data.get(
                    "projects",
                    []
                ),
                "#666666"
            )
        )

        html += (
            ResumeRenderer.render_entries(
                "Certifications",
                resume_data.get(
                    "certifications",
                    []
                ),
                "#666666"
            )
        )

        html += (
            ResumeRenderer.render_text_section(
                "Languages",
                resume_data.get(
                    "languages",
                    ""
                ),
                "#666666"
            )
        )

        html += "</div>"

        return html