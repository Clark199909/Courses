import unittest
from src.application import app
import json


class TestCourses(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        print("SET UP Succeed!!")

    def testCreateNewSection(self):
        #1. we can successfully create new section
        new_section = json.dumps({
                "year": "2018",
                "semester": "Fall",
                "day": "Mon",
                "start_hr": "9",
                "start_min": "10",
                "end_hr": "12",
                "end_min": "25",
                "professor": "Donald",
                "classroom": "ABC123",
                "section_type": "CVN"
            })
        headers = {"Content-Type": "application/json"},

        response = self.app.post("/api/sections/new_section",content_type='application/json',data=new_section)
        self.assertIn("Success",response.json)
        self.assertEqual(200, response.status_code)

        # #2. add an existing section
        response = self.app.post("/api/sections/new_section", content_type='application/json', data=new_section)
        self.assertIn("cannot be added", response.json)
        self.assertEqual(400, response.status_code)
        # #exception
        # #key error with status_code 500

    def testAddStudentToSection(self):
        student = json.dumps({
    "uni":"mm1024",
    "project_id":2
    })
        call_no = "10003"
        api = "/api/sections/{}/new_student".format(call_no)
        headers = {"Content-Type": "application/json"}
        #1. we can successfully add a new student to a section
        response = self.app.post(api,headers = headers,data = student)
        self.assertIn("Success", response.json)
        self.assertEqual(200, response.status_code)
        #2. if the student has been enrolled
        response = self.app.post(api,headers = headers,data = student)
        self.assertIn("has been added", response.json)
        self.assertEqual(400, response.status_code)
        #3. if the section does not exist
        call_no = "X"+ "1000"+"B"
        api = "/api/sections/{}/new_student".format(call_no)
        response = self.app.post(api,headers = headers,data = student)
        self.assertIn("section deos not exist", response.json)
        self.assertEqual(400, response.status_code)
        #4. error --> no uni  no project_id

    def testCreateNewProject(self):
        headers = {"Content-Type": "application/json"}
        project = json.dumps({
        "project_name":"Donald Trump MY GOAL",
        "team_name":"Cloud Computing Team 007"
    })

        call_no = "10001"
        api = "/api/sections/{}/new_project".format(call_no)
        #1. we can successfully add a project to a section
        response = self.app.post(api, headers = headers,data = project)
        self.assertIn("Success", response.json)
        self.assertEqual(200, response.status_code)
        #2. if the project has been added
        response = self.app.post(api,headers = headers,data = project)
        self.assertIn("already exists", response.json)
        self.assertEqual(400, response.status_code)

        #3. if the section does not exist
        call_no = "X"+ "1000"+"B"
        api = "/api/sections/{}/new_project".format(call_no)
        response = self.app.post(api,headers = headers,data = project)
        self.assertIn("does not exist", response.json)
        self.assertEqual(400, response.status_code)

    def testAddStudentToProject(self):
        headers = {"Content-Type": "application/json"}
        student = json.dumps({ "uni":"sw1234"})
        call_no = "10002"
        project_id = "3"
        api = "/api/sections/{}/projects/{}/new_student".format(call_no,project_id)
        # 1. we can successfully add a student to a section
        response = self.app.post(api, headers=headers, data=student)
        self.assertIn("Success", response.json)
        self.assertEqual(200, response.status_code)


        # 2. if the section does not exist
        call_no = "X" + "1000" + "B"
        api = "/api/sections/{}/projects/{}/new_student".format(call_no,project_id)
        response = self.app.post(api, headers=headers, data=student)
        self.assertIn("Section does not exist", response.json)
        self.assertEqual(400, response.status_code)
        # 3. if the project does not exist
        call_no = "10002"
        project_id = "X" + "1000" + "B"
        api = "/api/sections/{}/projects/{}/new_student".format(call_no,project_id)
        response = self.app.post(api, headers=headers, data=student)
        self.assertIn("project does not exist", response.json)
        self.assertEqual(400, response.status_code)


#READ
    def testGetAllSections(self):
        #1. successfully get
        response = self.app.get("/api/sections")
        self.assertEqual(list, type(response.json))
        # 2. if no sections
        self.assertNotIn("No sections found",response.json)
        self.assertEqual(200,response.status_code)
        #3. attributes
        if len(response.json) > 0:
            self.assertEqual({'classroom', 'professor', 'call_no', 'section_type_id', 'period_id'},set(response.json[0].keys()))

    def testGetAllStudents(self):
        # 1. successfully get
        response = self.app.get("/api/sections/students")
        self.assertEqual(list, type(response.json))
        # 2. if no sections
        self.assertNotIn("No sections found", response.json)
        self.assertEqual(200, response.status_code)
        # 3. attributes
        if len(response.json) > 0:
            self.assertEqual({"call_no", "project_id", "uni"},
                             set(response.json[0].keys()))

    def testGetOneSection(self):
        section = "10001"
        # 1. successfully get
        response = self.app.get("/api/sections/{}".format(section))
        self.assertEqual(dict, type(response.json))
        self.assertEqual(
            set(['call_no', 'classroom', 'day', 'end_hr', 'end_min', 'professor', 'section_type', 'semester',
                 'start_hr', 'start_min', 'year']), set(response.json.keys()))
        self.assertEqual(200, response.status_code)
        # 2. if no such section
        section = "XXXXXX"
        response = self.app.get("/api/sections/{}".format(section))
        self.assertIn("Section does not exist", response.json)
        # 3. section type
        self.assertNotIn("Section type does not exist",response.json)
        # 4. Period type
        self.assertNotIn("Period does not exist",response.json)



    def testGetStudentsInOneSection(self):
        call_no = "10001"
        # 1. successfully get

        response = self.app.get("/api/sections/{}/students".format(call_no))
        #2 .response  type
        self.assertEqual(list, type(response.json))

        self.assertEqual(200, response.status_code)
        # 3. No record --- ?????? BUG in the application.py return []
        call_no = "XXXXXXXXX"
        response = self.app.get("/api/sections/{}/students".format(call_no))

        # self.assertIn("No record found", response.json)
        # self.assertEqual(400,response.status_code)


    def testGetProjectsInOneSection(self):
        call_no = "10001"
        # 1. successfully get
        response = self.app.get("/api/sections/{}/projects".format(call_no))

        # 2. response type
        self.assertEqual(list, type(response.json))
        self.assertEqual(dict, type(response.json[0]))
        self.assertEqual(set(["project_id","project_name","team_name"]),set(response.json[0].keys()))
        self.assertEqual(200, response.status_code)
        # 3. No record --- ?????? BUG in the application.py return []
        # flask_sqlalchemy.BaseQuery -- should not use flask_sqlalchemy.BaseQuery == None

        response = self.app.get("/api/sections/{}/projects".format("XXXXXXXXX"))
        #self.assertIn("No record found", response.json)

    def testGetOneProjectInOneSection(self):
        call_no = "10001"
        project_id = "1"
        # 1. successfully get
        response = self.app.get("/api/sections/{}/projects/{}".format(call_no,project_id))

        self.assertEqual(200,response.status_code)
        self.assertEqual(dict,type(response.json))
        self.assertEqual(set(['project_name', 'project_id', 'team_name']),set(response.json.keys()))

        # 2. Fail - no such project or no such section
        call_no = "XXXXXXX"
        project_id = "KKKKKKK"
        response = self.app.get("/api/sections/{}/projects/{}".format(call_no, project_id))

        self.assertEqual(400,response.status_code)
        self.assertIn("does not exist", response.json)

    def testGetStudentsInOneProject(self):
        call_no = "10001"
        project_id = "1"
        #1. successfully get
        response = self.app.get("/api/sections/{}/projects/{}/all_students".format(call_no,project_id))
        self.assertEqual(200, response.status_code)
        self.assertEqual(list, type(response.json))

        # 2. no such record --- problem with api
        call_no = "XXXXXXX"
        project_id = "BBBBBBB"
        response = self.app.get("/api/sections/{}/projects/{}/all_students".format(call_no, project_id))
        # self.assertEqual(400, response.status_code)

    def testGetOneStudentInOneSection(self):
        call_no = "10001"
        uni  = "df999"
        response = self.app.get("/api/sections/{}/students/{}".format(call_no, uni))
        self.assertEqual(200, response.status_code)
        self.assertEqual(dict, type(response.json))
        self.assertEqual({'project_name', 'uni', 'project_id', 'team_name'},set(response.json.keys()))

        call_no = "XXXXXXXXXXX"
        uni = "KKKKKKKKK"
        response = self.app.get("/api/sections/{}/students/{}".format(call_no, uni))
        self.assertIn("No record found!",response.json)

if __name__ == '__main__':
    unittest.main()