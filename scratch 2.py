# This file was created by Robbie Raiche

# Write a function that takes two arguments and multiplies them togeher
# Use a return statement
# Print is

def multiply(x,y):
    return x*y
def printer(x,y):
    print("I am", str(multiply(x,y)), "ft away from your house and approaching rapidly")

n=0
while n < 10:
    printer(4,5)
    n += 1
# m=0
# while True:
#     printer(4,5)               Alternate way to write it. More abstractible if you want to use the while loop for different lengths..
#     m += 1
#     if m <= 10:
#         break