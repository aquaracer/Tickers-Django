def get_delta(stock_list, goal_delta, type):
    """ Функция получает на входе список словарей(stock_list) формата {'type': типа цены на акцию, 'date' : дата},
    искомую величину изменения цены на акцию(goal_delta), типы цены(type).
    Производит поиск минимального периода (дата начала-дата конца) когда указанная цена изменила на
    величину goal_delta или более. Возвращает переменную got_essential_period со значение True, означающую
    что по заданным данным минимальный период найден и cписок с единственным элементом - словарем c данными
    о начале и конце периода. Если таких периодов несколько - возвращает переменную got_essential_period со значением
    True, означающую, что по заданным данным как минимум один период найден и список словарей с данными о начале и конце
    периодов. Если период не найден возвращает переменную got_essential_period со значение False, означающую что
    по заданным данным пероиl не найден и список с одним элементом - словарем, где значения ключей начала и конца
    периода равны None"""
    current_delta = 0
    current_period = 0
    index_end = 0
    index_begin = 0
    got_essential_period = False
    duration = 93
    data = [{'start_date': None, 'end_date': None}]
    while True:
        if current_delta < goal_delta:
            if current_delta < 0:
                index_begin = index_end
                current_period = 0
                current_delta = 0
            index_end += 1
            if index_end == len(stock_list):
                break
            current_period += 1
            current_delta += float("{0:.2f}".format(
                float(stock_list[index_end][type][1:]) - float(stock_list[index_end - 1][type][1:])))
        elif current_delta == goal_delta:
            if current_period < duration:  # если найден более короткий период меняем данные о минимальном
                got_essential_period = True
                duration = current_period
                data = [{'start_date': stock_list[index_begin]['date'], 'end_date': stock_list[index_end]['date']}]
            elif current_period == duration:  # если найден период с такойже продолжительностью добавляем
                got_essential_period = True
                duration = current_period
                data.append({'start_date': stock_list[index_begin]['date'],  # его в список минимальных периодов
                             'end_date': stock_list[index_end]['date']})
            index_end += 1
            if index_end == len(stock_list):
                break
            index_begin += 1
            current_delta = current_delta + float("{0:.2f}".format(
                float(stock_list[index_end][type][1:]) - float(stock_list[index_end - 1][type][1:]) - (
                        float(stock_list[index_begin][type][1:]) - float(stock_list[index_begin - 1][type][1:]))))
        elif current_delta > goal_delta:
            if current_period < duration:
                got_essential_period = True
                duration = current_period
                data = [{'start_date': stock_list[index_begin]['date'], 'end_date': stock_list[index_end]['date']}]
                index_begin += 1
                if index_begin == len(stock_list) - 1:
                    break
                current_delta -= float("{0:.2f}".format(
                    float(stock_list[index_begin][type][1:]) - float(stock_list[index_begin - 1][type][1:])))
                current_period -= 1
            elif current_period == duration:  # если найден период с такой же продолжительностью добавляем
                got_essential_period = True
                data.append({'start_date': stock_list[index_begin]['date'],  # его в список минимальных периодов
                             'end_date': stock_list[index_end]['date']})
                index_end += 1
                if index_end == len(stock_list):
                    break
                index_begin += 1
                current_delta = current_delta + float("{0:.2f}".format(
                    float(stock_list[index_end][type][1:]) - float(stock_list[index_end - 1][type][1:]) - (
                            float(stock_list[index_begin][type][1:]) - float(stock_list[index_begin - 1][type][1:]))))
            elif current_period > duration:
                index_begin += 1
                if index_begin == len(stock_list) - 1:
                    break
                current_delta -= float("{0:.2f}".format(
                    float(stock_list[index_begin][type][1:]) - float(stock_list[index_begin - 1][type][1:])))
                current_period -= 1
    return got_essential_period, data
