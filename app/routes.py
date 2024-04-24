import csv
import json
from lib2to3.pgen2.grammar import line
from turtle import pd

import requests
from bs4 import BeautifulSoup
from flask import render_template, request
from src.PhoneNumberInformator import PhoneNumberInformator


def configure_routes(app):
    fetcher = PhoneNumberInformator()

    @app.route("/")
    def index():
        return render_template('index.html')

    @app.route("/save_table", methods=['POST'])
    def save_table():
        data = request.form['data'].replace("'", '"')
        data_json = json.loads(data)
        print(data_json[0])

        with open("output.csv", 'w', encoding='utf-8') as file:
            csv_writer = csv.writer(file, delimiter=',')
            csv_writer.writerow(['Номер', 'Регион', 'Оператор'])

            for item in data_json:
                csv_writer.writerow([item['number'], item['region'], item['op']])

        return f'Таблица сохранена в файл output.csv'

    @app.route("/details", methods=['GET', 'POST'])
    def details():
        if request.method == 'POST':
            # заменяю все возможные варианты ввода номера телефона пользователем ('(', ')', '-', ' ')

            if 'file' in request.files:
                file = request.files['file']

                if file.filename:  # если есть какой-то загруженный файл - читаю оттуда
                    file.save(file.filename)
                    phone_numbers = read_numbers_from_file(file)
                    phone_info = [fetcher.get_number_info(number) for number in phone_numbers]
                    return render_template('phone_numbers.html', numbers=phone_info)

                else:  # иначе читаю с формы ввода
                    number = request.form['number'].replace(" ", "") \
                        .replace("(", "").replace(")", "").replace("-", "")

                    phone_number_info = fetcher.get_number_info(number=number)
                    return render_template('details.html', phone_number_info=phone_number_info, number=number)

        return render_template('index.html')

    @app.route('/details/<number>')
    def show_details(number):
        number_info = fetcher.get_number_info(number=number)
        return render_template('details.html', number_info=number_info, number=number)

    def read_numbers_from_file(file):
        phone_numbers = []
        with open(file.filename, 'r') as file:
            for line in file:
                phone_number = line.strip()  # Удаляем символы переноса строки и пробелы
                phone_numbers.append(phone_number)

        return phone_numbers
