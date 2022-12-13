from src import db
from src.models.enrollment import Enrollment
from src.resources.project_resource import ProjectResource
from src.resources.section_resource import SectionResource


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
        enrollments_dict = {}
        for enrollment in all_enrollments:
            enrollment_dict = {}
            for c in enrollment.__table__.columns:
                enrollment_dict[c.name] = getattr(enrollment,c.name)

            enrollment_dict['project_name'] = ""
            enrollment_dict['team_name'] = ""
            if enrollment.project_id is not None:
                project = ProjectResource.get_by_id(enrollment.project_id)
                enrollment_dict['project_name'] = project.project_name
                enrollment_dict['team_name'] = project.team_name
            enrollment_dict["section_period"] = SectionResource.get_section_info(enrollment.call_no)
            enrollments_dict[enrollment.uni] = enrollment_dict
        return enrollments_dict

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
            project = ProjectResource.get_by_id(record.project_id)
            db.session.delete(record)
            if len(project.enrollments) == 0:
                db.session.delete(project)
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


        
        
  
