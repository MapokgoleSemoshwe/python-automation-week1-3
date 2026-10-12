def check_password_strength(password):
    """Check the strength of a password."""

    score = 0
    feedback = []

    # Check password length
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Use at least 8 characters.")

    # Check for uppercase letters
    if any(character.isupper() for character in password):
        score += 1
    else:
        feedback.append("Add at least one uppercase letter.")

    # Check for lowercase letters
    if any(character.islower() for character in password):
        score += 1
    else:
        feedback.append("Add at least one lowercase letter.")

    # Check for numbers
    if any(character.isdigit() for character in password):
        score += 1
    else:
        feedback.append("Add at least one number.")

    # Check for special characters
    special_characters = "!@#$%^&*()-_=+[]{};:,.<>?/"

    if any(character in special_characters for character in password):
        score += 1
    else:
        feedback.append("Add at least one special character.")

    # Determine password strength
    if score == 5:
        strength = "Very Strong"
    elif score >= 4:
        strength = "Strong"
    elif score >= 3:
        strength = "Moderate"
    else:
        strength = "Weak"

    return strength, feedback


try:
    password = input("Enter a password to check: ")

    strength, feedback = check_password_strength(password)

    print("\nPassword Strength:", strength)

    if feedback:
        print("\nSuggestions:")
        for suggestion in feedback:
            print("-", suggestion)

except Exception as error:
    print(f"An error occurred: {error}")