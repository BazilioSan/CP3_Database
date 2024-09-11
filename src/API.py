from ABC import ABC, abstractmethod
from typing import Any, List

import requests


class Parser(ABC):
    """Класс по работе с API"""

    @abstractmethod
    def load_vacancies(self) -> None:
        pass

    @abstractmethod
    def export_vacancies(self) -> List[Any]:
        pass


class HH(Parser):
    """Класс для парсинга вакансий с hh.ru (Родительский - Parser)"""

    def __init__(self) -> None:
        self.url = "https://api.hh.ru/vacancies"
        self.headers = {"User-Agent": "HH-User-Agent"}
        self.params = {
            "employer_id": "",
            "area": 113,
            "page": 0,
            "per_page": 100
        }
        self.vacancies = []
        self.vacancies_for_base = []

    def load_vacancies(self, id:list[Any]) -> None:
        """Функция загружает вакансии по списку id юзера с HH"""

        self.params["employer_id"] = id

        while self.params.get("page") != 20:
            try:
                response = requests.get(self.url, headers=self.headers, params=self.params)
            except Exception as e:
                print(f"Произошла ошибка {e}")
            else:
                vacancies = response.json()["items"]
                self.vacancies.extend(vacancies)
                self.params["page"] += 1

        for vacancie in self.vacancies:
            if vacancie["employer"]["name"]:
                employer = vacancie["employer"]["name"]
                if vacancie["name"]:
                    title = vacancie["name"]
                else:
                    title = "Не указано."
                if vacancie["alternate_url"]:
                    link = vacancie["alternate_url"]
                else:
                    link = "Не указано."
                if vacancie["snippet"]["responsibility"]:
                    description = vacancie["snippet"]["responsibility"]
                else:
                    description = "Не указано."
                if vacancie["snippet"]["requirement"]:
                    requirement = vacancie["snippet"]["requirement"]
                else:
                    requirement = "Не указано."

                if vacancie["salary"]:
                    if vacancie["salary"]["from"]:
                        salary = vacancie["salary"]["from"]
                    elif vacancie["salary"]["to"]:
                        salary = vacancie["salary"]["to"]
                    else:
                        salary = 0
                else:
                    salary = 0

                if vacancie["area"]["name"]:
                    area = vacancie["area"]["name"]
                else:
                    area = "Не указано."
                self.vacancies_for_base.append(
                    {
                        "employer": employer,
                        "title": title,
                        "link": link,
                        "description": description,
                        "requirement": requirement,
                        "salary": salary,
                        "area": area,
                    }
                )

