"""
Module: gameSelect.py
Programmer: F329597, Written: August-September 2024
Description: Contains functionality to identify popular game titles
             and recommend which games to purchase more copies about.
             It also recommends the most popular genre for future
             acquisitions. The program makes use of matplotlib for
             graphical visualisation to help the user in decision
             making for future game purchases.
Usage - Enter a time period for the data you want to look at,
        choose the significance of popularity and price, e.g
        0.7 price and 0.3 popularity suggests you think price
        has a higher importance for recommending future games
        than popularity, and finally enter your budget and run.
"""


import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
import database as DB
import math
from datetime import datetime, timedelta

rental_file_path = "data/Rental_History.txt"
game_file_path = "data/Game_Info.txt"


#####################################################
#        Functions to obtain and return values      #
#        and dictionaries used in algorithms to     #
#        recommend games, and used for graph        #
#        visualisation.                             #
#####################################################
def create_id_genre_dict():
    """Creates a dictionary with each game id as a key and its genre
       as a value

        Returns:
            game_genre_dict = A dictionary {ID: Genre} (dict)
    """
    game_data = DB.read_game_info()
    game_genre_dict = {}

    for game in game_data:
        # "game" is a dict, "game_data" is a list of dicts
        # Line below gets the value of ID from "game" and uses it as
        # a key and sets its value as the value of "Genre" from "game"
        game_genre_dict[game["ID"]] = game["Genre"]

    return game_genre_dict


def create_id_title_dict():
    """Creates a dictionary with each game id as a key and its title
       as a value

       Returns:
           game_title_dict = A dictionary {ID: Title} (dict)
    """
    game_data = DB.read_game_info()
    game_title_dict = {}

    for game in game_data:
        # "game" is a dict, "game_data" is a list of dicts
        # Line below gets the value of ID from "game" and uses it as
        # a key and sets its value as the value of "Title" from "game"
        game_title_dict[game["ID"]] = game["Title"]

    return game_title_dict


def num_of_rents_per_genre():
    """Calculates the total number of rentals per genre from
       rental history, including both past and active rentals

       Returns:
           game_genre_count_dict = A dictionary {Genre: Count}
                                   (dict)
    """
    rental_info_lines = DB.read_file(rental_file_path)
    game_genre_dict = create_id_genre_dict()
    game_genre_count_dict = {}

    current_date = datetime.now()
    
    for line in rental_info_lines[1:]:
        game_id, _, _, _ = line.strip().split(",")
        # Gets the genre from each game that has been rented
        genre = game_genre_dict[game_id]
        # Increments the total count of the games rented with that genre
        game_genre_count_dict[genre] = game_genre_count_dict.get(genre, 0) + 1

    return game_genre_count_dict   


def num_of_rents_per_title(filtered_history_lines):
    """Calculates the total number of rentals per title from
       rental history, including both past and active rentals

       Parameters:
           filtered_history_lines = This is lines from the rental
                                    history file that have been filtered
                                    according to a certain date (list)

       Returns:
           game_title_count_dict = A dictiomary {Title: Count}
                                   (dict)
    """
    game_title_dict = create_id_title_dict()
    game_title_count_dict = {}

    for line in filtered_history_lines[1:]:
        game_id, _, _, _ = line.strip().split(",")
        # Gets the title from each game that has been rented
        title = game_title_dict[game_id]
        # Increments the total count of the games rented with that genre
        game_title_count_dict[title] = game_title_count_dict.get(title, 0) + 1
    return game_title_count_dict


def display_price_of_games():
    """Extracts the purchase price from the game info database file
       and takes the value to create a dictionary.

        Returns:
            purchase_price_dict = A dictionary {Title: Price} (dict)
    """
    game_info_lines = DB.read_file(game_file_path)
    purchase_price_dict = {}
    for line in game_info_lines[1:]:
        _, _, _, title, purchase_price, _ = line.strip().split(",")
        purchase_price_dict[title] = purchase_price
    return purchase_price_dict


