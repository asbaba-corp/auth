import random
import string


def generate_random_string(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    random_string = "".join(random.choice(characters) for _ in range(length))
    return random_string


# Example usage: Generate a random string of length 10
RANDOM_STR = generate_random_string(10)
print(RANDOM_STR)
