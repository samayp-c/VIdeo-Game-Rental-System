"""
Module: gameRent.py
Programmer: F329597, Written: August-September 2024
Description: Contains functionality to rent games, first validates
             the user input and then uses provided
             subscriptionManager.pyc to check customer status.
             Once all validation checks including customer limits
             and game availability. The database is then updated to
             show game has been rented.
Usage - Enter customer id and game id and run. Then check the database
        files to make sure if a rent was successful that it was
        updated correctly.
"""

import subscriptionManager as SM
import database as DB
from datetime import datetime as DT

rental_file_path = "data/Rental_History.txt"

def validate_input(customer_id):
    """Checks whether customer id input is correctly formatted

       Parameters:
           customer_id = Inputted customer id from user (str)

       Returns:
           True and empty str if formatted correctly (bool, str)
           False and error message if incorrectly formatted (bool, str)
    """
    if not customer_id:
        # If ID is empty, returns invalid
        return False, "Customer ID can not be empty"
    if not customer_id.isdigit() or len(customer_id) != 4:
        # if ID isn't numeric or 4 digits, returns invalid
        return False, "Customer ID has been incorrectly inputted"

    return True, ""


def active_rentals_count(customer_id, rental_lines):
    """Checks the number of current active rentals the customer has.

       Parameters:
           customer_id = id of the customer being checked for active rentals
                         (str)
           rental_lines = A list of lines from the rental history file
                          containing all the details of previous rent
                          transactions (list)

       Returns:
           rental_count = The number of active rentals for that customer
                          (int)
    """
    rental_count = 0
    for line in rental_lines[1:]:
        _, _, return_date, renter_id = line.strip().split(",")
        if renter_id == customer_id and return_date == "":
            # If any active rentals are found (Empty return date)
            rental_count += 1
    return rental_count


def validate_rent_game(customer_id, inputted_game_id, game_data):
    """Handles the game rental process for a customer, ensuring the
       customer has an active subscription, and the game is available
       for rent.

       Parameters:
           customer_id = ID of the customer attempting to rent a game (str)
           inputted_game_id = ID of the game the customer wants to rent (str)
           game_data = List of dictionaries containing all game information
                       (list)

       Returns:
           string = A message indicating the result of the rental
                    attempt (str)
    """
    validation_check, error_message = validate_input(customer_id)
    if not validation_check:
        return error_message

    # Returns a tuple containing, start date, end date, and rental limit
    # for their subscription
    (x,y,z) = SM.check_subscription_status(customer_id)

    # Tuple will return (None, None, None) if ID is not found
    if x == None:
        return "Customer does not exist"

    subscription_end_date = y
    # Converts string date to a date type that can be compared with current date
    conversion_end_date = DT.strptime(y, "%d/%m/%Y")
    if conversion_end_date < DT.now():
        return "Customer subscription has ran out"

    game = DB.find_game_by_id(inputted_game_id, game_data)
    if game is None:
        return "Invalid game ID"

    if game["Availability"] == "Not available":
        return "Game is not available right now"

    rental_limit = z
    rental_lines = DB.read_file(rental_file_path)
    
    rental_count = active_rentals_count(customer_id, rental_lines)
    if rental_count == rental_limit:
        return "Customer has reached their rental limit"

    # All checks passed, game rented and database is updated
    DB.update_database(customer_id, inputted_game_id)
    return (f"Customer {customer_id} has been able to rent the game "
            "successfully")


def renting_game(customer_id, inputted_game_id):
    """Coordinates the whole rental process.

       Parameters:
           cusomter_id = ID of the customer trying to rent a game (str)
           inputted_game_id = ID of the game the customer is trying to
                              rent (int)

       Returns:
           result = The result of the renting attempt
    """

    game_data = DB.read_game_info()

    result = validate_rent_game(customer_id, inputted_game_id, game_data)

    return result


if __name__ == "__main__":
    # Checking functions individually without self input:
    validation_check, error_message = validate_input("1001")
    print("User 1001 exists:")
    print(validation_check)
    rental_lines = DB.read_file(rental_file_path)
    rental_count = active_rentals_count("1001", rental_lines)
    print("Number of rentals from user 1001")
    print(rental_count)

    # Checking functions with self input (These will check all
    # remaining functions with the test cases below, checking
    # database file after will confirm working database function
    customer_id = input("Please enter the customers ID: ")
    inputted_game_id = input("Please enter the game ID: ")
    result = renting_game(customer_id, inputted_game_id)
    print(result)


#Test cases: customer_id,game_id (reason)
#Test case 1: "",_  (Checking empty customer inputs)
#Test case 2: abcd,_ (Checking non numeric customer inputs)
#Test case 3: 00000,_ (Checking customer id length is 4)
#Test case 4: 0020,_ (Checking non existent customer id)
#Test case 5: 1002,_ (Checking a customer with a subscription that has run out)
#Test case 6: 1001,xxxx (any valid customer id, checks non existent game id)
#Test case 7: 1001,"" (Checks empty game id input)
#Test case 8: "1001",.... (Do any game that you know is unavailable)
#Test case 9: 1001,.... (Any available game and a customer id 1001 (set database so
#                        they are at limit)
#Test case 10: ....,.... (Any customer id & game id that allows successful rent TBD)
#(Make sure to check database files after as well)


    




