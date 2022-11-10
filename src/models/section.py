from src import db


class Section(db.Model):
    db.__tablename__ = 'section'

    call_no = db.Column(db.Integer, primary_key=True)
    professor = db.Column(db.String(255), nullable=False)
    period_id = db.Column(db.Integer, db.ForeignKey('period.id'), nullable=False)
    classroom = db.Column(db.String(20), nullable=False)
