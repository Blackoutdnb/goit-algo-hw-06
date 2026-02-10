from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not isinstance(value, str):
            raise ValueError        
        if not (len(value) == 10 and value.isdigit()):
            raise ValueError   
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone_value):
        phone = Phone(phone_value)
        self.phones.append(phone)

    def find_phone(self, phone_value):
        for phone in self.phones:
            if phone.value == phone_value:
                return phone
        return None

    def remove_phone(self, phone_value):
        found_phone = self.find_phone(phone_value)
        if found_phone is None:
            raise ValueError("Phone not found")
        
        self.phones.remove(found_phone)
        return found_phone
    
    def edit_phone(self, old_number, new_number):
        old_phone = self.find_phone(old_number)
        if old_phone is None:
            raise ValueError("Phone not found") 
        
        new_phone = Phone(new_number)
        phone_index = self.phones.index(old_phone)
        self.phones[phone_index] = new_phone
        return new_phone
    
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(phone.value for phone in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)
    
    def delete(self, name):
        return self.data.pop(name, None)
    
    def __str__(self):
        lines = []
        for record in self.data.values():
            name = record.name.value
            phones = ", ".join(phone.value for phone in record.phones)
            lines.append(f"{name}: {phones}")
        return "\n".join(lines)

def parse_input(user_input):
    command, *args = user_input.split()
    command = command.lower()
    return command, args

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Enter user name"
        except KeyError:
            return "Contact not found"
    return inner

@input_error
def add_contact(args, contacts):
    name, phone = args
    contacts[name] = phone
    return "Contact added."

@input_error
def change_contact(args, contacts):
    name, phone = args
    _ = contacts[name]
    contacts[name] = phone
    return "Contact updated."

@input_error    
def show_phone (args, contacts):
    name = args[0]
    return contacts[name]

@input_error
def show_all_contacts(contacts):
    if not contacts:
        return "No contacts."
    else:
        lines = []
        for name, phone in contacts.items():
            lines.append(f"{name}: {phone}")
        return "\n".join(lines)

def main():
    contacts = {}

    while True:
        user_input = input("").strip()
        if not user_input: continue
        command, args = parse_input(user_input)

        if command in ("exit", "close"):
            print("Good bye!")
            break
        elif command == "hello":
            print("How can i help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all_contacts(contacts))
        else:
            print("Invalid command")

if __name__ == "__main__":
    main()