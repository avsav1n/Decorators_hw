import datetime
import time
import os

class Logger:
    '''Класс кастомного логгера

    '''

    def __new__(cls):
        '''Инициализатор одиночки

        '''
        if not hasattr(cls, 'existence'):
            cls.existence = super(Logger, cls).__new__(cls)
        return cls.existence

    @classmethod
    def init(cls, old_function):
        '''Простой декоратор инициализации логгирования функции

        '''
        def new_function(*args, **kwargs):
            info = (f'START FUNCTION "{old_function.__name__}";\n'
                    f'\tВремя запуска: {datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')};\n')
            info += (f'\tАргументы: {args}, {kwargs};\n')
            start_time = time.perf_counter()

            result = old_function(*args, **kwargs)

            finish_time = time.perf_counter() - start_time
            info += f'\tВремя работы: {finish_time};\n'
            info += f'\tРезультат выполнения: {result};\n'
            with open('main.log', 'a', encoding='utf-8') as fw:
                fw.write(info)
            return result
        return new_function
    
    @classmethod
    def init_with_path(cls, path):
        '''Параметризованный декоратор инициализации логгирования функции

        '''
        def init(old_function):
            def new_function(*args, **kwargs):
                info = (f'START FUNCTION "{old_function.__name__}";\n'
                        f'\tВремя запуска: {datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')};\n')
                info += (f'\tАргументы: {args}, {kwargs};\n')
                start_time = time.perf_counter()

                result = old_function(*args, **kwargs)

                finish_time = time.perf_counter() - start_time
                info += f'\tВремя работы: {finish_time};\n'
                info += f'\tРезультат выполнения: {result};\n'
                with open(path, 'a', encoding='utf-8') as fw:
                    fw.write(info)
                return result
            return new_function
        return init


def test_1():

    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @Logger.init
    def hello_world():
        return 'Hello World'

    @Logger.init
    def summator(a, b=0):
        return a + b

    @Logger.init
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

def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @Logger.init_with_path(path)
        def hello_world():
            return 'Hello World'

        @Logger.init_with_path(path)
        def summator(a, b=0):
            return a + b

        @Logger.init_with_path(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_1()
    test_2()
