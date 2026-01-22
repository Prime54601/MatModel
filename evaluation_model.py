import matplotlib.pyplot as plt

from common import *
from readFile import *
from functools import lru_cache

def counter():
    n = 0
    n += 1
    yield n

@lru_cache(None)
def Eval(Pa, Pb, server, qa, qb):
    if Pa - Pb >= 2 and Pa >= 4:
        return 1
    if Pb - Pa >= 2 and Pb >= 4:
        return 0
    if Pa == Pb and Pa >= 3:
        p = qa if server == "A" else (1 - qb)
        if server != "A":
            t = qa
            qa = qb
            qb = t
        return qa**2 / (qa**2 + (1 - qb)**2)
    else:
        p = qa if server == "A" else (1 - qb)
        return (p * Eval(Pa + 1, Pb, server, qa, qb) + (1 - p) * Eval(Pa, Pb + 1, server, qa, qb))

@lru_cache(None)
def Eval_tiebreaker(Pa, Pb, initserver, qa, qb, rounds):
    if rounds == 1 or ((rounds - 2) // 2) % 2 == 1:
        server = initserver
    else:
        server = "B" if initserver == "A" else "A"
    if Pa - Pb >= 2 and Pa >= 7:
        return 1
    if Pb - Pa >= 2 and Pb >= 7:
        return 0
    if Pa == Pb and Pa == 6:
        # if rounds > 101:
        #     return qa**2 / (qa**2 + (1 - qa)**2) if server == "A" else 1 - qb**2 / (qb**2 + (1 - qb)**2)
        # else:
        #     p = qa if server == "A" else (1 - qb)
        #     return (p * Eval_tiebreaker(Pa + 1, Pb, initserver, qa, qb, rounds + 1) + (1 - p) * Eval_tiebreaker(Pa, Pb + 1, initserver, qa, qb, rounds + 1))
        if server != "A":
            t = qa
            qa = qb
            qb = t
        return (qa * (1 - qb)) / (qa * (1 - qb) + qb * (1 - qa))
    else:
        p = qa if server == "A" else (1 - qb)
        return (p * Eval_tiebreaker(Pa + 1, Pb, initserver, qa, qb, rounds + 1) + (1 - p) * Eval_tiebreaker(Pa, Pb + 1, initserver, qa, qb, rounds + 1))

prob_a_serve = -1 # probability of A winning a serve
prob_b_serve = -1 # probability of A winning a catch
@lru_cache(None)   
def Eval_set(nextserver, qa, qb, Pa = 0, Pb = 0):
    k = 0
    global prob_a_serve
    global prob_b_serve
    if nextserver == "A":
        if prob_a_serve == -1:
            prob_a_serve = Eval(0, 0, "A", qa, qb)
        k = prob_a_serve
    else:
        if prob_b_serve == -1:
            prob_b_serve = Eval(0, 0, "B", qa, qb)
        k = 1 - prob_b_serve
    # k = Eval(0, 0, nextserver, qa, qb)
    if Pa - Pb >= 2 and Pa >= 6:
        return 1
    if Pb - Pa >= 2 and Pb >= 6:
        return 0
    if Pa == Pb and Pa == 6:
        return Eval_tiebreaker(0, 0, nextserver, qa, qb, 1)
    else:
        return (k * Eval_set("B" if nextserver == "A" else "A", qa, qb, Pa + 1, Pb) + (1 - k) * Eval_set("B" if nextserver == "A" else "A", qa, qb, Pa, Pb + 1))
    
def getMatch(data, matchNo): # extract a match by its number
    tarMatch = []
    for match in data:
        if(match[0][0] == str(matchNo)):
            tarMatch = match
            break
    if tarMatch == []:
        print("Match not found")
        exit()
    return tarMatch

def getQ(match, server, setNo, gameNo):
    totalPoint = [0]
    scoredPoint = [0]
    reached = [False]
    for _set in match:
        if(type(_set) == tuple):
            continue
        for game in _set:
            if game[0][10] == playerDict[server]:
                totalPoint[0] += 1
                if game[-1][12] == playerDict[server]:
                    scoredPoint[0] += 1
            if game[-1][1] == setNo and game[-1][2] == gameNo:
                reached[0] = True
                break
        if reached[0]:
            break

    if totalPoint[0] == 0:
        return 0.5
    q = scoredPoint[0] / totalPoint[0]
    return q


if __name__ == "__main__":
    MATCHNO = 1701

    rawData = readFile()
    data = preProcessing(rawData)
    match = getMatch(data, MATCHNO)


    # for _set in match:
    #     if(type(_set) == tuple):
    #         print("a new match begins here\n", "# and players of this match:")
    #         print(_set, "\n\nbelow are the point records of this match:\n")
    #     else:
    #         for game in _set:
    #             for point in game:
    #                 print(point)
    #             print("\nend of game\n")
    #         print("end of set\n")
    # print("end of match\n")
    # print(Eval_set("A", 0.53, 0.49, 0, 0))
    # print(Eval(0, 0, "A", 0.49, 0.53))
    # print(getQ(match, "A", 2, 2))

    alist = []
    blist = []
    for i in range(len(match)):
        _set = match[i]
        if type(_set) == tuple:
            continue
        for j in range(len(_set)):
            qa = getQ(match, "A", i + 1, j)
            qb = getQ(match, "B", i + 1, j)
            Pa = int(_set[j][-1][6])
            Pb = int(_set[j][-1][7])
            server = reversePlayerDict[_set[j][-1][10]]
            alist.append(Eval(Pa, Pb, server, qa, qb))
            blist.append(1 - Eval(Pa, Pb, server, qa, qb))
    #=========================code by qwen=========================
    # Plotting the list using matplotlib
    plt.figure(figsize=(12, 6))
    plt.plot(range(1, len(alist) + 1), alist, marker='o', linestyle='-', color='r', label='Player A')
    plt.plot(range(1, len(alist) + 1), blist, marker='o', linestyle='-', color='b', label='Player B')
    
    # Find points where A's value crosses 0.5 (swing points)
    swing_points_x = []
    swing_points_y = []
    for i in range(len(alist)):
        x = i + 1
        y = alist[i]
        
        # Check if this point is close to 0.5 or crosses over 0.5
        if abs(y - 0.5) < 0.01:  # Direct crossing or very close
            swing_points_x.append(x)
            swing_points_y.append(y)
        elif i < len(alist) - 1:  # Need at least one latter point to check for crossing
            prev_y = alist[i - 1]
            # Check if line segment crosses 0.5
            if (prev_y < 0.5 and y > 0.5) or (prev_y > 0.5 and y < 0.5):
                swing_points_x.append(i)
                swing_points_y.append(prev_y)
    
    # Mark swing points
    if swing_points_x:
        plt.scatter(swing_points_x, swing_points_y, color='green', s=100, zorder=5, label='Swing Points')
        for x, y in zip(swing_points_x, swing_points_y):
            plt.annotate('swing', (x, y), xytext=(x, y+0.05), fontsize=9, ha='center')

    plt.title(f'Evaluation Values for Match {MATCHNO}')
    plt.xlabel('Game Number')
    plt.ylabel('Evaluation Value')
    plt.grid(True)
    plt.legend()
    plt.savefig('/home/prime54601/Downloads/2024_MCM_Problem_C_Data/evaluation_plot.png')
    print("Plot saved as 'evaluation_plot.png'")
    #================================================================