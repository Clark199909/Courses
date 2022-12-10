import json

from flask import request, jsonify

from src import app

from src.resources.period_resource import PeriodResource
from src.resources.section_resource import SectionResource
from src.resources.enrollment_resource import EnrollmentResource
from src.resources.project_resource import ProjectResource



# send request body:
# {
#     "year": "2022",
#     "semester": "Fall",
#     "day": "MW",
#     "start_hr": "9",
#     "start_min": "10",
#     "end_hr": "10",
#     "end_min": "25",
#     "professor": "Donald Ferguson",
#     "classroom": "ABC123",
#     "section_type": "CVN"
# }

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
    """
    :param call_no: 10001
    :return: request body
    {
    "uni":"tk1024",
    "project_id":2
    }
    """
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
    enrollment_exist = EnrollmentResource.get_by_callno_and_uni(call_no,uni)

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
    """
    :param call_no: 10001 (make sure the call_no has been added to the database
    request body:
    {
    "project_name":"Donald's Fans",
    "team_name":"Cloud Computing Team 3"
    }
    """
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
    """
    :param call_no:10001
    :param project_id:1
    request body:
    {
    "uni":"df989"
    }
    """
    data = request.json
    #check if section exist
    if SectionResource.get_a_section_by_callno(call_no) is None:
        response = jsonify('Section does not exist!')
        response.status_code = 400
        return response

    #check if project exist
    project_exist = ProjectResource.get_by_id(project_id)
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
    """
    :return: response body
    [
    {
        "call_no": 10001,
        "classroom": "Mudd311",
        "period_id": 1,
        "professor": "Donald Ferguson",
        "section_type_id": 1
    },
    {
        "call_no": 10002,
        "classroom": "Mudd302",
        "period_id": 2,
        "professor": "Yuri",
        "section_type_id": 1
    }]
    """
    all_sections = SectionResource.get_all_sections()
    if all_sections is None:
        response =  jsonify("No sections found")
        response.status_code = 400
        return response

    response = jsonify(all_sections)
    response.status_code = 200
    return response



# Stephanie
@app.route("/api/sections/students", methods=['GET'])
def get_all_students():
    """
    :return: response body
    [
    {
        "call_no": 10001,
        "project_id": 1,
        "uni": "df999"
    },
    {
        "call_no": 10001,
        "project_id": 1,
        "uni": "tt1024"
    }]
    """

    all_students = EnrollmentResource.get_all_enrollments()
    response = jsonify(all_students)
    response.status_code = 200
    return response


# Zhiyuan
'''
example return
success
{
    "call_no": 1,
    "classroom": "CSB451",
    "day": "Fri",
    "end_hr": 15,
    "end_min": 40,
    "professor": "Feguson",
    "section_type": "in_person",
    "semester": "Fall",
    "start_hr": 13,
    "start_min": 10,
    "year": 2022
}
fail
"Section does not exist!"
'''
@app.route("/api/sections/<call_no>", methods=['GET'])
def get_one_section(call_no):
    section = SectionResource.get_a_section_by_callno(call_no)

    if section is None:
        response = jsonify('Section does not exist!')
        response.status_code = 400
        return response

    section_type_id = section.section_type_id
    section_type = SectionResource.search_section_type_by_id(section_type_id)
    if section_type is None:
        response = jsonify('Section type does not exist! Check db for consistency!')
        response.status_code = 400
        return response

    period_id = section.period_id
    period = PeriodResource.get_period_by_id(period_id)
    if period is None:
        response = jsonify('Period does not exist! Check db for consistency!')
        response.status_code = 400
        return response

    data = {"call_no": section.call_no,
            "professor": section.professor,
            "classroom": section.classroom,
            "section_type": section_type.description,
            "year": period.year,
            "semester": period.semester,
            "day": period.day,
            "start_hr": period.start_hr,
            "start_min": period.start_min,
            "end_hr": period.end_hr,
            "end_min": period.end_min,
            }
    response = jsonify(data)
    response.status_code = 200
    return response


