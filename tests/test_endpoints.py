import unittest
from main import app


class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_main_page_loads(self):
        """Главная страница загружается корректно"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>', response.data)

    def test_get_weather_with_valid_city(self):
        """ '/get_weather' корректно обрабатывает верный город"""
        response = self.client.post('/get_weather', data={'city': 'Москва'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Москва', response.data.decode('utf-8'))

    def test_get_weather_with_invalid_city(self):
        """ '/get_weather' корректно обрабатывает неверный город"""
        response = self.client.post('/get_weather', data={'city': ''}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('ошибка', response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()