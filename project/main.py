# Валидаторы

def process_exit_input(user_input: str):
    if user_input == "exit": exit_app()
def process_menu_input(user_input: str):
    if user_input == "menu": menu()

def prepare_value(value: str):
    process_exit_input(value)
    process_menu_input(value)
    return value.strip()

def is_empty_value(value: str):
    if not value:
        print("Ввод не может быть пустым\n")
        return False
    return True

def is_content_has_enter(value: str):
    if "\n" in value:
        print("В строке есть перенос строки, это недопустимо")
        return False

    return True

def full_validate(value: str):
    prepared_value = prepare_value(value)
    return is_content_has_enter(prepared_value) and is_empty_value(prepared_value)

def integer_validate(value: str):
    try: int(value)
    except ValueError:
        print("Введенным данным должно быть число")
        return False
    return True

def validate_phone(phone: str):
    result = True

    if len(phone) != 12:result = False
    if not integer_validate(phone): result = False
    if not result: print("Номер должен быть длинной 12 символов\n")
    return result

def validate_email(email: str):
    result = "@" in email and "." in email
    if not result: print("Почта должна содержать \"@\" и \".\".\n")
    return result

# БД
def get_contacts():
    with open("contacts.txt", "r") as file:
        return file.readlines()

def decode_contact(contact: str) -> dict:
    name, phone, email = contact.strip("\n").split(",")
    return {"name": name, "phone": phone, "email": email}

def get_decoded_contacts():
    return [decode_contact(contact) for contact in get_contacts()]

def show_contact(contact: dict):
    print()
    print("Имя: ", contact["name"])
    print("Номер телефона: ", contact["phone"])
    print("Электронная почта: ", contact["email"])
    print()

# Остальное


# old_get_input

def get_input(message: str, default_value=None, *validators):
    while True:
        user_input = input(message)
        if not user_input: user_input = default_value
        if all(validator(user_input) for validator in validators):
            return user_input

def exit_app():
    print()
    print("👋 Программа завершена. До свидания!")
    exit()

def check_unique_contact(phone: str, email: str):
    contacts = get_contacts()
    for contact in contacts:
        contact = decode_contact(contact)
        if contact["phone"] == str(phone) or contact["email"] == email:
            return False
    return True

def add_contact():
    print("-"*60)
    print("Добавление контакта")
    while True:
        print()

        # old_get_input

        name  = get_input("Введите имя: ", full_validate)
        phone = get_input("Введите номер телефона (12 цифр): +", full_validate, validate_phone)
        email = get_input("Введите электронную почту: ", full_validate, validate_email)

        if not check_unique_contact(phone, email):
            print("Такой контакт уже существует, попробуйте создать другой")
            continue

        break

    with open("contacts.txt", "a") as db:
        to_write = f"{name},{phone},{email}\n"
        db.write(to_write)

    print("✅ Контакт успешно добавлен!")
    return to_write

def find_contact(get_user_choose: bool = False):
    print("-"*60)
    print("Поисковик контактов :3")

    while True:
        print("Дабы найти контакт введите:")
        print("- Точное имя")
        print("- Номер телефона (начиная с +)")
        contact_to_find = get_input("> ", prepare_value, full_validate)
        raw_contacts = get_contacts()

        found_contacts = []
        search_query = "name"

        if contact_to_find.startswith("+"):
            search_query = "phone"
            contact_to_find = contact_to_find[1:]

        for contact in raw_contacts:
            contact = decode_contact(contact)
            value = contact[search_query]
            if value.lower() == contact_to_find.lower():
                found_contacts.append(contact)

        if len(found_contacts) > 1:
            print(f"Найдено {len(found_contacts)} контактов с такими данными")
            for contact in found_contacts:
                contact_index = found_contacts.index(contact) + 1
                print(f"{contact_index} | {contact['name']}, {contact['phone']}, {contact['email']}")
            if get_user_choose:
                true_choose = False
                while not true_choose:
                    user_choose = int(get_input("Выберите контакт по айди: ", integer_validate)) - 1
                    try:
                        show_contact(found_contacts[user_choose])
                        true_choose = True
                        return found_contacts[user_choose]
                    except IndexError:
                        print("Данного индекса нет, выберите из предложенных выше")
                        continue
            else: return found_contacts # Возвращаю все контакты, первый по индексу это основной
        elif len(found_contacts) == 1:
            print("Найден 1 контакт с такими данными")
            show_contact(found_contacts[0])
            return found_contacts[0]
        else:
            print("❌ Контакт не найден")
            return None

def remove_contact():
    print("-"*60)
    print("Удаление аккаунта")
    raw_contacts = get_contacts()
    contact = find_contact(True)
    if not contact: return None
    raw_contacts.remove(f"{contact['name']},{contact['phone']},{contact['email']}\n")
    with open("contacts.txt", "w") as db:
        db.writelines(raw_contacts)
    print("✅ Контакт удалён!")
    return contact

def update_contact():
    print("-"*60)
    print("Обновление аккаунта")
    contact = find_contact(True)
    new_contact = {}
    if not contact: return None
    print("Если не хотите менять поле просто впишите пустую строку")

    while True:
        name = get_input("Введите имя: ", contact["name"], prepare_value, is_content_has_enter)
        phone = get_input("Введите номер телефона (12 цифр): +", contact["phone"], prepare_value, validate_phone, is_content_has_enter)
        email = get_input("Введите электронную почту: ", contact["email"], prepare_value, validate_email, is_content_has_enter)

        if phone != contact["phone"] or email != contact["email"]:
            if not check_unique_contact(phone, email):
                print("Такой контакт уже существует, попробуйте создать другой")
                break

        new_contact["name"] = name
        new_contact["phone"] = phone
        new_contact["email"] = email

        old_line = f"{contact['name']},{contact['phone']},{contact['email']}\n"
        new_line = f"{new_contact['name']},{new_contact['phone']},{new_contact['email']}\n"

        contacts = get_contacts()
        found = False
        for index, line in enumerate(contacts):
            if line.strip() == old_line.strip():
                contacts[index] = new_line
                found = True
                break

        if found:
            with open("contacts.txt", "w") as db:
                db.writelines(contacts)
            print("✅ Контакт успешно обновлен!")
            show_contact(new_contact)
            break
        else:
            print("Не удалось найти оригинальный контакт для обновления")

def show_contacts():
    print("-"*60)
    print("Все контакты в базе")
    sorted_contacts = sorted(get_decoded_contacts(), key=lambda contact: contact["name"])
    for contact in sorted_contacts:
        show_contact(contact)

def process_menu(user_input: str):
    full_validate(user_input)
    match user_input:
        case "1":
            add_contact()
        case "2":
            find_contact(False)
        case "3":
            remove_contact()
        case "4":
            update_contact()
        case "5":
            show_contacts()
        case "6":
            exit_app()
        case _:
            print()
            print("Данного пункта нет в меню")


def menu():
    while True:
        print("-" * 60)
        print()
        print("1. Добавить контакт")
        print("2. Найти контакт")
        print("3. Удалить контакт")
        print("4. Обновить контакт")
        print("5. Просмотреть контакты")
        print("6. Выйти")
        user_input = input("Введите действие: ")
        process_menu(user_input)

# Запуск приложения
print("Добро пожаловать в телефонную книгу")
print("Note: Для выхода вы всегда можете прописать exit в любом месте")
menu()