def rental_history_filtered_by_date(time_period):
    """Filters the rental history that is used for representation
       by the last 6 months or the last 12 months or returns all
       time history

       Parameters:
           time_period = This is the inputted time period that they
                         want to filter by (str)

        Returns:
            filtered_history = A list of lines containing each
                               rental record (list)
    """
    rental_info_lines = DB.read_file(rental_file_path)

    filtered_history = []

    current_date = datetime.now()
    
    if time_period == "6":
        # Calculates the date 6 months before todays date
        cut_off_date = current_date - timedelta(days=6 * 30)
    elif time_period == "12":
        # Calculates the date a year before todays date
        cut_off_date = current_date - timedelta(days=12*30)
    else:
        return rental_info_lines[1:]

    for line in rental_info_lines[1:]:
        _, rent_date, _, _ = line.strip().split(",")
        # Converts the date into the same format so it can be used
        # in comparison
        converted_rent_date = datetime.strptime(rent_date, "%d/%m/%Y")
        if converted_rent_date > cut_off_date:
            filtered_history.append(line)
    return filtered_history
    

#########################################################
#        Functions for calculating the optimal game     #
#        recommendations including weightings, and      #
#        combined scores.                               #
#########################################################
def calculate_weights_for_games(filtered_history_lines):
    """Calculates normalised values for popularity and price for each
       game so that they can be used together for comparison

       Parameters:
           filtered_history_lines = This is lines from the rental
                                    history file that have been filtered
                                    according to a certain date (list)

       Returns:
           normalised_popularity_values = {title: normalised value}
                                          (dict)
           normalised_price_values = {title: normalised value}
                                     {dict}
    """
    rents = num_of_rents_per_title(filtered_history_lines)
    rental_counts = []
    prices = display_price_of_games()
    game_prices = []
    
    for key in rents:
        rental_counts.append(rents[key])
    
    for key in prices:
        game_prices.append(int(prices[key]))

    min_popularity = min(rental_counts)
    max_popularity = max(rental_counts)
    min_price = min(game_prices)
    max_price = max(game_prices)

    normalised_popularity_values = {}

    if max_popularity == min_popularity:
        for key in rents:
            normalised_popularity_values[key] = 1
    
    else:
        for key in rents:
            normalised_popularity_values[key] = (
                rents[key] - min_popularity)/(max_popularity - min_popularity)

    normalised_price_values = {}
    
    for key in prices:
        normalised_price_values[key] = (
            max_price - int(prices[key]))/(max_price - min_price)
        
    return normalised_popularity_values, normalised_price_values


def calculate_combined_score(popularity_weight, pricing_weight,
                             normalised_popularity_values,
                             normalised_price_values):
    """Takes the normalised values for popularity and price and uses
        them to create a combined score which can be used for a final
        comparison

        Parameters:
            popularity_weight = The weighting decided by the user (How
                                important popularity is to them) (int)
            pricing_weight = The weighting decided by the user (How
                             important price is to them) (int)
            normalised_popularity_values = {title: normalised value}
                                              (dict)
            normalised_price_values = {title: normalised value}
                                         {dict}

        Returns:
            combined_scored = {title: score} (dict)
        
    """
    pop_weight = popularity_weight
    price_weight = pricing_weight
    combined_score = {}

    for title in normalised_popularity_values:
        pop_score = normalised_popularity_values.get(title)
        price_score = normalised_price_values.get(title) 

        combined_score[title] = (
            pop_score * pop_weight) + (price_score * price_weight)
        
    return combined_score


def budget_recommendation(budget, combined_score):
    """Orders the games by top 3 scores (in other words most important
       according to the weighting chose by user) and then creates a
       recommendation of how many copies of those games you should
       and can buy with the budget provided.

       Parameters:
           budget = Budget allowed to buy games (int)
           combined_scored = {title: score} (dict)

       Returns:
           recommendations = {title: num of copies recommended to buy}
                             (dict)
      
    """
    # Using .items() on a dictionary gives a view in the from of
    # a list of tuples, e.g [(name, price), (name, price)]
    # Then the inline lambda function says to use the second element
    # of the tuple "x[1]" to be used for the sorted() function
    # dict() then converts the sorted view back into a dictionary
    combined_score_ordered = dict(sorted(combined_score.items(), key=lambda x: x[1],
                                   reverse=True))
    remaining_budget = budget    
    max_num_of_games = 3
    top_three_games = {}
    count = 0
    prices = display_price_of_games()
    recommendations = {}
    
    for i in combined_score_ordered:
        if count == 3:
            break
        top_three_games[i] = combined_score_ordered.get(i)
        count += 1
    loop = True
    
    while loop:
        for i in top_three_games:
            if remaining_budget == 0:
                return recommendations
            remaining_budget = remaining_budget - int(prices.get(i))
            if remaining_budget < 0:
                loop = False
                return recommendations
            recommendations[i] =  recommendations.get(i, 0) + 1
    return recommendations

