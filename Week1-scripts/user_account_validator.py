def validate_accounts(accounts):
    """Validate a list of user accounts."""

    valid_accounts = []
    invalid_accounts = []

    for account in accounts:

        # Remove unnecessary spaces
        account = account.strip()

        # Check that the username contains a value
        if not account:
            invalid_accounts.append((account, "Username is empty"))
            continue

        # Check username length
        if len(account) < 3:
            invalid_accounts.append((account, "Username is too short"))
            continue

        # Check that the username contains only letters and numbers
        if not account.isalnum():
            invalid_accounts.append(
                (account, "Username contains invalid characters")
            )
            continue

        # If all checks pass
        valid_accounts.append(account)

    return valid_accounts, invalid_accounts


# List of user accounts
user_accounts = [
    "john123",
    "mary",
    "admin01",
    "ab",
    "user@123",
    "  david2026  ",
    "",
    "support01"
]


try:
    valid, invalid = validate_accounts(user_accounts)

    print("=" * 40)
    print("       USER ACCOUNT VALIDATION")
    print("=" * 40)

    print("\nValid Accounts:")

    for account in valid:
        print(f"✓ {account}")

    print("\nInvalid Accounts:")

    for account, reason in invalid:
        print(f"✗ {account} - {reason}")

    print("\nSummary")
    print("-" * 40)
    print(f"Total accounts : {len(user_accounts)}")
    print(f"Valid accounts : {len(valid)}")
    print(f"Invalid accounts: {len(invalid)}")

except Exception as error:
    print(f"An error occurred: {error}")