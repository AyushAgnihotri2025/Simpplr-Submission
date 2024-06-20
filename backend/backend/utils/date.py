from datetime import date
from datetime import datetime


def calculate_age(born: str | datetime) -> int:
    if isinstance(born, str):
        born = datetime.strptime(born, "%Y-%m-%d")

    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
