import random
import csv
import os

def main():
    print_description()
    
    # Get number of wines from user
    number_of_wines = get_number_of_wines()

    # Get names, prices and currency from user.
    # Names of wines returned as dictionary
    # Currency not yet saved/implemented.
    currency, nameprice = get_names_of_wines(number_of_wines)

    # Assign random aliases to each of the wines and save these as a list item within dictionary values  
    # Also returns wine aliases as a list - this is used in tasting_sequence to randomise the tasting order for each player
    winedict, letters = random_assignment(nameprice)
    wines_to_csv(winedict)
    
    # Get name of first player, returns list of players with one entry. 
    players = get_player_one()
    # Get next players
    players, number_of_players = get_next_players(players, 1)
    

    while True:
        # Explains next rules - if users wish to do blind testing, the tasters must not view the next screen as this shows the randomly assigned aliases.
        # Allows user to return to previous screen if they wish to add more players.
        if explain_next_rules(number_of_players, len(winedict)) == True:
            break
        else:
            players, number_of_players = get_next_players(players, number_of_players)
            continue
    
    # Show randomly assigned aliases to the person who labels the glasses
    show_aliases(winedict)

    # Randomly organise tasting sequence and show this to the users.
    tasting_sequence(players, letters)



def print_description():
    # Clear screen and read rules to user 
    os.system('cls||clear')
    print('This program enables you to test your skills in wine tasting. \n') 
    print('What you need: ')
    print("     * at least two bottles of wine")
    print("     * at least two players")
    print("     * pen and paper for the players to record their scores \n")
    print('The program will test whether you can tell the difference between cheap and expensive wines \n')
    print('Therefore, the wines selected for the study should ideally be a similar type but at a range of different prices \n')
    
    # Get 'Enter' input from user to continue showing rules
    while True:
        if input('Press Enter to continue') == '':
            break
    os.system('cls||clear')

    print('Each wine will be assigned a random letter. Only one person should know the letters that have been assigned to each wine. This person should label the glasses. \n')
    
    print('Ideally, the person who labels and pours the glasses should NOT participate in tasting or even be present in the room during the tastings! \n')

    print("This allows the study to follow a 'double blind' experimental method and helps to eliminate unconscious bias. \n")

    while True:
        if input('Press Enter to continue') == '':
            break
    os.system('cls||clear')




def get_number_of_wines():    
# Ensure the user inputs a valid number of wines. Repromt if not an integer.
    while True:
        try:
            number_of_wines = int(input("How many bottles of wine do you have? "))
        except ValueError:
            print("\nPlease enter a valid number\n")
        else:
            # Number of wines is limited to 26 as aliases will be assigned letters from A up to Z using ASCII values.
            if number_of_wines > 26:
                print("\nMax number of wines: 26\n")
                continue
            elif number_of_wines == 1:
                print("\nYou can't compare just 1 wine!\n")
            return number_of_wines



def get_names_of_wines(number_of_wines):
    # Assign default currency to $
    currency = '$'

    # Initialise dictionary that will be returned to main with wines + prices
    nameprice = {}
    for i in range(number_of_wines):

        print('')
        wine = input("Enter the name of wine number " + str(i + 1) + ": ")

        while True:
            price = input("How much did " + wine + " cost? ")
            
            # Check if price contains currency symbol, reassign currency to pounds or euros if pound or euro symbol used.
            # If currency symbol is included, remove from string to then proceed to input validity
            if price[0] in '$€£':
                currency = price[0]
                price = price[1:]
            
            # Ensure the user inputs valid price
            # Prices can be inputted as a simple number in the format 'XX' or 'XX.XX'
            # Repromt user if not valid.
            try:
                # Captures prices entered as whole dollar amounts
                price = int(price)  
            except ValueError:
                # Captures prices in dollar/cent notation.
                # Reject invalid cent notation; e.g. 9.999 is not valid as there cannot be 0.9 of a cent.
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
    os.system('cls||clear')
    return currency, nameprice




