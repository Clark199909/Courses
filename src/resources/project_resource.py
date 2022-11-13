from src import db
from src.models.project import Project

class ProjectResource:
    def __int__(self):
        pass

    @staticmethod
    def get_by_id(project_id):
        return db.session.query(Project).filter_by(id=project_id).first()

    @staticmethod
    def get_by_callno_and_id(call_no, project_id):
        return db.session.query(Project).filter_by(call_no=call_no, id=project_id).first()

    
