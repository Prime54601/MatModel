def Eval(Pa, Pb, server, qa, qb):
    if Pa - Pb >= 2 and Pa >= 4:
        return 1
    if Pb - Pa >= 2 and Pb >= 4:
        return 0
    if Pa == Pb and Pa == 3:
        return qa**2 / (qa**2 + (1 - qa)**2) if server == "A" else 1 - qb**2 / (qb**2 + (1 - qb)**2)
    else:
        p = qa if server == "A" else qb
        return (p * Eval(Pa + 1, Pb, server, qa, qb) + (1 - p) * Eval(Pa, Pb + 1, server, qa, qb))
    
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
        return qa**2 / (qa**2 + (1 - qa)**2) if server == "A" else 1 - qb**2 / (qb**2 + (1 - qb)**2)
    else:
        p = qa if server == "A" else qb
        return (p * Eval_tiebreaker(Pa + 1, Pb, initserver, qa, qb, rounds + 1) + (1 - p) * Eval_tiebreaker(Pa, Pb + 1, initserver, qa, qb, rounds + 1))
    
def Eval_set(nextserver, initserver, gamesplayed, qa, qb, Pa = 0, Pb = 0):
    server = "B" if nextserver == "A" else "A"
    k = Eval(0, 0, server, qa, qb)
    if Pa - Pb >= 2 and Pa >= 6:
        return 1
    if Pb - Pa >= 2 and Pb >= 6:
        return 0
    if Pa == Pb and Pa == 6:
        return Eval_tiebreaker(0, 0, server, qa, qb, 1)
    else:
        return (k * Eval_set(server, initserver, gamesplayed + 1, qa, qb, Pa + 1, Pb) + (1 - k) * Eval_set(server, initserver, gamesplayed + 1, qa, qb, Pa, Pb + 1))
    

if __name__ == "__main__":
    print(Eval_set("B", "A", 0, 0.55, 0.6))