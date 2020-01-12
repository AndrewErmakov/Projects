import os
import json
from collections import namedtuple

PlayerResult = namedtuple('PlayerResult', ['name_player', 'count_points', 'count_mistakes'])


class RecordTable:

    def is_there_file(self):
        """
        Функция проверки наличия файла
        :return: Существует файл или нет?
        """
        return os.path.exists(self.file_name)

    # функция создания пустого файла БД
    def create_empty_file(self):
        self.data = []
        with open(self.file_name, 'w') as file:
            json.dump(self.data, file)

    def read_file(self):
        """
        Функция чтения файла
        :return: таблица рекордов
        """
        with open(self.file_name, 'r') as read_file:
            self.data = json.load(read_file)
            return self.data

    def add_record(self, some_data: PlayerResult):
        """
        Функция добавления записи в таблицу
        :return: обновленная таблица рекордов
        """
        self.data.append([some_data.name_player, some_data.count_points, some_data.count_mistakes])
        self.write_file()

    def write_file(self):
        """
        Функция записи в файл
        """
        with open(self.file_name, 'w') as file:
            json.dump(self.data, file)

    # функция работы с файлом БД
    def __init__(self, file_name):
        self.file_name = file_name

        if not self.is_there_file():
            self.create_empty_file()

        else:
            self.read_file()

    # pass
