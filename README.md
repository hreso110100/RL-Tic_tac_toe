# Tic-Tac-Toe bots using reinforcement learning algorithms

This project contains python implementation of bots, which are able to play Tic-Tac-Toe game at human level on the game board of size 3x3 and more.  

**Included reinforcement learning algorithms:** 

1. SARSA
2. Q-learning
3. Approximate Q-learning
4. TD(0)
5. DDQN

**How to use application:** 

Application is designed to train bots, monitor progress of training and also to verify trained bots against various type of opponents.

To start application run Main.py (Use at least Python 3.6)

At settings screen you can select size of board, type of agent algorithm to train and type of opponent.
Here you are also able to load already trained bots from pickle files located in **trained_bots folder**.

After pressing train button, application will start displaying progress of training, once training is completed you will find graphs displaying total reward over episodes under **graphs folder**.

On the last screen you can verify your trained bot against yourself. First move is randomly given by game.

**List of dependencies:** 

<ul>
<li>pickle</li>
<li>pygame</li>
<li>itertools</li>
<li>matplotlib</li>
<li>numpy</li>
</ul>
