start_contacts = "Yaroslav,420123123123,yaroslav@gmail.com\nAlex,420123123124,alex@gmail.com\n"

with open("contacts-v2.txt", "w") as file:
    file.write(start_contacts)

new_contact = "Alice,420123123125,alice@gmail.com\n"

with open("contacts-v2.txt", "a") as file:
    file.write(new_contact)