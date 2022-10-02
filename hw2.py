import csv


def menu() -> None:
    """
    The function displays a menu with options for the user
    """
    file = 'C:/AAA/Corp_Summary.csv'
    data = read_csv_to_dict(file)
    is_run = True
    options = ['1', '2', '3', '0']
    while is_run:
        option = ''
        print(
            'Выберите опцию:\n'
            '1. Вывести иерархию команд\n'
            '2. Вывести сводный отчёт по департаментам\n'
            '3. Сохранить сводный отчёт по департаментам\n'
            '0. Выход\n'
        )
        while option not in options:
            print('Выберите: {}/{}/{}/{}'.format(*options))
            option = input()
        if option == '1':
            print_hierarchy(data)
        elif option == '2':
            print_corp_report(data)
        elif option == '3':
            file_out = 'C:/AAA/corp_report.csv'
            corp_report_to_csv(data, file_out)
        else:
            is_run = False
    print('Программа завершена.')


def read_csv_to_dict(path: str) -> list[dict]:
    """
    The function reads a csv file and returns a list of dictionaries
    :param path: path to csv file.
    :return: list of dictionaries with records about employees.
    """
    with open(path, encoding='UTF-8') as csv_file:
        corp_reader = csv.DictReader(csv_file, delimiter=';')
        return [row for row in corp_reader]


def print_hierarchy(data: list[dict]) -> None:
    """
    The function print a hierarchy of teams for each department
    :param data: list of dictionaries with records about employees.
    """
    departments = get_departments(data)
    for department in departments:
        print(f'Департамент: {department}')
        print('{:>12}'.format('Команды:'))
        for team in departments[department]:
            print('{:>12}'.format('•'), team)
        print('')


def get_departments(data: list[dict]) -> dict[str, list]:
    """
    The function returns a list of teams for each department
    :param data: list of dictionaries with records about employees.
    :return: dictionary {department: teams}.
    """
    departments = {}
    for row in data:
        if row['Департамент'] not in departments.keys():
            departments[row['Департамент']] = []
            departments[row['Департамент']].append(row['Отдел'])
        else:
            if row['Отдел'] not in departments[row['Департамент']]:
                departments[row['Департамент']].append(row['Отдел'])
    return departments


def print_corp_report(data: list[dict]) -> None:
    """
    The function print a summary report by department
    :param data: list of dictionaries with records about employees.
    """
    departments_salaries = get_department_salaries(data)
    departments_summary = get_departments_summary(departments_salaries)
    print('', '-' * 74, '')
    print('|{:^15}|{:^20}|{:^18}|{:^18}|'.format('Департамент',
                                                 'Кол-во сотрудников',
                                                 'Вилка зарплаты',
                                                 'Средняя зарплата'))
    print('|{:-^15}|{:-^20}|{:-^18}|{:-^18}|'.format('', '', '', ''))
    for k, v in departments_summary.items():
        num_workers, fork_salary, mean_salary = v
        print('|{:^15}|{:^20}|{:^18}|{:^18}|'.format(k, num_workers, fork_salary, mean_salary))
    print('', '¯' * 74, '')


def get_department_salaries(data: list[dict]) -> dict[str, list]:
    """
    The function returns a list of salaries for each department
    :param data: list of dictionaries with records about employees.
    :return: dictionary {department: salaries}.
    """
    departments_salaries = {}
    for row in data:
        if row['Департамент'] not in departments_salaries.keys():
            departments_salaries[row['Департамент']] = []
        departments_salaries[row['Департамент']].append(int(row['Оклад']))
    return departments_salaries


def get_departments_summary(departments_salaries: dict[str, list]) -> dict[str, list]:
    """
    The function returns a list with
    summary statistics (number of workers, fork salary, mean salary)
    for each department
    :param departments_salaries: dictionary {department: salaries}.
    :return: dictionary {department: summary statistics}.
    """
    departments_summary = {}
    for department in departments_salaries:
        num_workers = len(departments_salaries[department])
        min_salary = min(departments_salaries[department])
        max_salary = max(departments_salaries[department])
        fork_salary = str(min_salary) + '–' + str(max_salary)
        sum_salary = sum(departments_salaries[department])
        mean_salary = f'{sum_salary / num_workers:.2f}'
        departments_summary[department] = [num_workers, fork_salary, mean_salary]
    return departments_summary


def corp_report_to_csv(data: list[dict], file_out: str) -> None:
    """
    The function saves a summary report on departments in a csv file
    :param data: list of dictionaries with records about employees
    :param file_out: path to csv file.
    """
    departments_salaries = get_department_salaries(data)
    departments_summary = get_departments_summary(departments_salaries)
    with open(file_out, 'w', newline='') as csvfile:
        fieldnames = ['Департамент', 'Кол-во сотрудников', 'Вилка зарплаты', 'Средняя зарплата']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        for department in departments_summary:
            writer.writerow({'Департамент': department,
                             'Кол-во сотрудников': departments_summary[department][0],
                             'Вилка зарплаты': departments_summary[department][1],
                             'Средняя зарплата': departments_summary[department][2]
                             })
    print(f'Файл c отчетом успешно сохранен в {file_out}.\n')


if __name__ == '__main__':
    menu()
