import requests as requests
from bs4 import BeautifulSoup

from src.Config import Config


class PhoneNumberInformator:
    def __init__(self, url=Config.BASE_URL):
        self.url = url

    def get_number_info(self, number):
        try:
            search_url = f"{Config.BASE_URL}/{number}"  # ссылка на номер
            html = self.url_to_html(search_url)  # получаю html

            soup = BeautifulSoup(html, features="html.parser")

            region = self.parse_number_region(soup)
            op = self.parse_number_op(soup)

            if region == -1 or op == -1:
                return "Некорректно задан номер (или) информация о номере не найдена!"

            return {
                "number": number,
                "region": region,
                "op": op
            }

        except requests.RequestException as e:
            return {"error": str(e)}

    def parse_number_region(self, soup):
        region = soup.find("h2")
        if region:
            final_region = soup.find("h2").next_sibling.next_sibling.text  # получаю регион
            return final_region[4:-4]

        return -1

    def parse_number_op(self, soup):
        op = soup.find("p", class_="actualOp")
        if op:
            final_op = op.text  # получаю регион
            return final_op[4:-4]

        return -1

    def url_to_html(self, url):
        response = requests.get(url, headers=Config.HEADERS)
        response.raise_for_status()
        return response.text
