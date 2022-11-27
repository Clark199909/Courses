from src import db
from src.models.section_type import SectionType
from src.models.project import Project
from src.models.enrollment import Enrollment


class Section(db.Model):
    __tablename__ = 'section'

    call_no = db.Column(db.Integer, primary_key=True)
    professor = db.Column(db.String(255), nullable=False)
    period_id = db.Column(db.Integer, db.ForeignKey('period.id'), nullable=False)
    classroom = db.Column(db.String(20), nullable=False)
    section_type_id = db.Column(db.Integer, db.ForeignKey('section_type.id'), nullable=False)

    section_type = db.relationship("SectionType")
    projects = db.relationship('Project', backref='section')
    enrollments = db.relationship('Enrollment', backref='section')
