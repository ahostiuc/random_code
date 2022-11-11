'''O(n) solution to 538's Nov 11th Classic Riddler, via MC simulation
'''

import numpy as np

# number of events in the sim
n_evts = 1000000000

# counter of reasonable cuts, and area of the smaller piece
count_reasonable = 0
area = 0

for i in range(n_evts):

    random_1 = np.random.random_sample()
    random_2 = 4*np.random.random_sample()
    
# if the 2 points are on the same side, area is 0
    if random_2<1:
        area = 0

# if the 2 points are on perpendicular sides, area is computed as below
# of course we could condense the next 2 cases by symmetry, 
# as the area > 0.25 yields the same answer for either
# but this more explicit and perhaps more instructional

    elif 1<random_2<2:
        area = (1-random_1)*(random_2-1)/2

    elif 3<random_2<4:
        area = (random_1)*(4-random_2)/2

# if the points are on opposing sides, find the point closest to a corner, 
# calculate the distance and implicitly multiply by 1, length of an unit square, 
# since we can always rescale by a factor of the sandwich's side length
# then, calculate the area of the rectangle defined by the sides and the 2 points & divide by 2
# add to the rest of minimum dist to find the smallest area

    else:
        minimum_dist_from_corner = min(random_1,1-random_1,random_2-2,3-random_2)
        area = abs((1-random_1)-(random_2-2))/2+minimum_dist_from_corner

#in all cases, if area is larger than 0.25, the cut is reasonable

    if area > 0.25:
        count_reasonable += 1
        
#compute percent of events passing with reasonable slices

print("The probability is "+str(count_reasonable/n_evts*100)+"%")
