'''XT WC2022 prediction league calculator
Display results, calculate round scores and display them, calculate standings and display,
calculate round winner and display all round winners
'''

import sys
import numpy as np

#input round number when running python

round = int(sys.argv[1])

#get number of participants and number of games (fixed)

list_part = ['foresta','ToniSamp','AndyChrist','Beaux Balkans','DinamoBuc','szövkap']

n_part = len(list_part)
n_games = 8

file1 = open('predictions_round_'+str(round)+'_WC.txt', 'r')
lines = file1.readlines()

#for all rounds except first, get information from previous round

if round != 1:
    file2 = open('standings_round_'+str(round-1)+'_WC.txt', 'r')
    standings = file2.readlines()

f3 = open('standings_round_'+str(round)+'_WC.txt', 'w')

result = []
prediction = []
list_to_sort = []
list_names = []

#get active participants' names from input text files

for n in range(6):
    list_names.append(lines[(n_games+1)*(n+1)].rstrip())
    
n_active_part = len(list_names)

print("list: ",list_names)

#get actual results to compare predictions against

for n in range(n_games):
    result.append(lines[n+1].split(" ")[-1].rstrip())

#print results to screen & to file

print("Results:")
f3.write("Results: \n")

for n in range(n_games):
    print(lines[n+1].rstrip())
    f3.write(lines[n+1])
    
# initialize scores: 
# score is the round score
# bonus score is the score in the bonus game, needed to track round winners
# total score is the total score
# current round score and bonus score: calculate only for active participants

score = np.zeros(n_active_part)
bonus_score = np.zeros(n_active_part)
total_score = np.zeros(n_part)


#calculate each round score/bonus score

for i in range(len(list_names)):
    prediction.clear()
    for j in range(n_games):
    
        #parse predictions

        if lines[(1+n_games)*(i+1)+j+1].split(" ")[-1].rstrip()[1] == '-':
            prediction.append(lines[(1+n_games)*(i+1)+j+1].split(" ")[-1].rstrip())
        elif len(lines[(1+n_games)*(i+1)+j+1].split(" ")[1].rstrip()) == 3:
            if lines[(1+n_games)*(i+1)+j+1].split(" ")[1].rstrip()[1] == '-':
                prediction.append(lines[(1+n_games)*(i+1)+j+1].split(" ")[1].rstrip())
        elif len(lines[(1+n_games)*(i+1)+j+1].split(" ")[2].rstrip()) == 3:
            if lines[(1+n_games)*(i+1)+j+1].split(" ")[2].rstrip()[1] == '-':
                prediction.append(lines[(1+n_games)*(i+1)+j+1].split(" ")[2].rstrip())
        print(i,prediction)

        #compare predictions to results and calculate the scores
        #bonus game indicated by tilde 
        
        print(result[j], prediction[j])
        if result[j] == prediction[j]:
            if lines[(1+n_games)*(i+1)+j+1].split(" ")[0][0] == "~":
                score[i] += 4
                bonus_score[i] += 4
            else:
                score[i] += 2
            
        elif ((result[j].split("-")[0]>result[j].split("-")[1].rstrip()) and (prediction[j].split("-")[0]>prediction[j].split("-")[1].rstrip())) or ((result[j].split("-")[0]==result[j].split("-")[1].rstrip()) and (prediction[j].split("-")[0]==prediction[j].split("-")[1].rstrip())) or ((result[j].split("-")[0]<result[j].split("-")[1].rstrip()) and (prediction[j].split("-")[0]<prediction[j].split("-")[1].rstrip())): 
            if lines[(1+n_games)*(i+1)+j+1].split(" ")[0][0] == "~":
                score[i] += 2
                bonus_score[i] += 2
            else:
                score[i] += 1
        else:
            score[i] += 0
            
        #R16 round gets an extra factor of 2
        
        if round == '7':
            score[i] *= 2
        
        #final round gets an extra factor of 4
        
        if round == '8':
            score[i] *= 4

#sort list of names by score

list_to_sort = zip(list_names,score,bonus_score)

sorted_list = sorted(list_to_sort,key=lambda l:l[1],reverse=True)

#initialize winner list, tiebreaker information

winner = []
tiebreaker_bonus = []
tiebreaker_name = []

#get winner and add info

tiebreaker_bonus.append(int(sorted_list[0][2]))
tiebreaker_name.append(sorted_list[0][0])

#if same score for more than 1 participant, add their info to tiebreakers

for n in range(n_active_part-1):
    if (int(sorted_list[0][1]) == int(sorted_list[n+1][1])):
        tiebreaker_bonus.append(int(sorted_list[n+1][2]))
        tiebreaker_name.append(sorted_list[n+1][0])
        
#sort list by tiebreaker bonus

