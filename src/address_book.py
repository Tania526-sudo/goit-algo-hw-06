from __future__ import annotations

import re
from collections import UserDict
from typing import List, Optional


class Field:
    """Базове поле запису. Зберігає значення у .value з можливістю перевизначення валідації."""

    def __init__(self, value):
        self._value = None
        self.value = value  # використовує setter

    def __str__(self) -> str:
        return str(self.value)

    # даємо нащадкам можливість перевизначати валідацію
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


class Name(Field):
    """Обов'язкове поле — ім'я контакту."""

    @Field.value.setter  # type: ignore[misc]
    def value(self, new_value: str):
        if not isinstance(new_value, str) or not new_value.strip():
            raise ValueError("Name must be a non-empty string.")
        self._value = new_value.strip()


class Phone(Field):
    """Поле з валідацією: рівно 10 цифр."""

    _PATTERN = re.compile(r"^\d{10}$")

    @Field.value.setter  # type: ignore[misc]
    def value(self, new_value: str):
        if isinstance(new_value, int):
            new_value = str(new_value)
        if not isinstance(new_value, str):
            raise ValueError("Phone must be a string of 10 digits.")
        s = new_value.strip()
        if not self._PATTERN.fullmatch(s):
            raise ValueError("Phone must contain exactly 10 digits.")
        self._value = s


class Record:
    """Запис контакту: ім'я (Name) + набір телефонів (список Phone)."""

    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: List[Phone] = []

    # --- Вимоги по функціоналу ---

    def add_phone(self, phone: str) -> Phone:
        """Додати телефон (з валідацією). Повертає створений об'єкт Phone."""
        p = Phone(phone)
        self.phones.append(p)
        return p

    def remove_phone(self, phone: str) -> bool:
        """Видалити телефон. Повертає True, якщо знайдено і видалено, інакше False."""
        target = self.find_phone(phone)
        if target:
            self.phones.remove(target)
            return True
        return False

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        """
        Замінити існуючий телефон на новий.
        Кидає ValueError, якщо старого номера не знайдено або новий невалідний.
        """
        target = self.find_phone(old_phone)
        if not target:
            raise ValueError("Old phone number not found.")
        target.value = new_phone  # валідація відпрацює у setter Phone.value

    def find_phone(self, phone: str) -> Optional[Phone]:
        """Знайти телефон у записі. Повертає Phone або None."""
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self) -> str:
        phones_str = "; ".join(p.value for p in self.phones) if self.phones else ""
        return f"Contact name: {self.name.value}, phones: {phones_str}"


class AddressBook(UserDict):
    """
    Адресна книга. Зберігає записи Record у self.data як:
      ключ   -> record.name.value
      значення -> Record
    """

    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
        return self.data.get(name)

    def delete(self, name: str) -> bool:
        """Видаляє запис за ім'ям. Повертає True, якщо існував і був видалений."""
        return self.data.pop(name, None) is not None

    def __str__(self) -> str:
        if not self.data:
            return "AddressBook is empty."
        
        lines = [str(self.data[key]) for key in sorted(self.data.keys())]
        return "\n".join(lines)
