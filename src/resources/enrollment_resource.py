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
    def get_by_callno_and_uni(call_no, uni):
        return db.session.query(Enrollment).filter_by(call_no=call_no, uni=uni).first()

    @staticmethod
    def update_project_id(call_no,uni,project_id):
        record = db.session.query(Enrollment).filter_by(call_no=call_no, uni=uni).first()
        record.project_id = project_id
        db.session.commit()
