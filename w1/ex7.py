def fibonacci(n):
    x = 1
    x_1 = 1
    while n > 0:
        yield x_1
        n-=1
        temp = x
        x = x + x_1
        x_1 = temp

for i in fibonacci(6):
    print(i)
