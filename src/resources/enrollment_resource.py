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
    def get_all_uni():
        return db.session.query(Enrollment.uni)
    @staticmethod
    def get_enrollment(call_no, uni):
        return db.session.query(Enrollment).filter_by(call_no=call_no,
                                                      uni=uni).first()
    @staticmethod
    def update_project_id(call_no,uni,project_id):
        record = db.session.query(Enrollment).filter_by(call_no=call_no, uni=uni).first()
        record.project_id = project_id
        db.session.commit()
