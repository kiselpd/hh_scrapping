import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import json

class HH:

    def __init__(self):
        self.__url = "https://hh.ru"

    
    def __make_text_header(self, text: str):
        return "text=" + text.replace(" ", "+")
    

    def __make_areas_header(self, areas):
        output_header = [f"area={area}" for area in areas]
        return "&".join(output_header)
            

    def __get_vacancy_html(self, areas=[], text=""):
        params = Headers(browser="google", os="linux").generate()
        vacancy_url = f"{self.__url}/search/vacancy?"

        if text:
            vacancy_url = vacancy_url + self.__make_text_header(text) + "&"
        
        if areas:
            vacancy_url = vacancy_url + self.__make_areas_header(areas)

        return requests.get(url=vacancy_url, headers=params)
    

    def __parse_name(self, div_vacancy):
        vacancy = div_vacancy.find(class_="serp-item__title")
        return vacancy.text, vacancy["href"]
    

    def __parse_company(self, div_vacancy):
        company = div_vacancy.find(class_="bloko-link_kind-tertiary")
        return company.text


    def __parse_city(self, div_vacancy):
        div_city = div_vacancy.find(class_="vacancy-serp-item__info")
        city = div_city.find_all(class_="bloko-text")
        return city[1].text
    

    def __parse_salary(self, div_vacancy):
        salary = div_vacancy.find_all(class_="bloko-header-section-3")
        if len(salary) > 1:
            return salary[1].text
        else:
            return None


    def __scrapping_html(self, html):

        soup = BeautifulSoup(html.text, features="lxml")
        vacancy_list = []

        for vacancy in soup.find_all(class_="vacancy-serp-item-body__main-info"):
            vacancy_name, vacancy_href = self.__parse_name(vacancy)
            vacancy_company = self.__parse_company(vacancy)
            vacancy_city = self.__parse_city(vacancy)
            vacancy_salary = self.__parse_salary(vacancy)
            
            vacancy_list.append(
                {"vacancy": vacancy_name,
                 "href": vacancy_href,
                 "salary": vacancy_salary,
                 "company": vacancy_company,
                 "city": vacancy_city}
            )

        return vacancy_list
    

    def get_vacancy(self, areas=[], text=""):
        html = self.__get_vacancy_html(areas, text)

        return json.dumps(self.__scrapping_html(html),
                          indent=4,
                          ensure_ascii=False,
                          )

