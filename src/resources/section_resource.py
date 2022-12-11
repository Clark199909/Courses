from src import db
from src.models.section import Section
from src.models.section_type import SectionType


class SectionResource:
    def __int__(self):
        pass

    @staticmethod
    def get_all_sections():
        """
        :return: a list of dictionaries
        """
        all_sections =  db.session.query(Section).all()
        sections_list = []
        for section in all_sections:
            section_dict = {
                "call_no": section.call_no,
                "professor": section.professor,
                "classroom": section.classroom,
                "year": section.period.year,
                "semester": section.period.semester,
                "day": section.period.day,
                "start_hr": section.period.start_hr,
                "start_min": section.period.start_min,
                "end_hr": section.period.end_hr,
                "end_min": section.period.end_min,
                "section_type": section.section_type.description,
                "projects_num": len(section.projects),
                "enrollments_num": len(section.enrollments)
            }
            sections_list.append(section_dict)
        return sections_list



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
    def delete_a_section_by_call_no(call_no):
        section = db.session.query(Section).filter_by(call_no=call_no).first()
        db.session.delete(section)
        db.session.commit()
    
    @staticmethod
    def update_a_section(call_no, professor, period_id, classroom, section_type_id):
        db.session.query(Section).filter_by(call_no=call_no).update(
            {'professor': professor,
            'period_id': period_id,
            'classroom': classroom,
            'section_type_id': section_type_id})
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

    @staticmethod
    def delete_a_section_by_call_no(call_no):
        section = db.session.query(Section).filter_by(call_no=call_no).first()
        db.session.delete(section)
        db.session.commit()

