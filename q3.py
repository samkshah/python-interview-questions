# Below are low complexity questions. It is expected that you will be able to solve these questions in 10-15 minutes.
# Fix below codes to make them work as expected.
 
# Question 1: Create sum of numbers provided in input arguments
# - Input: a list of integers
# - Output: a single integer which is the sum of all numbers in the input list
# - Example: sum_numbers([1, 2, 3, 4, 5]) => 15

def sum_numbers(nums):
    total = 0
    for num in nums:
        total = num
    return total


# print result - Expected output is 15
print(sum_numbers([1, 2, 3, 4, 5]))

