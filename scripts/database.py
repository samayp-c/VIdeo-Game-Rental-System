"""
Module: database.py
Programmer: F329597, Written: August-September 2024
Description: Contains functionality that is commonly used to
             interact with the database across the game search,
             rent, return and select modules.
Usage - Reading rental info and reading game info, printed
        automatically upon running, can check it corresponds
        correctly to the database files. For the find game by id
        function, enter a valid id and the game should then be displayed
        with its information.
"""



from datetime import datetime as DT

game_file_path = "data/Game_Info.txt"
rental_file_path = "data/Rental_History.txt"

def read_file(file):
    """Reads contents of a file and returns a list of lines.

       Parameters:
           file = Path of the file to be read (str)

       Returns:
           file.readlines() = A list of lines from the file (list)
    """
    
    # Using with open for files automatically closes file after use
    with open(file, "r") as file:
        return file.readlines()


def read_rental_info(rental_file_path):
    """Reads rental information from a file, creates a dictionary of 
       {ID: availability} and returns the dictionary.

       Parameters:
           rental_file = Name of the file containing rental information (str)

       Returns:
           rental_data = A dictionary with game IDs as keys and the availability
                         status as values (dict)
    """
    rental_data = {}
    rental_info_lines = read_file(rental_file_path)
    
    for line in rental_info_lines[1:]:
        # Splits each line into 4 separate variables
        game_id, rent_date, return_date, customer_id = line.strip().split(",")
        if return_date == "":
            rental_data[game_id] = "Not available"
        else:
            rental_data[game_id] = "Available"
            
    return rental_data


def read_game_info():
    """Uses both the game and rental information from files and returns a list
       of each game with its information and availability

       Returns:
           game_data = A list of dictionaries, each containing information
                       about a game (list)
    """
    game_data = []
    
    rental_data = read_rental_info(rental_file_path)
    game_info_lines = read_file(game_file_path)
    
    for line in game_info_lines[1:]:
        game_info_split = line.strip().split(",")
        game_id = game_info_split[0]
        # Creates a dictionary for each game containing all its information
        game = {
            "ID": game_id,
            "Platform": game_info_split[1],
            "Genre": game_info_split[2],
            "Title": game_info_split[3],
            "Purchase Price £": game_info_split[4],
            "Purchase Date": game_info_split[5],
            "Availability": rental_data.get(game_id)
        }
        game_data.append(game)
        
    return game_data


def find_game_by_id(game_id, game_data):
    """Checks if the inputted game id exists in the database

       Parameters:
           game_id = inputted game id (str)
           game_data = List of dictionaries containing all game information
                       (list)

       Returns:
           game = a dictionary containing the games information if
                  found (dict)
           None = if the game ID does not exist
    """
    for game in game_data:
        if game["ID"] == game_id:
            # If game with matching ID is found
            return game
    # No matching ID found
    return None


def write_column_headinDB():
    """Writes the column headinDB at the top of the file."""
    with open(rental_file_path, "w") as rent_history:
        rent_history.write("Game ID, Rental Date, Return Date, Customer ID")


def write_old_returned_rental_history(rented_game_id,rent_date,return_date,
                                      customer_id):
    """Adds the previous rental history to the file excluding the
       active rentals.

       Parameters:
           rented_game_id = ID of the game that was rented (str)
           rent_date = Date the game was rented (str)
           return_date = Date the game was returned (str)
           customer_id = ID of the customer who rented the game (str)
    """
    with open(rental_file_path, "a") as rent_history:
        rent_history.write(
            f"\n{rented_game_id},{rent_date},{return_date},{customer_id}"
        )

   
def write_newly_returned_game(rented_game_id, rent_date,customer_id):
    """Rewrites the game thats being returned with its return date and
       adds to rental history file.

       Parameters:
           rented_game_id = ID of the game being returned (str)
           rent_date = Date the game was rented (str)
           customer_id = ID of customer who rented and returned the game
                         (str)
    """
    return_date = DT.now()
    # Formats the date consistent with the database
    converted_return_date = return_date.strftime("%d/%m/%Y")
    with open(rental_file_path, "a") as rent_history:
        rent_history.write(
            f"\n{rented_game_id},{rent_date},{converted_return_date},"
            f"{customer_id}"
        )
        

def write_current_active_rentals(active_rental_history):
    """Adds the active rentals back to the file excluding the game
       that just got returned (No longer active).

       Parameters:
           active_rental_history = A list storing the rental history of the
                                   games currently out on rent (list)
    """
    with open(rental_file_path, "a") as rent_history:
        rent_history.write("\n")
        for i in active_rental_history[:-1]:
            rent_history.write(f"{i}")
        
        # Removes the newline character from the last active rental
        # that is written to the file
        last_entry = active_rental_history[-1].rstrip("\n")
        rent_history.write(last_entry)


def update_database(customer_id, inputted_game_id):
    """Updates the rental history database with a new rental record.

       Parameters:
           customer_id = ID of the customer renting the game (str)
           inputted_game_id = ID of the game being rented (str)
    """
    date = DT.now()
    # Formats current date into same format as database dates
    formatted_date = date.strftime("%d/%m/%Y")

    with open(rental_file_path, "a") as rent_history:
        rent_history.write(f"\n{inputted_game_id},{formatted_date},,"
                           f"{customer_id}") 


if __name__ == "__main__":
    # Testing individual functions

    lines = read_file(rental_file_Path)
    print("Rental file lines:")
    print(lines)
    rental_data = read_rental_info(rental_file_Path)
    print("Game availability:")
    print(rental_data)
    game_data = read_game_info()
    print("Game information:")
    print(game_data)
    game = find_game_by_id("1", game_data)
    print("found game by id:")
    print(game)
