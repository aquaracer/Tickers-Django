import datetime
from datetime import datetime
from app1.models import Tickers, Insiders
from django.http import JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from django.http import Http404
from app1.get_delta import get_delta


def index(request):
    """"Функция запускается при переходе на главную страницу /api.
      Выбирает из базы уникальные названия акций. Затем создает словарь, в котором
      ключом является название акции, значением - ссылка на акцию. Возвращает
      полученный словарь в виде JSON"""
    ordered_stocks = Tickers.objects.distinct('stock_name').values('stock_name')
    stocks = {}
    for stock in ordered_stocks:
        stocks[stock['stock_name']] = f"http://194.87.239.177/api/%{stock['stock_name']}%"  # формируем ссылку на акцию
    return JsonResponse(stocks)


def get_tickers_list(request, stock_name):
    """Функция принимает название акции(stock_name) из ссылки.
    Назначение функции - создать список с ценами на акцию по заданному названию за последние 3 месяца.
    Cначала функция проверяет есть ли акция с заданным названием в базе данных. Если нет -
    сразу возвращает ошибку 404. Если есть создает список данных на акцию за 3 месяца.
    Затем создает ссылку на веб-страницу с данными торговли владельцев компании.
    Возвращает JSON со следующими данными: 'insiders_url' : ссылка на веб-страницу с данными торговли
    владельцев компании, 'stocks' - список данных на акцию за 3 месяца """

    stock_name = stock_name.lower()  # переводим в нижний регистр (на случай если в ссылке введены данные в верхней регистре)
    ordered_stocks = Tickers.objects.all().order_by("-date")
    stocks = get_list_or_404(ordered_stocks,
                             stock_name=stock_name)  # проверяем есть ли акция с данным названием в базе. если нет
    # возвращаем ошибку 404. если есть получаем список с данными из базы
    stock_list = []
    for stock in stocks:  # создаем список с данными на акцию
        temp_dict = {'date': stock.date.strftime("%m/%d/%Y"),
                     'close_last': stock.close,
                     'volume': stock.volume,
                     'high': stock.high,
                     'low': stock.low,
                     'open': stock.open}
        stock_list.append(temp_dict)  # добавляем словарь с данными по акции в общий список данных с ценами
    insiders_url = f"http://194.87.239.177/api/%{stock_name}%/insider"  # создаем ссылку на страницу с данными торговли владельцев компании
    data = {'insiders_url': insiders_url, 'stocks': stock_list}
    return JsonResponse(data)


def get_insiders_list(request, stock_name):
    """Функция принимает название акции(stock_name) из ссылки.
    Назначение функции - создать список с данными торговли владельцев компании, выпустившей акцию.
    Cначала функция проверяет есть ли акция с заданным названием в базе данных. Если нет -
    возвращает ошибку 404. Если есть - создает список с данными торговли владельцев компании.
    Возвращает JSON с данными: 'insiders' - список с данными торговли владельцев компании."""

    stock_name = stock_name.lower()  # переводим в нижний регистр (на случай если в ссылке введены данные в верхней регистре)
    ordered_insder_list = Insiders.objects.all().order_by("-last_date")
    insiders = get_list_or_404(ordered_insder_list,
                               stock_name=stock_name)  # проверяем есть ли акция с данным названием в базе
    insiders_list = []
    for insider in insiders:  # создаем список с данными торговоли
        insider_name = insider.insider.replace(" ", "_")
        temp_dict = {'insider_trades_url': f"http://194.87.239.177/api/%{stock_name}%/insider/%{insider_name}%",
                     # заменяем пробел на нижнее подчеркивание чтобы ссылка была валдидной
                     'stock_name': insider.stock_name,
                     'insider': insider.insider,
                     'relation': insider.relation,
                     'last_date': insider.last_date.strftime("%m/%d/%Y"),
                     'transaction_type': insider.transaction_type,
                     'owner_type': insider.owner_type,
                     'shares_traded': insider.shares_traded,
                     'last_price': insider.last_price,
                     'shares_held': insider.shares_held}
        insiders_list.append(temp_dict)  # добавляем словарь с данными о торговле в общий список данных
    data = {'insiders': insiders_list}
    return JsonResponse(data)


