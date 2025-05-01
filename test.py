def roadFindAdjRoads(n):
    if n == 1:
        return [2, 7]
    elif n == 2:
        return [1, 3, 8]
    elif n == 3:
        return [2, 4, 8]
    elif n == 4:
        return [3, 5, 9]
    elif n == 5:
        return [4, 6, 9]
    elif n == 6:
        return [5, 10]
    
    elif n == 7:
        return [1, 11, 12]
    elif n == 8:
        return [2, 3, 13, 14]
    elif n == 9:
        return [4, 5, 15, 16]
    elif n == 10:
        return [6, 17, 18]
    
    elif n == 11:
        return [7, 12, 19]
    elif n == 12:
        return [7, 11, 13, 20]
    elif n == 13:
        return [8, 12, 14, 20]
    elif n == 14:
        return [8, 13, 15, 21]
    elif n == 15:
        return [9, 14, 16, 21]
    elif n == 16:
        return [9, 15, 17, 22]
    elif n == 17:
        return [10, 16, 18, 22]
    elif n == 18:
        return [10, 17, 23]
    
    elif n == 19:
        return [11, 24, 25]
    elif n == 20:
        return [12, 13, 26, 27]
    elif n == 21:
        return [14, 15, 28, 29]
    elif n == 22:
        return [16, 17, 30, 31]
    elif n == 23:
        return [18, 32, 33]
    

    elif n == 24:
        return [19, 25, 34]
    elif n == 25:
        return [19, 24, 26, 35]
    elif n == 26:
        return [20, 25, 27, 35]
    elif n == 27:
        return [20, 26, 28, 36]
    elif n == 28:
        return [21, 27, 29, 36]
    elif n == 29:
        return [21, 28, 30, 37]
    elif n == 30:
        return [22, 29, 31, 37]
    elif n == 31:
        return [22, 30, 32, 38]
    elif n == 32:
        return [23, 31, 33, 38]
    elif n == 33:
        return [23, 32, 39]
    
    elif n == 34:
        return [24, 40]
    elif n == 35:
        return [25, 26, 41, 42]
    elif n == 36:
        return [27, 28, 43, 44]
    elif n == 37:
        return [29, 30, 45, 46]
    elif n == 38:
        return [31, 32, 47, 48]
    elif n == 39:
        return [33, 49]
    
    elif n == 40:
        return [34, 41, 50]
    elif n == 41:
        return [35, 40, 42, 50]
    elif n == 42:
        return [35, 41, 43, 51]
    elif n == 43:
        return [36, 42, 44, 51]
    elif n == 44:
        return [36, 43, 45, 52]
    elif n == 45:
        return [37, 44, 46, 52]
    elif n == 46:
        return [37, 45, 47, 53]
    elif n == 47:
        return [38, 46, 48, 53]
    elif n == 48:
        return [38, 47, 49, 54]
    elif n == 49:
        return [39, 48, 54]
    
    elif n == 50:
        return [40, 41, 55]
    elif n == 51:
        return [42, 43, 56, 57]
    elif n == 52:
        return [44, 45, 58, 59]
    elif n == 53:
        return [46, 47, 60, 61]
    elif n == 54:
        return [48, 49, 62]
    
    elif n == 55:
        return [50, 56, 63]
    elif n == 56:
        return [51, 55, 57, 63]
    elif n == 57:
        return [51, 56, 58, 64]
    elif n == 58:
        return [52, 57, 59, 64]
    elif n == 59:
        return [52, 58, 60, 65]
    elif n == 60:
        return [53, 59, 61, 65]
    elif n == 61:
        return [53, 60, 62, 66]
    elif n == 62:
        return [54, 61, 66]
    
    elif n == 63:
        return [55, 56, 67]
    elif n == 64:
        return [57, 58, 68, 69]
    elif n == 65:
        return [59, 60, 70, 71]
    elif n == 66:
        return [61, 62, 72]
    
    elif n == 67:
        return [63, 68]
    elif n == 68:
        return [64, 67, 69]
    elif n == 69:
        return [64, 68, 70]
    elif n == 70:
        return [65, 69, 71]
    elif n == 71:
        return [65, 70, 72]
    elif n == 72:
        return [66, 71]


for i in range(1, 73):
    for neighbor in roadFindAdjRoads(i):
        if i not in roadFindAdjRoads(neighbor):
            print(f"Inconsistent: {i} <-> {neighbor}")
print("beep")

def settlementFindAdjSettlements(n):
    if n == 1:
        return [4, 5]
    elif n == 2:
        return [5, 6]
    elif n == 3:
        return [6, 7]
    elif n == 4:
        return [1, 8]
    elif n == 5:
        return [1, 2, 9]
    elif n == 6:
        return [2, 3, 10]
    elif n == 7:
        return [3, 11]
    elif n == 8:
        return [4, 12, 13]
    elif n == 9:
        return [5, 13, 14]
    elif n == 10:
        return [6, 14, 15]
    elif n == 11:
        return [7, 15, 16]
    elif n == 12:
        return [8, 17]
    elif n == 13:
        return [8, 9, 18]
    elif n == 14:
        return [9, 10, 19]
    elif n == 15:
        return [10, 11, 20]
    elif n == 16:
        return [11, 21]
    elif n == 17:
        return [12, 22, 23]
    elif n == 18:
        return [13, 23, 24]
    elif n == 19:
        return [14, 24, 25]
    elif n == 20:
        return [15, 25, 26]
    elif n == 21:
        return [16, 26, 27]
    elif n == 22:
        return [17, 28]
    elif n == 23:
        return [17, 18, 29]
    elif n == 24:
        return [18, 19, 30]
    elif n == 25:
        return [19, 20, 31]
    elif n == 26:
        return [20, 21, 32]
    elif n == 27:
        return [21, 33]
    elif n == 28:
        return [22, 34]
    elif n == 29:
        return [23, 34, 35]
    elif n == 30:
        return [24, 35, 36]
    elif n == 31:
        return [25, 36, 37]
    elif n == 32:
        return [26, 37, 38]
    elif n == 33:
        return [27, 38]
    elif n == 34:
        return [28, 29, 39]
    elif n == 35:
        return [29, 30, 40]
    elif n == 36:
        return [30, 31, 41]
    elif n == 37:
        return [31, 32, 42]
    elif n == 38:
        return [32, 33, 43]
    elif n == 39:
        return [34, 44]
    elif n == 40:
        return [35, 44, 45]
    elif n == 41:
        return [36, 45, 46]
    elif n == 42:
        return [37, 46, 47]
    elif n == 43:
        return [38, 47]
    elif n == 44:
        return [39, 40, 48]
    elif n == 45:
        return [40, 41, 49]
    elif n == 46:
        return [41, 42, 50]
    elif n == 47:
        return [42, 43, 51]
    elif n == 48:
        return [44, 52]
    elif n == 49:
        return [45, 52, 53]
    elif n == 50:
        return [46, 53, 54]
    elif n == 51:
        return [47, 54]
    elif n == 52:
        return [48, 49]
    elif n == 53:
        return [49, 50]
    elif n == 54:
        return [50, 51]

def validate_adjacency():
    all_good = True
    for n in range(1, 55):
        adj = settlementFindAdjSettlements(n)
        for m in adj:
            if n not in settlementFindAdjSettlements(m):
                print(f"Inconsistency: {n} → {m} but not {m} → {n}")
                all_good = False
    if all_good:
        print("✅ All adjacencies are consistent!")

validate_adjacency()
