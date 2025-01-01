from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value: str):
        if self.valid(value):
            self.value = value
        else:
            raise ValueError
    
    def valid(self, value):
        return True

    def __str__(self):
        return str(self.value)

class Name(Field):
    # реалізація класу
		pass

class Phone(Field):
    def valid(self, value):
        return len(value) == 10 and value.isdigit()
    
class Birthday(Field):
    def __init__(self, value):
        try:
            value = datetime.strptime(value, "%d.%m.%Y").date()
            super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
            
    

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def find_phone(self, phone_number):
        for ph in self.phones:
            if ph.value == phone_number:
                return ph
        return None
    
    def remove_phone(self, phone_number):
        phone = self.find_phone(phone_number)
        if phone is None:
            raise ValueError
        self.phones.remove(phone)

    def edit_phone(self, old_number, new_number):
        phone = self.find_phone(old_number)
        if phone is None:
            raise ValueError
        self.add_phone(new_number)
        self.remove_phone(old_number)

    def add_birthday(self, birhday):
        self.birthday = Birthday(birhday)
        

             
    def __str__(self):
        return f"Contact name: {str(self.name)}, phones: {'; '.join(str(p) for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)
    
    def delete(self, name):
        del self.data[name]

    def get_upcoming_birthdays(self):
        prepared_users = []
        today = datetime.today().date()
        for user in self.data.values():
                birthday = user.birthday.value
                birthday = birthday.replace(year=today.year)
                if birthday < today:
                        birthday = birthday.replace(year=today.year+1)
                diference = (birthday - today).days
                if diference < 7:
                        week_day = birthday.strftime("%A")
                        if week_day == "Saturday" or week_day == "Sunday":
                             birthday += timedelta(days=7-birthday.weekday())
                                                   
                        prepared_users.append({"name": str(user.name), "congratulation_date": birthday})
        return prepared_users

    def __str__(self):
        return f"{'\n'.join(str(p) for p in self.data.values())}"

if __name__ == "__main__":

# Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: John: 5555555555

    # Видалення запису Jane
    book.delete("Jane")