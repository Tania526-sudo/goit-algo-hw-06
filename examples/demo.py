from src.address_book import AddressBook, Record

# Create a new address book
book = AddressBook()

# Create a record for John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Add John's record to the address book
book.add_record(john_record)

# Create and add a new record for Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Print all records in the address book
print(book)

# Find and edit John's phone number
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Contact name: John, phones: 1112223333; 5555555555

# Search for a specific phone number in John's record
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # John: 5555555555

# Delete Jane's record
book.delete("Jane")

