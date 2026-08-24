
# ResumeForge — Modules 1 to 4

A modular PySide6 desktop application.

## Included
1. Application shell and persistent left navigation
2. Dashboard and resume management
3. Complete structured resume builder
4. Live preview, three templates, and version management

## Run
```bash
pip install -r requirements.txt
python main.py
```

## Notes
The application uses SQLite and SQLAlchemy. Resume records use normalized section tables,
while versions store complete JSON snapshots so a version can be restored independently.
=======
A desktop resume builder application that allows users to create, edit, manage, and export professional resumes using customizable templates.