def random_assignment(ddict):
    # Assign each wine a random alias from A -->
    inorder = list(ddict.keys())
    winelist = sorted(inorder, key=lambda k: random.random())
    
    letters = []

    number = 65
    for i in winelist:
        ddict[i].append(chr(number))
        letters.append(chr(number))
        number += 1
    return ddict, letters





def wines_to_csv(winedict):
    NamePriceAssignment = {}
    # Write headers to CSV file
    with open('wines.csv', 'w', newline='') as winecsv:
        fieldnames = ['Wine Name', 'Price', 'Random Assignment']
        writer = csv.DictWriter(winecsv, fieldnames=fieldnames)
        writer.writeheader()

        # Write names, prices and aliases of each wine to CSV
        for key, value in winedict.items():
            NamePriceAssignment['Wine Name'] = key
            NamePriceAssignment['Price'] = value[0]
            NamePriceAssignment['Random Assignment'] = value[1]
            writer.writerow(NamePriceAssignment)



def explain_next_rules(number_of_players, lenOf_winedict):
    # Explain next rules and encourage user to set up needed equipment.
    os.system('cls||clear')
    number_of_glasses = number_of_players * lenOf_winedict
    print('You have ' + str(lenOf_winedict) + ' bottles and there are ' + str(number_of_players) + ' players, so you need ' + str(number_of_glasses) + ' glasses. \n')
    
    print('Random letters will now be assigned to each wine. \n')
    
    print('~~~ Reminder: to avoid bias, only one person should see the assigned letters. ~~~ \n')
    
    print('~~~ And ideally, the person who does the labeling should also not be present for the tastings! ~~~ \n')

    # Require user to type 'yes' to continue as the next screen shows the randomly assigned letters.
    # If 'yes' typed, send True back to main so the next function can be called.
    # If 'yes' not typed, return False and main will kick the user back to previous function (input more users).
    if input('Are you ready to see the secret letters? Type yes to continue, or no to return to add more players ') in ['yes', 'YES', 'Yes', 'y', 'Y']:
        return True
    else:
        os.system('cls||clear')
        return False




def get_player_one():
    # Initialise array containing player names, get name of first player.
    players = []
    os.system('cls||clear')
    players.append(input("Enter Player 1 Name: "))

    return players



def get_next_players(players, number):
    # Get names of next players. Players can simply press 'Enter' to continue once all player names have been inputted.
    # Next function allows user to return to this function if they wish to add more players.
    
    while number <= 25:
    # Number of players limited to 25 based on vague assumption that something like this could lead to buffer overflow style attacks.
        player = input("Enter Player " + str(number) + " name or press Enter to continue: ")
        if len(player) == 0:
            break
        else:
            players.append(player)
            number += 1

    return players, number



def show_aliases(winedict):

    # Clear screen and show randomly assigned aliases to the user.
    os.system('cls||clear')
    
    print('The randomly assigned letters are: \n')

    for key, value in winedict.items():
        print(key + ': ' + value[1])
    
    print('')
    
    while True:
        if input('Press Enter once all the glasses have been poured and labelled.') == '':
            break



def tasting_sequence(players, letters):
    os.system('cls||clear')
    print('The tasting order has been randomised for each player. \n')
    while True:
        if input('Press Enter when you are ready to start tasting. Good luck!') == '':
            break
    os.system('cls||clear')

    print('Players, please taste the wines in the following order. After tasting each wine, write a score out of 10 on your scorecard \n')

    for player in players:
        # Randomises the order in which each player tastes each wine.
        print(player + ': ', end ='')
        letters1 = random.sample(letters, len(letters))
        for letter in letters1:
            print(letter + ', ', end='')
        print('\n')
    print('Thank you for participating! This program will now exit \n')
    print("Open the program next program ('scores.py') when you are ready to input your ratings and calculate the winner :) \n")



if __name__ == '__main__':
    main()




# Future features/functions to implement:

# def input_scores:
    # For simplicity, players are asked to record their scores on paper
    # This function would allow player scores to be inputted.


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
