import os
import json

class RecordTable:
    # функция проверки наличия файла
    def is_there_file(self, file_name='db.json'):
        self.file_name = file_name
        return os.path.exists(self.file_name)

    # функция создания пустого файла БД
    def create_empty_file(self):
        with open(self.file_name, 'w') as file:
            json.dump([], file)

    # функция чтения файла
    def read_file(self):
        with open(self.file_name, "r") as read_file:
            data = json.load(read_file)
            return data

    # функция записи в файл
    def write_file(self):
        pass

    # функция работы с файлом БД
    def work_with_db_file(self):
        if not self.is_there_file(self.file_name):
            self.create_empty_file()

        else:
            reader_file = self.read_file()
            new_file = self.write_file()
    # pass
