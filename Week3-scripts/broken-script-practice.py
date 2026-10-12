import json
 
 
def calculate_average(numbers):
    # BUG 1: division by len(numbers) crashes if the list is empty
    total = sum(numbers)
    if len(numbers) == 0:
        return 0
    return total / len(numbers)
 
 
def get_user_by_id(users, user_id):
    # BUG 2: off-by-one — list indices start at 0, not 1
    return users[user_id]
 
 
def load_config(filepath):
    # BUG 3: file is never closed, and no error handling for missing file
    f = open(filepath)
    data = json.load(f)
    return data
 
 
def build_greeting(name, age):
    # BUG 4: mixing str and int without converting age to a string
    return "Hello " + name + ", you are " + age + " years old."
 
 
def find_duplicates(items):
    # BUG 5: wrong logic — this always returns an empty list because
    # 'seen' and 'duplicates' both get the same items appended
    seen = []
    duplicates = []
    for item in items:
        seen.append(item)
        if item in seen:
            duplicates.append(item)
    return duplicates
 
 
if __name__ == "__main__":
    print(calculate_average([]))  # triggers BUG 1
    print(get_user_by_id(["Alice", "Bob", "Charlie"], 3))  # triggers BUG 2
    print(load_config("does_not_exist.json"))  # triggers BUG 3
    print(build_greeting("Sam", 22))  # triggers BUG 4
    print(find_duplicates([1, 2, 2, 3, 3, 3]))  # triggers BUG 5 (silent, no crash)
 