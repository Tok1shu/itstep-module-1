# dict contacts

contacts = [
    {
        "number":"420123123123",
        "name":"Yaroslav",
        "email":"yaroslav@gmail.com"
    },
    {
        "number":"420123123124",
        "name":"Alex",
        "email":"alex@gmail.com"
    }
]

with open('contacts-v1.txt', 'w') as f:
    f.write(str(contacts))

def get_contacts():
    with open('contacts-v1.txt', 'r') as f:
        return f.read()

contacts = eval(get_contacts()) # в идеале бы ast.literal_eval

new_contact = {
    "number":"420123123125",
    "name":"Alice",
    "email":"alice@gmail.com"
}

with open('contacts-v1.txt', 'w') as f:
    contacts.append(new_contact)
    f.write(str(contacts))

