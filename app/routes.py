from flask import render_template, request
from src.PhoneNumberInformator import PhoneNumberInformator


def configure_routes(app):
    fetcher = PhoneNumberInformator()

    @app.route("/")
    def index():
        return render_template('index.html')

    @app.route("/details", methods=['GET', 'POST'])
    def details():
        if request.method == 'POST':
            # заменяю все возможные варианты ввода номера телефона пользователем ('(', ')', '-', ' ')
            number = request.form['number'].replace(" ", "")\
                .replace("(", "").replace(")", "").replace("-", "")
            phone_number_info = fetcher.get_number_info(number=number)
            return render_template('details.html', phone_number_info=phone_number_info, number=number)
        return render_template('index.html')

    @app.route('/details/<number>')
    def show_details(number):
        number_info = fetcher.get_number_info(number=number)
        return render_template('details.html', number_info=number_info, number=number)
