from src import db
from src.models.section import Section


class SectionResource:
    def __int__(self):
        pass

    @staticmethod
    def get_a_section(professor, period_id, classroom):
        return db.session.query(Section).filter_by(professor=professor,
                                                   period_id=period_id,
                                                   classroom=classroom).first()

    @staticmethod
    def add_new_section(professor, period_id, classroom):
        section = Section(professor=professor,
                          period_id=period_id,
                          classroom=classroom)
        db.session.add(section)
        db.session.commit()
