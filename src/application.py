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
    # TODO need to check fields in data
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
    # can only accept POST, Body(raw)
    data = request.json
    # Add a resource called StudentResource
    section = SectionResource.get_a_section_by_callno(call_no)

    if section is None:
        # No such section
        response = jsonify('The section deos not exist.')
        response.status_code = 400
        return response

    uni = data['uni']
    # we assume uni exists
    enrollment_exist = EnrollmentResource.get_by_callno_and_uni(call_no, uni)

    if enrollment_exist is not None:
        response = jsonify('The student has been added to the section.')
        response.status_code = 400
        return response

    project_id = data['project_id']
    EnrollmentResource.add_new_enrollment(call_no, uni, project_id)
    response = jsonify('Successfully added')
    response.status_code = 200
    return response


# Stephanie
# Create a new project
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
    # check if the section exists
    section_exist = SectionResource.get_a_section_by_callno(call_no)
    if section_exist is None:
        response = jsonify('Section does not exist!')
        response.status_code = 400
        return response

    project_exist = ProjectResource.get_project_id(call_no, data['project_name'], data['team_name'])

    # the project has been added!
    if project_exist is not None:
        response = jsonify('Project already exists!')
        response.status_code = 400
        return response

    ProjectResource.add_new_project(call_no, data['project_name'], data['team_name'])

    project_id_res = ProjectResource.get_project_id(call_no, data['project_name'], data['team_name'])
    project_id = None if project_id_res is None else project_id_res[0]
    for uni in data['project_members']:
        if SectionResource.get_a_section_by_callno(call_no) is None:
            response = jsonify('Section does not exist!')
            response.status_code = 400
            return response

        # check if project exist
        project_exist = ProjectResource.get_by_id(project_id)
        if project_exist is None:
            response = jsonify('The project does not exist!')
            response.status_code = 400
            return response

        EnrollmentResource.update_project_id(call_no, uni, project_id)

    response = jsonify('Successfully added')
    response.status_code = 200
    return response


# Stephanie
# Add an enrolled student to an existing project
# change the enrollment
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
    # check if section exist
    if SectionResource.get_a_section_by_callno(call_no) is None:
        response = jsonify('Section does not exist!')
        response.status_code = 400
        return response

    # check if project exist
    project_exist = ProjectResource.get_by_id(project_id)
    if project_exist is None:
        response = jsonify('The project does not exist!')
        response.status_code = 400
        return response

    # add the student to the enrollment table
    EnrollmentResource.add_new_enrollment(call_no, data['uni'], project_id)
    response = jsonify('Successfully add the student to the project')
    response.status_code = 200
    return response


@app.route("/api/sections/<call_no>/projects/<project_id>/new_students", methods=['POST'])
def add_students_to_project(call_no, project_id):
    data = request.json
    # check if section exist

    for uni in data['project_members']:

        if SectionResource.get_a_section_by_callno(call_no) is None:
            response = jsonify('Section does not exist!')
            response.status_code = 400
            return response

        # check if project exist
        project_exist = ProjectResource.get_by_id(project_id)
        if project_exist is None:
            response = jsonify('The project does not exist!')
            response.status_code = 400
            return response

        EnrollmentResource.update_project_id(call_no, uni, project_id)

    response = jsonify('Successfully add students to the project')
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
        response = jsonify("No sections found")
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


@app.route("/api/sections/<call_no>/students/no_project", methods=['GET'])
def get_students_in_one_section_with_no_project(call_no):
    enrollments = EnrollmentResource.get_enrollments_by_callno(call_no)
    if enrollments is None:
        response = jsonify('No record found!')
        response.status_code = 400
        return response

    data = [enrollment.uni for enrollment in enrollments if enrollment.project_id is None]
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


def _delete_a_project(project_id):
    try:
        EnrollmentResource.remove_project(project_id)
        ProjectResource.delete_by_id(project_id)
    except Exception as err:
        print(f"error: {repr(err)}")


# Zhiyuan
@app.route("/api/sections/<call_no>/students/<uni>", methods=['DELETE'])
def delete_a_student_in_one_section(call_no, uni):
    """
    response
    "enrollment deletion done"
    """
    record = EnrollmentResource.get_by_callno_and_uni(call_no, uni)
    if record is None:
        response = jsonify('Student is not in the section!')
        response.status_code = 400
        return response

    try:
        EnrollmentResource.delete_by_section_and_uni(call_no, uni)
    except Exception as err:
        print(f"error: {repr(err)}")
    response = jsonify("enrollment deletion done")
    response.status_code = 200
    return response


