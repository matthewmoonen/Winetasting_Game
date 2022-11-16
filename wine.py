import random
import csv


def main():
    print_description()
    x = get_number_of_wines()
    currency, nameprice = get_names_of_wines(x)
    y = random_assignment(nameprice)
    
    players = get_player_1()
    players, number_of_players = get_players(players, 2)
    

    while True:
        if explain_next_rules() == True:
            break
        else:
            players, number_of_players = get_players(players, number_of_players)
            continue
    wines_to_csv(y)
    


# def order_randomisation:
    # The order of tasting is ransomised per wine and per player
    # Players taste the wines one by one and record their scores on paper

# def input_scores:
    # The players will record their scores on paper, so this part can occur more quickly at the end
    # Each player one by one, each wine one by one.

# def calculate_expected:
    # Calculate the EXPECTED score for each wine based on the price
    # i.e. if the cheapest wine costs $10 and the most expensive wine costs $100 then EXPECTED scores will be
            # • cheapest: 1.0
            # • most expensive: 10.0


# def determine_winner:

    # Calculate the mean score for each wine:
        # mean score is the mean given by all players

    # Calculate the standard deviation:
        # Standard deviation from the mean?
        # Or standard deviation from expected?

    # Assign scores to each guess:
        # It would probably be 


# def calculate_stats:
    # The p-value represents the likelihood that a given result is the result of random chance
    # p-value of < 0.05 is statistically significant
    # Calculate the chance that each taster, and the group as a whole, can tell the difference between expensive and cheap
    # There may be a point of diminishing returns where below a certain price point, users can distinguish the cheaper ones. But above this point it may no longer be possible.


def explain_next_rules():
    print('Explain to the user ')
    if input('Are you ready? Type yes to continue, or ') in ['yes', 'YES', 'Yes', 'y', 'Y']:
        return True
    else:
        return False



def print_description():
    print('description here')

def get_number_of_wines():
    
# Ensure the user inputs a valid number of wines. Repromt if not an integer.
    while True:
        try:
            number_of_wines = int(input("How many bottles of wine do you have? "))
        except ValueError:
            print("\nPlease enter a valid number\n")
        else:
            # Number of wines is limited to 26 -> A to Z
            if number_of_wines > 26:
                print("\nMax number of wines: 26\n")
                continue
            elif number_of_wines == 1:
                print("\nYou can't compare just 1 wine!\n")
            return number_of_wines

def get_names_of_wines(number_of_wines):
    currency = '$'
    nameprice = {}
    for i in range(number_of_wines):

        wine = input("Enter the name of wine number " + str(i + 1) + ": ")

        while True:
            price = input("How much did " + wine + " cost? ")
            
            # Check if price contains currency symbol
            if price[0] in '$€£':
                currency = price[0]
                price = price[1:]
            
            try:
                price = int(price)
            except ValueError:
                dollars_cents = price.split(".")
                if len(dollars_cents) == 2 and len(dollars_cents[1]) == 2:
                    try:
                        dollars = int(dollars_cents[0])
                        cents = int(dollars_cents[1])
                    except ValueError:
                        print('\nInvalid price. Please try again\n')
                        continue
                    else:
                        break
                else: 
                    print('\nInvalid price. Please try again\n')
                    continue
            else:
                break
        nameprice[wine] = [float(price)]
    print(nameprice)
    return currency, nameprice

# Ensure the user inputs valid prices. Prices can be inputted as dollars, pounds, euros or a simple number in the format 'XX' or 'XX.XX'
# Repromt user if not valid.

"""
Potential bugs!!!: if the user inputs prices with different currency symbols, only the last inputted currency will be outputted to the CSV.
Also, this may be better handled with a RegEx of some kind.
"""
        # initialise default currency to $


def wines_to_csv(xxx):
    NamePriceAssignment = {}
    with open('wines.csv', 'w', newline='') as winecsv:
        fieldnames = ['WineName', 'Price', 'RandomAssignment']
        writer = csv.DictWriter(winecsv, fieldnames=fieldnames)
        writer.writeheader()

        for key, value in xxx.items():
            NamePriceAssignment['WineName'] = key
            NamePriceAssignment['Price'] = value[0]
            NamePriceAssignment['RandomAssignment'] = value[1]
            writer.writerow(NamePriceAssignment)

def get_player_1():
    players = []

    players.append(input("Enter Player 1 Name: "))

    return players

def get_players(players, number):
    while number <= 25:
        player = input("Enter Player " + str(number) + " name or press Enter to continue: ")
        if len(player) == 0:
            break
        else:
            players.append(player)
            number += 1

    return players, number



def random_assignment(ddict):
    inorder = list(ddict.keys())
    winelist = sorted(inorder, key=lambda k: random.random())

    number = 65
    for i in winelist:
        ddict[i].append(chr(number))
        number += 1

    return ddict

if __name__ == '__main__':
    main()


