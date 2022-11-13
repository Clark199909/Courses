from src import db
from src.models.section import Section
from src.models.section_type import SectionType


class SectionResource:
    def __int__(self):
        pass

    @staticmethod
    def get_a_section(professor, period_id, classroom):
        return db.session.query(Section).filter_by(professor=professor,
                                                   period_id=period_id,
                                                   classroom=classroom).first()

    @staticmethod
    def add_new_section(professor, period_id, classroom, section_type_id):
        section = Section(professor=professor,
                          period_id=period_id,
                          classroom=classroom,
                          section_type_id=section_type_id)
        db.session.add(section)
        db.session.commit()

    @staticmethod
    def search_section_type(description):
        return db.session.query(SectionType.id).filter_by(description=description).first()

    @staticmethod
    def get_a_section_by_callno(callno):
        return db.session.query(Section).filter_by(call_no=callno).first()

    @staticmethod
    def search_section_type_by_id(section_type_id):
        return db.session.query(SectionType).filter_by(id=section_type_id).first()
