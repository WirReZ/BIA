import math
import random
import matplotlib.pyplot as plt
import numpy as np

# math globals
fabs = math.fabs
sin = math.sin
cos = math.cos
exp = math.exp
pi = math.pi

numsolutions = 3

lb = -5.0
ub = 5.0

testx = []
testy = []
test1x = []
test1y = []
# function
def func(x):

    return x * sin( x )
def funcplot(x):
    return x * np.sin( x )




# I am doing gradient ascent here, since I want to maximize the function
def grad_ascent(x):
    # scalar multiple for grad-ascent
    scalar = 0.5

    # central difference method to calculate gradient of the function
    delta = 0.5
    delta_x = (func(x + delta) - func(x - delta)) / (2.0 * delta)

    return x + (scalar * delta_x)


# Definition of the simple hill climbing search
def hill_climb(x, next_move):
    # starting point
    current = x

    # maximum number of times till it tries when
    # it gets stuck
    maxstuck = 10

    # initialize counter
    stuck = 0
    while True:
        current_val = func(current)

        next = next_move(current)

        # check the quality of the move
        if func(next) > current_val:

            current = next
            plt.scatter(current, funcplot(current))
        else:

            if stuck < maxstuck:


                stuck = stuck + 1

                current = next + (random.uniform(0.1, 0.5) * next)


                if current < lb:
                    current = lb

                if current > ub:
                    current = ub
            else:

                break

    return current, current_val


# the beginning
if __name__ == '__main__':

    t = np.arange(lb, ub, 0.01)
    plt.plot(t, funcplot(t), color='blue', linewidth=3,zorder=1)
    # to make results reproducible
    random.seed()


    x_init = []

    for i in range(numsolutions):
        val = lb + (ub - lb) * random.random()
        plt.scatter(val, funcplot(val),marker='s',c='blue',zorder=2)
        x_init.append(val)

    # Try to reach the highest point starting from
    # the different solutions
    for x in x_init:
        # start the procedure
        bestx, bestf = hill_climb(x, grad_ascent)

        print
        'Best {0:f} :: {1:f}'.format(x, bestf)

        plt.scatter(bestx,funcplot(bestx),marker='d',c='red',zorder=3)



    plt.show()