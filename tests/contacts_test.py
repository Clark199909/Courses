import unittest
from src.application import app
import json


class TestContacts(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        print("SET UP Succeed!!")


    def testAddStudent(self):
        #1. successfully added
        student = json.dumps( { "uni": "dw3013" })
        response = self.app.post("/api/contacts/new_student", content_type='application/json', data=student)
        self.assertEqual(200,response.status_code)
        self.assertIn("Success", response.json)
        #2. fail because already existed
        response = self.app.post("/api/contacts/new_student", content_type='application/json', data=student)
        self.assertEqual(400,response.status_code)
        self.assertIn("Student already exists", response.json)

    def testDeleteStudent(self):
        # 1. no such student
        student = json.dumps({"uni": "xxxxx"})
        response = self.app.post("/api/contacts/del_student", content_type='application/json', data=student)
        self.assertEqual(400, response.status_code)
        self.assertIn("Student does not exist", response.json)
        #2. successfully
        student = json.dumps({"uni": "dw3013"})
        response = self.app.post("/api/contacts/del_student", content_type='application/json', data=student)
        self.assertEqual(200, response.status_code)
        self.assertIn("Success", response.json)

    def testAddAddress(self):
        address = json.dumps({
            "description": "home",
            "country": "USA",
            "state": "NY",
            "city": "NY",
            "zip_code": "10025",
            "street": "125W 109th St"
        })
        #1. student does not exist
        uni = "kkkkk"
        response = self.app.post("/api/contacts/{}/new_address".format(uni), content_type='application/json', data=address)
        self.assertEqual(400, response.status_code)
        self.assertIn("Student does not exist", response.json)
        #2. successfully added
        uni = "dw3013"
        response = self.app.post("/api/contacts/{}/new_address".format(uni), content_type='application/json', data=address)
        self.assertEqual(200, response.status_code)
        self.assertIn("Success", response.json)
        #3. This address type already exists for this student
        response = self.app.post("/api/contacts/{}/new_address".format(uni), content_type='application/json', data=address)
        self.assertEqual(400, response.status_code)
        self.assertIn("This address type already exists for this student", response.json)

    def testDeleteAddress(self):
        #1. student does not exist
        uni = "kkkkk"
        response = self.app.post("/api/contacts/{}/del_address".format(uni), content_type='application/json',
                                 data=address)
        self.assertEqual(400, response.status_code)
        self.assertIn("Student does not exist",response.json)

        #2. no such address
        uni = "dw3013"
        address = json.dumps({
            "description": "KKKKK"
        })
        response = self.app.post("/api/contacts/{}/del_address".format(uni), content_type='application/json',
                                 data=address)
        self.assertEqual(400, response.status_code)
        self.assertIn("This address does not exist for this student", response.json)

        # 3. success
        address = json.dumps({
            "description": "home"
        })
        response = self.app.post("/api/contacts/{}/del_address".format(uni), content_type='application/json',
                                 data=address)
        self.assertEqual(200, response.status_code)
        self.assertIn("Success", response.json)

    def testUpdateAddress(self):
        address = json.dumps({
            "description": "home",
            "country": "USA",
            "state": "NY",
            "city": "NY",
            "zip_code": "10026",
            "street": "125W 109th St"
        })
        #1. no such student
        uni = "kkkkkk"

        response = self.app.post("/api/contacts/{}/update_address".format(uni), content_type='application/json',
                                 data=address)
        self.assertEqual(400, response.status_code)
        self.assertIn("Student does not exist",response.json)
        #2. no such address
        uni = "dw3013"
        address = json.dumps({
            "description": "XXXXXXXX",
            "country": "USA",
            "state": "NY",
            "city": "NY",
            "zip_code": "10026",
            "street": "125W 109th St"
        })
        response = self.app.post("/api/contacts/{}/update_address".format(uni), content_type='application/json',
                                 data=address)
        self.assertEqual(400, response.status_code)
        self.assertIn("This address does not exist for this student", response.json)
        #3. success
        address = json.dumps({
            "description": "home",
            "country": "USA",
            "state": "NY",
            "city": "NY",
            "zip_code": "10026",
            "street": "125W 109th St"
        })
        uni = "dw3013"
        response = self.app.post("/api/contacts/{}/update_address".format(uni), content_type='application/json',
                                 data=address)
        self.assertEqual(200, response.status_code)
        self.assertIn("Success", response.json)


    def testAddPhone(self):
        phone = json.dumps({
            "description": "mobile",
            "country_code": "1",
            "phone_no": "3476290991"
        })
        #1. no such student
        uni = "kkkkk"
        response = self.app.post("/api/contacts/{}/new_phone".format(uni), content_type='application/json',
                                 data=phone)
        self.assertEqual(400, response.status_code)
        self.assertIn("Student does not exist", response.json)

        #2. type already exist
        phone = json.dumps({
            "description": "home",
            "country_code": "1",
            "phone_no": "3476290991"
        })
        uni = "dw3013"
        response = self.app.post("/api/contacts/{}/new_phone".format(uni), content_type='application/json',
                                 data=phone)
        self.assertEqual(400, response.status_code)
        self.assertIn("This phone type already exists for this student", response.json)

        #3. success
        phone = json.dumps({
            "description": "mobile",
            "country_code": "1",
            "phone_no": "3476290991"
        })
        response = self.app.post("/api/contacts/{}/new_phone".format(uni), content_type='application/json',
                                 data=phone)
        self.assertEqual(200, response.status_code)
        self.assertIn("Success", response.json)

    def testDeletePhone(self):
        phone = json.dumps({
            "description": "mobile"
        })
        # 1. no such student
        uni = "kkkkk"
        response = self.app.post("/api/contacts/{}/del_phone".format(uni), content_type='application/json',
                                 data=phone)
        self.assertEqual(400, response.status_code)
        self.assertIn("Student does not exist", response.json)
        # 2. no such phone
        phone = json.dumps({
            "description": "XXXXX"
        })
        uni = "dw3013"
        response = self.app.post("/api/contacts/{}/del_phone".format(uni), content_type='application/json',
                                 data=phone)
        self.assertEqual(400, response.status_code)
        self.assertIn("This phone does not exist for this student", response.json)

        #3. success
        phone = json.dumps({
            "description": "mobile"
        })
        response = self.app.post("/api/contacts/{}/del_phone".format(uni), content_type='application/json',
                                 data=phone)
        self.assertEqual(200, response.status_code)
        self.assertIn("Success", response.json)

    def testUpdatePhone(self):
        phone = json.dumps({
            "description": "mobile",
            "country_code": "1",
            "phone_no": "1234567890"
        })
        # 1. no such student
        uni = "kkkkk"
        response = self.app.post("/api/contacts/{}/update_phone".format(uni), content_type='application/json',
                                 data=phone)
        self.assertEqual(400, response.status_code)
        self.assertIn("Student does not exist", response.json)
        # 2. no such phone
        phone = json.dumps({
            "description": "XXXX",
            "country_code": "1",
            "phone_no": "1234567890"
        })
        uni = "dw3013"
        response = self.app.post("/api/contacts/{}/update_phone".format(uni), content_type='application/json',
                                 data=phone)
        self.assertEqual(400, response.status_code)
        self.assertIn("This phone does not exist for this student", response.json)

        #3. success
        phone = json.dumps({
            "description": "mobile",
            "country_code": "1",
            "phone_no": "1234567890"
        })
        response = self.app.post("/api/contacts/{}/update_phone".format(uni), content_type='application/json',
                                 data=phone)
        self.assertEqual(200, response.status_code)
        self.assertIn("Success", response.json)


    def testAddEmail(self):
        email = json.dumps({
            "description": "mobile",
            "country_code": "1",
            "phone_no": "3476290991"
        })
        #1. no such student
        uni = "kkkkk"
        response = self.app.post("/api/contacts/{}/new_email".format(uni), content_type='application/json',
                                 data=email)
        self.assertEqual(400, response.status_code)
        self.assertIn("Student does not exist", response.json)

        #2. type already exist
        email = json.dumps({
            "description": "home",
            "country_code": "1",
            "phone_no": "3476290991"
        })
        uni = "dw3013"
        response = self.app.post("/api/contacts/{}/new_email".format(uni), content_type='application/json',
                                 data=email)
        self.assertEqual(400, response.status_code)
        self.assertIn("already exists for this student", response.json)

        #3. success
        email = json.dumps({
            "description": "mobile",
            "country_code": "1",
            "phone_no": "3476290991"
        })
        response = self.app.post("/api/contacts/{}/new_email".format(uni), content_type='application/json',
                                 data=email)
        self.assertEqual(200, response.status_code)
        self.assertIn("Success", response.json)

    def testDeleteEmail(self):
        email = json.dumps({
        "description": "personal"
        })
        # 1. no such student
        uni = "kkkkk"
        response = self.app.post("//api/contacts/{}/del_email".format(uni), content_type='application/json',
                                 data=email)
        self.assertEqual(400, response.status_code)
        self.assertIn("Student does not exist", response.json)
        # 2. no such email
        email= json.dumps({
            "description": "XXXXX"
        })
        uni = "dw3013"
        response = self.app.post("//api/contacts/{}/del_email".format(uni), content_type='application/json',
                                 data=email)
        self.assertEqual(400, response.status_code)
        self.assertIn("This email does not exist for this student", response.json)

        #3. success
        email = json.dumps({
            "description": "personal"
        })
        response = self.app.post("//api/contacts/{}/del_email".format(uni), content_type='application/json',
                                 data=email)
        self.assertEqual(200, response.status_code)
        self.assertIn("Success", response.json)

    def testUpdateEmail(self):
        email = json.dumps({
            "description": "personal",
            "address": "12345678@columbia.edu"
        })
        # 1. no such student
        uni = "kkkkk"
        response = self.app.post("/api/contacts/{}}update_email".format(uni), content_type='application/json',
                                 data=email)
        self.assertEqual(400, response.status_code)
        self.assertIn("Student does not exist", response.json)
        # 2. no such email
        email = json.dumps({
        "description": "XXXXXX",
        "address": "12345678@columbia.edu"
    })
        uni = "dw3013"
        response = self.app.post("/api/contacts/{}/update_email".format(uni), content_type='application/json',
                                 data=email)
        self.assertEqual(400, response.status_code)
        self.assertIn("This email does not exist for this student", response.json)

        #3. success
        email = json.dumps({
            "description": "personal",
            "address": "12345678@columbia.edu"
        })
        response = self.app.post("/api/contacts/{}/update_email".format(uni), content_type='application/json',
                                 data=email)
        self.assertEqual(200, response.status_code)
        self.assertIn("Success", response.json)

    def testGetAllAddressesofAStudent(self):
        uni = "dw3013"
        response = self.app.get("/api/contacts/{}/all_addresses".format(uni))
        self.assertEqual(200,response.status_code)
        self.assertEqual(list,type(response.json))
        for add in response.json:
            self.assertEqual(dict,type(add))

    def testGetAllPhonesofAStudent(self):
        uni = "dw3013"

        response = self.app.get("/api/contacts/{}/all_phones".format(uni))
        self.assertEqual(200,response.status_code)
        self.assertEqual(list,type(response.json))
        for phone in response.json:
            self.assertEqual(dict,type(phone))

    def testGetAllEmailsofAStudent(self):
        uni = "dw3013"
        response = self.app.get("/api/contacts/{}/all_emails".format(uni))
        self.assertEqual(200, response.status_code)
        self.assertEqual(list, type(response.json))
        for email in response.json:
            self.assertEqual(dict, type(email))

    def testGetAllContactsofAStudent(self):
        uni = "dw3013"
        response = self.app.get("/api/contacts/{}/all_contacts".format(uni))
        self.assertEqual(200, response.status_code)
        self.assertEqual(list, type(response.json))
        for contact in response.json:
            self.assertEqual(list, type(contact))

    def testGetAllAddresses(self):
        response = self.app.get("/api/contacts/all_addresses")
        self.assertEqual(200, response.status_code)
        self.assertEqual(list, type(response.json))
        for add in response.json:
            self.assertEqual(dict, type(add))

    def testGetAllPhones(self):
        response = self.app.get("/api/contacts/all_phones")
        self.assertEqual(200, response.status_code)
        self.assertEqual(list, type(response.json))
        for phone in response.json:
            self.assertEqual(dict, type(phone))

    def testGetAllEmails(self):
        response = self.app.get("/api/contacts/all_emails")
        self.assertEqual(200, response.status_code)
        self.assertEqual(list, type(response.json))
        for e in response.json:
            self.assertEqual(dict, type(e))

    def testGetAllContacts(self):
        response = self.app.get("/api/contacts/all_contacts")
        self.assertEqual(200, response.status_code)
        self.assertEqual(list, type(response.json))
        for c in response.json:
            self.assertEqual(list, type(c))


if __name__ == '__main__':
    unittest.main()














