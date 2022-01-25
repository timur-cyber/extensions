"""
Программа представляет собой генератор команд и таблиц путём стандартизированных алгоритмов
"""

import random
import sqlite3

TEMPLATE_NAMES = [
    'Альфа',
    'Омега',
    'Бета',
    'Гамма',
    'Дельта',
    'Лямбда',
    'Сигма',
    'Ипсилон'
]

COUNTRIES = [
    'Россия',
    'Италия',
    'Нидерланды',
    'Германия',
    'Франция',
    'Испания',
    'Бельгия',
    'Польша',
    'Англия'
]

POWERS = [
    'слабый',
    'средний',
    'сильный'
]

GROUP_ALPHABET = 'A B C D E F G H I J K L M N O P'.split()


class Team:
    numbers = []

    def __init__(self, num, name, country, power):
        self.number = num
        self.name = name
        self.country = country
        self.power = power
        self.numbers.append(self.number)

    def __str__(self):
        return f'Команда: {self.name}\n' \
               f'Страна: {self.country}\n' \
               f'Номер {self.number}\n' \
               f'Сила: {self.power}'


def generate_team(power=random.choice(POWERS)) -> Team:
    while True:
        number = random.randint(1, 64)
        if number not in Team.numbers:
            name = random.choice(TEMPLATE_NAMES)
            country = random.choice(COUNTRIES)
            return Team(number, name, country, power)


def generate_groups(grands: list, average: list, underdogs: list) -> list:
    groups = []
    i = 0
    for _ in range(len(grands)):
        grand_1 = random.choice(grands)
        grands.remove(grand_1)
        average_1 = random.choice(average)
        average.remove(average_1)
        average_2 = random.choice(average)
        average.remove(average_2)
        underdog_1 = random.choice(underdogs)
        underdogs.remove(underdog_1)
        group_letter = GROUP_ALPHABET[i]
        group = (group_letter, grand_1, average_1, average_2, underdog_1)
        i += 1
        groups.append(group)
    return groups


def generate_test_data(c: sqlite3.Cursor, number_of_groups: int) -> None:
    if 4 <= number_of_groups <= 16:
        grands = [generate_team(power='сильный') for _ in range(number_of_groups)]
        average = [generate_team(power='средний') for _ in range(number_of_groups * 2)]
        underdogs = [generate_team(power='слабый') for _ in range(number_of_groups)]
        for team in grands + average + underdogs:
            c.execute("""
            INSERT INTO commands (command_number, command_name, command_country, command_level)
            VALUES (?, ?, ?, ?)
            """, (team.number, team.name, team.country, team.power))

        groups = generate_groups(grands, average, underdogs)
        for group in groups:
            letter = group[0]
            for team in group[1:]:
                c.execute("""
                INSERT INTO team_draw (command_number, group_number)
                VALUES (?, ?)
                """, (team.number, letter))
    else:
        raise ValueError('Введено неверное значение')


def reset_tables(c: sqlite3.Cursor) -> None:
    c.execute("""DELETE FROM commands""")
    c.execute("""DELETE FROM team_draw""")


def create_tables(c: sqlite3.Cursor):
    sql_request = """
    CREATE TABLE IF NOT EXISTS `commands` (
        command_number INTEGER PRIMARY KEY,
        command_name VARCHAR(255) NOT NULL,
        command_country VARCHAR(255) NOT NULL,
        command_level VARCHAR(255) NOT NULL
    );

    CREATE TABLE IF NOT EXISTS `team_draw` (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        command_number INTEGER NOT NULL UNIQUE,
        group_number INTEGER NOT NULL,
        FOREIGN KEY (command_number) REFERENCES `commands` (command_number)
    );
    """
    c.executescript(sql_request)


if __name__ == '__main__':
    with sqlite3.connect('team.db') as conn:
        cursor = conn.cursor()
        create_tables(cursor)
        reset_tables(cursor)
        generate_test_data(cursor, 16)
