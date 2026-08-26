ResumeForge — Professional Resume Builder

ResumeForge is a modular desktop application built with Python and PySide6 that helps users create, edit, manage, preview, and organize professional resumes through an intuitive interface.

Features
Persistent left-side navigation and application dashboard
Resume creation and management
Structured resume builder for organizing professional information
Live resume preview
Three customizable resume templates
Resume version management
Save and restore previous resume versions
SQLite database integration using SQLAlchemy
Normalized database structure for resume sections
Complete JSON snapshots for independent version restoration
Technologies Used
Python
PySide6
SQLite
SQLAlchemy
Run the Application

Install the required dependencies:

pip install -r requirements.txt

Then start the application:

python main.py
Architecture

ResumeForge uses a modular architecture to keep the application organized and maintainable. Resume data is stored using normalized section tables, while resume versions are preserved as complete JSON snapshots, allowing users to restore previous versions independently.
