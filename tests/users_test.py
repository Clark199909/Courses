import unittest
from src.application import app
import json

#NOT CONFIGURED



class TestUsers(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        print("SET UP Succeed!!")


    def testUserRegister(self):
        #1. Successfully register
        new_user = json.dumps({
            'username':'HelloWorld',
            'email': 'HelloWorld@gmail.com',
            'phone':'998-981-9898'
        })
        response = self.app.post("/api/users/register",content_type='application/json',data=new_user)
        self.assertIn("Success",response.json)
        self.assertEqual(200,response.status_code)
        #2. user name
        new_user = json.dumps({
            'username':'HelloWorld',
            'email': 'xxx@163.com',
            'phone':'000-000-0000'
        })
        response = self.app.post("/api/users/register",content_type='application/json',data=new_user)
        self.assertIn("User name already exists!",response.json)
        self.assertEqual(400,response.status_code)
        #3. email
        new_user = json.dumps({
            'username':'Hello',
            'email': 'HelloWorld@gmail.com',
            'phone':'000-000-0000'
        })
        response = self.app.post("/api/users/register",content_type='application/json',data=new_user)
        self.assertIn("Email already exists",response.json)
        self.assertEqual(400,response.status_code)

        #4. Phone
        new_user = json.dumps({
            'username':'Hello',
            'email': 'xxx@163.com',
            'phone':'998-981-9898'
        })
        response = self.app.post("/api/users/register",content_type='application/json',data=new_user)
        self.assertIn("Phone already exists",response.json)
        self.assertEqual(400,response.status_code)

    ###WHY WE USE POST METHOD HERE FOR LOGIN

    def testUserLogin(self):
        user = json.dumps({
            'email': 'HelloWorld@gmail.com',
            'password': '123456'
        })
        response = self.app.post("/api/users/login", content_type='application/json',data=user)
        self.assertEqual(200,response.status_code)
        self.assertIn("Success",response.json)

        user = json.dumps({
            'email': 'HelloWorld@gmail.com',
            'password': '11111111'
        })
        response = self.app.post("/api/users/login", content_type='application/json', data=user)
        self.assertEqual(400, response.status_code)
        self.assertIn("Password is incorrect", response.json)

        user = json.dumps({
            'email': 'Hello@gmail.com',
            'password': '123456'
        })
        response = self.app.post("/api/users/login", content_type='application/json', data=user)
        self.assertEqual(400, response.status_code)
        self.assertIn("User does not exist", response.json)


if __name__ == '__main__':
    unittest.main()

