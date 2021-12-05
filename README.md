# CISC474_EuchreProject
By Adam Farley and Grace Smith

This project is our attempt at making a Reinforment Learning based Euchre Player using Q-Learning and a linear function approximator. There are multiple files, please use this as a guide to figure out which ones you'd need to run to accurately test it on your own.

The only files that should be run are Game.py and Game_Lone_Wolf.py, all other files contain helper functions and logic to facilitate the proper running of Euchre games through Game.py and Game_Lone_Wolf.py.

## Repo Structure
dumb_player.py contains the logic for non-learning agents. There are three strategies the non-learning agents can take of varying difficulty.
They can either play ranomdly, greedily, or a strategic form of greediness where they're only greedy if they have a realistic chance of winning the trick.

Deck.py contains functions and classes that encapsulate how a deck of cards should behave. This includes shuffling and dealing of the deck to the players.

rules.py contains a series of logical tests and card comparison functions to help enforce the rules of Euchre (specifically around how trumps and lead cards behave)

Game.py uses Feature_Approximation.py to run a standard game of Euchre with two sets of partners. Game.py contains all of the logic for training and learning, Feature_Approximation.py contains all of the feature realted code for our linear approximation.

Game_Lone_Wolf.py and Feature_Lone_Wolf are very similar to their non-Lone-Wolf counterparts, the main difference being that in these files there are no partners, these files implement a four way free for all version of Euchre. This was made after seeing poor learning results in the vanilla Euchre that Game.py implements. We thought that it might be because the learning agent's partner was playing so poorly that the learning agent's play could not influence the result of the game no matter how well it played. In a free for all, the learning agent's play would not be hindered by a non-learning partner so we hypothesized that the agent would show better results. This ended up not being correct, but we kept these filse in the repo for completness of our process.

## Running the repo
To run either version of Euchre (vanilla or lone wolf), simply run the Game.py file for that particular version. The final line in either file will allow you to toggle between the type of non-learning agent used and the hyperparameters of the learning agent (alpha, epsilon, and gamma). For example, game_setup(greedy_choice, 0.1, 0.1, 0.8) runs a greedy agent with alpha=0.1, epsilon=0.1, and gamma=0.8
