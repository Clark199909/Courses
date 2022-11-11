from src import db


class SectionType(db.Model):
    db.__tablename__ = 'section_type'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(10), nullable=False)