# Zhiyuan
@app.route("/api/sections/delete_project/<project_id>", methods=['DELETE'])
def delete_project(project_id):
    """
    response
    "project deletion done"
    """
    project = ProjectResource.get_by_id(project_id)
    if project is None:
        response = jsonify('Project does not exist!')
        response.status_code = 400
        return response

    _delete_a_project(project_id)
    response = jsonify("project deletion done")
    response.status_code = 200
    return response


# Zhiyuan
@app.route("/api/sections/<call_no>", methods=['DELETE'])
def delete_section(call_no):
    """
    response
    "project deletion done"
    """
    section = SectionResource.get_a_section_by_callno(call_no)
    if section is None:
        response = jsonify('Section does not exist!')
        response.status_code = 400
        return response

    projects = ProjectResource.get_by_callno(call_no)
    for project in projects:
        _delete_a_project(project.id)
    SectionResource.delete_a_section_by_call_no(call_no)

    response = jsonify("section deletion done")
    response.status_code = 200
    return response


# Zhiyuan
@app.route("/api/enrollment/<uni>", methods=['PUT'])
def update_enrollment(uni):
    """
    request body:
    {
        "call_no": 2,
        "project_id": 3,
    }
    response:
    "Successfully updated"
    """
    data = request.json
    call_no, project_id = data['call_no'], data['project_id']
    # check if section exist
    section_exist = SectionResource.get_a_section_by_callno(call_no)
    if section_exist is None:
        response = jsonify('Section does not exist!')
        response.status_code = 400
        return response

    if project_id is not None and ProjectResource.get_by_callno_and_id(call_no, project_id) is None:
        response = jsonify('The project does not exist!')
        response.status_code = 400
        return response

    # modify the enrollment table
    EnrollmentResource.update(uni, call_no, project_id)
    response = jsonify('Successfully updated')
    response.status_code = 200
    return response


# Zhiyuan
@app.route("/api/sections/<call_no>/update_project/<project_id>", methods=['PUT'])
def update_project(call_no, project_id):
    """
    request body:
    {
    "project_name":"Donald's Fans",
    "team_name":"Cloud Computing Team 3",
    "project_members": ["ab1234"]
    }
    response:
    "Successfully updated"
    """
    # only project_name and team_name are allowed to be udpated. 
    # it does not make sense to change its section, as it is subject to constraints of student enrollment

    data = request.json
    # check if the project exists
    project_exist = ProjectResource.get_by_id(project_id)
    if project_exist is None:
        response = jsonify('Project does not exist!')
        response.status_code = 400
        return response

    ProjectResource.update_a_project(project_id, data['project_name'], data['team_name'])
    original_members = set()
    original_members_res = EnrollmentResource.get_uni_by_callno_and_id(call_no, project_id)
    for r in original_members_res:
        original_members.add(r[0])
    cur_members = set(data['project_members'])
    print(original_members, cur_members)

    for uni in cur_members:
        if uni not in original_members:
            EnrollmentResource.update_project_id(call_no, uni, project_id)

    for uni in original_members:
        if uni not in cur_members:
            EnrollmentResource.update_project_id(call_no, uni, None)

    response = jsonify('Successfully updated')
    response.status_code = 200
    return response


# Zhiyuan
@app.route("/api/sections/<call_no>", methods=['PUT'])
def update_section(call_no):
    """
    send request body:
    {
        "year": "2022",
        "semester": "Fall",
        "day": "MW",
        "start_hr": "9",
        "start_min": "10",
        "end_hr": "10",
        "end_min": "25",
        "professor": "Donald Ferguson",
        "classroom": "ABC123",
        "section_type": "CVN"
    }
    response
    "Successfully updated"
    """
    # TODO need to check fields in data
    data = request.json

    section_exists = SectionResource.get_a_section_by_callno(call_no)
    if section_exists is None:
        response = jsonify('Section does not exist!')
        response.status_code = 400
        return response

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

    # TODO handle section_type not exist error
    section_type_id = SectionResource.search_section_type(data['section_type'])
    SectionResource.update_a_section(call_no, data['professor'], period_id[0], data['classroom'], section_type_id[0])

    response = jsonify('Successfully updated')
    response.status_code = 200
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5013)
