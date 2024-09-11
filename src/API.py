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
    """Класс для парсинга вакансий с hh.ru"""

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

