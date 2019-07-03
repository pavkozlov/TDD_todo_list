from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import WebDriverException
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import os

MAX_WAIT = 10


class NewVisitorTest(StaticLiveServerTestCase):
    '''Тест нового посетителя'''

    def setUp(self):
        '''Установка'''
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://'+staging_server

    def tearDown(self):
        '''Демонтаж'''
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.1)

    def test_can_start_a_list_and_retrieve_it_later(self):
        '''тест: можно начать список и получить его позже'''
        # Пользователь 1 слышал про крутое новое онлайн-приложение со списком
        # неотложных дел. Он решает оценить его домашнюю страницу
        self.browser.get(self.live_server_url)

        # Он видит что заголовок и шапка страницы говорят о списках
        # неотложных дел
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Ему сразу же предлагается ввести элемент списка
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # Он набирает в текстовом поле "Купить павлиньи перья" (его хобби -
        # вязание рыболовных мушек)
        inputbox.send_keys("Купить павлиньи перья")

        # Когда он нажимает Enter, страница обновляется, и теперь страница
        # содержит "1 : Купить павлиньи перья" в качестве элемента списка
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить павлиньи перья')

        # Текстовое поле по прежнему приглашает его добавить ещё один элемент.
        # Он вводит "Сделать мушку из павлиньих перьев"
        # (он очень методичен)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys("Сделать мушку из павлиньих перьев")
        inputbox.send_keys(Keys.ENTER)

        # Страница снова обновляется, и теперь показывает оба элемента его списка
        self.wait_for_row_in_list_table('1: Купить павлиньи перья')
        self.wait_for_row_in_list_table('2: Сделать мушку из павлиньих перьев')

        # Пользователю интересно, запомнит ли сайт его список. Далее он видит, что
        # сайт сгенерировал для него уникальный URL - адрес - об этом
        # выводится небольшой текст с объяснениеми.

        # Он посещает этот URL - адрес - его список по прежнему там.

        # Удовлетворенный, он ложится спать.

    def test_multiple_users_can_start_lists_at_different_urls(self):
        '''тест: многочисленные пользователи могут начать списки по разным url'''
        # Пользователь 1 начинает новый список
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys("Купить павлиньи перья")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить павлиньи перья')

        # Он замечает что список имеет уникальный URL - адрес
        user1_list_url = self.browser.current_url
        self.assertRegex(user1_list_url, '/lists/.+')

        # Теперь пользователь 2 приходит на сайт
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Пользователь 2 посещает домашнюю страницу, нет никаких признаков списка пользователя 1
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn("Купить павлиньи перья", page_text)
        self.assertNotIn("Сделать мушку из павлиньих перьев", page_text)

        # Пользователь 2 начинает свой список дел, вводя новый элемент
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys("Купить молоко")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить молоко')

        # Пользователь 2 получает уникальный URL - адрес
        user2_list_url = self.browser.current_url
        self.assertRegex(user2_list_url, '/lists/.+')
        self.assertNotEqual(user1_list_url, user2_list_url)

        # Нет ни следа от пользователя 1
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Купить павлиньи перья', page_text)
        self.assertIn('Купить молоко', page_text)

    def test_layout_and_styling(self):
        '''тест макета и стилевого оформления'''
        # Пользователь 1 открыает домашнюю страницу
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # Он замечает что поле воода аккуратно центрировано
        inpuntbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inpuntbox.location['x'] + inpuntbox.size['width'] / 2,
            512,
            delta=10
        )

        # Он начинает новый список и видит, что поле ввода там тоже
        # аккуратно центрировано
        inpuntbox.send_keys('testing')
        inpuntbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inpuntbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inpuntbox.location['x'] + inpuntbox.size['width'] / 2,
            512,
            delta=10
        )
        self.fail('Закончить тест!')


if __name__ == '__main__':
    unittest.main()
