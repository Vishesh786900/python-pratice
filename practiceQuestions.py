'''1.  Write a script to perform the following three operations on given list
Access the third element of a list
List Length: Print the total number of items
Check if the list is empty
Given Input: numbers = [10, 20, 30, 40, 50]'''

numbers = [10, 20, 30, 40, 50]
print("The third element of the list is: ", numbers[2])
print("The length of the list is: ", len(numbers))
if not numbers:
    print("The list is empty.")
else:
    print("The list is not empty.")
print("---------------------------------")
'''2. Take a given list and modify it through five specific actions:
Change Element: Change the second element of a list to 200 and print the updated list.
Append Element: Add 600 o the end of a list and print the new list.
Insert Element: Insert 300 at the third position (index 2) of a list and print the result.
Remove Element (by value): Remove 600 from the list and print the list.
Remove Element (by index): Remove the element at index 0 from the list print the list.
Given Input: Initial List: [100, 50, 400, 500]'''

initial_list = [100, 50, 400, 500]
print("Initial List: ", initial_list)
initial_list[1] = 200
print("After changing the second element to 200: ", initial_list)
initial_list.append(600)
print("After appending 600 to the list: ", initial_list)
initial_list.insert(2, 300)
print("After inserting 300 at index 2: ", initial_list)
initial_list.remove(600)
print("After removing 600 from the list: ", initial_list)
del initial_list[0]
print("After removing the element at index 0: ", initial_list)

print("---------------------------------")
'''3.  Calculate the total sum of all integers in a list and find the arithmetic mean (average).
Given Input: Numbers: [10, 20, 30, 40, 50]'''

numbers = [10, 20, 30, 40, 50]
total=sum(numbers)
mean=total/len(numbers)
print("The total sum of the list is : ", total)
print("The arithmetic mean (average) of the list is : ", mean)
print("---------------------------------")

'''4. Identify the largest and smallest numerical values within a provided list.
Given Input: Data: [45, 12, 89, 2, 67]'''

data=[45, 12, 89, 2, 67]
print("The largest value in the list is: ", max(data))
print("The smallest value in the list is: ", min(data))

print("---------------------------------")
'''5.  Given a list of integers, iterate through the items and count how many are even and how
many are odd.
Given Input: Numbers: [10, 21, 4, 45, 66, 93, 11]'''

numbers = [10, 21, 4, 45, 66, 93, 11]

even_count = 0
odd_count = 0       

for n in numbers:
    if n % 2 == 0:
        even_count += 1
    else:
        odd_count += 1

print("The number of even numbers in the list is: ", even_count)
print("The number of odd numbers in the list is: ", odd_count)

print("---------------------------------")
'''6.  Write a Python program to create a set, add a new element to it, remove an element
using remove(), and discard an element using discard().
Given Input: fruits = {&quot;apple&quot;, &quot;banana&quot;, &quot;cherry&quot;}'''

fruits = {"apple", "banana", "cherry"}
print("Initial Set: ", fruits)

fruits.add("date")
print("After adding 'date': ", fruits)

fruits.remove("banana")
print("After removing 'banana': ", fruits)

fruits.discard("cherry")
print("After discarding 'cherry': ", fruits)

print("---------------------------------")
'''7. Write a Python program to remove all elements from a set using .clear(), while keeping
the variable itself intact.
Given Input: colors = {&quot;red&quot;, &quot;green&quot;, &quot;blue&quot;}'''

colors={"red", "green", "blue"}
print("Initial Set: ", colors)
colors.clear()
print("After clearing the set: ", colors)

print("---------------------------------")
'''8. Write a Python program to determine how many elements are in a set without using the
built-in len() function.
Given Input: animals = {&quot;cat&quot;, &quot;dog&quot;, &quot;bird&quot;, &quot;fish&quot;}'''

animals={"cat", "dog", "bird", "fish"}
count=0
for animal in range(len(animals)):
    count+=1
print("The number of elements in the set is: ", count)
print("---------------------------------")

'''9. Write a Python program to check whether a set is empty using conditional logic, and print
an appropriate message based on the result.
Given Input: data = set()'''

data=set()
if not data:
    print("The set is empty.")
else:
    print("The set is not empty.")

print("---------------------------------")
'''10. Write a Python program to combine two sets into one, containing all unique elements
from both sets.
Given Input: set_a = {1, 2, 3, 4} and set_b = {3, 4, 5, 6}'''

