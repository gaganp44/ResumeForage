from PySide6.QtWidgets import QWidget,QVBoxLayout,QFormLayout,QLineEdit,QTextEdit,QPushButton,QScrollArea,QHBoxLayout,QLabel

class PersonalForm(QWidget):
    fields=["full_name","professional_title","email","phone","location","linkedin","github","portfolio"]
    def __init__(self):
        super().__init__(); f=QFormLayout(self); self.inputs={}
        for x in self.fields: self.inputs[x]=QLineEdit(); f.addRow(x.replace("_"," ").title(),self.inputs[x])
    def load(self,obj):
        for k,w in self.inputs.items(): w.setText(getattr(obj,k,"") or "")
    def values(self): return {k:w.text() for k,w in self.inputs.items()}

class TextForm(QWidget):
    def __init__(self,title):
        super().__init__(); l=QVBoxLayout(self); l.addWidget(QLabel(title)); self.edit=QTextEdit(); self.edit.textChanged.connect(lambda: None); l.addWidget(self.edit)
    def text(self): return self.edit.toPlainText()
    def set_text(self,x): self.edit.setPlainText(x or "")

class ListForm(QWidget):
    def __init__(self,fields):
        super().__init__(); self.fields=fields; self.rows_layout=QVBoxLayout(); outer=QVBoxLayout(self); add=QPushButton("+ Add Entry"); add.clicked.connect(self.add); outer.addWidget(add)
        box=QWidget(); box.setLayout(self.rows_layout); sc=QScrollArea(); sc.setWidgetResizable(True); sc.setWidget(box); outer.addWidget(sc)
    def add(self,values=None):
        w=QWidget(); f=QFormLayout(w); inputs=[]
        for i,name in enumerate(self.fields):
            inp=QTextEdit() if "Description" in name else QLineEdit()
            if values: (inp.setPlainText if isinstance(inp,QTextEdit) else inp.setText)(values[i])
            f.addRow(name,inp); inputs.append(inp)
        d=QPushButton("Remove"); d.clicked.connect(lambda:self.remove(w)); f.addRow(d); w.inputs=inputs; self.rows_layout.addWidget(w)
    def remove(self,w): self.rows_layout.removeWidget(w); w.deleteLater()
    def rows(self):
        out=[]
        for i in range(self.rows_layout.count()):
            w=self.rows_layout.itemAt(i).widget()
            if w: out.append([x.toPlainText() if isinstance(x,QTextEdit) else x.text() for x in w.inputs])
        return out
    def load(self,rows):
        for i in range(self.rows_layout.count()-1,-1,-1):
            w=self.rows_layout.itemAt(i).widget()
            if w: w.deleteLater()
        for row in rows:self.add(row)
