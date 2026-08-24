from sqlalchemy import asc, desc

from app.database.connection import SessionLocal
from app.database.models import CoverLetter


class CoverLetterService:

    # =========================================================
    # CREATE
    # =========================================================

    @staticmethod
    def create_cover_letter(
        title="Untitled Cover Letter"
    ):
        title = (
            title or "Untitled Cover Letter"
        ).strip()

        with SessionLocal() as session:

            cover_letter = CoverLetter(
                title=title
            )

            session.add(
                cover_letter
            )

            session.commit()

            session.refresh(
                cover_letter
            )

            return cover_letter

    # =========================================================
    # GET ONE
    # =========================================================

    @staticmethod
    def get_cover_letter(
        cover_letter_id
    ):
        with SessionLocal() as session:

            return session.get(
                CoverLetter,
                cover_letter_id
            )

    # =========================================================
    # GET ALL
    # =========================================================

    @staticmethod
    def get_all_cover_letters(
        search_text="",
        sort_by="Recently Edited"
    ):

        with SessionLocal() as session:

            query = session.query(
                CoverLetter
            )

            # ---------------------------------------------
            # SEARCH
            # ---------------------------------------------

            if search_text:

                search_text = (
                    search_text
                    .strip()
                )

                if search_text:

                    search = (
                        f"%{search_text}%"
                    )

                    query = query.filter(
                        (
                            CoverLetter.title.ilike(
                                search
                            )
                        )
                        |
                        (
                            CoverLetter.company_name.ilike(
                                search
                            )
                        )
                        |
                        (
                            CoverLetter.job_position.ilike(
                                search
                            )
                        )
                    )

            # ---------------------------------------------
            # SORT
            # ---------------------------------------------

            if sort_by == "Recently Edited":

                query = query.order_by(
                    desc(
                        CoverLetter.updated_at
                    )
                )

            elif sort_by == "Oldest":

                query = query.order_by(
                    asc(
                        CoverLetter.created_at
                    )
                )

            elif sort_by == "Name A-Z":

                query = query.order_by(
                    asc(
                        CoverLetter.title
                    )
                )

            return query.all()

    # =========================================================
    # UPDATE
    # =========================================================

    @staticmethod
    def update_cover_letter(
        cover_letter_id,
        data
    ):

        with SessionLocal() as session:

            cover_letter = session.get(
                CoverLetter,
                cover_letter_id
            )

            if not cover_letter:
                return False

            for key, value in data.items():

                if hasattr(
                    cover_letter,
                    key
                ):

                    setattr(
                        cover_letter,
                        key,
                        value
                    )

            session.commit()

            return True

    # =========================================================
    # RENAME
    # =========================================================

    @staticmethod
    def rename_cover_letter(
        cover_letter_id,
        new_title
    ):

        new_title = (
            new_title or ""
        ).strip()

        if not new_title:
            return False

        with SessionLocal() as session:

            cover_letter = session.get(
                CoverLetter,
                cover_letter_id
            )

            if not cover_letter:
                return False

            cover_letter.title = (
                new_title
            )

            session.commit()

            return True

    # =========================================================
    # DELETE
    # =========================================================

    @staticmethod
    def delete_cover_letter(
        cover_letter_id
    ):

        with SessionLocal() as session:

            cover_letter = session.get(
                CoverLetter,
                cover_letter_id
            )

            if not cover_letter:
                return False

            session.delete(
                cover_letter
            )

            session.commit()

            return True

    # =========================================================
    # DUPLICATE
    # =========================================================

    @staticmethod
    def duplicate_cover_letter(
        cover_letter_id
    ):

        with SessionLocal() as session:

            original = session.get(
                CoverLetter,
                cover_letter_id
            )

            if not original:
                return None

            copied = CoverLetter()

            # Copy all database fields except IDs/timestamps
            for column in original.__table__.columns:

                if column.name in (
                    "id",
                    "created_at",
                    "updated_at"
                ):
                    continue

                value = getattr(
                    original,
                    column.name
                )

                setattr(
                    copied,
                    column.name,
                    value
                )

            # Give duplicated letter a new title
            original_title = (
                original.title
                or "Untitled Cover Letter"
            )

            copied.title = (
                f"{original_title} Copy"
            )

            session.add(
                copied
            )

            session.commit()

            session.refresh(
                copied
            )

            return copied