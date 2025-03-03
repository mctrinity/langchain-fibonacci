# fibonacci.py

def generate_fibonacci_sequence(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]

    fibonacci_sequence = [0, 1]
    for i in range(2, n):
        next_num = fibonacci_sequence[i-1] + fibonacci_sequence[i-2]
        fibonacci_sequence.append(next_num)

    return fibonacci_sequence
