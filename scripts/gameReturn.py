"""
Module: gameReturn.py
Programmer: F329597, Written: August-September 2024
Description: Contains functionality to allow the user to return
             games by providing game ids, the database will then
             be updated accordingly.
Usage - Enter a game id and if it passes all validation and
        successfully returns then check the database file to
        make sure to it is appropriately updated.
"""


import database as DB
from datetime import datetime as DT

rental_file_path = "data/Rental_History.txt"

def complete_return_process(game_id):
    """Rewrites the database accordingly with the new returned game.

       Parameters:
           game_id = ID of the game being returned (str)
    """
    active_rental_history = []
    # Reads existing rental information and stores it
    rental_information_lines = DB.read_file(rental_file_path)
    
    DB.write_column_headinDB()
    
    for line in rental_information_lines[1:]:
        rented_game_id, rent_date, return_date, customer_id = (
            line.strip().split(",")
        )
        
        if return_date:
            DB.write_old_returned_rental_history(rented_game_id,rent_date,
                                              return_date,customer_id)
        else:
            if rented_game_id == game_id:
                DB.write_newly_returned_game(rented_game_id, rent_date,customer_id)
            else:
                active_rental_history.append(line)

    DB.write_current_active_rentals(active_rental_history)
    

def return_game(game_id):
    """Validates game id and ability to be returned then coordiantes
       the return process.

       Parameters:
           game_id = ID of the game being returned (str)

       Returns:
           String = A message indicating the result of the return
                    attempt (str)
    """
    game_data = DB.read_game_info()
    game = DB.find_game_by_id(game_id, game_data)

    if game == None:
        # If no game with that ID is found
        return "Invalid game ID"

    rental_data = DB.read_rental_info(rental_file_path)
    if rental_data.get(game_id) == "Available":
        # If the game is available, hence not rented, cannot be returned
        return "This game is available for rent, can't be returned"
    
    else:
        complete_return_process(game_id)
        return "Game has successfully been returned"

    
if __name__ == "__main__":
    # Testing functions, running code below will test the return_game
    # and complete_return_process functions however check the database
    # file is correctly updated to make sure first 4 database files
    # functions are working correctly
    game_id_being_returned = input("Please input the game id you want to return")
    result = return_game(game_id_being_returned)
    print(result)


#Test cases game_id (reason)
#Test case 1: "xxxx" (Checks invalid game ID)
#Test case 2: .... (Any game ID which is available for rent)
#Test case 3: .... (A valid game ID that can be returned)
#(Make sure to check database files after as well)
