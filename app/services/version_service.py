from app.database.connection import SessionLocal
from app.database.models import Resume, ResumeVersion
from app.services.snapshot_service import serialize_resume

class VersionService:
    @staticmethod
    def create(resume_id, name, notes=""):
        with SessionLocal() as s:
            r=s.get(Resume,resume_id)
            next_no=(max([v.version_number for v in r.versions], default=0)+1)
            v=ResumeVersion(resume_id=resume_id, version_name=name, version_number=next_no,
                            notes=notes, snapshot_data=serialize_resume(r))
            s.add(v); s.commit()

    @staticmethod
    def list(resume_id):
        with SessionLocal() as s:
            return s.query(ResumeVersion).filter_by(resume_id=resume_id).order_by(ResumeVersion.version_number.desc()).all()

    @staticmethod
    def duplicate(version_id):
        with SessionLocal() as s:
            v=s.get(ResumeVersion,version_id)
            r=s.get(Resume,v.resume_id)
            n=max([x.version_number for x in r.versions], default=0)+1
            s.add(ResumeVersion(resume_id=v.resume_id, version_name=v.version_name+" (Copy)",
                  version_number=n, notes=v.notes, snapshot_data=v.snapshot_data)); s.commit()

    @staticmethod
    def delete(version_id):
        with SessionLocal() as s:
            v=s.get(ResumeVersion,version_id)
            if v: s.delete(v); s.commit()
