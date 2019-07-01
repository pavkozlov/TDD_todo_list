from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys
import time


class NewVisitorTest(unittest.TestCase):
    '''Тест нового посетителя'''

    def setUp(self):
        '''Установка'''
        self.browser = webdriver.Firefox()

    def tearDown(self):
        '''Демонтаж'''
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        '''тест: можно начать список и получить его позже'''
        # Пользователь 1 слышал про крутое новое онлайн-приложение со списком
        # неотложных дел. Он решает оценить его домашнюю страницу
        self.browser.get('http://127.0.0.1:8000/')

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
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1 : Купить павлиньи перья' for row in rows),
            "Новый элемент списка не появился в таблице"
        )

        # Текстовое поле по прежнему приглашает его добавить ещё один элемент.
        # Он вводит "Сделать мушку из павлиньих перьев"
        # (он очень методичен)

        # Страница снова обновляется, и теперь показывает оба элемента его списка

        # Пользователю интересно, запомнит ли сайт его список. Далее он видит, что
        # сайт сгенерировал для него уникальный URL - адрес - об этом
        # выводится небольшой текст с объяснениеми.

        # Он посещает этот URL - адрес - его список по прежнему там.

        # Удовлетворенный, он ложится спать.
        self.fail('Закончить тест!')


if __name__ == '__main__':
    unittest.main()