list_to_sort_tie = zip(tiebreaker_name,tiebreaker_bonus)

sorted_list_tie = sorted(list_to_sort_tie,key=lambda l:l[1])

# get winner(s) and write to list

winner.append(sorted_list_tie[0][0])

for n in range(1,len(sorted_list_tie)):
    if (sorted_list_tie[0][1] == sorted_list_tie[n][1]):
        winner.append(sorted_list_tie[n][0])

#output Round's Rankings to screen & file

print('\n')
f3.write('\n')
print("Round's Rankings:")
f3.write("Round's Rankings: \n")
for n in range(n_active_part):

#     print out winner(s) with stars, and then other participants 
    
    if n == 0:
        f3.write(str(sorted_list[n][0])+" "+str(int(sorted_list[n][1]))+" :star: \n")
        print(sorted_list[n][0], int(sorted_list[n][1]), ":star:")
        
    # you only get a star if the points & tiebreaker info is the same as the winner's
    
    elif int(sorted_list[n][1]) == int(sorted_list[0][1]) and int(sorted_list[n][2]) == int(sorted_list[0][2]):
        f3.write(str(sorted_list[n][0])+" "+str(int(sorted_list[n][1]))+" :star: \n")
        print(sorted_list[n][0], int(sorted_list[n][1]), ":star:")

    else:
        f3.write(str(sorted_list[n][0])+" "+str(int(sorted_list[n][1]))+"\n")
        print(sorted_list[n][0], int(sorted_list[n][1]))
        
#   keep track of everyone's total score

    total_score[n] += int(sorted_list[n][1])

print('\n')
f3.write('\n')

#initialize list for overall standings && calc line_offset needed to read data from file

list_for_standings = []
line_offset = 1+n_games+1+1+n_active_part+1


# if it's the first round, just append the scores directly; otherwise, search for 
# name of participant and their score, and add prev. score to compute total score

if round == 1:
    for n in range(n_active_part):
#         for i in range(n_part):
        list_for_standings.append(sorted_list[n][0])
    
else:
    for n in range(n_active_part):
        for i in range(n_part):
    #         print(standings[17+i])
            if(sorted_list[n][0] == standings[line_offset+i].split(" ")[0]):
                print(sorted_list[n][0],standings[line_offset+i].split(" ")[0],standings[line_offset+i].split(" ")[1])
                total_score[n] += int(standings[line_offset+i].split(" ")[1])
    #     print(sorted_list[n][0], int(total_score[n]))
        list_for_standings.append(sorted_list[n][0])

#sort list of parts by total score

list_to_sort_2 = zip(list_for_standings,total_score)

sorted_list_2 = sorted(list_to_sort_2,key=lambda l:l[1],reverse=True)

#print standings

print("Standings:")
f3.write("Standings: \n")
for n in range(n_part):
#     print(lines[(8+1)*(n+1)].rstrip(),int(score[n]))
    print(n+1,". ",sorted_list_2[n][0]," ",int(sorted_list_2[n][1]),sep='')
    f3.write(str(n+1)+". "+str(sorted_list_2[n][0])+" "+str(int(sorted_list_2[n][1]))+'\n')
print('\n')
f3.write('\n')

#print round winners, with correct line offset to get previous round winners from file

print("Round Winners:")
f3.write("Round Winners: \n")

line_offset_2 = line_offset + n_part + 3

for n in range(round-1):
    print((str(standings[line_offset_2+n])))
    f3.write(str(standings[line_offset_2+n]))

#get number of winners and output correctly to screen & file

n_winners = len(winner)

if n_winners == 1:
    print(round,": ",winner[0]," (",int(sorted_list[0][1]),")",sep="")
    f3.write(str(round)+": "+str(winner[0])+" ("+str(int(sorted_list[0][1]))+")\n")
elif n_winners == 2:
    print(round,": ",winner[0],", ",winner[1]," (",int(sorted_list[0][1]),")",sep="")
    f3.write(str(round)+": "+str(winner[0])+", "+str(winner[1])+" ("+str(int(sorted_list[0][1]))+")\n")
elif n_winners == 3:
    print(round,": ",winner[0],", ",winner[1],", ",winner[2]," (",int(sorted_list[0][1]),")",sep="")
    f3.write(str(round)+": "+str(winner[0])+", "+str(winner[1])+", "+str(winner[2])+" ("+str(int(sorted_list[0][1]))+")\n")
elif n_winners == 4:
    print(round,": ",winner[0],", ",winner[1],", ",winner[2],", ",winner[3]," (",int(sorted_list[0][1]),")",sep="")
    f3.write(str(round)+": "+str(winner[0])+", "+str(winner[1])+", "+str(winner[2])+", "+str(winner[3])+" ("+str(int(sorted_list[0][1]))+")\n")

