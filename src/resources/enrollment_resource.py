from src import db
from src.models.enrollment import Enrollment


class EnrollmentResource:
    def __int__(self):
        pass

    @staticmethod
    def get_uni_by_callno(call_no):
        return db.session.query(Enrollment.uni).filter_by(call_no=call_no)

    @staticmethod
    def get_project_by_callno(call_no):
        return db.session.query(Enrollment.project_id).filter_by(call_no=call_no).distinct()
    
