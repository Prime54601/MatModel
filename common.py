# common constants and functions intended to be used by many files

fileName = "./2024_Wimbledon_featured_matches.csv"
pointDict = {"15": "1",
             "30": "2",
             "40": "3"} # convert points to normalized format

playerDict = {"A": "1", "B": "2"}
reversePlayerDict = {v: k for k, v in playerDict.items()}