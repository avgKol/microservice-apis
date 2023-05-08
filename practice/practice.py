# Defining a function to find the factorial of a number
from functools import reduce
import time


def factorial(num):
    if num == 0:                     # If num is 0, return 1 as factorial of 0 is 1
        return 1
    else:
        return num * factorial(num-1)     # Recursive call to find the factorial of given number

# Defining a function to find the nth term in fibonacci series
def fibonacci(num):
    if num <= 1:                    # If num is less than or equal to 1, return num
        return num
    else:
        return(fibonacci(num-1) + fibonacci(num-2))   # Recursive call to calculate the nth term in fibonacci series

# Defining a function to check whether a number is prime or not
def is_prime(num):
    if num > 1:                 # If num is greater than 1, check for divisibility with numbers from 2 to num-1
        for i in range(2,num):
            if (num % i) == 0:  # If num is divisible by any number between 2 and num-1, return False
                return False
                break
        else:
            return True        # If num is not divisible by any number between 2 and num-1, return True
    else:
        return False           # Return False if num is less than or equal to 1

# Defining a function to find the largest prime factor of a given number
def largest_prime(n):
    if n <= 1:                  # If n is less than or equal to 1, return None
        return None
    largest_prime = n           # Assigning n to largest_prime initially
    for i in range(2, int(n ** 0.5) + 1):   # Checking for divisibility with numbers from 2 to square root of n
        if n % i == 0:
            largest_prime = i    # Assigning the divisor as largest_prime
            break
    return largest_prime

# Defining a function to print all the prime numbers less than a given number
def print_primes(n):
    for i in range(2, n):           # Checking for each number from 2 to n
        if is_prime(i):            # Calling is_prime() function to check if number is prime or not
            print(i)               # If the number is prime, print it

# Defining a function to find all factors of a given number
def factors(n):
    factors = []                   # Initializing an empty list to store factors
    for i in range(1, int(n ** 0.5) + 1):  # Checking for factors till square root of n
        if n % i == 0:
            factors.append(i)      # Adding the divisor as factor
            if i * i != n:        # If divisor is not equal to square root of n, add the quotient as factor as well
                factors.append(n // i)
    return factors

# Defining a function to find the greatest common divisor of two numbers
def gcd(a, b):
    if b == 0:
        return a                # If b is zero, return a as gcd
    else:
        return gcd(b, a % b)    # Recursive call with a and remainder of a and b as arguments

# Defining a function to find the least common multiple of two numbers
def lcm(a, b):
    return a * b // gcd(a, b)    # Calculate lcm using gcd function and return the result



def gen_func():
    for i in range(10):
        yield i

def gen_func2():
    yield from range(10)

def gen_func3():
    yield from gen_func2()

def gen_func4():
    yield from gen_func3()

def gen_func5():
    yield from gen_func4()

# print   (next(gen_func()))
# print   (list(gen_func2()))
# print   (list(gen_func3()))
# print   (list(gen_func4()))
# print   (list(gen_func5()))    



def negate_all(nums):
    print ("negate_all Start")
    for num in nums:
        print ("this number is", -num)
        yield -num
    print ("negate_all End")

def is_odd(x):
    return x % 2 == 1

negatives= negate_all([1, 2, 3, 4, 5])
print (negatives)
# loop 10 times
# for i in range(10):
#     print (next(negatives))

squares = [n**2 for n in range(10)]
print (squares)
print( list(map(factorial,[1,2,3])))
print (list(filter(is_odd, [1,2,3,4,5,6,7,8,9,10])))
print (reduce(lambda x,y: x+y, [1,2,3,4,5,6,7,8,9,10]))
 # get current time
start_time = time.perf_counter()
print(time.strftime("%H:%M:%S", time.localtime()))

# run code
is_prime(418353193)

# get current time
end_time = time.perf_counter()
print(time.strftime("%H:%M:%S", time.localtime(end_time)))

# calculate the elapsed time
elapsed_time = end_time - start_time
print("Elapsed time:", elapsed_time)

numa = int(input("Enter a number: "))
numb = int(input("Enter another number: "))
print("The factorial of", numa, "is", factorial(numa))
print ("The fibonacci of", numa, "is", fibonacci(numa))
print ("The number", numa, "is prime:", is_prime(numa))
print ("The largest prime of", numa, "is", largest_prime(numa))
print ("The prime numbers less than", numa, "are:", print_primes(numa) )
print ("The factors of", numa, "are:", factors(numa) )
print ("The greatest common divisor of", numa, "and", numb, "is", gcd(numa, numb))

