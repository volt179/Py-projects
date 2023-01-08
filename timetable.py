from bs4 import BeautifulSoup
from datetime import datetime
import requests

URL = "https://guap.ru/rasp/"
HEADERS = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}
DAYS = {
    "0": "Понедельник",
    "1": "Вторник",
    "2": "Среда",
    "3": "Четверг",
    "4": "Пятница",
    "5": "Суббота",
    "6": "Воскресенье"
}


def get_timetable(group):
    req = requests.get(URL + f"?g={group}").text

    # flag_write = 0
    # if flag_write:
    #     req = requests.get(URL + f"?g={group}").text
    #     with open("text.html", "w") as file:
    #         file.write(req)
    # else:
    #     with open("text.html") as file:
    #         req = file.read()

    flag_void = 1
    flag_parity_week = ""
    soup = BeautifulSoup(req, 'lxml')
    if "▲" in soup.find(class_="dn"):
        flag_parity_week = "▲"
    else:
        flag_parity_week = "▼"

    current_day = DAYS[f"{datetime.now().weekday()}"]
    all_lessons = [i for i in soup.find(class_="result")]
    n = 0
    while n < len(all_lessons[1:]):
        if all_lessons[n].text == current_day:
            n += 1
            print(all_lessons[n-1].text)
            while all_lessons[n].name != "h3":
                if flag_parity_week in all_lessons[n].text\
                        or ("▼" not in all_lessons[n].text and "▲" not in all_lessons[n].text
                            and all_lessons[n].name == "div"):
                    flag_void = 0
                    if all_lessons[n-1].name == "div":
                        print(all_lessons[n-2].text)
                    else:
                        print(all_lessons[n-1].text)
                    print(all_lessons[n].span.text)
                n += 1
                if n >= len(all_lessons):
                    break
        n += 1

    if flag_void:
        print(f"{current_day}: занятий нет")


def input_group():
    group = str(input("Введите номер группы: "))
    req = requests.get(URL, headers=HEADERS).text
    soup = BeautifulSoup(req, 'lxml')
    group_data = soup.find(attrs={"name": "ctl00$cphMain$ctl05"})
    for i in group_data:
        if i.text == group:
            id_page = i["value"]
            return id_page
    return None


def main():
    while True:
        ans = input("1. Показать расписание на сегодня\n2. Выйти\nВыбор: ")
        if ans == "1":
            q = input_group()
            get_timetable(q)
        elif ans == "2":
            break
        else:
            print("Введи 1 или 2")


if __name__ == "__main__":
    main();