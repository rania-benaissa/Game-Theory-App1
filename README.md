# Game Theory App1

 An application that determines some game theory's notions in pure strategy games with at least two players.

# Description

This simple interactive application allows you to generate a game of more than two players in pure strategies and determines:

* Nash Equilibriums.
* Strictly and weakly dominant strategies of each player.
* Pareto optimality (as well as pareto dominant profiles).
* The security level of a strategy and a player.
* Equilibriums resulting from successive elimination of strongly and weakly dominated strategies.


# Technologies
To run this app, install:

* Python 3.*
* PyQt5
* Itertools
* Numpy
* QDarkStyle : is a dark stylesheet for Python and Qt applications. 

# Usage

To lunch the application, run _**Application.py**_ file:

![interface](/README_images/interface.jpg)

1. The user can change his game's players number, which updates the strategies table (table below).

2. The user must add each player's strategies separated by commas.

3. The _**Generate Profiles** button_ generates all the possible profiles from the strategies entered and inserts them in the payoffs table.

4. The _**Reset Game** button_ resets the game parameters (players, strategies and profiles).

5. When the user clicks on the _**Generate Profiles** button_, the possible profiles are inserted in the payoffs table, all that remains is to complete the table with the corresponding payoffs.

6. The  _**Start Game** button_  validates the payoffs table if it's correctly filled and displays the game's results.

7. The user can select the results to view.

8. This area displays the results of the performed calculations.

# Exemple

Let's consider the following three players game:

![interface](/README_images/players.jpg)


To which we match the payment table below:

![interface](/README_images/table.png)

Now that the game is launched, we will visualize some results:

## Nash Equilibriums

![interface](/README_images/nash.jpg)

## Pareto Optimality

![interface](/README_images/pareto.jpg)

## Equilibriums resulting from successive elimination of strongly dominated strategies

![interface](/README_images/equilibre.jpg)