def get_insider_trades(request, stock_name, insider_name):
    """Функция принимает название компании(stock_name) и имя владельца (insider_name) из ссылки.
    Сначала проверяет есть ли в базе данный владелец и обладает ли он акциями с заданным названием.
    В случае неудачи возвращает ошибку 404. В случае успешной проверка по полученной информации создает
    запрос к базе и формирует список с данными о торговле владельца компании. Возвращает JSON c
    сформированным списком """
    stock_name = stock_name.lower()
    insider_name = insider_name.upper().replace("_", " ")  # При наличии символов нижнего подчеркивания заменяем на
    # пробелы для корректного поиска в базе
    get_list_or_404(Insiders, stock_name=stock_name, insider=insider_name)  # проверяем есть ли
    insiders_list = []
    insiders = Insiders.objects.filter(stock_name=stock_name, insider=insider_name).order_by("-last_date")
    for insider in insiders:  # создаем список словарей с данными о торговле данного владельца компании
        temp_dict = {"last_date": insider.last_date.strftime("%m/%d/%Y"),
                     'transaction_type': insider.transaction_type,
                     'owner_type': insider.owner_type,
                     'shares_traded': insider.owner_type,
                     'last_price': insider.last_price,
                     'shares_held': insider.shares_held}
        insiders_list.append(temp_dict)  # добавляем в обший список данные о торговле владельца
    data = {'insider_operations': insiders_list}
    return JsonResponse(data)


def get_analysis(request, stock_name):
    """Функция принимает название акции(stock_name) и даты начала и конца периода.
    Проверяет есть ли акции с данным названием в базе. Если нет - возвращает ошибку 404.
    Далее проводит валидацию дат начала и конца периода. Если валидация не пройдена - возвращает
    ошибку 404. Далее проверяет есть ли в базе операций по акциям в заданные даты. Если операций
    по какой-либо из дат нет - возвращает ошибку 404. Если все проверки успешно пройдены высчитывает
    разницу цен(открытия, закрытия, максимума, минимума) в текущих датах. Возвращает JSON с данными
    о разнице цен """
    stock_name = stock_name.lower()
    get_list_or_404(Tickers, stock_name=stock_name)  # проверяем есть ли акции с таким названием в базе
    current_url = request.get_raw_uri()
    current_url = current_url.split('/')
    try:
        date_from = f'{current_url[6][-2:]}/{current_url[7]}/{current_url[8][:4]}'  # создаем начальную дату в формате '{month}/{day}/{year}'
        date_to = f'{current_url[8][-2:]}/{current_url[9]}/{current_url[10]}'  # создаем начальную дату в формате '{month}/{day}/{year}'
        date_from = datetime.strptime(date_from, '%m/%d/%Y')
        date_to = datetime.strptime(date_to, '%m/%d/%Y')
    except Exception as e:
        raise Http404()
    filtered_tickers = Tickers.objects.filter(stock_name=stock_name)
    date_from_object = get_object_or_404(filtered_tickers,
                                         date=date_from)  # проверяем были ли операции с акцией в заданную дату.
    date_to_object = get_object_or_404(filtered_tickers,
                                       date=date_to)  # проверяем были ли операции с акцией в заданную дату.
    delta_close = float("{0:.2f}".format(float(date_from_object.close[1:]) - float(date_to_object.close[1:])))
    delta_open = float("{0:.2f}".format(float(date_from_object.open[1:]) - float(date_to_object.open[1:])))
    delta_high = float("{0:.2f}".format(float(date_from_object.high[1:]) - float(date_to_object.high[1:])))
    delta_low = float("{0:.2f}".format(float(date_from_object.low[1:]) - float(date_to_object.low[1:])))
    data = {'delta_close_last': delta_close, 'delta_open': delta_open, 'delta_high': delta_high, 'delta_low': delta_low}
    return JsonResponse(data)


def delta_func(request, stock_name):
    """
    Функция принимает название акции(stock_name), величину изменения цены на акцию(N) и
    тип цены(open/high/low/close). Проверяет есть ли акция с данным названием в базе.
    Если нет - возвращает ошибку 404. Далее пытается найти минимальный период, за который указанная цена
    изменилась на N . В случае успеха возвращает JSON с данными о минимальном периоде
    (дата начала-дата конца). В случае неудачи возвращает JSON с сообщение о том, что данный период не найден.
    """
    stock_name = stock_name.lower()  # переводим в нижний регистр (на случай если в ссылке введены данные в верхней регистре)
    get_list_or_404(Tickers, stock_name=stock_name)  # проверяем есть ли акции с таким названием в базе
    current_url = request.get_raw_uri()
    current_url = current_url.split('/')
    data = current_url[-1]
    data = data.split('&')
    value = int(data[0][7:])  # получаем величину изменения цены на акцию из ссылки
    type = data[1][5:]  # получаем тип цены из ссылки
    filtered_tickers = Tickers.objects.filter(stock_name=stock_name).order_by('date').values(type, 'date')
    essential_period, data = get_delta(filtered_tickers, value, type) # запускаем функцию get_delta. функция возвращает 2 
                                                                      # параметра: essential_period(bool type) - данный параметр
                                                                      # указывает был ли найден заданный период, data - словарь с
                                                                      # c данными о минимальном периоде(или периодах если таких 
                                                                      # несколько).
    if essential_period:
        responce = {'periods': data}  # ответ с данными о периоде
    else:
        responce = {"error": "we can't find such period"}  # ответ с данными об ошибке
    return JsonResponse(responce)
