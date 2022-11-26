import json

from flask import request, jsonify

from src import app

from src.resources.period_resource import PeriodResource
from src.resources.section_resource import SectionResource
from src.resources.enrollment_resource import EnrollmentResource
from src.resources.project_resource import ProjectResource

@app.route("/api/sections/health",methods = ['GET'])
def health_check():
    return "Hello! Health Check Succeed!"

@app.route("/api/sections/new_section", methods=['POST'])
def add_new_section():
    data = request.json
    period_id = PeriodResource.get_period_id(data['year'],
                                             data['semester'],
                                             data['day'],
                                             data['start_hr'],
                                             data['start_min'],
                                             data['end_hr'],
                                             data['end_min'])

    if period_id is None:
        PeriodResource.add_new_period(data['year'],
                                      data['semester'],
                                      data['day'],
                                      data['start_hr'],
                                      data['start_min'],
                                      data['end_hr'],
                                      data['end_min'])
        period_id = PeriodResource.get_period_id(data['year'],
                                                 data['semester'],
                                                 data['day'],
                                                 data['start_hr'],
                                                 data['start_min'],
                                                 data['end_hr'],
                                                 data['end_min'])

    section_exists = SectionResource.get_a_section(data['professor'], period_id[0], data['classroom'])
    if section_exists is not None:
        response = jsonify('Section cannot be added!')
        response.status_code = 400
        return response

    section_type_id = SectionResource.search_section_type(data['section_type'])
    SectionResource.add_new_section(data['professor'], period_id[0], data['classroom'], section_type_id[0])

    response = jsonify('Successfully added')
    response.status_code = 200
    return response


# Stephanie
# Add a new student to an existing section
@app.route("/api/sections/<call_no>/new_student", methods=['POST'])
def add_new_student(call_no):
    #can only accept POST, Body(raw)
    data = request.json
    # Add a resource called StudentResource
    section = SectionResource.get_a_section_by_callno(call_no)

    if section is None:
        #No such section
        response = jsonify('The section deos not exist.')
        response.status_code = 400
        return response

    uni = data['uni']
    #we assume uni exists
    enrollment_exist = EnrollmentResource.get_enrollment(call_no,uni)

    if enrollment_exist is not None:
        response = jsonify('The student has been added to the section.')
        response.status_code = 400
        return response



    EnrollmentResource.add_new_enrollment(call_no,uni,data['project_id'])

    response = jsonify('Successfully added')
    response.status_code = 200
    return response




# Stephanie
#Create a new project
@app.route("/api/sections/<call_no>/new_project", methods=['POST'])
def add_new_project(call_no):
    data = request.json
    #check if the section exists
    section_exist = SectionResource.get_a_section_by_callno(call_no)
    if section_exist is None:
        response = jsonify('Section does not exist!')
        response.status_code = 400
        return response

    project_exist = ProjectResource.get_project_id(call_no,data['project_name'],data['team_name'])

    #the project has been added!
    if project_exist is not None:
        response = jsonify('Project already exists!')
        response.status_code = 400
        return response

    ProjectResource.add_new_project(call_no,data['project_name'],data['team_name'])
    response = jsonify('Successfully added')
    response.status_code = 200
    return response

# Stephanie
#Add an enrolled student to an existing project
#change the enrollment
@app.route("/api/sections/<call_no>/projects/<project_id>/new_student", methods=['POST'])
def add_student_to_project(call_no, project_id):
    data = request.json
    #check if section exist
    if SectionResource.get_a_section_by_callno(call_no) is None:
        response = jsonify('Section does not exist!')
        response.status_code = 400
        return response

    #check if project exist
    project_exist = ProjectResource.get_project_by_project_id(project_id)
    if project_exist is None:
        response = jsonify('The project does not exist!')
        response.status_code = 400
        return response

    #add the student to the enrollment table
    EnrollmentResource.add_new_enrollment(call_no,data['uni'],project_id)
    response = jsonify('Successfully add the student to the project')
    response.status_code = 200
    return response

# Stephanie
@app.route("/api/sections", methods=['GET'])
def get_all_sections():
    all_sections = SectionResource.get_all_sections()
    result = {}
    result["sections"] = []
    for section in all_sections:
        section_dict = {}
        for c in section.__table__.columns:
            section_dict[c.name] = getattr(section,c.name)
        result["sections"].append(json.dumps(section_dict))

    response = jsonify(result)

    response.status_code = 200
    return response



# Stephanie
@app.route("/api/sections/students", methods=['GET'])
def get_all_students():

    all_students = EnrollmentResource.get_all()
    result = {}
    result["students"] = []
    for student in all_students:
        student_dict = {}
        for c in student.__table__.columns:
            student_dict[c.name] = getattr(student, c.name)
        result["students"].append(json.dumps(student_dict))

    response = jsonify(result)

    response.status_code = 200
    return response


# Zhiyuan
@app.route("/api/sections/<call_no>", methods=['GET'])
def get_one_section(call_no):
    pass


# Zhiyuan
@app.route("/api/sections/<call_no>/students", methods=['GET'])
def get_students_in_one_section(call_no):
    pass


# Zhiyuan
@app.route("/api/sections/<call_no>/projects", methods=['GET'])
def get_all_projects_in_one_section(call_no):
    pass


# Zhiyuan
@app.route("/api/sections/<call_no>/projects/<project_id>", methods=['GET'])
def get_one_project_in_one_section(call_no, project_id):
    pass


# Zhiyuan
@app.route("/api/sections/<call_no>/projects/<project_id>/all_students", methods=['GET'])
def get_all_students_in_one_project_in_one_section(call_no, project_id):
    pass


# Zhiyuan
@app.route("/api/sections/<call_no>/students/<uni>", methods=['GET'])
def get_a_student_in_one_section(uni):
    pass


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011)
