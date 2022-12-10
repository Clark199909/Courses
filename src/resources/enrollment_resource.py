from src import db
from src.models.enrollment import Enrollment


class EnrollmentResource:
    def __int__(self):
        pass

    @staticmethod
    def add_new_enrollment(call_no, uni, project_id):
        enrollment = Enrollment(call_no=call_no,
                                uni=uni,
                                project_id=project_id)

        db.session.add(enrollment)
        db.session.commit()


    @staticmethod
    def get_all_enrollments():
        """
        :return:  a list of dictionaries
        """
        all_enrollments =  db.session.query(Enrollment).all()
        enrollments_list = []
        for enrollment in all_enrollments:
            enrollment_dict = {}
            for c in enrollment.__table__.columns:
                enrollment_dict[c.name] = getattr(enrollment,c.name)
            enrollments_list.append(enrollment_dict)
        return enrollments_list

    @staticmethod
    def get_uni_by_callno(call_no):
        return db.session.query(Enrollment.uni).filter_by(call_no=call_no)

    @staticmethod
    def get_project_by_callno(call_no):
        return db.session.query(Enrollment.project_id).filter_by(call_no=call_no).distinct()

    @staticmethod
    def get_uni_by_callno_and_id(call_no, project_id):
        return db.session.query(Enrollment.uni).filter_by(call_no=call_no, project_id=project_id)


    @staticmethod
    def get_by_callno_and_uni(call_no, uni):
        return db.session.query(Enrollment).filter_by(call_no=call_no, uni=uni).first()


    @staticmethod
    def update_project_id(call_no,uni,project_id):
        record = db.session.query(Enrollment).filter_by(call_no=call_no, uni=uni).first()
        record.project_id = project_id
        db.session.commit()

    @staticmethod
    def delete_by_section_and_uni(call_no, uni):
        records = db.session.query(Enrollment).filter_by(call_no=call_no, uni=uni)
        for record in records:
            db.session.delete(record)
        db.session.commit()

    @staticmethod
    def delete_by_project_id(project_id):
        records = db.session.query(Enrollment).filter_by(project_id = project_id)
        for record in records:
            db.session.delete(record)
        db.session.commit()

    @staticmethod
    def update(uni, call_no, project_id):
        db.session.query(Enrollment).filter_by(uni=uni).update(
            {'call_no': call_no,
            'project_id': project_id,
            })
        db.session.commit()


        
        
  
