import unittest
from src.application import app
import json


class TestComposite(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        print("SET UP Succeed!!")

    def testAddNewStudent(self):
        new_student = json.dumps(
            {
                "uni": "ab1234",
                "first_name": "David",
                "last_name": "Martin",
                "nationality": "United States",
                "race": "White",
                "gender": "Male",
                "admission_date": "12/14/2022",
                "call_no": 1,
                "project_id": "2"
            }
        )
        response = self.app.post("/api/students/add", content_type='application/json', data=new_student)
        self.assertEqual(200, response.status_code)

    def testDeleteStudent(self):
        #/api/students/delete/<call_no>/<uni>
        #1. delete an existing student
        call_no = "1"
        uni = "ab1234"
        url = "/api/students/delete/{}/{}".format(call_no,uni)
        response = self.app.delete(url)
        self.assertEqual(200,response.status_code)
        #2. delete a student not in the db
        call_no = "1"
        uni = "notindb"
        url = "/api/students/delete/{}/{}".format(call_no, uni)
        response = self.app.delete(url)
        self.assertEqual(400,response.status_code)
        #3. delete with the wrong call_no
        call_no = "XXX"
        uni = "ab1111"
        url = "/api/students/delete/{}/{}".format(call_no, uni)
        response = self.app.delete(url)
        self.assertEqual(400, response.status_code)

    def testUpdateStudent(self):
        student = json.dumps(
            {
                "first_name": "Daviiiid",
                "last_name": "Martin",
                "nationality": "United States",
                "race": "White",
                "gender": "Male",
                "admission_date": "12/14/2022",
                "call_no": 1,
                "project_id": null
            }
        )
        response = self.app.put("/api/students/add", content_type='application/json', data=student)
        self.assertEqual(200, response.status_code)

    def testGetStudentByUni(self):
        # 1. successfully get
        uni = "ab1234"
        response = self.app.get("/api/students/get/{}".format(uni))
        self.assertEqual(200, response.status_code)
        self.assertEqual(list, type(response.json))
        # 2. attributes
        if len(response.json) > 0:
            s = {"admission_date","email","race","gender","name","nationality","uni"}
            self.assertEqual(s,set(response.json[0].keys()))

    def testGetAllStudent(self):
        response = self.app.get("/api/students/all")
        self.assertEqual(200, response.status_code)
        self.assertEqual(list, type(response.json))

    def testAvailableStudentsInAProject(self):
        call_no = "1"
        project_id = "2"
        #/api/courses/<call_no>/projects/<project_id>/available_students
        response = self.app.get("/api/courses/{}/projects/{}/available_students".format(call_no,project_id))
        self.assertEqual(200, response.status_code)
        self.assertEqual(list, type(response.json))

    def testAddNewContact(self):
        #1. Successfully
        phone = json.dumps(
            {
                "description": "mobile",
                "country_code": "1",
                "phone_no": "3476290991"
            }
        )
        email = json.dumps(
            {
                "description": "personal",
                "address": "dw3013@columbia.edu"
            }
        )
        address = json.dumps(
            {
                "description": "home",
                "country": "USA",
                "state": "NY",
                "city": "NY",
                "zip_code": "10025",
                "street": "125W 109th St"
            }
        )
        uni = "ab1234"
        response_p = self.app.post("/api/contacts/{}/add/{}".format(uni,"phone"), content_type='application/json', data=phone)
        response_e = self.app.post("/api/contacts/{}/add/{}".format(uni,"email"),content_type='application/json', data=email)
        response_a = self.app.post("/api/contacts/{}/add/{}".format(uni,"address"), content_type='application/json', data=address)
        self.assertEqual(200, response_p.status_code)
        self.assertEqual(200, response_e.status_code)
        self.assertEqual(200, response_a.status_code)

        #2. non existing type
        response_nonexisting = self.app.post("/api/contacts/{}/add/{}".format(uni,"telephone"), content_type='application/json', data=phone)
        self.assertEqual(400, response_nonexisting.status_code)
        self.assertIn("Not existing type",response_nonexisting.json)
        #3. address verification failed
        fake_address = json.dumps(
            {
                "description": "home",
                "country": "USA",
                "state": "NY",
                "city": "NY",
                "zip_code": "10025",
                "street": "THIS IS A FAKE ADDRESS"
            }
        )
        response_fake = self.app.post("/api/contacts/{}/add/{}".format(uni, "address"), content_type='application/json', data=fake_address)
        self.assertEqual(400,response_fake.status_code)
        self.assertIn("address verification failed",response_fake.json)

    def testUpdateContact(self):
        # 1. Successfully
        phone = json.dumps(
            {
                "description": "mobile",
                "country_code": "1",
                "phone_no": "3476290991"
            }
        )
        email = json.dumps(
            {
                "description": "personal",
                "address": "dw3013@columbia.edu"
            }
        )
        address = json.dumps(
            {
                "description": "home",
                "country": "USA",
                "state": "NY",
                "city": "NY",
                "zip_code": "10025",
                "street": "125W 109th St"
            }
        )
        uni = "ab1234"
        response_p = self.app.put("/api/contacts/{}/update/{}".format(uni, "phone"), content_type='application/json',
                                   data=phone)
        response_e = self.app.put("/api/contacts/{}/update/{}".format(uni, "email"), content_type='application/json',
                                   data=email)
        response_a = self.app.put("/api/contacts/{}/update/{}".format(uni, "address"), content_type='application/json',
                                   data=address)
        self.assertEqual(200, response_p.status_code)
        self.assertEqual(200, response_e.status_code)
        self.assertEqual(200, response_a.status_code)

        # 2. non existing type
        response_nonexisting = self.app.put("/api/contacts/{}/update/{}".format(uni, "telephone"),
                                             content_type='application/json', data=phone)
        self.assertEqual(400, response_nonexisting.status_code)
        self.assertIn("Not existing type", response_nonexisting.json)
        # 3. address verification failed
        fake_address = json.dumps(
            {
                "description": "home",
                "country": "USA",
                "state": "NY",
                "city": "NY",
                "zip_code": "10025",
                "street": "THIS IS A FAKE ADDRESS"
            }
        )
        response_fake = self.app.put("/api/contacts/{}/add/{}".format(uni, "address"), content_type='application/json',
                                      data=fake_address)
        self.assertEqual(400, response_fake.status_code)
        self.assertIn("address verification failed", response_fake.json)

    def testDeleteContact(self):
        #1. Non-existing type
        uni = "ab1234"
        type = "INS"
        note = "mobile"
        response1 = self.app.delete("/api/contacts/{}/del/{}/{}".format(uni,type,note))
        self.assertEqual(400,response1.status_code)
        type = "phone"
        response2 = self.app.delete("/api/contacts/{}/del/{}/{}".format(uni, type, note))
        self.assertEqual(200, response2.status_code)

    def testGetContactByTypeAndUni(self):
        uni = "ab1234"
        type = "phone"

        response = self.app.get("/api/contacts/{}/{}".format(uni,type))
        self.assertEqual(200, response.status_code)
        self.assertEqual(list, type(response.json))
        if len(response.json) > 0:
            s = {"content","id","name","note","type","uni"}
            self.assertEqual(s,set(response.json[0].keys()))

    def testGetContactByType(self):
        #1. successfully
        type = "phone"
        response = self.app.get("/api/contacts/{}".format(type))
        self.assertEqual(200, response.status_code)
        self.assertEqual(list, type(response.json))
        #2. non-existing type
        type = "INS"
        response = self.app.get("/api/contacts/{}".format(type))
        self.assertEqual(400, response.status_code)
        self.assertIn("Not existing type", response.json)

    def testGetContactByUni(self):
        uni = "ab1234"
        response = self.app.get("/api/contacts/{}".format(uni))
        self.assertEqual(200, response.status_code)
        self.assertEqual(list, type(response.json))

    def testGetAllContact(self):
        response = self.app.get("/api/contacts/all")
        self.assertEqual(200, response.status_code)
        self.assertEqual(list, type(response.json))

    def testAddNewSection(self):
        section = json.dumps(
            {
                "call_no": 1,
                "professor": "Donald",
                "classroom": "Mudd 314",
                "year": 2022,
                "semester": "Spring",
                "day": "M",
                "start_hr": 9,
                "start_min": 30,
                "end_hr": 12,
                "end_min": 145,
                "section_type": "CVN"
            }
        )
        response = self.app.post("/api/courses/new_section", content_type='application/json',
                                      data=section)
        self.assertEqual(200, response.status_code)


    def testGetAllSection(self):
        response = self.app.get("/api/courses/all_sections")
        self.assertEqual(200, response.status_code)

    def testManipulateSection(self):
        call_no = "1"
        update_section = json.dumps(
            {
                "call_no": "number",
                "professor": "string",
                "classroom": "string",
                "year": "number",
                "semester": "string",
                "day": "string",
                "start_hr": "number",
                "start_min": "number",
                "end_hr": "number",
                "end_min": "number",
                "section_type": "string"
            }
        )
        url = "/api/courses/{}"
        response_update = self.app.put(url.format(call_no), content_type='application/json',data=update_section)
        self.assertEqual(200, response_update.status_code)

        response_delete = self.app.delete(url.format(call_no))
        self.assertEqual(200, response_delete.status_code)

    def testAddNewProject(self):
        call_no = "1"
        project = json.dumps(
            {
                "project_name": "happy",
                "team_name": "new",
                "project_members": ["A","B","C"]
            }
        )
        url = "/api/courses/{}/new_project"
        response = self.app.post(url.format(call_no), content_type='application/json', data=update_section)
        self.assertEqual(200, response.status_code)

    def testGetAllProjects(self):
        url = "/api/courses/all_projects"
        response = self.app.get(url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(list, type(response.json))
        if len(response.json) > 0:
            s = {"call_no","id","project_name","team_name","project_members","section_period"}
            self.assertEqual(s,set(response.json[0].keys()))


    def testManipulateProject(self):
        url = "/api/courses/{}/projects/{}"
        call_no = "1"
        project_id = "1"
        update_project = json.dumps(
        {
            "project_name": "string",
            "team_name": "string",
            "project_members": ["A","B","C"]
        }
        )
        response_update = self.app.put(url.format(call_no,project_id), content_type='application/json', data=update_project)
        self.assertEqual(200, response_update.status_code)

        response_delete = self.app.delete(url.format(call_no))
        self.assertEqual(200, response_delete.status_code)








