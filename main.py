import re
import json

def readContacts():
    with open('contacts.txt') as f:
        lines = f.readlines()
        updated_lines = []
        for l in lines:
            updated_lines.append(l.strip())
        return updated_lines

def ValidName(name):
    if re.match(r'^[A-Z][a-z]+ [A-Z][a-z]+$', name):
        return True
    else:
        return False

def validEmail(email):
    if re.match(r"^\w+(?:[.-]\w+)*@(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}$",email):
        return True
    else:
        return False

def validPhone(number):
    if re.match(r"^\+38[157] 6[0-9] [0-9]{3} [0-9]{4}$",number):
        return True
    else:
        return False

def filterContacts():
    contacts = readContacts()
    list_of_correct_contacts = []
    row_counter = 0
    for contact in contacts:
        row_counter += 1
        part = contact.split(';')
        if len(part) != 3:
            with open('wrongFormat.log', 'a') as f:
                f.write('Not a suitable row!\n')
            continue
        name = part[0]
        mail = part[1]
        phone = part[2]
        if ValidName(name) and validEmail(mail) and validPhone(phone):
            correct_contacts = {}
            correct_contacts['name'] = name
            correct_contacts['mail'] = mail
            correct_contacts['phone'] = phone
            if phone[0:4] == '+381':
                correct_contacts['country'] = 'Serbia'
            elif phone[0:4] == '+385':
                correct_contacts['country'] = 'Croatia'
            else:
                correct_contacts['country'] = 'BiH'
            list_of_correct_contacts.append(correct_contacts)
        else:
            added_message = f"Row:{row_counter}"
            if not ValidName(name):
                added_message += " wrong name|"
            if not validEmail(mail):
                added_message += " wrong email|"
            if not validPhone(phone):
                added_message += " wrong phone|"
            with open('wrongFormat.log', 'a') as f:
                f.write(added_message + contact + '\n')
    with open('correctFormat.json', 'w') as f:
        json.dump(list_of_correct_contacts, f,indent=4,ensure_ascii=False)
    bubble()

def GetValidContacts():
    try:
        with open("correctFormat.json", encoding="utf-8") as f:
            contacts = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    return contacts if isinstance(contacts, list) else []

def GetFaultyContacts():
    with open('wrongFormat.log') as f:
        contacts = f.readlines()
    updated_contacts = []
    for contact in contacts:
        updated_contacts.append(contact.strip())
    return updated_contacts if updated_contacts else []

def bubble():
    with open('correctFormat.json') as f:
        contacts = json.load(f)
    for i in range(len(contacts), 0, -1):
        status = False
        for j in range(i - 1):
            if contacts[j]['name'] > contacts[j + 1]['name']:
                contacts[j], contacts[j + 1] = contacts[j + 1], contacts[j]
                status = True
        if not status:
            break
    return contacts

def get_contacts_with_surname():
    sur = input("Enter surname: ")
    possible_answers = []
    for contact in GetValidContacts():
        if re.match(rf"[A-za-z]+ {sur}", contact['name']):
            possible_answers.append(contact)
    return "No such surname" if not possible_answers else possible_answers

def main():
    while True:
        print("1: Filter Contacts")
        print("2: Get Valid Formated Contacts")
        print("3: Get Wrong Formated Contacts")
        print("4: Search by surname")
        print("0: Exit")
        x = int(input("Enter your choice: "))
        if x == 1:
            filterContacts()
        elif x == 2:
            print(GetValidContacts())
        elif x == 3:
            print(GetFaultyContacts())
        elif x == 4:
            print(get_contacts_with_surname())
        else:
            correct = GetValidContacts()
            faulty = GetFaultyContacts()
            print(f"Number of all contacts: {len(correct) + len(faulty)}|Number of correct contacts: {len(correct)}|Number of faulty contacts: {len(faulty)}")
            countries = {'Serbia':0, 'Croatia':0, 'BiH':0}
            for cor in correct:
                countries[cor['country']] += 1
            print(countries)
            return



main()