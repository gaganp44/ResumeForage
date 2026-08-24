from datetime import datetime

from sqlalchemy import (
    String,
    Integer,
    DateTime,
    Text,
    ForeignKey,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.database.connection import Base


# ============================================================
# RESUME MODEL
# ============================================================

class Resume(Base):

    __tablename__ = "resumes"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    title: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    template_name: Mapped[str] = mapped_column(
        String(50),
        default="Modern"
    )

    full_name: Mapped[str] = mapped_column(
        String(150),
        default=""
    )

    email: Mapped[str] = mapped_column(
        String(150),
        default=""
    )

    phone: Mapped[str] = mapped_column(
        String(50),
        default=""
    )

    location: Mapped[str] = mapped_column(
        String(150),
        default=""
    )

    linkedin: Mapped[str] = mapped_column(
        String(250),
        default=""
    )

    github: Mapped[str] = mapped_column(
        String(250),
        default=""
    )

    website: Mapped[str] = mapped_column(
        String(250),
        default=""
    )

    professional_summary: Mapped[str] = mapped_column(
        Text,
        default=""
    )

    experience: Mapped[str] = mapped_column(
        Text,
        default="[]"
    )

    education: Mapped[str] = mapped_column(
        Text,
        default="[]"
    )

    skills: Mapped[str] = mapped_column(
        Text,
        default=""
    )

    projects: Mapped[str] = mapped_column(
        Text,
        default="[]"
    )

    certifications: Mapped[str] = mapped_column(
        Text,
        default="[]"
    )

    languages: Mapped[str] = mapped_column(
        Text,
        default=""
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now
    )


# ============================================================
# COVER LETTER MODEL
# ============================================================

class CoverLetter(Base):

    __tablename__ = "cover_letters"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    recipient_name: Mapped[str] = mapped_column(
        String(150),
        default=""
    )

    company_name: Mapped[str] = mapped_column(
        String(200),
        default=""
    )

    job_position: Mapped[str] = mapped_column(
        String(200),
        default=""
    )

    letter_date: Mapped[str] = mapped_column(
        String(100),
        default=""
    )

    salutation: Mapped[str] = mapped_column(
        String(200),
        default="Dear Hiring Manager,"
    )

    content: Mapped[str] = mapped_column(
        Text,
        default=""
    )

    closing: Mapped[str] = mapped_column(
        String(100),
        default="Sincerely,"
    )

    signature_name: Mapped[str] = mapped_column(
        String(150),
        default=""
    )

    # Optional link to a resume
    resume_id: Mapped[int | None] = mapped_column(
        ForeignKey("resumes.id"),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now
    )