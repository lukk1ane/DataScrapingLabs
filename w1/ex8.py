a = [i for i in range(1, 50)]
b = [i for i in a if i % 2 == 0]
c = [i*i for i in a if i % 2 == 1]
d = [i for i in a if i % 5 == 0]

print(f"""numbers 1 to 50: {str(a)}
even numbers: {str(b)}
squares of odd numbers: {str(c)}
multiples of 5 {str(d)}
""")