from __future__ import annotations

import re
from collections import UserDict
from typing import List, Optional


class Field:
    """Base field class. Stores the value in .value with optional validation override."""

    def __init__(self, value):
        self._value = None
        self.value = value  # uses the setter

    def __str__(self) -> str:
        return str(self.value)

    # Allow descendants to override validation
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


class Name(Field):
    """Required field – contact name."""

    @Field.value.setter  # type: ignore[misc]
    def value(self, new_value: str):
        if not isinstance(new_value, str) or not new_value.strip():
            raise ValueError("Name must be a non-empty string.")
        self._value = new_value.strip()


class Phone(Field):
    """Field with validation: exactly 10 digits."""

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
    """Contact record: name (Name) + a list of phones (Phone objects)."""

    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: List[Phone] = []

    # --- Required functionality ---

    def add_phone(self, phone: str) -> Phone:
        """Add a phone (with validation). Returns the created Phone object."""
        p = Phone(phone)
        self.phones.append(p)
        return p

    def remove_phone(self, phone: str) -> bool:
        """Remove a phone. Returns True if found and removed, otherwise False."""
        target = self.find_phone(phone)
        if target:
            self.phones.remove(target)
            return True
        return False

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        """
        Replace an existing phone with a new one.
        Raises ValueError if the old number is not found or the new one is invalid.
        """
        target = self.find_phone(old_phone)
        if not target:
            raise ValueError("Old phone number not found.")
        target.value = new_phone  # validation is handled in the Phone.value setter

    def find_phone(self, phone: str) -> Optional[Phone]:
        """Find a phone in the record. Returns Phone or None."""
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self) -> str:
        phones_str = "; ".join(p.value for p in self.phones) if self.phones else ""
        return f"Contact name: {self.name.value}, phones: {phones_str}"


class AddressBook(UserDict):
    """
    Address book. Stores Record objects in self.data as:
      key     -> record.name.value
      value   -> Record
    """

    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
        return self.data.get(name)

    def delete(self, name: str) -> bool:
        """Deletes a record by name. Returns True if it existed and was removed."""
        return self.data.pop(name, None) is not None

    def __str__(self) -> str:
        if not self.data:
            return "AddressBook is empty."
        
        lines = [str(self.data[key]) for key in sorted(self.data.keys())]
        return "\n".join(lines)

