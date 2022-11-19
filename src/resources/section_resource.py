from src import db
from src.models.section import Section
from src.models.section_type import SectionType


class SectionResource:
    def __int__(self):
        pass

    @staticmethod
    def get_all_sections():
        return db.session.query(Section)
    @staticmethod
    def get_a_section(professor, period_id, classroom):
        return db.session.query(Section).filter_by(professor=professor,
                                                   period_id=period_id,
                                                   classroom=classroom).first()

    #Stephanie
    @staticmethod
    def get_a_section_by_callno(call_no):
        return db.session.query(Section).filter_by(call_no=call_no).first()

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
