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

    @staticmethod

    def get_by_callno(call_no):
        return db.session.query(Project).filter_by(call_no=call_no)

    @staticmethod
    def delete_by_id(project_id):
        project = db.session.query(Project).filter_by(id = project_id).first()
        db.session.delete(project)
        db.session.commit()

    @staticmethod
    def update_a_project(project_id, project_name, team_name):
        db.session.query(Project).filter_by(id=project_id).update(
            {'project_name': project_name,
             'team_name': team_name})
        db.session.commit()

    def get_all_projects():
        all_projects = db.session.query(Project).all()
        projects_list = []
        for project in all_projects:
            project_dict = {}
            for c in project.__table__.columns:
                project_dict[c.name] = getattr(project, c.name)
            projects_list.append(project_dict)
        return projects_list
