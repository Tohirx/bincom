def fibonacci(n, a=0, b=1, total=0, count=0):
    # Base case: stop when we've processed 50 numbers
    if count == n:
        return total
    
    # Add current fibonacci number to total, then recurse
    return fibonacci(n, b, a + b, total + a, count + 1)


result = fibonacci(50)
print(f"Sum of first 50 Fibonacci numbers: {result}")