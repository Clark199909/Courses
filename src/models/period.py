from src import db


class Period(db.Model):
    db.__tablename__ = 'period'

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.String(10), nullable=False)
    day = db.Column(db.String(10), nullable=False)
    start_hr = db.Column(db.Integer, nullable=False)
    start_min = db.Column(db.Integer, nullable=False)
    end_hr = db.Column(db.Integer, nullable=False)
    end_min = db.Column(db.Integer, nullable=False)

    sections = db.relationship('Section', backref='period')
