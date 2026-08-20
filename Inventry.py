# Inventory Stock Analysis System

# Arrays (Lists)
items = ["Laptop", "Mouse", "Keyboard", "Monitor", "Printer"]
stock = [15, 50, 30, 10, 8]
sales = [0, 0, 0, 0, 0]
price = [55000, 800, 1500, 12000, 9000]
reorder = [5, 10, 8, 3, 2]


while True:

    print("\n===== INVENTORY SYSTEM =====")
    print("1. Show Inventory")
    print("2. Sell Item")
    print("3. Restock Item")
    print("4. Stock Alert")
    print("5. Item Summary")
    print("6. Exit")

    choice = int(input("Enter your choice: "))

    # 1. Show Inventory
    if choice == 1:

        print("\nItem\t\tStock\tSold\tPrice")

        for i in range(5):
            print(items[i], "\t", stock[i], "\t", sales[i], "\t", price[i])


    # 2. Sell Item
    elif choice == 2:

        print("\nItems:")
        for i in range(5):
            print(i + 1, ".", items[i])

        item = int(input("Enter item number: "))
        quantity = int(input("Enter quantity sold: "))

        item = item - 1

        if quantity <= stock[item]:
            stock[item] = stock[item] - quantity
            sales[item] = sales[item] + quantity

            print("Item sold successfully!")

        else:
            print("Not enough stock!")


    # 3. Restock Item
    elif choice == 3:

        print("\nItems:")
        for i in range(5):
            print(i + 1, ".", items[i])

        item = int(input("Enter item number: "))
        quantity = int(input("Enter quantity to add: "))

        item = item - 1

        stock[item] = stock[item] + quantity

        print("Item restocked successfully!")


    # 4. Stock Alert
    elif choice == 4:

        print("\n===== STOCK ALERT =====")

        for i in range(5):

            if stock[i] <= reorder[i]:
                print(items[i], "needs restocking!")

            else:
                print(items[i], "stock is OK.")


    # 5. Item Summary
    elif choice == 5:

        print("\n===== ITEM SUMMARY =====")

        for i in range(5):

            total = sales[i] * price[i]

            print("\nItem:", items[i])
            print("Current Stock:", stock[i])
            print("Items Sold:", sales[i])
            print("Total Sales: ₹", total)


    # 6. Exit
    elif choice == 6:

        print("Thank you!")
        break

    else:

        print("Invalid choice!")