#################################################
#        Functions for graph visualisation      #
#################################################
def get_values_for_bar_chart():
    """Retrieves the dictionary needed to extract values from
       in order to create a bar chart

       Returns:
           rents = A dictiomary {Title: Count}
                   (dict)
    """
    lines = DB.read_file(rental_file_path)
    rents = num_of_rents_per_title(lines)

    return rents
    
def bar_chart_count_per_title(rents):
    """Creates a bar chart with title on the x-axis and rental
       count on the y-axis.

       Parameters:
           rents = A dictiomary {Title: Count}
                   (dict)
    """
    y = []
    for key in rents:
        y.append(rents[key])
    x = list(rents.keys())
    plt.figure(figsize=(14, 7))
    plt.bar(x, y, label="Number of rents by title", color="black")
    plt.xlabel("Title")
    plt.ylabel("Rents")
    plt.xticks(rotation=90, ha='right')
    plt.title("Number of Rentals per Game Title")
    plt.legend(loc="upper right")
    plt.tight_layout()
    plt.show()


def plot_weighted_scores(price_weight, popularity_weight,
                         filtered_history_lines):
    """Plots a bar chart with title on the x-axis and combined
       score on the y-axis

       Parameters:
           price_weight = The weighting decided by the user (How
                             important price is to them) (int)
           popularity_weight = The weighting decided by the user (How
                                important popularity is to them) (int) 
    """
    pop, prices = calculate_weights_for_games(filtered_history_lines)
    combined_score = calculate_combined_score(popularity_weight,
                                              price_weight, pop, prices)
    y = []
    for key in combined_score:
        y.append(combined_score[key])
    x = list(combined_score.keys())
    plt.figure(figsize=(16, 8))
    plt.bar(x, y, color="black")  
    plt.xlabel("Title")
    plt.ylabel("Score")
    plt.xticks(rotation=90, ha='right')
    plt.title("Best Game Choices: Balancing Popularity \n"
              "and Price Based on Your Preferences")  
    plt.legend(["Combined Score"], loc="upper right")  
    plt.tight_layout()
    plt.show()


def values_for_pie_and_bar_chart():
    """Obtains all the values needed to plot a pie chart for
       genre and rental count, and then a bar chart breaking
       down the rental counts per title of the genre with the
       highest count

       Returns:
           genres = list of genres (list)
           rents = list of rental counts for each genre (list)
           max_genre = genre with the highest number of rents (str)
           title_rents = A dictionary {title: count} (dict)
           game_genre_dict = {ID: Genre} (dict)
           game_title_dict = {ID: Title}
    """
    genre_rents = num_of_rents_per_genre()
    genres = list(genre_rents.keys())
    rents = list(genre_rents.values())

    # Finds largest wedge of the pie (most popular genre)
    max_genre_index = rents.index(max(rents))
    max_genre = genres[max_genre_index]

    filtered_lines = DB.read_file(rental_file_path)
    title_rents = num_of_rents_per_title(filtered_lines) # {Title: count}
    
    # Filter the titles belonging to the largest genre
    game_genre_dict = create_id_genre_dict() # {ID: Genre}
    game_title_dict = create_id_title_dict() # {ID: Title}
    
    return genres, rents, max_genre, title_rents, game_genre_dict, game_title_dict


