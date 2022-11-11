from flask import request, jsonify

from src import app

from src.resources.period_resource import PeriodResource
from src.resources.section_resource import SectionResource


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
@app.route("/api/sections/<call_no>/new_student", methods=['POST'])
def add_new_student(call_no):
    pass


# Stephanie
@app.route("/api/sections/<call_no>/new_project", methods=['POST'])
def add_new_project(call_no):
    pass


# Stephanie
@app.route("/api/sections/<call_no>/projects/<project_id>/new_student", methods=['POST'])
def add_student_to_project(call_no, project_id):
    pass


# Stephanie
@app.route("/api/sections", methods=['GET'])
def get_all_sections():
    pass


# Stephanie
@app.route("/api/sections/students", methods=['GET'])
def get_all_students():
    pass


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
