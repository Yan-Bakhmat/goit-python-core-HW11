from collections import UserDict
from datetime import datetime, timedelta
import re


class Iterable:
    def __init__(self, N):
        self.current_value = 0
        self.N = N

    def __next__(self):
        if self.current_value < self.N:
            self.current_value += 1
            return self.current_value
        raise StopIteration


class Iterator:
    def __iter__(self, N):
        return Iterable(N)


class AddressBook(UserDict):
    def add_record(self, Record):
        self.update({Record.Name.name: Record})
        return "Done!"

    def show_number(self, Name):
        return self.data[Name.name].Phones.phone

    def show_all(self, N=None):
        self.N = N if N else len(self.data)
        for name, numbers in self.data.items():
            yield f'{name}: {numbers.Phones.phone}'


class Record:
    def __init__(self, Name, Phones=None, Birthday=None):
        self.Name = Name
        self.Phones = Phones
        self.Birthday = Birthday

    def add_phone(self, Phone):
        self.Phones.phone = list(set(self.Phones.phone) | set(Phone.phone))
        return "Done!"

    def change_phone(self, Phone):
        self.Phones = Phone
        return "Done!"

    def delite_phone(self, Phone):
        self.Phones.phone = list(set(self.Phones.phone) - set(Phone.phone))
        return "Done!"

    def days_to_birthday(self):
        if self.Birthday:
            current_datetime = datetime.now()
        else:
            return "The birthsay date is unknown."


class Field:
    def __init__(self, name_and_number):
        name_and_number = name_and_number.split(' ')
        self.name = name_and_number[0]
        self.phone = name_and_number[1:]


class Name(Field):
    def __init__(self, name):
        super().__init__(name)


class Phone(Field):
    def __init__(self, phone):
        super().__init__(phone)


class Birthday(Field):
    def __init__(self, birthday):
        super().__init__(birthday)


CONTACTS = AddressBook()


def hello():
    return 'How can I help you?'


def close():
    return "Good bye!"


def input_error(func):
    def inner():
        flag = True
        while flag:
            try:
                result = func()
                flag = False
            except IndexError:
                print('Enter the name and numbers separated by a space.')
            except ValueError:
                print('I have no idea how you did it, try again.')
            except KeyError:
                print("The contact is missing.")
        return result
    return inner


@ input_error
def main():
    bot_status = True
    while bot_status:
        command = input('Enter the command: ').lower()
        if command == 'hello':
            print(hello())
        elif 'add' in command:
            command = command.removeprefix('add ')
            if Name(command).name in CONTACTS.data:
                print(CONTACTS.data[Name(command).name].add_phone(
                    Phone(command)))
            else:
                print(CONTACTS.add_record(Record(Name(command), Phone(command))))
        elif "change" in command:
            command = command.removeprefix('change ')
            print(CONTACTS.data[Name(command).name].change_phone(
                Phone(command)))
        elif "delite" in command:
            command = command.removeprefix('delite ')
            print(CONTACTS.data[Name(command).name].delite_phone(
                Phone(command)))
        elif "phone" in command:
            command = command.removeprefix("phone ")
            print(CONTACTS.show_number(Name(command)))
        elif command == "show all":
            if CONTACTS:
                for contact in CONTACTS.show_all():
                    print(contact)
            else:
                print('The contact list is empty.')
        elif command in ("good bye", "bye", "close", "exit"):
            print(close())
            bot_status = False
        else:
            print("Enter correct command, please.")


if __name__ == '__main__':
    main()
