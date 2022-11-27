from src import db


class Enrollment(db.Model):
    __tablename__ = 'enrollment'

    call_no = db.Column(db.Integer, db.ForeignKey('section.call_no'), primary_key=True, nullable=False)
    uni = db.Column(db.String(10), primary_key=True, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