set_a = {1, 2, 3, 4}
set_b = {3, 4, 5, 6}
combined_set = set_a.union(set_b)
print("The combined set is: ", combined_set)

print("---------------------------------")
'''11. Write a Python program to add a new key-value pair to a dictionary, modify an existing
value, and access a specific key.
Given Input: student = {&quot;name&quot;: &quot;Alice&quot;, &quot;age&quot;: 20, &quot;grade&quot;: &quot;B&quot;}'''

student = {"name": "Alice", "age": 20, "grade": "B"}
student["course"] = "Computer Science"
student["age"] = 21
print("Student Information:")
for key, value in student.items():
    print(f"{key}: {value}")

print("---------------------------------")
'''12. Write a Python program to remove a specific key from a dictionary, retrieve all key-value
pairs, and check whether a given key exists.
Given Input: car = {&quot;brand&quot;: &quot;Toyota&quot;, &quot;model&quot;: &quot;Camry&quot;, &quot;year&quot;: 2022, &quot;color&quot;:
&quot;blue&quot;}'''

car = {"brand": "Toyota", "model": "Camry", "year": 2022, "color": "blue"}
car.pop("color")
print("Car Information:")
for key, value in car.items():
    print(f"{key}: {value}")
if "color" in car:
    print("The key 'color' exists in the dictionary.")
else:
    print("The key 'color' does not exist in the dictionary.")

print("---------------------------------")

'''13. Write a Python program to create a dictionary by mapping two equal-length lists, one
containing keys and the other containing values.
Given Input: keys = [&quot;name&quot;, &quot;age&quot;, &quot;city&quot;] and values = [&quot;Bob&quot;, 25, &quot;London&quot;]'''

keys=["name", "age", "city"]
values=["Bob", 25, "London"]
student_dict = dict(zip(keys, values))
print("Student Dictionary:", student_dict)

print("---------------------------------")
'''14. Write a Python program to remove all items from a dictionary while keeping the
dictionary object itself intact.
Given Input: inventory = {&quot;apples&quot;: 10, &quot;bananas&quot;: 5, &quot;oranges&quot;: 8}'''

inventory = {"apples": 10, "bananas": 5, "oranges": 8}
inventory.clear()
print("After clearing the dictionary: ", inventory) 
print("---------------------------------")

'''15. Write a Python program to combine two dictionaries into a single dictionary. If both
dictionaries share a key, the value from the second dictionary should take precedence.
Given Input: dict1 = {&quot;a&quot;: 1, &quot;b&quot;: 2} and dict2 = {&quot;b&quot;: 3, &quot;c&quot;: 4}'''

dict1 = {"a": 1, "b": 2}
dict2 = {"b": 3, "c": 4}
combined_dict = {**dict1, **dict2}
print("The combined dictionary is: ", combined_dict)

print("---------------------------------")
'''16. Write a Python program to create a tuple, access its elements by index, and find its
length.
Given Input: fruits = (&quot;apple&quot;, &quot;banana&quot;, &quot;cherry&quot;, &quot;date&quot;)'''

fruits = ("apple", "banana", "cherry", "date")
print("The first element of the tuple is: ", fruits[0:3])
print("The length of the tuple is: ", len(fruits))

print("---------------------------------")
'''17. Write a Python program to create a tuple containing a single item, the number 50, and
confirm its type.
Given Input: A single integer value 50'''

single_item_tuple = (50,)
print("The single item tuple is: ", single_item_tuple)
print("The type of the single item tuple is: ", type(single_item_tuple))
print("---------------------------------")

'''18. Write a Python program to join three separate tuples into one new tuple using
the + operator.
Given Input: a = (1, 2), b = (3, 4), and c = (5, 6)'''

a = (1, 2)
b = (3, 4)
c= (5, 6)
combined_tuple = a + b + c
print("The combined tuple is: ", combined_tuple)

print("---------------------------------")
'''19. Write a Python program to reverse the order of elements in a tuple.
Given Input: items = (1, 2, 3, 4, 5)'''

items = (1, 2, 3, 4, 5)
reversed_items = items[::-1]
print("The reversed tuple is: ", reversed_items)

print("---------------------------------")
'''20. Write a Python program to convert a tuple of characters into a single joined string.
Given Input: chars = (&#39;a&#39;, &#39;b&#39;, &#39;c&#39;)'''

chars = ('a', 'b', 'c')
joined_string = ''.join(chars)
print("The joined string is: ", joined_string)
print("---------------------------------")