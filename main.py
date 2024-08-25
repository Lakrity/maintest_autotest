import unittest
from zeep import Client
from zeep.transports import Transport
from requests.auth import HTTPBasicAuth
import requests

class TestSOAPService(unittest.TestCase):

    def setUp(self):
        self.wsdl = 'https://dev.maintest.ru/m-tests/api/1.11.2.0?wsdl'
        self.username = 'student-123'
        self.password = 'Test)123'
        
        # Настройка транспорта с авторизацией
        session = requests.Session()
        session.auth = HTTPBasicAuth(self.username, self.password)
        transport = Transport(session=session)
        
        # Инициализация клиента с транспортом
        self.client = Client(self.wsdl, transport=transport)

    def test_api_version(self):
        print ('=====================Тест №1=====================')
        # Создаем запрос
        response = self.client.service.getApiVersionNumber()

        # Выводим весь ответ для диагностики
        print("Полученный ответ:", response)

        # Извлекаем номер версии из ответа
        version_number = getattr(response, 'VersionNumber', None)

        # Ожидаемая версия
        expected_version = '1.11.0.1'

        # Проверяем, что полученная от бэка версия соответствует ожидаемой
        try:
            self.assertEqual(version_number, expected_version, f"Версия API не соответствует ожидаемой. Полученная версия: {version_number}")
        except AssertionError as e:
            print(f"Ошибка: {e}")
            raise

    def test_required_tests(self):
        print ('=====================Тест №2=====================')
        # Создаем запрос
        response = self.client.service.getTestsAttribsList()

        # Выводим весь ответ для диагностики
        print("Полученный ответ:", response)

        # Извлекаем список тестов
        tests = response['TestsAttribsList']['TestAttribs']

        # Нужные нам тесты по MainTestName
        required_tests = {"BackStaff2", "docAttention14", "11lf_blagonadezh"}

        # Проверяем, что как минимум 3 нужных теста присутствуют
        found_tests = set()
        for test in tests:
            if test['MaintestName'] in required_tests:
                found_tests.add(test['MaintestName'])

        # Проверяем, что найдено как минимум 3 нужных теста
        try:
            self.assertGreaterEqual(len(found_tests), 3, f"Найдено недостаточно нужных тестов. Найдено: {found_tests}")
        except AssertionError as e:
            print(f"Ошибка: {e}")
            raise

if __name__ == '__main__':
    unittest.main()
