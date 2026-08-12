"""
Module: gameSearch.py
Programmer: F329597, Written: August-September 2024
Description: Contains functionality to allow the user to search for
             games based on their title and will return the game
             with its associated information.
Usage - Enter the title of the game you want to search for and
        the corresponding games will be shown.
"""


import database as DB

def search_games(search_term):
    """Uses a search term (title) inputted from the user to be used to find a
       certain game within the list of games

       Parameters:
            search_term = Name of the game the user wants to find (str)

        Returns:
            found_games, empty str = A list containing all games that fit the
                                     search criteria, empty string (list, str)
            empty str, str = empty string, a string message raising the error
                             (str, str)
    """
    game_data_list = []
    if search_term:
        game_data_list = DB.read_game_info()
        found_games = []
        for game in game_data_list:
            if search_term.upper() == game["Title"].upper():
                found_games.append(game)
        if found_games:
            return found_games, ""
        else:
            return "", "No game with that name could be found"
        
    else:
        return "", "Invalid search term specified"
            

def get_user_input():
    """Gets the user to input the title of the game they want to search, allows
       the user to exit the program.

       Returns:
           None = used to break out of the loop
           user_search_by_name = user input (str)
    """
    while True:
        try:
            user_search_by_name = input("Please enter the name of the game you "
                                        "want to find or to leave type exit: ")
            if user_search_by_name.lower() == "exit":
                return None
            if not user_search_by_name.strip():
                raise ValueError("Your game name cannot be empty, please try "
                                 "again.")
            return user_search_by_name
        except ValueError as ve:
            print("Input Error: {}".format(ve))
            

#Example usage:
if __name__ == "__main__":
    # Testing code function works without self input:
    found_games, error_message = search_games("cod")
    print("games with name 'cod'")
    print(found_games)
    while True:
        # Testing code function works with self input:
        user_search_by_name = get_user_input()

        if user_search_by_name is None:
            print("Exiting the system")
            break

        found_games, error_message = search_games(user_search_by_name)
        if found_games:
            for game in found_games:
                print(game)
        else:
            print(error_message)

        #


#Test cases: search_term (reason)
#Test case 1: "" (checking empty input)
#Test case 2: "exit" (For console only, ends program)
#Test case 3: "xxx" (Checking any invalid game name)
#Test case 4: "cod" (Checking valid game name LOWERCASE)
#Test case 5: "COD" (Checking valid game name UPPERCASE)


    
    



