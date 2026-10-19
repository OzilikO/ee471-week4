from custom_classes import Calculator

# 1. Create the calculator
my_calc = Calculator()

# 2. Perform a series of operations
print(my_calc.add(10))       # Output: 10 (0 + 10)
print(my_calc.multiply(5))   # Output: 50 (10 * 5)
print(my_calc.sub(8))        # Output: 42 (50 - 8)
print(my_calc.divide(2))     # Output: 21.0 (42 / 2)

# 3. Reset to 0
print(my_calc.clear())       # Output: 0