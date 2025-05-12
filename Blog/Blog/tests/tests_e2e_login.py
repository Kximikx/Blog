from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User
import time

class E2ELoginTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()  
        self.browser.implicitly_wait(5)  

        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def tearDown(self):
        self.browser.quit()  

    def test_login_and_view_posts(self):
        self.browser.get(self.live_server_url)

        login_button = self.browser.find_element(By.LINK_TEXT, "Увійти")
        login_button.click()

        username_input = self.browser.find_element(By.NAME, "username")
        password_input = self.browser.find_element(By.NAME, "password")
        username_input.send_keys("testuser")
        password_input.send_keys("testpassword")
        password_input.send_keys(Keys.ENTER)

        time.sleep(2)  

        self.assertIn("Cloud Technologies & DevOps", self.browser.page_source)

        my_posts_button = self.browser.find_element(By.LINK_TEXT, "Мої дописи")
        my_posts_button.click()

        self.assertIn("Мої дописи", self.browser.page_source)
