import re
import threading
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from app import create_app, db
from app.models import Role, User, Post


class SeleniumTestCase(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls):
        # Запусить веб-браузер Firefox
        try:
            cls.client = webdriver.Firefox()
        except:
            pass
        # Пропустить следующие тесты, если браузер не был запущен
        if cls.client:
            # Создать приложение
            cls.app = create_app('testing')
            cls.app_context = cls.app.app_context()
            cls.app_context.push()

            # Подавить вывод отладочных сообщений, чтобы очистить
            # вывод от лишнего мусора
            import logging
            logger = logging.getLogger('werkzeug')
            logger.setLevel("ERROR")

            # Создать базу данных и наполнить её фиктивными данными
            db.create_all()
            Role.insert_roles()
            User.generate_fake(10)
            Post.generate_fake(10)

            # Добавить учётную запись администратора
            admin_role = Role.query.filter_by(permissions=0xff).first()
            admin = User(email='john@example.com',
                         username='john', password='cat',
                         role=admin_role, confirmed=True)
            db.session.add(admin)
            db.session.commit()

            # Запустить сервер Flask в отдельном потоке
            threading.Thread(target=cls.app.run).start()

    @classmethod
    def tearDownClass(cls):
        if cls.client:
            # Останвоить сервер Flask и закрыть браузер
            cls.client.get('http://localhost:5000/shutdown')
            cls.client.close()

            # Уничтожить базу данных
            db.drop_all()
            db.session.remove()

            # Удаление контекста приложения
            cls.app_context.pop()

    def setUp(self):
        if not self.client:
            self.skipTest('Web browser not available')

    def tearDown(self):
        pass

    def test_admin_home_page(self):
        # Переход на главную страницу
        self.client.get('http://localhost:5000/')
        self.assertTrue(re.search('Hello,\s+Stranger!',
                                  self.client.page_source))

        # Перейти на страницу аутентификации
        self.client.find_element(By.LINK_TEXT, 'Log In').click()
        self.assertTrue('<h1>Login</h1>' in self.client.page_source)

        # Выполнить аутентификацию
        self.client.find_element(By.NAME, 'email').\
            send_keys('john@example.com')
        self.client.find_element(By.NAME, 'password').send_keys('cat')
        self.client.find_element(By.NAME, 'submit').click()
        self.assertTrue(re.search('Hello,\s+john!', self.client.page_source))

        # Переход на страницу профиля пользователя
        self.client.find_element(By.LINK_TEXT, 'Profile').click()
        self.assertTrue(re.search('john', self.client.page_source))

        # Переход на домашнюю страницу
        self.client.find_element(By.LINK_TEXT, 'Home').click()
        self.assertTrue(re.search('mind', self.client.page_source))