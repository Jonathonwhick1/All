def get_card_details(card_number: str) -> dict:
    """Identify the card type, bank, and country based on the first few digits (BIN/IIN)."""
    card_number = card_number.replace(" ", "")  # Clean spaces from input
    bin_number = card_number[:6]  # First 6 digits for identifying issuer

    # Simple BIN mapping (you can extend this as needed or use a BIN database)
    bin_data = {
        '4': {'type': 'Visa', 'bank': 'Various Issuers', 'country': 'Global', 'vbv': True},
        '51': {'type': 'MasterCard', 'bank': 'Various Issuers', 'country': 'Global', 'vbv': False},
        '52': {'type': 'MasterCard', 'bank': 'Various Issuers', 'country': 'Global', 'vbv': False},
        '53': {'type': 'MasterCard', 'bank': 'Various Issuers', 'country': 'Global', 'vbv': False},
        '54': {'type': 'MasterCard', 'bank': 'Various Issuers', 'country': 'Global', 'vbv': False},
        '55': {'type': 'MasterCard', 'bank': 'Various Issuers', 'country': 'Global', 'vbv': False},
        '34': {'type': 'American Express', 'bank': 'Amex', 'country': 'Global', 'vbv': False},
        '37': {'type': 'American Express', 'bank': 'Amex', 'country': 'Global', 'vbv': False},
        '6011': {'type': 'Discover', 'bank': 'Discover', 'country': 'USA', 'vbv': False},
        '65': {'type': 'Discover', 'bank': 'Discover', 'country': 'USA', 'vbv': False},
        '622': {'type': 'China UnionPay', 'bank': 'Various Issuers', 'country': 'China', 'vbv': False},
        '35': {'type': 'JCB', 'bank': 'JCB', 'country': 'Japan', 'vbv': False},
        '36': {'type': 'Diners Club', 'bank': 'Diners Club International', 'country': 'Global', 'vbv': False},
        '38': {'type': 'Diners Club', 'bank': 'Diners Club International', 'country': 'Global', 'vbv': False}
    }

    # Try to match first 6, 4, 3, or 1 digits from the card number
    for i in range(6, 0, -1):
        prefix = card_number[:i]
        if prefix in bin_data:
            return bin_data[prefix]

    # If no match found
    return {'type': 'Unknown', 'bank': 'Unknown', 'country': 'Unknown', 'vbv': False}


def luhn_check(card_number: str) -> bool:
    """Check if the card number is valid using the Luhn algorithm."""
    card_number = card_number.replace(" ", "")  # Remove any spaces
    total = 0
    reverse_digits = card_number[::-1]

    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        if i % 2 == 1:  # Double every second digit from the right
            n *= 2
            if n > 9:
                n -= 9
        total += n

    return total % 10 == 0


def check_card(card_number: str):
    """Perform card validation and display details."""
    card_number = card_number.replace(" ", "")  # Clean spaces
    if not card_number.isdigit():
        return "Invalid card number (non-numeric characters detected)."

    # Get card details based on the first few digits (BIN/IIN)
    card_details = get_card_details(card_number)

    # Validate card using Luhn algorithm
    is_valid = luhn_check(card_number)

    # Display the results
    print(f"Card Number: {card_number}")
    print(f"Card Type: {card_details['type']}")
    print(f"Bank Name: {card_details['bank']}")
    print(f"Country: {card_details['country']}")
    print(f"VBV (Verified by Visa) Status: {'Yes' if card_details['vbv'] else 'No'}")
    print(f"Valid Card (Luhn Check): {is_valid}")


# Example usage
# card_number = "4532015112830366"  # Replace with your test card number
# check_card(card_number)