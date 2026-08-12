Student ID: F329597 Date Completed: Augsut-September 2024

Setup:
1) Download the zipped file named "F329597_Project"
2) Unzip and extract the folder in a location of your choosing
3) Once the folder is extracted open the command prompt and navigate to the         installation directory and then enter "jupyter notebook"
   This should launch notebook in a browser, then locate the "F329597_Project" folder
4) From that folder open "menu.ipynb" in jupyter notebook.
(Folder contains package called "scripts" which contains all the python 
modules created by me including an __init__.py file.)


Special Information/Instructions:
All test cases are included at the end of each module code including console only and GUI only test cases as well as cases which can be used in either console or GUI. (database.py file has no test cases, some testing functionality is included)
E.g gameRent File first test case:
#Test cases: customer_id,game_id (reason)
#Test case 1: "",_  (Checking empty customer inputs)

Testing functionality for every function is included in the modules apart from functions which edit the database, those functions are tested by console inputs in each module and checking the database files after to see if those functions function correctly (All have been tested and work).

Task 1.6 gameSelect.py, a blank input for time period refers to all time. If budget 
is too low for any of the top 3 games retrieved from my algorithm then no game will be recommended for purchase and no visualisation will be done. E.g if budget entered is £10 and top 3 games all cost £15 then no recommendations will be made.  The two analysis charts (in the black box) are not based on any input parameters.
Recommended to do minimum £100 budget to gurantee a result everytime. (Smallest budget that can work is £5 but depends on your weightings) 

Initially I wanted to keep all the data files in the data subfolder however due to being unable to change the path location in the subscriptionManager.pyc compiled file I had to keep subscription_info.txt seperate and place it in the root directory so that the compiled file was able to locate it correctly. If I was to improve the readability and tidy up the data I would keep all the data files in one folder and edit the subscriptionManager file so that it extended its path to be able to access the text file.


Proud of:
gameSelect.py: My algorithm which takes weightings for both popularity and price based on what the user thinks is more important to them. It uses that to create
a combined score for each game allowing significant improvement in future game purchase recommendations. E.g if they have a low budget then you would input a higher price weighting meaning how expensive a game is, is more important than how popular a game is. Also proud of my visualisation charts for various factors.
I am also proud of the GUI tab layout and the simple but effective HCI.

At time of submission no errors were found, should be error free for every module.