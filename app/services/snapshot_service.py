import json
from sqlalchemy.inspection import inspect

def _row(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs if c.key not in ("id","resume_id")}

def serialize_resume(resume):
    return json.dumps({
        "title": resume.title, "template_name": resume.template_name, "summary": resume.summary,
        "section_order": resume.section_order, "section_visibility": resume.section_visibility,
        "personal": _row(resume.personal) if resume.personal else {},
        "education": [_row(x) for x in resume.education],
        "experience": [_row(x) for x in resume.experience],
        "projects": [_row(x) for x in resume.projects],
        "skills": [_row(x) for x in resume.skills],
        "certifications": [_row(x) for x in resume.certifications],
        "languages": [_row(x) for x in resume.languages],
    })
