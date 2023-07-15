import datetime
import requests
import os
import sys


def logger(old_function):
    """простой декоратор"""

    def new_function(*args, **kwargs):
        start = datetime.datetime.now()
        arg = f'{args}{kwargs}'
        result = ''
        try:
            result = old_function(*args, **kwargs)
        except Exception:
            error = sys.exc_info()[1]
            result = f'Ошибка при выполнении функции: {error.args[0]}'
        finally:
            log_content = ('<{}>  <{}>  <{}>  <{}>\n'.format(old_function.__name__, arg, start, result))
            with open('main.log', 'a', encoding='utf8') as file:
                file.write(log_content)
        return result

    return new_function


url_jsdelivr = 'https://cdn.jsdelivr.net/gh/akabab/superhero-api@0.3.0/api/all.json'


@logger
def who_is_smarted(url):
    resp = requests.get(url)
    result = resp.json()
    mind_of_heroes = {}
    for i in result:
        key = i.get('name')
        if key in 'Captain America Hulk Thanos':
            val = i.get('powerstats').get('intelligence')
            mind_of_heroes.setdefault(key, val)
    smartest = dict([max(mind_of_heroes.items(), key=lambda k_v: k_v[1])])
    return f'Самый умный из Captain America, Hulk, Thanos: {"".join(smartest.keys())}'


def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_1()

    print(who_is_smarted(url_jsdelivr))
