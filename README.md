# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: *Student should provide answer here*
The constraint here is that if two boxes with only two letters left in the same unit has the same value, 
all other boxes in the same unit cannot have these two numbers as candidate. If we apply this constraint 
to the sudoku board, we could reduce the candidates for other boxes. 
To find twins in the board, just simply loop through all the units, find the two boxes that have two and 
only two candidates left and have same value as each other. Then for all other boxes in the same unit, 
remove these two numbers from candidates.
Do so until there is no more naked twins on the board.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: *Student should provide answer here*
Other than all the constraints mentioned in the course, I also applied one more constraint: hidden twins, which I got 
the idea of from this reference as "Hidden Twin exclusion rule":
http://www.sudokudragon.com/sudokustrategy.htm
Hidden-twins constraint is that basically find two boxes in a unit where two digits both and only are these two boxes' 
candidates. Then assign only the two digits as the two boxes' only candidates.
The constraints I applied here are elimination, only choice,naked twins and hidden twins. Loop through the board, find
candidates that could be eliminated by using these three constrains, until the board doesn't change any more.
That is the constraint propagation. And if the board is left unsolved, then use search to try out the candidate
until found a solution.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

