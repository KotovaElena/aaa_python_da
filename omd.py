# Guido van Rossum <guido@python.org>

def step1():
    print(
        'Утка-маляр 🦆 решила выпить зайти в бар. '
        'Взять ей зонтик? ☂️'
    )
    option = ''
    options = {'да': True, 'нет': False}
    while option not in options:
        print('Выберите: {}/{}'.format(*options))
        option = input().lower()
    if options[option]:
        return step2_umbrella()
    return step2_no_umbrella()


def step2_umbrella():
    print(
        'Пошел дождь и зонтик пригодился ☔. Довольная утка зашла в бар.'
    )
    return step3_bar()


def step2_no_umbrella():
    print(
        'На небе не было ни облачка ☀. Довольная утка зашла в бар.'
    )
    return step3_bar()


def step3_bar():
    print(
        'Что заказать утке?'
    )
    option = ''
    options = {'виски', 'шампанское', 'пиво'}
    while option not in options:
        print('Выберите: {}/{}/{}'.format(*options))
        option = input().lower()
    return step4_order(option)


def step4_order(option):
    print(
        f'{option.capitalize()} понравилось утке. '
        'Бармен подходит к ней и предлагает повторить заказ.\n'
        'Повторить заказ?'
    )
    option = ''
    options = {'да': True, 'нет': False}
    while option not in options:
        print('Выберите: {}/{}'.format(*options))
        option = input().lower()

    if options[option]:
        return step5_drink()
    return step5_no_drink()


def step5_drink():
    print(
        'Бармен уходит за напитком.\n'
        'Когда он возращается, утки уже нет, а на барной стойке лежат 10$ 💵.\n'
    )
    return step6_end()


def step5_no_drink():
    print(
        'Утка платит 10$ 💵 и тут же исчезает.\n'
    )
    return step6_end()


def step6_end():
    print(
        '❗ Срочные новости! ❗\n'
        'В городе участились случаи обнаружения поддельных купюр.\n'
        'Разыскивается главарь банды фальшивомонетчиков по кличке Маляр 🚓.\n'
        'Особые приметы: утка.\n'
        'The End!'
    )


if __name__ == '__main__':
    step1()
