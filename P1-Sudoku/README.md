# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: To solve the naked twins problem, we perform check for twins/triplets in every units. Since twins/triplets means their values are their only possible values, then remaining boxes in the respective unit should not use those values.
The implementation is as follows.
```python
    for box in values.keys():
        for box_units in units[box]:
            twins = [unit for unit in box_units if values[box] == values[unit]]
            if len(twins) > 1 and len(twins) == len(values[box]):
                for unit in box_units:
                    if unit not in twins:
                        for value in values[box]:
                            values[unit] = values[unit].replace(value, "")
    return values
```

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: To solve the diagonal sudoku problem, we need to slightly modify how we validate the grid in which we add the diagonal validation in the grid validation.
The implementation is as follows.
```python
    left_diag_units = [[a+b for (a, b) in list(zip(rows[::-1], cols))]]
    right_diag_units = [[a+b for (a, b) in list(zip(rows, cols))]]
    unitlist = row_units + column_units + square_units + left_diag_units + right_diag_units
```

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

To visualize your solution, please only assign values to the values_dict using the `assign_value` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login) for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

