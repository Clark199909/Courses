from src import db


class Enrollment(db.Model):
    db.__tablename__ = 'enrollment'

    