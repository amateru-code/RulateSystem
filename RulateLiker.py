import os
import pickle
import time
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver

import rulate_config


class RulateLiker:
    def __init__(self, login, password, book, webdriver_url, headless=True, actions={}):
        # Sets account data and book's url
        self.__login = login
        self.__password = password
        self.__book = book
        self._webdriver = webdriver_url

        self.__liked_chapters = 0
        # Boot up the webdriver and gets to the book
        try:
            # Cookies loading
            self.get_cookies()

            # Driver boot up
            self.options = webdriver.ChromeOptions()
            self.options.add_argument(
                "user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
            self.options.add_argument("--disable-blink-features=AutomationControlled")
            if headless is True:
                self.options.headless = True
            self._driver = webdriver.Chrome(executable_path=f"{self._webdriver}", options=self.options)
            self._driver.get(self.__book)

            # Load the cookies
            self.load_cookies()
            self._driver.refresh()
            time.sleep(2)
        except Exception as ex:
            print(ex)
            self.close_driver()

        self.manage_routine(like=actions.get('like'),
                            thx=actions.get('thx'),
                            thx_amount=actions.get('thx_amount'),
                            stars=actions.get('stars'),
                            stars_value=actions.get('stars_value'))

    def manage_routine(self, like=True, thx=True, thx_amount=999999, stars=False, stars_value=5):
        self.age_submit()  # Age submission
        if stars:
            self.put_stars(value=stars_value)
        if like:
            self.like_book()  # Likes the page
        if thx:
            self.thx_chapters(amount=thx_amount)

    def put_stars(self, value):
        stars = list(self._driver.find_elements(By.CLASS_NAME, 'star'))
        if value == 1:
            try:
                stars[0].click()
                stars[5].click()
                stars[10].click()
            except Exception:
                pass
        elif value == 2:
            try:
                stars[1].click()
                stars[6].click()
                stars[11].click()
            except Exception:
                pass
        elif value == 3:
            try:
                stars[2].click()
                stars[7].click()
                stars[12].click()
            except Exception:
                pass
        elif value == 4:
            try:
                stars[3].click()
                stars[8].click()
                stars[13].click()
            except Exception:
                pass
        elif value == 5:
            try:
                stars[4].click()
                stars[9].click()
                stars[14].click()
            except Exception:
                pass
        print('Stars - Done!')

    def like_chapters(self, amount=999999):
        try:
            while self.__liked_chapters <= amount:
                if self.is_class_exists('like_btn'):
                    self._driver.find_element(By.CLASS_NAME, 'like_btn').click()
                    self.__liked_chapters += 1
                    print(f'liked: {self.__liked_chapters}')
                self._driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + Keys.ARROW_RIGHT)
                if self.is_id_exists('subscription'):
                    raise Exception
        except Exception as e:
            print("All accessible chapters were liked")

    def thx_chapters(self, amount=0):
        self.get_first_chapter()  # Goes to the first accessed chapter
        self.old_reader()  # Old reader on
        print("Starting liking chapters...")
        self.like_chapters()  # Like all chapters

    def old_reader(self):
        self._driver.find_element(By.CLASS_NAME, 'icon-cog').click()
        self._driver.find_element(By.CLASS_NAME, 'btn-primary').click()

    def is_logged_in(self):
        """Checks if you are logged in"""
        if not self._driver.find_element(By.NAME, 'login[login]'):
            return True
        else:
            return False

    def is_class_exists(self, class_name):
        try:
            self._driver.find_element(By.CLASS_NAME, f'{class_name}')
            exist = True
        except Exception:
            exist = False
        return exist

    def is_xpath_exists(self, xpath):
        try:
            self._driver.find_element(By.XPATH, f'{xpath}')
            exist = True
        except Exception:
            exist = False
        return exist

    def is_id_exists(self, id):
        try:
            self._driver.find_element(By.ID, f'{id}')
            exist = True
        except Exception:
            exist = False
        return exist

    def close_driver(self):
        self._driver.close()
        self._driver.quit()

    def load_cookies(self):
        for cookie in pickle.load(open(f'D:\\rulate\\cookies\\{self.__login}_cookies', "rb")):
            self._driver.add_cookie(cookie)

    def get_cookies(self):
        """Gets cookies"""
        # Checks if cookies exist
        if os.path.exists(f'D:\\rulate\\cookies\\{self.__login}_cookies'):
            print('Cookies exists')
        else:
            # Loging in
            self.options = webdriver.ChromeOptions()
            self.options.add_argument("--disable-blink-features=AutomationControlled")
            self._driver = webdriver.Chrome(executable_path=f"{self._webdriver}", options=self.options)
            self._driver.get(self.__book)

            if self._driver.find_element(By.NAME, 'login[login]'):
                self._driver.find_element(By.NAME, 'login[login]').send_keys(self.__login)
                self._driver.find_element(By.NAME, 'login[pass]').send_keys(self.__password, Keys.ENTER)
                time.sleep(2)
                # Gets cookies
                pickle.dump(
                    self._driver.get_cookies(),
                    open(f'D:\\rulate\\cookies\\{self.__login}_cookies', 'wb')
                )
                self.close_driver()

    def get_first_chapter(self):
        try:
            self.read_btn = self._driver.find_element(By.XPATH, '//a[@title="Получить готовый перевод."]')
            self.read_btn.click()
        except Exception as ex:
            print(ex)
            self.close_driver()

    def like_book(self):
        try:
            like_btn = self._driver.find_element(By.XPATH, '//*[@id="liker"]/a[1]')
            if "disabled" in like_btn.get_attribute("class").split():
                print('Already liked the page')
            else:
                self._driver.find_element(By.CLASS_NAME, 'like-btn').click()
        except Exception:
            print("Can't like the book...Skipping...")

    def age_submit(self):
        try:
            if self._driver.find_element(By.NAME, 'ok'):
                self._driver.find_element(By.NAME, 'ok').click()
        except Exception:
            print('No age permission found')