# response fields:
# Zhiyuan
'''
example return
success
[
    "stu1",
    "stu2",
    "stu3",
    "stu4",
    "stu5"
]
fail
"No record found!"
'''
@app.route("/api/sections/<call_no>/students", methods=['GET'])
def get_students_in_one_section(call_no):
    enrollments = EnrollmentResource.get_uni_by_callno(call_no)
    if enrollments is None:
        response = jsonify('No record found!')
        response.status_code = 400
        return response

    data = [enrollment.uni for enrollment in enrollments]
    response = jsonify(data)
    response.status_code = 200
    return response


# Zhiyuan
'''
example return 
success
[
    {
        "project_id": 1,
        "project_name": "proj1",
        "team_name": "team1"
    },
    {
        "project_id": 2,
        "project_name": "proj2",
        "team_name": "team2"
    }
]
fail
"No record found!"
'''
@app.route("/api/sections/<call_no>/projects", methods=['GET'])
def get_all_projects_in_one_section(call_no):
    enrollments = EnrollmentResource.get_project_by_callno(call_no)
    if enrollments is None:
        response = jsonify('No record found!')
        response.status_code = 400
        return response

    data = []
    for enrollment in enrollments:
        project_id = enrollment.project_id
        # project id is foreign key
        project = ProjectResource.get_by_id(project_id)
        data.append({"project_id": project_id,
                     "project_name": project.project_name,
                     "team_name": project.team_name
                     })
    response = jsonify(data)
    response.status_code = 200
    return response


@app.route("/api/sections/all_projects", methods=['GET'])
def get_all_projects():
    all_projects = ProjectResource.get_all_projects()
    if all_projects is None:
        response = jsonify("No projects found")
        response.status_code = 400
        return response

    response = jsonify(all_projects)
    response.status_code = 200
    return response


# Zhiyuan
'''
example return
success
{
    "project_id": "2",
    "project_name": "proj2",
    "team_name": "team2"
}
fail
"Section/Project does not exist!"
'''
@app.route("/api/sections/<call_no>/projects/<project_id>", methods=['GET'])
def get_one_project_in_one_section(call_no, project_id):
    project = ProjectResource.get_by_callno_and_id(call_no, project_id)
    if project is None:
        response = jsonify('Section/Project does not exist!')
        response.status_code = 400
        return response

    data = {"project_id": project_id,
            "project_name": project.project_name,
            "team_name": project.team_name
            }
    response = jsonify(data)
    response.status_code = 200
    return response


# Zhiyuan
'''
example return
[
    "stu3",
    "stu4",
    "stu5"
]
fail
"No record found!"
'''
@app.route("/api/sections/<call_no>/projects/<project_id>/all_students", methods=['GET'])
def get_all_students_in_one_project_in_one_section(call_no, project_id):
    enrollments = EnrollmentResource.get_uni_by_callno_and_id(call_no, project_id)
    if enrollments is None:
        response = jsonify('No record found!')
        response.status_code = 400
        return response

    data = [enrollment.uni for enrollment in enrollments]
    response = jsonify(data)
    response.status_code = 200
    return response


# Zhiyuan
'''
example return
success:
{
    "project_id": 1,
    "project_name": "proj1",
    "team_name": "team1",
    "uni": "stu2"
}
fail
"No record found!"
'''
@app.route("/api/sections/<call_no>/students/<uni>", methods=['GET'])
def get_a_student_in_one_section(call_no, uni):
    enrollment = EnrollmentResource.get_by_callno_and_uni(call_no, uni)
    if enrollment is None:
        response = jsonify('No record found!')
        response.status_code = 400
        return response

    # also return the project that the student belongs to
    project_id = enrollment.project_id
    project = ProjectResource.get_by_id(project_id)  # foreign key must exist
    data = {"uni": uni,
            "project_id": project_id,
            "project_name": project.project_name,
            "team_name": project.team_name}
    response = jsonify(data)
    response.status_code = 200
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5013)
