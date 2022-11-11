from src import db


class Project(db.Model):
    db.__tablename__ = 'project'

    id = db.Column(db.Integer, primary_key=True)
    call_no = db.Column(db.Integer, db.ForeignKey('section.call_no'), nullable=False)
    project_name = db.Column(db.String(255), nullable=False)
    team_name = db.Column(db.String(255), nullable=False)
