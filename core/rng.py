import random

randomsnums = []

def set_seed(seed):
    random.seed(seed)
    print(f"Random seed set to: {seed}")
    
def get_random_number():
    number = random.randint(1, 1000)
    return number

def main(count):
    set_seed(42)
    for _ in range(count):
        randomsnums.append(get_random_number())
    return randomsnums