def pie_chart_popularity_per_genre(genres, rents, max_genre, title_rents,
                                   game_genre_dict, game_title_dict):
    """Creates a pie chart showing popularity per genre and then
       creates a bar chart breaking down the largest
       genre by title and rental count.

       Parameters:
           genres = list of genres (list)
           rents = list of rental counts for each genre (list)
           max_genre = genre with the highest number of rents (str)
           title_rents = A dictionary {title: count} (dict)
           game_genre_dict = {ID: Genre} (dict)
           game_title_dict = {ID: Title}
    """

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    fig.subplots_adjust(wspace=0.5)

    wedges, _, autotexts = ax1.pie(
        rents, autopct="%1.1f%%", startangle=90,
        colors=plt.cm.tab10.colors, wedgeprops=dict(edgecolor='black', linewidth=1.5)
    )
    ax1.legend(wedges, genres, title="Genres", loc="center left", bbox_to_anchor=(1, 0, 0.2, 1))
    ax1.set_title("Popularity per Genre")


    max_genre_titles = {}
    title_to_genre_id = {}

    for genre_id, title in game_title_dict.items():
        title_to_genre_id[title] = genre_id # {Title: Genre}

    for title, count in title_rents.items():
        genre_id = title_to_genre_id.get(title) 

        if genre_id is not None and game_genre_dict.get(genre_id) == max_genre:
            max_genre_titles[title] = count

    titles = list(max_genre_titles.keys())
    counts = list(max_genre_titles.values())
    total_count = sum(counts)

    # Creates bar chart displaying breakdown of the most popular genre
    ax2.barh(titles, counts, color='C0', alpha=0.7)
    ax2.set_title(f"Breakdown of \"{max_genre}\" by Title")
    ax2.set_xlabel("Rental Count") 

    plt.tight_layout()

    plt.show()


#########################################################
#        Functions to coordinate the whole              #
#        recommendation and visualisation process       #
#########################################################
def recommend_top_genre():
    """Finds the genre with the most amount of rents

       Returns:
           max_genre = name of the genre with the most rents (str)
    """
    genre_rents = num_of_rents_per_genre()
    genres = list(genre_rents.keys())
    max_genre_index = rents.index(max(rents))
    max_genre = genres[max_genre_index]
    return max_genre
    
def coordinate_process(months, popularity_weight, price_weight, budget):
    """Coordinates the whole process of calculating and displaying
       results from combined weighted scores

       Parameters:
           months = The time period that the user wants to filter histoy
                    by (str)
           popularity_weight = The weighting decided by the user (How
                                important popularity is to them) (int)
           price_weight = The weighting decided by the user (How
                             important price is to them) (int)
           budget = Budget for purchasing new games (int)

       Returns:
           string,string,string = Error message and two empty strings
                           (str, str, str)
           string, recommened, lines = empty string, recommended games
                                       for purchase, and rental history
                                       lines (str, dict, list)
    
    """
    if budget <= 0:
        return "Warning: No budget entered", "", ""
    if months != "6" and months != "12" and months.lower() != "all":
        return "Invalid time period inputted", "", ""
    if (popularity_weight + price_weight) != 1:
        return "Warning: Your weights must add to a total of one", "", ""
    
    lines = rental_history_filtered_by_date(months)
    pop, prices = calculate_weights_for_games(lines)
    test = calculate_combined_score(popularity_weight, price_weight, pop,
                                    prices)
    recommended = budget_recommendation(budget, test)
    return "", recommended, lines


if __name__ == "__main__":
    (genres, rents, max_genre,
     title_rents, game_genre_dict,
     game_title_dict
    ) = values_for_pie_and_bar_chart()
    pie_chart_popularity_per_genre(genres, rents, max_genre, title_rents,
                                   game_genre_dict, game_title_dict)
    rents = get_values_for_bar_chart()
    bar_chart_count_per_title(rents)
    months = input("How many months: ")
    price_weight = float(input("Enter the weighting for price: "))
    popularity_weight = float(input("Enter the weighting for popularity "))
    budget = int(input("Enter a budget: "))
    error_message, recommended, lines = coordinate_process(months, popularity_weight,
                                                           price_weight, budget)
    if lines != "" and recommended != "":
        print(recommended)
        plot_weighted_scores(price_weight, popularity_weight, lines)
    else:
        print(error_message)

# Test cases: months, price weight, popularity weight,  Budget (reason)
# Test case 1: 6,0.5,0.5,"" (checks empty budget input(GUI only))
# Test case 2: 6,0.5,0.5,0 (checks 0 as budget input (GUI only))
# Test case 3: 13,0.5,0.5,100 (Checks invalid time period (Console only))
# Test case 4: "",0.5,0.5,100 (Checks empty time period input (Console only))
# Test case 5: 12,1,0.5,100 (Checks error for weightings not adding to 1 (Console only))
# Test case 6 GUI: Press By Title Button (Should display barchart)
# Test case 7 GUI: Press by Genre Button (Should display pie chart and bar chart)

