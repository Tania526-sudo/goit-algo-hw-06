import pytest
from src.address_book import AddressBook, Record, Phone, Name

def test_address_book_add_find_delete():
    book = AddressBook()
    rec = Record("John")
    rec.add_phone("1234567890")
    book.add_record(rec)

    assert isinstance(book.find("John"), Record)
    assert book.delete("John") is True
    assert book.find("John") is None
    assert book.delete("John") is False  # повторне видалення

def test_record_phone_ops():
    rec = Record("Jane")
    p1 = rec.add_phone("1112223333")
    rec.add_phone("9998887777")

    assert rec.find_phone("1112223333") is p1
    assert rec.remove_phone("0000000000") is False
    assert rec.remove_phone("9998887777") is True

    rec.edit_phone("1112223333", "0001112222")
    assert rec.find_phone("0001112222") is not None

def test_phone_validation():
    with pytest.raises(ValueError):
        Record("A").add_phone("12345")       # замало цифр
    with pytest.raises(ValueError):
        Record("A").add_phone("12345678901") # забагато цифр
    with pytest.raises(ValueError):
        Record("A").add_phone("123-456-789") # не тільки цифри

def test_name_validation():
    with pytest.raises(ValueError):
        Record("")  # порожнє ім'я
