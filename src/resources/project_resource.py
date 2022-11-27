from src import db
from src.models.project import Project


class ProjectResource:
    def __int__(self):
        pass

    @staticmethod
    def add_new_project(call_no,project_name,team_name):
        project = Project(call_no=call_no,
                          project_name=project_name,
                          team_name = team_name)

        db.session.add(project)
        db.session.commit()

    @staticmethod
    def get_by_id(project_id):
        return db.session.query(Project).filter_by(id = project_id).first()


    @staticmethod
    def get_project_id(call_no,project_name,team_name):
        return db.session.query(Project.id).filter_by(call_no=call_no,
                                                      project_name=project_name,
                                                      team_name = team_name).first()

    @staticmethod
    def get_by_callno_and_id(call_no, project_id):
        return db.session.query(Project).filter_by(call_no=call_no, id=project_id).first()

    @staticmethod
    def get_by_id(project_id):
        return db.session.query(Project).filter_by(id=project_id).first()

    @staticmethod
    def get_by_callno_and_id(call_no, project_id):
        return db.session.query(Project).filter_by(call_no=call_no, id=project_id).first()

    
