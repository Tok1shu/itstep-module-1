"""
Код не рабочий, ИИ предложил использовать all, о котором я благополучно забыл пока писал функцию
который сократил объем функции в 4 раза.
"""

def get_input(message: str, *validators):
    passed_validators = 0
    while passed_validators < len(validators):
        user_input = input(message)
        for validator in validators:
            if not validator(user_input):
                passed_validators = 0
                break
            passed_validators += 1

    return user_input

"""
Без этой функции приходилось делать такие штуки
"""

# Код чтоб ide не жаловалась
basic_validate = lambda x: True
validate_phone = lambda x: True
validate_email = lambda x: True

# Часть функции создания пользователя
name = input("Введите имя: ")
while not basic_validate(name):
    name = input("Введите имя: ")

phone = input("Введите номер телефона (12 цифр): +")
while not validate_phone(phone):
    phone = input("Введите номер телефона (12 цифр): +")

email = input("Введите электронную почту: ")
while not validate_email(email):
    email = input("Введите электронную почту: ")
