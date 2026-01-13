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

def validate_phone(phone: str):
    if len(phone) == 12:
        result = False

    try: result = int(phone)
    except ValueError: result = False

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

def show_contact(contact: dict):
    print()
    print("Имя: ", contact["name"])
    print("Номер телефона: ", contact["phone"])
    print("Электронная почта: ", contact["email"])
    print()

# Остальное


# old_get_input

def get_input(message: str, *validators):
    while True:
        user_input = input(message)
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

# TODO: Если несоклько Вась в списке показать их всех, вынести логику куда-то отдельно чтоб переиспользовать
def find_contact():
    print("-"*60)
    print("Поисковик контактов :3")

    while True:
        print("Дабы найти контакт введите:")
        print("- Точное имя")
        print("- Номер телефона (начиная с +)")
        contact_to_find = get_input("> ", prepare_value, full_validate)
        raw_contacts = get_contacts()

        found = None
        search_query = "name"

        if contact_to_find.startswith("+"):
            search_query = "phone"
            contact_to_find = contact_to_find[1:]

        for contact in raw_contacts:
            contact = decode_contact(contact)
            if contact[search_query] == contact_to_find:
                show_contact(contact)
                found = contact
                break

        if found:
            return found
        else:
            print("❌ Контакт не найден")



def remove_contact():
    print("-"*60)
    print("Удаление аккаунта")
    raw_contacts = get_contacts()
    contact = find_contact()
    raw_contacts.remove(f"{contact['name']},{contact['phone']},{contact['email']}\n")
    with open("contacts.txt", "w") as db:
        db.writelines(raw_contacts)
    print("✅ Контакт удалён!")
    return contact

def update_contact():
    print("-"*60)
    print("Обновление аккаунта")
    contact = find_contact()
    print("Если не хотите менять поле просто впишите пустую строку")

    while True:
        name = get_input("Введите имя: ", prepare_value, is_content_has_enter)
        phone = get_input("Введите номер телефона (12 цифр): +", prepare_value, validate_phone, is_content_has_enter)
        email = get_input("Введите электронную почту: ", prepare_value, validate_email, is_content_has_enter)

        if not check_unique_contact(phone, email):
            print("Такой контакт уже существует, попробуйте создать другой")
            break

        contact["name"] = name if name else contact["name"]
        contact["phone"] = phone if phone else contact["phone"]
        contact["email"] = email if email else contact["email"]

        with open("contacts.txt", "a") as db:
            to_write = f"{contact["name"]},{contact["phone"]},{contact["email"]}\n"
            db.write(to_write)


def show_contacts():
    print()

# TODO: Снести рекурсию (menu -> process_menu -> menu -> ...)
def process_menu(user_input: str):
    full_validate(user_input)
    match user_input:
        case "1":
            add_contact()
            menu()
        case "2":
            find_contact()
            menu()
        case "3":
            remove_contact()
            menu()
        case "4":
            update_contact()
        case "5":
            show_contacts()
        case "6":
            exit_app()
        case _:
            print()
            print("Данного пункта нет в меню")
            menu()


def menu():
    print("-"*60)
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
