from flask import request, jsonify

from src import app

from src.resources.period_resource import PeriodResource
from src.resources.section_resource import SectionResource
from src.resources.enrollment_resource import EnrollmentResource
from src.resources.project_resource import ProjectResource

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
    data = request.json
    # Add a resource called StudentResource
    section = SectionResource.get_a_section_by_callno(call_no)

    if section is None:
        response = jsonify('The section deos not exist.')
        response.status_code = 400
        return response


    uni = data['uni']
    uni_exist = True
    #we need to check whether the uni exists
    if not uni_exist:
        response = jsonify('The uni is not correct')
        response.status_code = 400
        return response

    enrollment_exist = EnrollmentResource.get_enrollment(call_no,uni)
    if enrollment_exist is not None:
        response = jsonify('The student has been added to the section.')
        response.status_code = 400

    EnrollmentResource.add_new_enrollment(call_no,uni,data['project_id'])
    response = jsonify('Successfully added')
    response.status_code = 200
    return response




# Stephanie
#Create a new project
@app.route("/api/sections/<call_no>/new_project", methods=['POST'])
def add_new_project(call_no):
    data = request.json
    section_exist = SectionResource.get_a_section_by_callno(call_no)
    if section_exist is None:
        response = jsonify('Section does not exist!')
        response.status_code = 400
        return response
    project_exist = ProjectResource.get_project_id(call_no,data['project_name'],data['team_name'])
    if project_exist is None:
        response = jsonify('Project already exists!')
        response.status_code = 400
        return response
    ProjectResource.add_new_project(call_no,data['project_name'],data['team_name'])
    response = jsonify('Successfully added')
    response.status_code = 200
    return response

# Stephanie
#Add an enrolled student to an existing project
@app.route("/api/sections/<call_no>/projects/<project_id>/new_student", methods=['PUT'])
def add_student_to_project(call_no, project_id):
    data = request.json
    #check if section exist
    #check if project exist
    project_exist = ProjectResource.get_project_by_project_id(project_id)
    if project_exist is None:
        response = jsonify('The project does not exist!')
        response.status_code = 400
        return response
    #check if student is enrolled
    enrolled = EnrollmentResource.get_enrollment(call_no,data['uni'])
    if enrolled is None:
        response = jsonify('The student is not enrolled!')
        response.status_code = 400
        return response

    EnrollmentResource.update_project_id(call_no,data['uni'],project_id)
    response = jsonify('Successfully add the student to the project')
    response.status_code = 200
    return response

# Stephanie
@app.route("/api/sections", methods=['GET'])
def get_all_sections():


    #json?
    response = jsonify(SectionResource.get_all_sections())
    response.status_code = 200
    return response




# Stephanie
@app.route("/api/sections/students", methods=['GET'])
def get_all_students():

    EnrollmentResource.get_all_uni()
    #use the uni to get all the studentsß
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
