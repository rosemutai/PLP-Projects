num1 = int(input("Please enter the first number: "))
num2 = int(input("Please enter the second number: "))
mathOperation = input("Please enter an operation of your choice: ")

if mathOperation == '+':
    result = num1 + num2
    print(result)
elif mathOperation == '-':
    result = num1 - num2
    print(result)
elif mathOperation == '*':
    result = num1 * num2
    print(result)
elif mathOperation == '/':
    result = num1 / num2
    print(result)
else:
    print("Please enter a valid number or operation")