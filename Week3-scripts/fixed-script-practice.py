import json
import os
 
 
def calculate_average(numbers):
    # FIX: guard against an empty list before dividing, and raise a
    # clear error instead of letting ZeroDivisionError happen silently.
    if not numbers:
        raise ValueError("Cannot calculate average of an empty list")
    return sum(numbers) / len(numbers)
 
 
def get_user_by_id(users, user_id):
    # FIX: check bounds first and return None (or raise a clear error)
    # instead of letting an IndexError crash the whole program.
    if 0 <= user_id < len(users):
        return users[user_id]
    return None
 
 
def load_config(filepath):
    # FIX: use a 'with' block so the file is always closed automatically,
    # and catch the specific error so the caller gets a useful message
    # instead of a raw traceback.
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Config file not found: {filepath}")
    with open(filepath, "r") as f:
        return json.load(f)
 
 
def build_greeting(name, age):
    # FIX: convert age to a string before concatenating, or better,
    # use an f-string which handles type conversion automatically.
    return f"Hello {name}, you are {age} years old."
 
 
def find_duplicates(items):
    # FIX: check membership in 'duplicates' or a separate 'checked' set
    # BEFORE adding to 'seen', not after — the original logic added an
    # item to 'seen' and then immediately checked if it was in 'seen',
    # which is always true.
    seen = set()
    duplicates = set()
    for item in items:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
    return list(duplicates)
 
 
if __name__ == "__main__":
    try:
        print(calculate_average([1, 2, 3]))
        print(calculate_average([]))
    except ValueError as e:
        print(f"Handled error: {e}")
 
    print(get_user_by_id(["Alice", "Bob", "Charlie"], 3))  # now returns None, no crash
 
    try:
        print(load_config("does_not_exist.json"))
    except FileNotFoundError as e:
        print(f"Handled error: {e}")
 
    print(build_greeting("Sam", 22))
    print(find_duplicates([1, 2, 2, 3, 3, 3]))
 