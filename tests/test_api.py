import unittest
import json
import re
from base64 import b64encode
from app import create_app, db
from app.models import User, Role, Post, Comment
from flask import url_for


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_api_headers(self, username, password):
        return {
            'Authorization': 'Basic ' + b64encode(
                (username +':'+ password).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_no_auth(self):
        response = self.client.get(url_for('api_1_0.get_posts'), 
                                   content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_posts(self):

        # Добавить пользователя
        r = Role.query.filter_by(name='User').first()
        self.assertIsNotNone(r)
        u = User(email='john@example.com', password='cat', 
                 confirmed=True, role=r)
        db.session.add(u)
        db.session.commit()

        # Записать сообщение
        response = self.client.post(
            url_for('api_1_0.new_post'),
            headers=self.get_api_headers('john@example.com', 'cat'),
            data=json.dumps({'body': 'body of the *blog* post'}))
        self.assertEqual(response.status_code, 201)
        url = response.headers.get('Location')
        self.assertIsNotNone(url)

        # Получить новое сообщение обратно
        response = self.client.get(
            url,
            headers=self.get_api_headers('john@example.com', 'cat'))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['url'], 'http://localhost' + url)
        self.assertEqual(json_response['body'], 'body of the *blog* post')
        self.assertEqual(json_response['body_html'], 
                        '<p>body of the <em>blog</em> post</p>')