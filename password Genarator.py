import secrets
import string


def generate_smart_password(length: int = 16) -> str:
    """
    Generates a cryptographically secure, high-entropy password.
    Guarantees at least one lowercase letter, uppercase letter, digit, and special character.
    """
    if length < 4:
        raise ValueError("Password length must be at least 4 characters.")

    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = string.punctuation

    all_characters = lowercase + uppercase + digits + symbols

    # Guarantee at least one character from each mandatory group
    password_pool = [
        secrets.choice(lowercase),
        secrets.choice(uppercase),
        secrets.choice(digits),
        secrets.choice(symbols)
    ]

    # Fill the remaining length with random characters
    password_pool += [secrets.choice(all_characters) for _ in range(length - 4)]

    # Shuffle the list securely so the mandatory characters are not predictable
    secrets.SystemRandom().shuffle(password_pool)

    return "".join(password_pool)


if __name__ == "__main__":
    generated_password = generate_smart_password(16)
    print(f"Your secure password is: {generated_password}")
