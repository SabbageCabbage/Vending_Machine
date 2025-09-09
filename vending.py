# While this file contains a good deal of framework for the project, it is not 
# sufficient for the completion of the tasks.  Functions will need to be created,
# parameters passed, functions may need to return things, imports will have to be added,
# those kinds of things.   
import json
import csv
import os
from plotly.graph_objs import Bar
from plotly import offline
import requests

inventory_file = "inventory.json"
transaction_file = "transaction_log.csv"

def generate_slots():
    rows = ['A', 'B', 'C', 'D', 'E','F','G','H'] #should in theory generate the cool lil slots for us
    collumns = ['1','2','3','4',]
    for r in rows:
        for c in collumns:
            yield r + c

def loadInventory():
    """Open the inventory file and read the JSON contents"""
    file = open(inventory_file, 'r')
    data = json.load(file)['inventory'] #reads the inventory from the JSON
    inventory = {}
    slots = list(generate_slots())
    for i in range(min(len(slots), len(data))):
        inventory[slots[i]] = data[i]
    return inventory

def printMenu():
    """Helper function to print the menu"""
    print("Please choose from the following options:")
    print(" (d) Display items")
    print(" (p) Purchase item")
    print(" ($) Change currency")
    print(" (c) Generate inventory chart")
    print(" (q) Quit")

def displayInventory(my_inventory):
    """Prints the inventory to the screen"""
    #print the inventory to the screen
    print("----Current vending machine inventory-----")
    quantity_list = []
    for slot, item in my_inventory.items():
        name = item['item']
        price = item['price_usd']
        quantity = item['quantity']
        if quantity > 0:  #handles the sold out items or at least I hope it does...
            status = f"${price:.2f} {name}"
        else:
            status = "SOLD OUT"
        print(f"{slot} - {status}")
    #print the inventory here.
    print("------------------------------------------")

def decrementInventory(my_inventory, slot_id):
    """decrement the inventory item associated with the slot_id"""
    #what happens if they try to decrement an item with zero inventory?
    if my_inventory[slot_id]['quantity'] <= 0: #once again handling the sold out items but this time it's when you pick a sold out item
        print(f"oopsies silly me,{my_inventory[slot_id]['item']} are all sold out! :( )")
        return False
    my_inventory[slot_id]['quantity'] -= 1 
    return True
def saveTransaction(my_inventory, slot_id):
    """record a transaction for the slot_id item. """
    item = my_inventory[slot_id]
    transact_file = open(transaction_file, 'a', newline='')
    writer = csv.writer(transact_file)
    if os.path.getsize(transaction_file) == 0:
            writer.writerow(["SLOT_ID", "AMOUNT_USD", "ITEM"])
    writer.writerow([slot_id, f"{item['price_usd']:.2f}", item['item']]) #logs down the items bought 

def saveEndingInventory(my_inventory):
    """write inventory to file or database"""
    updated_inventory = open('updated_inventory.json', 'w')
    json.dump({"inventory": list(my_inventory.values())}, updated_inventory, indent=4 )
    
def Generate_Inventory_Graph(my_inventory): #makes bar graph, basically the same code as what was used to make the top 40 cve list but tweaked a lil bit
    item_names=[]
    quantities =[]
    for slot, item in my_inventory.items():
        label = f"{item['item']} ({slot})"
        item_names.append(label)
        quantities.append(item['quantity'])
    
    bar = Bar(
        x = item_names, 
        y = quantities, 
    )
    offline.plot({
        "data": [bar],
        "layout": {
            "title": "Current Inventory", #adding title as well as descriptors for x and y axis
            "xaxis": {"title": "item's name"},
            "yaxis": {"title": "quantity"}
        }},
        filename="quantity_barplot.html"
    )

def Exchange_Currency(my_inventory,target_currency='USD'): #requesting currency exchange
    API_KEY = "add ur own here :bS"
    url = "http://api.exchangeratesapi.io/v1/latest"
    params = {
        "access_key": API_KEY,
        "base": "EUR",
        "symbols": f"USD,{target_currency}"
    }

    response = requests.get(url, params=params)
    data = response.json()
    usd_to_eur = 1 / data['rates']['USD']
    target_rate = data['rates'][target_currency]
    usd_to_target = usd_to_eur * target_rate #since the base is EUR, we're doing exchanges from EUR to USD and then from USD to the target currency
    print(f"\nConverting USD prices to {target_currency}")
    for slot, item in my_inventory.items():
        original_price = item['price_usd']
        converted_price = original_price * usd_to_target
        print(f"{slot}: {item['item']} - {converted_price:.2f} {target_currency}")
        
if __name__=="__main__":
    print("Welcome to the TU Vending Machine!")
    #load data from tu_vending_inventory.json and save into memory or database
    if os.path.exists(transaction_file): #clears the logs before starting again
        os.remove(transaction_file)
    my_inventory = loadInventory()
    keepLooping = True
    runningSalesTotal = 0.0
    while(keepLooping):
        printMenu()
        user_input = input(">").upper().strip()
        #handle the user_input
        if (user_input == "D"):
            displayInventory(my_inventory)
        elif(user_input == 'P'):
            slot_id = input("Enter the slot ID of the item you wish to purchase (e.g., A1): ").upper().strip()
            if slot_id in my_inventory:
                    item = my_inventory[slot_id]
                    if decrementInventory(my_inventory, slot_id):
                        saveTransaction(my_inventory, slot_id)
                        price = my_inventory[slot_id]['price_usd']
                        runningSalesTotal += price
                        print(f"yippee!! You have purchased {item['item']} for ${price:.2f}. Thank you!!!")
        elif (user_input == "Q"):
            saveEndingInventory(my_inventory)
            print(f"Total sales for this session: ${runningSalesTotal:.2f}")
            keepLooping = False
        elif (user_input == "C"):
            Generate_Inventory_Graph(my_inventory)
        elif user_input == "$":
            print("\nPlease select from the following currencies:")
            print(" > USD (current)")
            print(" > CAD")
            print(" > EUR")
            print(" > JPY")
            valid_currencies = ["USD","CAD","EUR","JPY"]
            currency = input("Enter currency code: ").upper().strip()
            if currency in valid_currencies:
                Exchange_Currency(my_inventory, currency)
            else:
                print("Oopsies, invalid currency selected")

        else:
            print("Uh Oh :{, that's not an avaliable button")
            