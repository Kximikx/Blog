from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.service import Service

service = Service(r'C:\Users\Yura\Desktop\Brazzers\3 Курс\2СЕм\Фрейм\chrome-win64\chromedriver.exe')

class BlogE2ETest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        # Викликаємо метод батьківського класу для налаштування
        super().setUpClass()
        # Використовуємо Chrome WebDriver
        cls.driver = webdriver.Chrome(service=service)
        # Встановлюємо максимальний час очікування для елементів
        cls.driver.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        # Закриваємо браузер після завершення тестів
        cls.driver.quit()
        super().tearDownClass()

    def test_home_page_title(self):
        # Відкриваємо домашню сторінку
        self.driver.get(self.live_server_url)
        # Перевіряємо, що заголовок сторінки містить "Блог"
        self.assertIn("блог", self.driver.title.lower())
