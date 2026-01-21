import csv
from common import *

# labels = ["elapsed_time","set_no","game_no","point_no","p1_sets","p2_sets","p1_games","p2_games","p1_score","p2_score","server","serve_no","point_victor","p1_points_won","p2_points_won","game_victor","set_victor","p1_ace","p2_ace","p1_winner","p2_winner","winner_shot_type","p1_double_fault","p2_double_fault",'p1_unf_err','p2_unf_err','p1_net_pt','p2_net_pt','p1_net_pt_won','p2_net_pt_won','p1_break_pt','p2_break_pt','p1_break_pt_won','p2_break_pt_won','p1_break_pt_missed','p2_break_pt_missed','p1_distance_run','p2_distance_run','rally_count','speed_mph','serve_width','serve_depth','return_depth']

def readFile():
    rawData = []
    with open(fileName, "r") as dataSheet:
        csvReader = csv.reader(dataSheet)
        for row in csvReader:
            rawData.append(row)
    return rawData

def preProcessing(raw):
    # data = [raw[0]]
    data=[]
    raw.remove(raw[0])
    for row in raw:
        row[0] = row[0][-4:]

    match = [] # temp storage for one match
    _set = [] # temp storage for one set
    game = [] # temp storage for one game
    for i in range(len(raw)):
        game.append(raw[i][3:])

        if raw[i][15 + 3] != "0": # end of one game
            for points in game: # use 1, 2, and 3 to replace original scores for easier calculation afterwards
                if points[8] in pointDict:
                    points[8] = pointDict[points[8]]
                if points[9] in pointDict:
                    points[9] = pointDict[points[9]]
            
            _set.append(game)
            game = []

        if raw[i][16 + 3] != "0": # end of one set
            match.append(_set)
            _set = []

        if i != 0 and raw[i][0] != raw[i - 1][0]: # end of one match
            match.insert(0, tuple(raw[i - 1][:3]))
            data.append(match)
            match = []

        if i == len(raw) - 1: # end of file
            match.insert(0, tuple(raw[i - 1][:3]))
            data.append(match)
    
    return data

'''
content of data:
[
(match_id	player1	player2)	[elapsed_time	set_no	game_no	point_no	p1_sets	p2_sets	p1_games	p2_games	p1_score	p2_score	server	serve_no	point_victor	p1_points_won	p2_points_won
game_victor	set_victor	p1_ace	p2_ace	p1_winner	p2_winner	winner_shot_type	p1_double_fault	p2_double_fault	p1_unf_err	p2_unf_err	p1_net_pt	p2_net_pt	p1_net_pt_won	p2_net_pt_won
p1_break_pt	p2_break_pt	p1_break_pt_won	p2_break_pt_won	p1_break_pt_missed	p2_break_pt_missed	p1_distance_run	p2_distance_run	rally_count	speed_mph	serve_width	serve_depth	return_depth]
(one list for each game, one tuple for each match)
]
format:
data
|-matches
  |-sets
    |-games
      |-points

interprets for match terms:
index name                description                                                                     example
-     match_id            match identification                                                            "2023-wimbledon-1701 (""7"" is the round, and ""01"" the match number in that round)"
-     player1             first and last name of the first player                                         Carlos Alcaraz
-     player2             first and last name of the second player                                        Novak Djokovic
0     elapsed_time        time elapsed since start of first point to start of current point (H:MM:SS)     0:10:27
1     set_no              set number in match                                                             "1, 2, 3, 4, or 5"
2     game_no             game number in set                                                              "1, 2, ...,7"
3     point_no            point number in game                                                            "1, 2, 3... etc."
4     p1_sets             sets won by player 1                                                            "0, 1, or 2"
5     p2_sets             sets won by player 2                                                            "0, 1, or 2"
6     p1_games            games won by player 1 in current set                                            "0, 1,...,6"
7     p2_games            games won by player 2 in current set                                            "0, 1,...,6"
8     p1_score            player 1's score within current game                                            "0 (love), 15, 30, 40, AD (advantage)"
9     p2_score            player 2's score within current game                                            "0 (love), 15, 30, 40, AD (advantage)"
10    server              server of the point                                                             "1: player 1, 2: player 2"
11    serve_no            first or second serve                                                           "1: first serve, 2: second serve"
12    point_victor        winner of the point                                                             "1 if player 1 wins, 2 if player 2 wins"
13    p1_points_won       number of points won by player 1 in match                                       "0, 1, 2... etc."
14    p2_points_won       number of points won by player 2 in match                                       "0, 1, 2... etc."
15    game_victor         a player won a game this point                                                  "0: no one, 1: player 1, 2: player 2"
16    set_victor          a player won a set this point                                                   "0: no one, 1: player 1, 2: player 2"
17    p1_ace              player 1 hit an untouchable winning serve                                       0 or 1
18    p2_ace              player 2 hit an untouchable winning serve                                       0 or 1
19    p1_winner           player 1 hit an untouchable winning shot                                        0 or 1
20    p2_winner           player 2 hit an untouchable winning shot                                        0 or 1
21    winner_shot_type    category of untouchable shot                                                    "F: Forehand, B: Backhand"
22    p1_double_fault     player 1 missed both serves and lost the point                                  0 or 1
23    p2_double_fault     player 2 missed both serves and lost the point                                  0 or 1
24    p1_unf_err          player 1 made an unforced error                                                 0 or 1
25    p2_unf_err          player 2 made an unforced error                                                 0 or 1
26    p1_net_pt           player 1 made it to the net                                                     0 or 1
27    p2_net_pt           player 2 made it to the net                                                     0 or 1
28    p1_net_pt_won       player 1 won the point while at the net                                         0 or 1
29    p2_net_pt_won       player 2 won the point while at the net                                         0 or 1
30    p1_break_pt         player 1 has an opportunity to win a game player 2 is serving                   0 or 1
31    p2_break_pt         player 2 has an opportunity to win a game player 1 is serving                   0 or 1
32    p1_break_pt_won     player 1 won the game player 2 is serving                                       0 or 1
33    p2_break_pt_won     player 2 won the game player 1 is serving                                       0 or 1
34    p1_break_pt_missed  player 1 missed an opportunity to win a game player 2 is serving                0 or 1
35    p2_break_pt_missed  player 2 missed an opportunity to win a game player 1 is serving                0 or 1
36    p1_distance_run     player 1's distance ran during point (meters)                                   "5.376, 21.384, etc."
37    p2_distance_run     player 2's distance ran during point (meters)                                   "6.485, 12.473, etc."
38    rally_count         number of shots during the point                                                "1, 2, 4, etc. (includes serve)"
39    speed_mph           speed of serve (miles per hour; mph)                                            "81, 124, etc."
40    serve_width         direction of serve                                                              "B: Body, BC: Body/Center, BW: Body/Wide, C: Center, W: Wide"
41    serve_depth         depth of serve                                                                  "CTL: Close To Line, NCTL: Not Close To Line"
42    return_depth        depth of return                                                                 "D: Deep, ND: Not Deep"

special notes:
    points are changed to use continious numbers 1, 2, and 3 instead of 15, 30, and 40. "AD" is left untouched.
'''

# test program to test functionality of functions, won't be executed in actual run
if __name__ == "__main__":
    rawData = readFile()
    data = preProcessing(rawData)
    for match in data:
        for _set in match:
            if(type(_set) == tuple):
                print("a new match begins here\n", "# and players of this match:")
                print(_set, "\n\nbelow are the point records of this match:\n")
            else:
                for game in _set:
                    for point in game:
                        print(point)
                    print("\nend of game\n")
                print("end of set\n")
        print("end of match\n")