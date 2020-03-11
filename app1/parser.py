from selenium.webdriver.common.by import By
import datetime
from datetime import datetime
from app1.models import Tickers, Insiders
from selenium import webdriver


def get_date(str_object):
    """Назначение функции: преобразует данные из спарсенного объекта в объект datetime.
     На входе получает спарсенный объект с данными. Преобразует в строку.
     Разбивает строку по пробелу на список элементов. Выбирает элемент с датой.
     Преобразует дату из строки в обьект datetime. Возвращает объект datetime """
    date = str_object.text
    date = date.split()
    date = date[0]
    date_time_object = datetime.strptime(date, '%m/%d/%Y')
    return date_time_object


def save_row(str_object, date, stock_name):
    """Назначение функции: преобразовать спарсенные данные о ценах на акцию в текст и
    сохранить данные о ценах в соответствующих ячейках в базе данных.
    На входе функция получает спарсенный объект с данными, дату и название акции.
    спарсенный объект с данными преобразует в строку. Разбивает строку по пробелу на список элементов
    Сохраняет данные о ценах в соответствующих ячейках таблицы Tickers в базе данных"""
    data = str_object.text
    data = data.split()
    new_data = Tickers(stock_name=stock_name, date=date, close=data[1], volume=data[2],
                       open=data[3], high=data[4], low=data[5])
    new_data.save()


def save_insider_info(row, stock_name):
    """Назначение функции: сохранить спарсенные данные о владельце компании в соответствующих
       ячейках в базе данных. На входе функция спарсенные данные о владельце компании и название
       акции. Далее сохраняет данные в соответствующих ячейках таблицы Insiders в базе данных"""
    last_date = datetime.strptime(row[2], '%m/%d/%Y')
    new_data = Insiders(stock_name=stock_name, insider=row[0], relation=row[1],
                        last_date=last_date, transaction_type=row[3], owner_type=row[4],
                        shares_traded=row[5], last_price=row[6], shares_held=row[7])
    new_data.save()


def parse_stock_info(stock_name):
    """Назначение функции: cпарсить информацию об акциях за 3 месяца и сохранить ее в базе данных.
       На входе функция получает название акции. Далее при помощи эмулятора браузера
       пытается зайти по ссылке на страницу с ценами на акции и получить данные со страница.
       В случае неудачи функция завершает работу, возвращает None и закрывает браузер. В случае
       успеха собирает данные с сайта и сохраняет их в базе пока не будет превышен пероид в 3 месяца
       от текущей даты. Перед завершением закрывает браузер."""
    driver = webdriver.Chrome("/Users/pk/PycharmProjects/Tickers/app1/chromedriver")
    stock_activity_url = f'https://www.nasdaq.com/market-activity/stocks/{stock_name}/historical'
    try:
        driver.get(stock_activity_url)  # пытаемся перейти по ссылке
        btn_elem = driver.find_element_by_css_selector(
            """body > div.dialog-off-canvas-main-canvas > div > main > div >
               div.quote-subdetail__content > div:nth-child(2) >
               div > div.quote-subdetail__indented-components >
               div > div.historical-data > div.historical-data__controls > 
               div > div > div > button:nth-child(2)""")  # пытаемся получить ссылка на кнопку, которая переводит на список
        # с данными на акцию за пол-года
        btn_elem.click()  # пытаемся нажать на кнопку по полученной ссылке
        elements = driver.find_elements_by_class_name("historical-data__row")  # пытаемся получить элементы со страницы
    except Exception as e:
        driver.close()
        return
    last_date = get_date(elements[1])  # получаем самую позднюю дату изменения цен на акцию
    flag = True
    page_number = 1
    while flag:
        amount_of_objects = len(elements)  # вычисляем количество строк с ценами на акцию на странице
        for i in range(1,
                       amount_of_objects):  # идем по списку начиная с 1й (нулевая строка - это названия колонок в таблице)
            current_date = get_date(elements[i])  # получаем текущую дату
            save_row(elements[i], current_date, stock_name)  # сохраняем данные из строки в базе
            delta = last_date - current_date  # получаем разницу в датах
            if delta.days > 91:  # если разница в датах превышает 3 месяца - завершаем сбор данных
                flag = False
                break
        if not flag:
            break
        page_number += 1
        try:
            button_url = f"/html/body/div[4]/div/main/div/div[4]/div[2]/div/div[1]/div/div[1]/div[5]/div/button[{page_number}]"
            next_page_btn = driver.find_element(By.XPATH, button_url)
            next_page_btn.click()
            elements = driver.find_elements_by_class_name(
                "historical-data__row")  # пытаемся получить элементы со страницы
        except Exception as e:
            driver.close()
            return
    driver.close()


def pars_insider_info(stock_name):
    """Назначение функции:  спарсить информацию о торговле совладельцев компании, выпустившей акцию
    и сохранить ее в базе данных. На входе функция получает название акции. Далее при помощи эмулятора
    браузера пытается зайти по ссылке на страницу с данными о торговле и получить данные со страницы.
    В случае неудачи функция завершает работу, возвращает None и закрывает браузер. В случае
    успеха собирает данные с первых 10 страниц. Если страниц меньше 10 - то со всех что есть.
    Перед завершением закрывает эмулятор браузера."""

    driver = webdriver.Chrome("/Users/pk/PycharmProjects/Tickers/app1/chromedriver")
    insider_activity_url = f'https://www.nasdaq.com/market-activity/stocks/{stock_name}/insider-activity'
    try:
        driver.get(insider_activity_url)  # # пытаемся перейти по ссылке
        elements = driver.find_elements_by_class_name(
            "insider-activity__cell")  # пытаемся получить элементы со страницы
    except Exception as e:
        driver.close()
        return
    counter = 0
    page_number = 1
    for i in range(10):
        amount_of_items = len(elements)
        insider_info = []
        for j in range(21, amount_of_items):
            insider_info.append(elements[j].text)
            counter += 1
            if counter == 8:
                save_insider_info(insider_info, stock_name)
                insider_info = []
                counter = 0
        page_number += 1
        button_url = f"/html/body/div[4]/div/main/div/div[4]/div[2]/div/div[1]/div/div[1]/div[3]/div[3]/div/button[{page_number}]"
        try:
            next_page_btn = driver.find_element(By.XPATH, button_url)
            next_page_btn.click()  # пытаемся нажать на кнопку для перехода на следующую страницу
            elements = driver.find_elements_by_class_name(
                "insider-activity__cell")  # пытаемся получить элементы со страницы
        except Exception as e:
            driver.close()
            return
    driver.close()


def parse():
    """ Функция парсит данные по акциями, названия которых указаны в файле. Сначала
    пытается открыть и прочитать файл. В случае неудачи вызывает соответсвующее исключение,
    прекращает работу и возвращает None. В случае успеха создает список с названиями акций.
    Для каждой акции из списка парсит данные цен за 3 месяца и данные о торговле совладельцев компании.
    Данные сохраняются в базу."""
    try:  # пытаемся открыть файл и считать названия акций
        file = open('tickers.txt')
        stock_list = file.read()
    except EOFError as ex:
        return
    except IOError as e:
        return
    stock_list = stock_list.split('\n')  # создаем список
    for stock in stock_list:
        parse_stock_info(stock.lower())  # парсим цены на акции, прдварительно переведя название акции в нижний регистр
        pars_insider_info(stock.lower())  # парсим данные о торговле, прдварительно переведя название акции в нижний регистр


parse()
