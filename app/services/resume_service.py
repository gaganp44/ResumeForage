import json

from sqlalchemy import asc, desc

from app.database.connection import SessionLocal
from app.database.models import Resume


class ResumeService:

    @staticmethod
    def create_resume(
        title,
        template_name="Modern"
    ):
        title = title.strip()

        if not title:
            return None

        with SessionLocal() as session:

            resume = Resume(
                title=title,
                template_name=template_name
            )

            session.add(resume)
            session.commit()
            session.refresh(resume)

            return resume

    @staticmethod
    def get_resume(resume_id):

        with SessionLocal() as session:

            return session.get(
                Resume,
                resume_id
            )

    @staticmethod
    def get_all_resumes(
        search_text="",
        sort_by="Recently Edited"
    ):
        with SessionLocal() as session:

            query = session.query(Resume)

            if search_text:

                query = query.filter(
                    Resume.title.ilike(
                        f"%{search_text.strip()}%"
                    )
                )

            if sort_by == "Recently Edited":

                query = query.order_by(
                    desc(Resume.updated_at)
                )

            elif sort_by == "Oldest":

                query = query.order_by(
                    asc(Resume.created_at)
                )

            elif sort_by == "Name A-Z":

                query = query.order_by(
                    asc(Resume.title)
                )

            return query.all()

    @staticmethod
    def rename_resume(
        resume_id,
        new_title
    ):
        new_title = new_title.strip()

        if not new_title:
            return False

        with SessionLocal() as session:

            resume = session.get(
                Resume,
                resume_id
            )

            if not resume:
                return False

            resume.title = new_title

            session.commit()

            return True

    @staticmethod
    def delete_resume(resume_id):

        with SessionLocal() as session:

            resume = session.get(
                Resume,
                resume_id
            )

            if not resume:
                return False

            session.delete(resume)

            session.commit()

            return True

    @staticmethod
    def duplicate_resume(resume_id):

        with SessionLocal() as session:

            original = session.get(
                Resume,
                resume_id
            )

            if not original:
                return None

            copied_resume = Resume(
                title=f"{original.title} Copy",
                template_name=original.template_name,

                full_name=original.full_name,
                email=original.email,
                phone=original.phone,
                location=original.location,

                linkedin=original.linkedin,
                github=original.github,
                website=original.website,

                professional_summary=
                    original.professional_summary,

                experience=original.experience,
                education=original.education,
                skills=original.skills,
                projects=original.projects,
                certifications=
                    original.certifications,
                languages=original.languages,
            )

            session.add(copied_resume)

            session.commit()

            session.refresh(copied_resume)

            return copied_resume

    @staticmethod
    def change_template(
        resume_id,
        template_name
    ):
        allowed_templates = [
            "Modern",
            "Classic",
            "Minimal",
        ]

        if template_name not in allowed_templates:
            return False

        with SessionLocal() as session:

            resume = session.get(
                Resume,
                resume_id
            )

            if not resume:
                return False

            resume.template_name = (
                template_name
            )

            session.commit()

            return True

    @staticmethod
    def update_resume(
        resume_id,
        data
    ):
        with SessionLocal() as session:

            resume = session.get(
                Resume,
                resume_id
            )

            if not resume:
                return False

            for key, value in data.items():

                if hasattr(
                    resume,
                    key
                ):
                    setattr(
                        resume,
                        key,
                        value
                    )

            session.commit()

            return True

    @staticmethod
    def load_list_data(data):

        try:

            return json.loads(
                data or "[]"
            )

        except (
            json.JSONDecodeError,
            TypeError
        ):

            return []