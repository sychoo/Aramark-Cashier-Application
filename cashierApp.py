# Created by Simon Chu
# Wed Jan 16 20:47:31 EST 2019

# Program to help the cashier
# who works at the P.O.D, Stark Learning Center
# Wilkes University

import datetime
from prettytable import PrettyTable

# Set Parameters
less_bank = 150.0
location = "Stark P.O.D"
meal_period_shift = "Night Shift"
register_number = 1
cashier_name = "Simon Chu"
date_today = str(datetime.date.today())

# Decreasing order, eliminate rolled coins when take out deposits
starting_counts_currency_items = {
    #{"bill_value": 20.0, "number_of_bills": 0, "bill_amount": 0.0}
    # Paper Bills
    "$   20.00": {"bill_value": 20.0},
    "$   10.00": {"bill_value": 10.0},
    "$    5.00": {"bill_value": 5.0},
    "$    1.00": {"bill_value": 1.0},

    # Rolled coins are treated different when prompt
    "Rolled Quarters": {"bill_value": 10.00},
    "Rolled Dimes":    {"bill_value": 5.00},  # To be verified
    "Rolled Nickles":  {"bill_value": 2.00},
    "Rolled Pennies":  {"bill_value": 0.50},

    # Loose coins
    "Loose Dollar Coin": {"bill_value": 1.00},
    "Loose Quarters":    {"bill_value": 0.25},
    "Loose Dimes":       {"bill_value": 0.10},
    "Loose Nickles":     {"bill_value": 0.05},
    "Loose Pennies":     {"bill_value": 0.01}
}

# Decreasing Order, eliminate rolled coins when take out the deposits
ending_counts_currency_items = {
    # Paper Bills
    "$  100.00": {"bill_value": 100.0},
    "$   50.00": {"bill_value": 50.0},
    "$   20.00": {"bill_value": 20.0},
    "$   10.00": {"bill_value": 10.0},
    "$    5.00": {"bill_value": 5.0},
    "$    1.00": {"bill_value": 1.0},

    # Rolled coins are treated different when prompt
    "Rolled Quarters": {"bill_value": 10.00},
    "Rolled Dimes":    {"bill_value": 5.00}, # To be verified
    "Rolled Nickles":  {"bill_value": 2.00},
    "Rolled Pennies":  {"bill_value": 0.50},

    # Loose coins
    "Loose Dollar Coin" : {"bill_value": 1.00},
    "Loose Quarters":     {"bill_value": 0.25},
    "Loose Dimes":        {"bill_value": 0.10},
    "Loose Nickles":      {"bill_value": 0.05},
    "Loose Pennies":      {"bill_value": 0.01}
}

def intro():
    print()
    print("Cashier App V1.0")
    print("Created by Simon Chu")
    print("Created on Jan. 16, 2019")
    print("Today is " + date_today)
    print()

def process_user_input(mapUsed):
    print()
    print("Will Enter 0 by Default")
    print()
    lst = list(mapUsed.keys())
    i = 0
    while (i < len(lst)):
        userInput = input("Please Enter Number of {0:18}:".format(lst[i]))

        # undo previous entry if entry is not the first
        if userInput == "undo":
            if i > 0:
                i-=1
                continue
            else:
                print()
                print("Error: Earlier Record Not Available!")
                print()
        else:
            if userInput == "":
                userInput = 0
            try:
                userInput = int(userInput)
            except ValueError:
                print('Error: Input is not an integer. Please Retry!')
                continue
            mapUsed[lst[i]]["number_of_bills"] = userInput
            i+=1

def calculate_starting_counts(ending_count, starting_count):
    # Calculate the starting count using ending count
    map = {}
    takeout = {}
    subtotal = 0

    # calculating the subtotal
    for i in ending_count.values():
        bill_amount = i["bill_value"] * i["number_of_bills"]
        subtotal += bill_amount
        i["bill_amount"] = round(bill_amount, 2)
    subtotal = round(subtotal, 2)
    deposit = round((subtotal - less_bank), 2) # Calculate deposit

    if deposit < 0:
        print("Fatal Error: desposit can't be negative!")
        exit()

    print("Subtotal: " + str(subtotal))
    print("Deposit : " + str(deposit))

    map = {
        "Subtotal": subtotal,
        "Deposit" : deposit
        }

    # Set global deposit    
    deposit_global = deposit

    # Now we have to calculate how to effectively take out the deposit and calculate the rest
    # check if the cash left is equal to the amount of less_bank (magic number 150)
    # Avoid Taking out Rolled Coins (Rolled Coins has the lowest priority)
    keyword = "Rolled" # Word that has the lowest priority
    for i in starting_count.keys():
        if keyword not in i:
            # bill value of the current bill
            bill_value = starting_count[i]["bill_value"]

            # the actual number of bills in the current currency pool
            max_number_of_bills = ending_count[i]["number_of_bills"]

            # calculate the number of bill that needs to be taken out (if has adequate cash number)
            expected_number_of_bills = int(deposit / bill_value)

            # since the max number of bills is limited by the current currency pool, find the minimum
            actual_number_of_bills = int(min(expected_number_of_bills, max_number_of_bills))

            # deduct deposit amount     
            deposit -= round((actual_number_of_bills * bill_value), 2)
            deposit = round(deposit, 2)

            # calculate the number of bills left
            number_of_bills_left = max_number_of_bills - actual_number_of_bills

            # set the number of bills taken out
            takeout[i] = actual_number_of_bills

            # Set the starting_count map
            starting_count[i]["number_of_bills"] = number_of_bills_left
            starting_count[i]["bill_amount"] = round((bill_value * number_of_bills_left), 2)
    
    deposit = round(deposit, 2)

    # Divider
    takeout["---"] = "---"

    if round(deposit, 2) == 0.0:
        print("Passed!")
    else:
        print(keyword + " bills used!")
    for i in starting_count.keys():
        if keyword in i:
            # bill value of the current bill
            bill_value = starting_count[i]["bill_value"]

            # the actual number of bills in the current currency pool
            max_number_of_bills = ending_count[i]["number_of_bills"]

            # calculate the number of bill that needs to be taken out (if has adequate cash number)
            expected_number_of_bills = deposit // bill_value

            # since the max number of bills is limited by the current currency pool, find the minimum
            actual_number_of_bills = int(min(expected_number_of_bills, max_number_of_bills))

            # deduct deposit amount     
            deposit -= round((actual_number_of_bills * bill_value), 2)
            deposit = round(deposit, 2)

            # calculate the number of bills left
            number_of_bills_left = max_number_of_bills - actual_number_of_bills

            # set the number of bills taken out
            takeout[i] = actual_number_of_bills

            # Set the starting_count map
            starting_count[i]["number_of_bills"] = number_of_bills_left
            starting_count[i]["bill_amount"] = round((bill_value * number_of_bills_left), 2)
    if round(deposit, 2) == 0.0:
        print("Calculation Passed")
    else:
        print("Unknown Fatal Error!")

    return map, takeout, deposit_global

