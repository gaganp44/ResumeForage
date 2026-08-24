import json
from PySide6.QtWidgets import QMainWindow,QWidget,QHBoxLayout,QVBoxLayout,QPushButton,QStackedWidget,QLabel,QComboBox,QScrollArea,QInputDialog,QMessageBox
from app.database.connection import SessionLocal
from app.database.models import Resume,PersonalInfo,Education,Experience,Project,Skill,Certification,Language
from app.templates.renderers import ResumeRenderer
from app.services.version_service import VersionService
from app.ui.builder.forms import PersonalForm,TextForm,ListForm

class BuilderWindow(QMainWindow):
    def __init__(self,resume_id,parent=None):
        super().__init__(parent); self.resume_id=resume_id; self.setWindowTitle("Resume Builder — ResumeForge")
        root=QWidget(); self.setCentralWidget(root); main=QHBoxLayout(root)
        left=QVBoxLayout(); top=QHBoxLayout(); self.template=QComboBox(); self.template.addItems(["Modern","Classic","Minimal"]); self.template.currentTextChanged.connect(self.change_template)
        top.addWidget(QLabel("Template:")); top.addWidget(self.template); top.addStretch()
        save=QPushButton("Save"); save.clicked.connect(self.save_all); top.addWidget(save)
        versions=QPushButton("Versions"); versions.clicked.connect(self.manage_versions); top.addWidget(versions); left.addLayout(top)
        self.forms=QStackedWidget(); self.buttons={}
        names=["Personal Info","Summary","Experience","Education","Projects","Skills","Certifications","Languages"]
        for n in names:
            b=QPushButton(n); b.clicked.connect(lambda _,x=len(self.buttons):self.forms.setCurrentIndex(x)); left.addWidget(b); self.buttons[n]=b
        self.personal=PersonalForm(); self.summary=TextForm("Professional Summary")
        self.experience=ListForm(["Job Title","Company","Location","Start Date","End Date","Description"])
        self.education=ListForm(["Institution","Degree","Field of Study","Start Date","End Date","Grade","Description"])
        self.projects=ListForm(["Project Name","Technologies","Project Link","GitHub Link","Description"])
        self.skills=ListForm(["Category","Skill"])
        self.certifications=ListForm(["Certificate Name","Organization","Issue Date","Credential URL"])
        self.languages=ListForm(["Language","Proficiency"])
        for f in [self.personal,self.summary,self.experience,self.education,self.projects,self.skills,self.certifications,self.languages]: self.forms.addWidget(f)
        left.addWidget(self.forms,1); lw=QWidget(); lw.setLayout(left); lw.setFixedWidth(470); main.addWidget(lw)
        self.preview_area=QScrollArea(); self.preview_area.setWidgetResizable(True); main.addWidget(self.preview_area,1)
        self.load()
    def load(self):
        with SessionLocal() as s:
            r=s.get(Resume,self.resume_id); self.template.setCurrentText(r.template_name); self.personal.load(r.personal); self.summary.set_text(r.summary)
            self.experience.load([[x.job_title,x.company,x.location,x.start_date,x.end_date,x.description] for x in r.experience])
            self.education.load([[x.institution,x.degree,x.field_of_study,x.start_date,x.end_date,x.grade,x.description] for x in r.education])
            self.projects.load([[x.name,x.technologies,x.project_link,x.github_link,x.description] for x in r.projects])
            self.skills.load([[x.category,x.name] for x in r.skills]); self.certifications.load([[x.name,x.organization,x.issue_date,x.credential_url] for x in r.certifications]); self.languages.load([[x.name,x.proficiency] for x in r.languages])
        self.refresh_preview()
    def _replace(self,s,model,rows,fields):
        s.query(model).filter_by(resume_id=self.resume_id).delete()
        for i,row in enumerate(rows): s.add(model(resume_id=self.resume_id,display_order=i,**dict(zip(fields,row))))
    def save_all(self):
        with SessionLocal() as s:
            r=s.get(Resume,self.resume_id); r.template_name=self.template.currentText(); r.summary=self.summary.text(); vals=self.personal.values()
            for k,v in vals.items(): setattr(r.personal,k,v)
            self._replace(s,Experience,self.experience.rows(),["job_title","company","location","start_date","end_date","description"])
            self._replace(s,Education,self.education.rows(),["institution","degree","field_of_study","start_date","end_date","grade","description"])
            self._replace(s,Project,self.projects.rows(),["name","technologies","project_link","github_link","description"])
            s.query(Skill).filter_by(resume_id=self.resume_id).delete(); [s.add(Skill(resume_id=self.resume_id,category=x[0],name=x[1])) for x in self.skills.rows()]
            s.query(Certification).filter_by(resume_id=self.resume_id).delete(); [s.add(Certification(resume_id=self.resume_id,name=x[0],organization=x[1],issue_date=x[2],credential_url=x[3])) for x in self.certifications.rows()]
            s.query(Language).filter_by(resume_id=self.resume_id).delete(); [s.add(Language(resume_id=self.resume_id,name=x[0],proficiency=x[1])) for x in self.languages.rows()]
            s.commit()
        self.refresh_preview()
    def change_template(self,*_): self.refresh_preview()
    def refresh_preview(self):
        self.save_all_silent()
        with SessionLocal() as s:
            r=s.get(Resume,self.resume_id); data={"personal":{k:getattr(r.personal,k) for k in ["full_name","professional_title","email","phone","location"]},"summary":r.summary,"experience":[{"job_title":x.job_title,"company":x.company,"description":x.description} for x in r.experience],"education":[{"degree":x.degree,"institution":x.institution} for x in r.education],"projects":[{"name":x.name,"technologies":x.technologies,"description":x.description} for x in r.projects],"skills":[{"category":x.category,"name":x.name} for x in r.skills],"certifications":[{"name":x.name,"organization":x.organization} for x in r.certifications],"languages":[{"name":x.name,"proficiency":x.proficiency} for x in r.languages]}
        self.preview_area.setWidget(ResumeRenderer(self.template.currentText()).render(data))
    def save_all_silent(self): pass
    def manage_versions(self):
        name,ok=QInputDialog.getText(self,"Create Version","Version name:")
        if ok and name.strip(): self.save_all(); VersionService.create(self.resume_id,name.strip()); QMessageBox.information(self,"Versions","Version snapshot created.")
