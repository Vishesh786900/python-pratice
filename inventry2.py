items=["Laptop","Mouse","Keyboard","Monitor","Printer"]
stock=[15,50,30,10,8]
sales=[0,0,0,0,0]
price=[55000,800,1500,12000,9000]
reorder=[5,10,8,3,2]

while True:
    print("\n===== INVENTORY SYSTEM =====")
    print("1. Show Inventory")
    print("2. Sell Item")
    print("3. Restock Item")
    print("4. Stock Alert")
    print("5. Item Summary")
    print("6. Search Item")
    print("7. Total Inventory Value")
    print("8. Total Revenue")
    print("9. Exit")

    choice=int(input("Enter your choice: "))

    if choice==1:
        print("\nItem\t\tStock\tSold\tPrice")
        for i in range(len(items)):
            print(items[i],"\t",stock[i],"\t",sales[i],"\t",price[i])

    elif choice==2:
        print("\nItems:")
        for i in range(len(items)):
            print(i+1,".",items[i])
        item=int(input("Enter item number: "))-1
        quantity=int(input("Enter quantity sold: "))
        if item>=0 and item<len(items):
            if quantity<=stock[item]:
                stock[item]-=quantity
                sales[item]+=quantity
                print("Item sold successfully!")
            else:
                print("Not enough stock!")
        else:
            print("Invalid item number!")

    elif choice==3:
        print("\nItems:")
        for i in range(len(items)):
            print(i+1,".",items[i])
        item=int(input("Enter item number: "))-1
        quantity=int(input("Enter quantity to add: "))
        if item>=0 and item<len(items):
            stock[item]+=quantity
            print("Item restocked successfully!")
        else:
            print("Invalid item number!")

    elif choice==4:
        print("\n===== STOCK ALERT =====")
        for i in range(len(items)):
            if stock[i]<=reorder[i]:
                print(items[i],"needs restocking!")
            else:
                print(items[i],"stock is OK.")

    elif choice==5:
        print("\n===== ITEM SUMMARY =====")
        for i in range(len(items)):
            total=sales[i]*price[i]
            print("\nItem:",items[i])
            print("Current Stock:",stock[i])
            print("Items Sold:",sales[i])
            print("Total Sales: ₹",total)

    elif choice==6:
        search=input("Enter item name: ")
        found=False
        for i in range(len(items)):
            if search.lower()==items[i].lower():
                print("\nItem Found!")
                print("Item:",items[i])
                print("Stock:",stock[i])
                print("Sold:",sales[i])
                print("Price: ₹",price[i])
                found=True
        if found==False:
            print("Item not found!")

    elif choice==7:
        total_value=0
        for i in range(len(items)):
            total_value+=stock[i]*price[i]
        print("\nTotal Inventory Value: ₹",total_value)

    elif choice==8:
        total_revenue=0
        for i in range(len(items)):
            total_revenue+=sales[i]*price[i]
        print("\nTotal Revenue: ₹",total_revenue)

    elif choice==9:
        print("Thank you!")
        break

    else:
        print("Invalid choice!")