def process_form_entry(map, takeout):
    print()
    print(".......................")
    print("Processing Form Entry::")
    print()

    instruction = PrettyTable()
    ending_count_form = PrettyTable()
    starting_count_form = PrettyTable()

    instruction.field_names = ["Bill", "Number of Bills"]
    for i in takeout.keys():
        quantity = takeout[i]
        if quantity == 0:
            instruction.add_row([i, ""])
        else:
            instruction.add_row([i, takeout[i]])

    ending_count_form.field_names = ["", "Cashier"]
    for i in ending_counts_currency_items.keys():
        bill_amount = ending_counts_currency_items[i]["bill_amount"]
        if bill_amount == 0.0:
            ending_count_form.add_row([i, ""])
        else:
            ending_count_form.add_row([i, "{0:.2f}".format(bill_amount)])

    ending_count_form.add_row(["", ""])
    ending_count_form.add_row(["SUBTOTAL", "{0:.2f}".format(map["Subtotal"])])
    ending_count_form.add_row(["(LESS BANK)", "{0:.2f}".format(less_bank)])
    ending_count_form.add_row(["TOTAL DEPOSIT", "{0:.2f}".format(map["Deposit"])])

    starting_count_form.field_names = ["", "Cashier"]
    total_bank = 0
    for i in starting_counts_currency_items.keys():
        bill_amount = starting_counts_currency_items[i]["bill_amount"]
        if bill_amount == 0.0:
            starting_count_form.add_row([i, ""])
        else:
            starting_count_form.add_row([i, "{0:.2f}".format(bill_amount)])
        total_bank += starting_counts_currency_items[i]["bill_amount"]

    starting_count_form.add_row(["TOTAL BANK", "{0:.2f}".format(total_bank)])
    if total_bank == less_bank:
        print("Passed!")
    else:
        print("Fatal Error")
    return instruction, ending_count_form, starting_count_form


def show_form(instruction, ending_count_form, starting_count_form, deposit):
    print()
    print("...............................................")
    print("Please Put the following items in an envelope::")

    # set alignment
    instruction.align["Bill"] = "r"
    instruction.align["Number of Bills"] = "l"
    ending_count_form.align[""] = "r"
    ending_count_form.align["Cashier"] = "l"
    starting_count_form.align[""] = "r"
    starting_count_form.align["Cashier"] = "l"


    print(instruction)
    input()
    
    print()
    print("...............")
    print("Ending Counts::")
    print(ending_count_form)
    input()

    print()
    print(".................")
    print("Starting Counts::")
    print(starting_count_form)


    print()
    print("...........................................")
    print("Please Mark the Following on the Envelope::")
    print("Location: " + location)
    print("Shift   : " + meal_period_shift)
    print("Deposit : " + str(deposit))
    print("Today   : " + date_today)

    print()
    print("All Done :-)  Let's Go Home!")
    print()

def print_form():
    print()
    print("................")
    print("Printing Form...")

if __name__ == "__main__":
    # print intro
    intro()

    # Prompt user for number of each bill and enter it into the map
    print("..........................")
    print("Processing Ending Counts::")
    process_user_input(ending_counts_currency_items)

    # Calculate the total amount, fill in the map, and calculate the starting amount
    print()
    print(".............................")
    print("Calculating Starting Counts::")
    map, takeout, deposit = calculate_starting_counts(ending_counts_currency_items, starting_counts_currency_items)

    # Generate form using the map values, instruct the user to take out money
    instruction, ending_count_form, starting_count_form = process_form_entry(map, takeout) # function calculate the total amount

    # present the form
    show_form(instruction, ending_count_form, starting_count_form, deposit) # show the form on terminal
    
    # print a physical copy of the form
    #print_form() # print form on an available printer, ask user to confirm
