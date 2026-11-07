import re

# ASCII digits only. Python's int() and str.isdigit() also accept other
# Unicode digits (e.g. Arabic-Indic or superscript digits), which a fuzzer finds quickly.
WHOLE_NUMBER = re.compile(r'-?[0-9]+')


def to_whole_number(text):
    """Returns text as an int if it is a plain whole number, otherwise None."""
    text = text.strip()
    if not WHOLE_NUMBER.fullmatch(text):
        return None
    try:
        return int(text)
    except ValueError:
        # int() refuses very long digit strings (over 4300 digits by default)
        return None


def mask_card_number(number):
    """
    Hides all but the last four digits of a card number.
    Returns None if the input is not a valid card number.
    """
    if not isinstance(number, str):
        return None
    digits = number.strip().replace(' ', '').replace('-', '')
    # Card numbers are 12 to 19 digits long and contain nothing else
    if not re.fullmatch(r'[0-9]{12,19}', digits):
        return None
    return '*' * 12 + digits[-4:]


def parse_transaction(line):
    """
    Parses 'date,category,amount' into a (category, amount) tuple.
    Returns None if the line is not in that format.
    """
    if not isinstance(line, str):
        return None
    parts = line.split(',')
    if len(parts) != 3:
        return None
    category = parts[1].strip().lower()
    if not category:
        return None
    amount = to_whole_number(parts[2])
    if amount is None:
        return None
    return category, amount


def parse_statement_total(text):
    """
    Reads the amount from a line such as 'Total: 12,500'.
    Returns None if the line has no colon or no valid number after it.
    """
    if not isinstance(text, str) or ':' not in text:
        return None
    amount = text.split(':', 1)[1]
    return to_whole_number(amount.replace(',', ''))


def show(label, result):
    if result is None:
        print(label, "Invalid input")
    else:
        print(label, result)


def main():
    print("==== Running mask_card_number ====")
    value = input("Enter a card number (e.g. 4111 1111 1111 1234): ")
    show("Masked card number:", mask_card_number(value))

    print("\n==== Running parse_transaction ====")
    value = input("Enter a transaction as DATE,CATEGORY,AMOUNT (e.g. 2026-11-05,dining,1550): ")
    show("Category and amount:", parse_transaction(value))

    print("\n==== Running parse_statement_total ====")
    value = input("Enter the statement total line (e.g. Total: 12,500): ")
    show("Statement total:", parse_statement_total(value))

if __name__ == "__main__":
    main()