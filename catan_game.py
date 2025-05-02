import random
from enum import Enum
import time
from collections import defaultdict

class ResourceType(Enum):
    BRICK = "brick"
    LUMBER = "lumber"
    ORE = "ore"
    GRAIN = "grain"
    WOOL = "wool"

class BuildingType(Enum):
    SETTLEMENT = "settlement"
    CITY = "city"
    ROAD = "road"

class Player:
    def __init__(self, player_id):
        self.id = player_id

        self.resources = {"brick" : 0, "lumber" : 0, "ore" : 0, "grain" : 0, "wool" : 0}
        self.legacyResources = {"brick" : 0, "lumber" : 0, "ore" : 0, "grain" : 0, "wool" : 0}
        self.roadSpots = set()
        self.settlementSpots = set()
        self.citySpots = set()

        self.victory_points = 0
        self.downDevs = {"knight" : 0, "victoryPoint" : 0, "roadBuilding" : 0, "yearOfPlenty" : 0, "monopoly" : 0}
        self.upDevs = {"knight" : 0, "victoryPoint" : 0, "roadBuilding" : 0, "yearOfPlenty" : 0, "monopoly" : 0}
        self.largest_army = False
        self.longest_road = False
        # self.buildings = {bt: 0 for bt in BuildingType}
        # self.dev_cards = []
        # self.longest_road = False
        # self.largest_army = False

class TileSpace:
    def __init__(self, resource, number, adjSettlements):
        self.resource = resource
        self.number = number
        self.adjSettlements = adjSettlements

class RoadSpace:
    def __init__(self, adjRoads, adjSettlements):
        self.hasRoad = False
        self.controller = None
        self.adjRoads = adjRoads
        self.adjSettlements = adjSettlements

class SettlementSpace:
    def __init__(self, adjSettlements, adjRoads):
        self.blocked = False
        self.adjSettlements = adjSettlements
        self.adjRoads = adjRoads
        self.hasSettlement = False
        self.hasCity = False
        self.controller = None

def tileFindAdjSettlements(n):
    if n == 1:
        return [1, 4, 5, 8, 9, 13]
    elif n == 2:
        return [2, 5, 6, 9, 10, 14]
    elif n == 3:
        return [3, 6, 7, 10, 11, 15]
    elif n == 4:
        return [8, 12, 13, 17, 18, 23]
    elif n == 5:
        return [9, 13, 14, 18, 19, 24]
    elif n == 6:
        return [10, 14, 15, 19, 20, 25]
    elif n == 7:
        return [11, 15, 16, 20, 21, 26]
    elif n == 8:
        return [17, 22, 23, 28, 29, 34]
    elif n == 9:
        return [18, 23, 24, 29, 30, 35]
    elif n == 10:
        return [19, 24, 25, 30, 31, 36]
    elif n == 11:
        return [20, 25, 26, 31, 32, 37]
    elif n == 12:
        return [21, 26, 27, 32, 33, 38]
    elif n == 13:
        return [29, 34, 35, 39, 40, 44]
    elif n == 14:
        return [30, 35, 36, 40, 41, 45]
    elif n == 15:
        return [31, 36, 37, 41, 42, 46]
    elif n == 16:
        return [32, 37, 38, 42, 43, 47]
    elif n == 17:
        return [40, 44, 45, 48, 49, 52]
    elif n == 18:
        return [41, 45, 46, 49, 50, 53]
    elif n == 19:
        return [42, 46, 47, 50, 51, 54]

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

def roadFindAdjSettlements(n):
    if n == 1:
        return [1, 4]
    elif n == 2:
        return [1, 5]
    elif n == 3:
        return [2, 5]
    elif n == 4:
        return [2, 6]
    elif n == 5:
        return [3, 6]
    elif n == 6:
        return [3, 7]
    
    elif n == 7:
        return [4, 8]
    elif n == 8:
        return [5, 9]
    elif n == 9:
        return [6, 10]
    elif n == 10:
        return [7, 11]
    
    elif n == 11:
        return [8, 12]
    elif n == 12:
        return [8, 13]
    elif n == 13:
        return [9, 13]
    elif n == 14:
        return [9, 14]
    elif n == 15:
        return [10, 14]
    elif n == 16:
        return [10, 15]
    elif n == 17:
        return [11, 15]
    elif n == 18:
        return [11, 16]
    
    elif n == 19:
        return [12, 17]
    elif n == 20:
        return [13, 18]
    elif n == 21:
        return [14, 19]
    elif n == 22:
        return [15, 20]
    elif n == 23:
        return [16, 21]
    
    elif n == 24:
        return [17, 22]
    elif n == 25:
        return [17, 23]
    elif n == 26:
        return [18, 23]
    elif n == 27:
        return [18, 24]
    elif n == 28:
        return [19, 24]
    elif n == 29:
        return [19, 25]
    elif n == 30:
        return [20, 25]
    elif n == 31:
        return [20, 26]
    elif n == 32:
        return [21, 26]
    elif n == 33:
        return [21, 27]
    
    elif n == 34:
        return [22, 28]
    elif n == 35:
        return [23, 29]
    elif n == 36:
        return [24, 30]
    elif n == 37:
        return [25, 31]
    elif n == 38:
        return [26, 32]
    elif n == 39:
        return [27, 33]
    
    elif n == 40:
        return [28, 34]
    elif n == 41:
        return [29, 34]
    elif n == 42:
        return [29, 35]
    elif n == 43:
        return [30, 35]
    elif n == 44:
        return [30, 36]
    elif n == 45:
        return [31, 36]
    elif n == 46:
        return [31, 37]
    elif n == 47:
        return [32, 37]
    elif n == 48:
        return [32, 38]
    elif n == 49:
        return [33, 38]
    
    elif n == 50:
        return [34, 39]
    elif n == 51:
        return [35, 40]
    elif n == 52:
        return [36, 41]
    elif n == 53:
        return [37, 42]
    elif n == 54:
        return [38, 43]
    
    elif n == 55:
        return [39, 44]
    elif n == 56:
        return [40, 44]
    elif n == 57:
        return [40, 45]
    elif n == 58:
        return [41, 45]
    elif n == 59:
        return [41, 46]
    elif n == 60:
        return [42, 46]
    elif n == 61:
        return [42, 47]
    elif n == 62:
        return [43, 47]

    elif n == 63:
        return [44, 48]
    elif n == 64:
        return [45, 49]
    elif n == 65:
        return [46, 50]
    elif n == 66:
        return [47, 51]
    
    elif n == 67:
        return [48, 52]
    elif n == 68:
        return [49, 52]
    elif n == 69:
        return [49, 53]
    elif n == 70:
        return [50, 53]
    elif n == 71:
        return [50, 54]
    elif n == 72:
        return [51, 54]

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

def settlementFindAdjRoads(n):
    if n == 1:
        return [1, 2]
    elif n == 2:
        return [3, 4]
    elif n == 3:
        return [5, 6]
    elif n == 4:
        return [1, 7]
    elif n == 5:
        return [2, 3, 8]
    elif n == 6:
        return [4, 5, 9]
    elif n == 7:
        return [6, 10]
    elif n == 8:
        return [7, 11, 12]
    elif n == 9:
        return [8, 13, 14]
    elif n == 10:
        return [9, 15, 16]
    elif n == 11:
        return [10, 17, 18]
    elif n == 12:
        return [11, 19]
    elif n == 13:
        return [12, 13, 20]
    elif n == 14:
        return [14, 15, 21]
    elif n == 15:
        return [16, 17, 22]
    elif n == 16:
        return [18, 23]
    elif n == 17:
        return [19, 24, 25]
    elif n == 18:
        return [20, 26, 27]
    elif n == 19:
        return [21, 28, 29]
    elif n == 20:
        return [22, 30, 31]
    elif n == 21:
        return [23, 32, 33]
    elif n == 22:
        return [24, 34]
    elif n == 23:
        return [25, 26, 35]
    elif n == 24:
        return [27, 28, 36]
    elif n == 25:
        return [29, 30, 37]
    elif n == 26:
        return [31, 32, 38]
    elif n == 27:
        return [33, 39]
    elif n == 28:
        return [34, 40]
    elif n == 29:
        return [35, 41, 42]
    elif n == 30:
        return [36, 43, 44]
    elif n == 31:
        return [37, 45, 46]
    elif n == 32:
        return [38, 47, 48]
    elif n == 33:
        return [39, 49]
    elif n == 34:
        return [40, 41, 50]
    elif n == 35:
        return [42, 43, 51]
    elif n == 36:
        return [44, 45, 52]
    elif n == 37:
        return [46, 47, 53]
    elif n == 38:
        return [48, 49, 54]
    elif n == 39:
        return [50, 55]
    elif n == 40:
        return [51, 56, 57]
    elif n == 41:
        return [52, 58, 59]
    elif n == 42:
        return [53, 60, 61]
    elif n == 43:
        return [54, 62]
    elif n == 44:
        return [55, 56, 63]
    elif n == 45:
        return [57, 58, 64]
    elif n == 46:
        return [59, 60, 65]
    elif n == 47:
        return [61, 62, 66]
    elif n == 48:
        return [63, 67]
    elif n == 49:
        return [64, 68, 69]
    elif n == 50:
        return [65, 70, 71]
    elif n == 51:
        return [66, 72]
    elif n == 52:
        return [67, 68]
    elif n == 53:
        return [69, 70]
    elif n == 54:
        return [71, 72]

def color_tile(tile_code, resource):
    colors = {
        "g": "\033[93m",  # Grain -> Yellow
        "l": "\033[38;5;22m",  # Lumber -> Dark Green
        "w": "\033[92m",  # Wool -> Light Green
        "b": "\033[91m",  # Brick -> Orange (approx)
        "o": "\033[90m",  # Ore -> Gray
        "d": "\033[95m",  # Desert -> Purple
    }
    reset = "\033[0m"
    resource_letter = resource[:1].lower()
    color = colors.get(resource_letter, "")
    return f"{color}{tile_code}{reset}"

def printBoard(board):
    sv = {}
    for i in range(1, 55):
        key = f"s{i}"
        if board[key].hasSettlement:
            sv[key] = f"{board[key].controller}s"
        elif board[key].hasCity:
            sv[key] = f"{board[key].controller}c"
        elif board[key].blocked:
            sv[key] = "~~"
        else:
            sv[key] = "--"

    rv = {}
    for i in range(1, 73):
        key = f"r{i}"
        rv[key] = board[key].controller if board[key].hasRoad else " "

    tv = {}
    for i in range(1, 20):
        key = f"t{i}"
        temp = f"{(board[key].number)}"
        if board[key].number == "10":
            temp = "!"
        elif board[key].number == "11":
            temp = "@"
        elif board[key].number == "12":
            temp = "#"
        tile_code = f"{temp}{board[key].resource[:1].lower()}"
        tv[key] = color_tile(tile_code, board[key].resource)
    
    ascii_art = [
    f"               {sv["s1"]}        {sv["s2"]}        {sv["s3"]}",
    f"           /{rv["r1"]}/    \\{rv["r2"]}\\/{rv["r3"]}/    \\{rv["r4"]}\\/{rv["r5"]}/    \\{rv["r6"]}\\",
    f"          {sv["s4"]}        {sv["s5"]}        {sv["s6"]}        {sv["s7"]}",
    f"         |{rv["r7"]}|   {tv["t1"]}  |{rv["r8"]}|   {tv["t2"]}   |{rv["r9"]}|  {tv["t3"]}   |{rv["r10"]}|",
    f"          {sv["s8"]}        {sv["s9"]}        {sv["s10"]}        {sv["s11"]}",
    f"       /{rv["r11"]}/   \\{rv["r12"]}\\/{rv["r13"]}/    \\{rv["r14"]}\\/{rv["r15"]}/    \\{rv["r16"]}\\/{rv["r17"]}/    \\{rv["r18"]}\\",
    f"     {sv["s12"]}        {sv["s13"]}        {sv["s14"]}        {sv["s15"]}        {sv["s16"]}",
    f"    |{rv["r19"]}|   {tv["t4"]}  |{rv["r20"]}|   {tv["t5"]}  |{rv["r21"]}|   {tv["t6"]}   |{rv["r22"]}|  {tv["t7"]}   |{rv["r23"]}|",
    f"     {sv["s17"]}        {sv["s18"]}        {sv["s19"]}        {sv["s20"]}        {sv["s21"]}",   
    f" /{rv["r24"]}/    \\{rv["r25"]}\\/{rv["r26"]}/    \\{rv["r27"]}\\/{rv["r28"]}/    \\{rv["r29"]}\\/{rv["r30"]}/    \\{rv["r31"]}\\/{rv["r32"]}/    \\{rv["r33"]}\\",
    f" {sv["s22"]}       {sv["s23"]}        {sv["s24"]}        {sv["s25"]}        {sv["s26"]}       {sv["s27"]}",
    f"|{rv["r34"]}|  {tv["t8"]}  |{rv["r35"]}|   {tv["t9"]}  |{rv["r36"]}|   {tv["t10"]}   |{rv["r37"]}|  {tv["t11"]}   |{rv["r38"]}|  {tv["t12"]}  |{rv["r39"]}|",
    f" {sv["s28"]}       {sv["s29"]}        {sv["s30"]}        {sv["s31"]}        {sv["s32"]}       {sv["s33"]}",
    f" \\{rv["r40"]}\\    /{rv["r41"]}/\\{rv["r42"]}\\    /{rv["r43"]}/\\{rv["r44"]}\\    /{rv["r45"]}/\\{rv["r46"]}\\    /{rv["r47"]}/\\{rv["r48"]}\\    /{rv["r49"]}/",
    f"     {sv["s34"]}        {sv["s35"]}        {sv["s36"]}        {sv["s37"]}        {sv["s38"]}",
    f"    |{rv["r50"]}|   {tv["t13"]}  |{rv["r51"]}|   {tv["t14"]}  |{rv["r52"]}|   {tv["t15"]}   |{rv["r53"]}|  {tv["t16"]}   |{rv["r54"]}|",
    f"     {sv["s39"]}        {sv["s40"]}        {sv["s41"]}        {sv["s42"]}        {sv["s43"]}",
    f"     \\{rv["r55"]}\\     /{rv["r56"]}/\\{rv["r57"]}\\    /{rv["r58"]}/\\{rv["r59"]}\\    /{rv["r60"]}/\\{rv["r61"]}\\     /{rv["r62"]}/",
    f"          {sv["s44"]}        {sv["s45"]}        {sv["s46"]}        {sv["s47"]}",
    f"         |{rv["r63"]}|   {tv["t17"]}  |{rv["r64"]}|   {tv["t18"]}   |{rv["r65"]}|  {tv["t19"]}   |{rv["r66"]}|",
    f"          {sv["s48"]}        {sv["s49"]}        {sv["s50"]}        {sv["s51"]}",
    f"	  \\{rv["r67"]}\\     /{rv["r68"]}/\\{rv["r69"]}\\    /{rv["r70"]}/\\{rv["r71"]}\\     /{rv["r72"]}/",
    f"	       {sv["s52"]}        {sv["s53"]}        {sv["s54"]}"
    ]

    for line in ascii_art:
        print(line)

class CatanGame:
    def __init__(self, num_players=2):
        self.num_players = num_players
        self.players = [Player(i) for i in range(num_players)]
        self.board = self._initialize_board()
        self.current_player = 0
        self.turn_number = 0
        self.game_over = False
        self.winner = None
        
    def _initialize_board(self):
        """Initialize a simple board with random resources and numbers."""
        board = {}

        # create the board tiles
        resourceTiles = ["brick", "brick", "brick", 
                         "lumber", "lumber", "lumber", "lumber", 
                         "grain", "grain", "grain", "grain", 
                         "wool", "wool", "wool", "wool", 
                         "ore", "ore", "ore",
                         "desert"]
        random.shuffle(resourceTiles)
        
        productionTiles = ["2", 
                           "3", "3",
                           "4", "4",
                           "5", "5",
                           "6", "6",
                           "8", "8",
                           "9", "9",
                           "10", "10",
                           "11", "11",
                           "12"]
        random.shuffle(productionTiles)

        # for easy resource distribution
        # for i in range(13):
        #     board[f"{i}prod"] = []
        for i in range(1, 20):
            resource = resourceTiles.pop()
            if resource == "desert":
                production = 0
            else:
                production = productionTiles.pop()
            # board[f"{production}prod"].append(TileSpace(resource, production, tileFindAdjSettlements(i)))
            board[f"t{i}"] = TileSpace(resource, production, tileFindAdjSettlements(i))

        # create the board roads
        for i in range(1, 73):
            board[f"r{i}"] = RoadSpace(roadFindAdjRoads(i), roadFindAdjSettlements(i))

        # create the board settlements
        for i in range(1, 55):
            board[f"s{i}"] = SettlementSpace(settlementFindAdjSettlements(i), settlementFindAdjRoads(i))

        # create the dev card stack
        devStack = (
            ["knight"] * 14 +
            ["victoryPoint"] * 5 +
            ["roadBuilding"] * 2 +
            ["yearOfPlenty"] * 2 +
            ["monopoly"] * 2
        )
        random.shuffle(devStack)
        board["devStack"] = devStack

        # place initial settlements
        for _ in range(2):
            for p in self.players:
                player = self.players[p.id]

                # pick a random board spot
                num = random.randint(1, 54)
                while(board[f's{num}'].blocked == True):
                    num = random.randint(1, 54)

                # add the new spot to the cities list
                player.citySpots.add(num)

                # update the board
                board[f's{num}'].hasSettlement = True
                board[f's{num}'].controller = player.id
                board[f's{num}'].blocked = True
                for p in self.players:
                    p.settlementSpots.discard(num)
                for adj in board[f's{num}'].adjSettlements:
                    board[f's{adj}'].blocked = True
                    for p in self.players:
                        p.settlementSpots.discard(adj)
                
                # find the new roads from this settlement spot
                newRoadSpots = set()
                for adj in board[f's{num}'].adjRoads:
                    if board[f'r{adj}'].hasRoad == False:
                        newRoadSpots.add(adj)

                # place a road from among them
                rSpot = random.choice(list(newRoadSpots))
                board[f'r{rSpot}'].hasRoad = True
                board[f'r{rSpot}'].controller = player.id
                for p in self.players:
                    p.roadSpots.discard(rSpot)
                for adj in board[f'r{rSpot}'].adjRoads:
                    if board[f'r{adj}'].hasRoad == False:
                        newRoadSpots.add(adj)
                newRoadSpots.discard(rSpot)

                # update the players road list
                player.roadSpots.update(newRoadSpots)

                # Award victory point
                player.victory_points += 1
        # printBoard(board)
        # for p in self.players:
        #     print(f"player {p.id} resources", p.resources)
        #     print(f"player {p.id} road spots", p.roadSpots)
        #     print(f"player {p.id} settle spots", p.settlementSpots)
        #     print(f"player {p.id} city spots", p.citySpots)
        #     print("")
        return board

    def roll_dice(self):
        """Roll two dice and return the sum."""
        return random.randint(1, 6) + random.randint(1, 6)
    
    def collect_resources(self, roll):
        """Collect resources based on the dice roll."""
        # for pos, space in self.board.items():
        #     if space.number == roll:
        #         for player_id in space.settlements:
        #             resource = space.resource
        #             self.players[player_id].resources[resource] += 1
        for key, value in self.board.items():
            if key.startswith("t"):
                tile = value
                if int(tile.number) == roll:
                    for adj in tile.adjSettlements:
                        settle = self.board[f's{adj}']
                        if settle.hasSettlement:
                            self.players[settle.controller].resources[tile.resource] += 1
                            self.players[settle.controller].legacyResources[tile.resource] += 1
                            #print(f"player {settle.controller} collected 1 {tile.resource}!")
                        elif settle.hasCity:
                            self.players[settle.controller].resources[tile.resource] += 2
                            self.players[settle.controller].legacyResources[tile.resource] += 2
                            #print(f"player {settle.controller} collected 2 {tile.resource}!")
    
    def can_build_settlement(self, player_id):
        """Check if a player can build a settlement."""
        player = self.players[player_id]
        # print(player.settlementSpots)
        return (len(player.settlementSpots) != 0 and
                player.resources["brick"] >= 1 and
                player.resources["lumber"] >= 1 and
                player.resources["grain"] >= 1 and
                player.resources["wool"] >= 1)
    
    def build_settlement(self, player_id):
        """Build a settlement at the given position."""
        if not self.can_build_settlement(player_id):
            return False
        player = self.players[player_id]

        # spend resources
        player.resources["brick"] -= 1
        player.resources["lumber"] -= 1
        player.resources["grain"] -= 1
        player.resources["wool"] -= 1
        
        # pick a random spot and place it
        spot = random.choice(list(player.settlementSpots))
        player.settlementSpots.discard(spot)
        player.citySpots.add(spot)
        for p in self.players:
            p.settlementSpots.discard(spot)
        self.board[f's{spot}'].hasSettlement = True
        self.board[f's{spot}'].controller = player_id
        self.board[f's{spot}'].blocked = True
        for adj in self.board[f's{spot}'].adjSettlements:
            self.board[f's{adj}'].blocked = True
            for p in self.players:
                p.settlementSpots.discard(adj)
        
        # Award victory point
        player.victory_points += 1
        
        # Check for game over
        if player.victory_points >= 10:
            self.game_over = True
            self.winner = player_id
        
        return True
    
    def can_build_city(self, player_id):
        """Check if a player can build a city."""
        player = self.players[player_id]
        return (len(player.citySpots) != 0 and
                player.resources["grain"] >= 2 and
                player.resources["ore"] >= 3)
    
    def build_city(self, player_id):
        """Build a city at the given position."""
        if not self.can_build_city(player_id):
            return False
        
        player = self.players[player_id]
        player.resources["grain"] -= 2
        player.resources["ore"] -= 3
        
        spot = random.choice(list(player.citySpots))
        player.citySpots.discard(spot)
        self.board[f's{spot}'].hasCity = True
        self.board[f's{spot}'].hasSettlement = False
        
        # Award victory point
        player.victory_points += 1
        
        # Check for game over
        if player.victory_points >= 10:
            self.game_over = True
            self.winner = player_id
        
        return True
    
    def compute_longest_road(self, player_id):
        from collections import defaultdict

        max_length = 0

        # Build road graph
        road_graph = defaultdict(list)
        for i in range(1, 73):
            road = self.board[f"r{i}"]
            if road.controller != player_id:
                continue
            s1, s2 = road.adjSettlements
            if (self.board[f"s{s1}"].hasSettlement and self.board[f"s{s1}"].controller not in [None, player_id]) or \
            (self.board[f"s{s2}"].hasSettlement and self.board[f"s{s2}"].controller not in [None, player_id]):
                continue
            road_graph[s1].append((s2, i))
            road_graph[s2].append((s1, i))

        def dfs(node, visited_roads):
            max_len = 0
            for neighbor, road_id in road_graph[node]:
                if road_id not in visited_roads:
                    visited_roads.add(road_id)
                    length = 1 + dfs(neighbor, visited_roads)
                    max_len = max(max_len, length)
                    visited_roads.remove(road_id)
            return max_len

        for start in road_graph:
            max_length = max(max_length, dfs(start, set()))

        return max_length

    def update_longest_road(self):
        longest = 4  # must be at least 5 to get Longest Road
        holder = None
        for player in self.players:
            length = self.compute_longest_road(player.id)
            if length > longest:
                longest = length
                holder = player.id

        for player in self.players:
            if player.id == holder:
                if not player.longest_road:
                    player.victory_points += 2
                    player.longest_road = True
            else:
                if player.longest_road:
                    player.victory_points -= 2
                    player.longest_road = False

    
    def can_build_road(self, player_id):
        """Check if a player can build a road."""
        player = self.players[player_id]
        return (len(player.roadSpots) != 0 and
                player.resources["brick"] >= 1 and
                player.resources["lumber"] >= 1)
    
    def build_road(self, player_id):
        """Build a road between two positions."""
        if not self.can_build_road(player_id):
            return False
        
        player = self.players[player_id]
        player.resources["brick"] -= 1
        player.resources["lumber"] -= 1
        
        spot = random.choice(list(player.roadSpots))
        player.roadSpots.discard(spot)
        for p in self.players:
            p.roadSpots.discard(spot)
        
        self.board[f'r{spot}'].hasRoad = True
        self.board[f'r{spot}'].controller = player_id
        for adj in self.board[f'r{spot}'].adjRoads:
            if self.board[f'r{adj}'].hasRoad == False:
                player.roadSpots.add(adj)
        for adj in self.board[f'r{spot}'].adjSettlements:
            if self.board[f's{adj}'].blocked == False:
                player.settlementSpots.add(adj)
        self.update_longest_road()

    def can_port(self, player_id):
        player = self.players[player_id]
        return (player.resources["brick"] >= 4 or
                player.resources["lumber"] >= 4 or
                player.resources["ore"] >= 4 or
                player.resources["grain"] >= 4 or
                player.resources["wool"] >= 4)
    
    def port(self, player_id):
        if not self.can_port(player_id):
            return False
        player = self.players[player_id]
        portables = []
        for resource, count in player.resources.items():
            if count >= 4:
                portables.append(resource)
        choice = random.choice(portables)
        resourceList = ["lumber", "brick", "ore", "grain", "wool"]
        resourceList.remove(choice)
        reception = random.choice(resourceList)
        player.resources[choice] -= 4
        player.resources[reception] += 1

        return True
    
    def can_buy_dev_card(self, player_id):
        # Check if a player can buy a development card
        player = self.players[player_id]
        return (len(self.board["devStack"]) != 0 and
                player.resources["ore"] >= 1 and
                player.resources["grain"] >= 1 and
                player.resources["wool"] >= 1)
    
    def buy_dev_card(self, player_id):
        # Buy a development card
        if not self.can_buy_dev_card(player_id):
            return False
        
        player = self.players[player_id]
        player.resources["ore"] -= 1
        player.resources["grain"] -= 1
        player.resources["wool"] -= 1
        
        # Randomly select a development card
        card = self.board["devStack"].pop()
        if card == "victoryPoint":
            player.victory_points += 1
            player.upDevs["victoryPoint"] += 1
            if player.victory_points >= 10:
                self.game_over = True
                self.winner = player_id
        else:
            player.downDevs[card] += 1
        
        return True
    
    def update_largest_army(self):
        MIN_KNIGHTS = 3
        top_player = None
        top_knights = 0

        # Find the player with the most knights played (>= 3)
        for player in self.players:
            knights_played = player.upDevs["knight"]
            if knights_played >= MIN_KNIGHTS:
                if knights_played > top_knights:
                    top_knights = knights_played
                    top_player = player
                elif knights_played == top_knights:
                    top_player = None  # Tie — no one gets Largest Army

        # Find current Largest Army holder
        current_holder = next((p for p in self.players if p.largest_army), None)

        if top_player is not None and top_player != current_holder:
            # Transfer Largest Army
            if current_holder:
                current_holder.largest_army = False
                current_holder.victory_points -= 2
            top_player.largest_army = True
            top_player.victory_points += 2

        elif top_player is None and current_holder:
            # No valid top player — remove Largest Army
            current_holder.largest_army = False
            current_holder.victory_points -= 2
    
    def can_play_dev_card(self, player_id):
        # Check if a player can buy a development card
        player = self.players[player_id]
        return (player.downDevs["knight"] > 0 or 
                player.downDevs["roadBuilding"] > 0 or
                player.downDevs["yearOfPlenty"] > 0 or
                player.downDevs["monopoly"] > 0)
    
    def play_dev_card(self, player_id):
        # Play a development card
        if not self.can_play_dev_card(player_id):
            return False
        player = self.players[player_id]
        
        availableCards = []
        for key, value in player.downDevs.items():
            if key == "victoryPoint":
                continue
            availableCards += [key] * value
        card = random.choice(availableCards)

        if card == "knight":
            player.upDevs["knight"] += 1
            player.downDevs["knight"] -= 1
            opponents = [i for i in range(4) if i != player_id]
            target = self.players[random.choice(opponents)]
            nonzero_resources = [resource for resource, count in target.resources.items() if count > 0]
            if nonzero_resources == []:
                return True
            stealType = random.choice(nonzero_resources)
            target.resources[stealType] -= 1
            player.resources[stealType] += 1
            self.update_largest_army()

        elif card == "roadBuilding":
            player.upDevs["roadBuilding"] += 1
            player.downDevs["roadBuilding"] -= 1
            if not self.can_build_road(player_id):
                return True
            player.resources["lumber"] += 1
            player.resources["brick"] += 1
            self.build_road(player_id)
            if not self.can_build_road(player_id):
                return True
            player.resources["lumber"] += 1
            player.resources["brick"] += 1
            self.build_road(player_id)           

        elif card == "yearOfPlenty":
            player.upDevs["yearOfPlenty"] += 1
            player.downDevs["yearOfPlenty"] -= 1
            possible = [resource for resource, _ in player.resources.items()]
            resourceOne = random.choice(possible)
            resourceTwo = random.choice(possible)
            player.resources[resourceOne] += 1
            player.resources[resourceTwo] += 1

        elif card == "monopoly":
            player.upDevs["monopoly"] += 1
            player.downDevs["monopoly"] -= 1
            possible = [resource for resource, _ in player.resources.items()]
            steal = random.choice(possible)
            opponents = [i for i in range(4) if i != player_id]
            for op in opponents:
                opp = self.players[op]
                temp = opp.resources[steal]
                opp.resources[steal] = 0
                player.resources[steal] += temp

        return True
    
    def play_turn(self, player_id):
        """Play a turn for the given player."""
        if self.game_over:
            return
        
        # Roll dice
        roll = self.roll_dice()
        # print(f"{roll} was rolled!")
        self.collect_resources(roll)
        
        # Random actions for this simple AI
        # actions = ["settlement", "city", "road", "port", "end_turn"]
        actions = ["end_turn"]
        if self.can_build_settlement(player_id):
            actions.append("settlement")
        if self.can_build_city(player_id):
            actions.append("city")
        if self.can_build_road(player_id):
            actions.append("road")
        if self.can_port(player_id):
            actions.append("port")
        if self.can_buy_dev_card:
            actions.append("buyDev")
        if self.can_play_dev_card:
            actions.append("playDev")

        action = random.choice(actions)
        # print(f"player {player_id} chose to {action}!")
        
        if action == "settlement" and self.can_build_settlement(player_id):
            # # Find a random empty position
            # empty_positions = [pos for pos, space in self.board.items() 
            #                   if not space.settlements]
            # if empty_positions:
            #     pos = random.choice(empty_positions)
            self.build_settlement(player_id)
        
        elif action == "city" and self.can_build_city(player_id):
            # # Find a position with the player's settlement
            # player_positions = [pos for pos, space in self.board.items() 
            #                    if player_id in space.settlements]
            # if player_positions:
            #     pos = random.choice(player_positions)
            self.build_city(player_id)
        
        elif action == "road" and self.can_build_road(player_id):
            # # Find two adjacent positions
            # positions = list(self.board.keys())
            # if len(positions) >= 2:
            #     pos1, pos2 = random.sample(positions, 2)
            self.build_road(player_id)

        elif action == "port" and self.can_port(player_id):
            self.port(player_id)

        elif action == "buyDev" and self.can_buy_dev_card:
            self.buy_dev_card(player_id)

        elif action == "playDev" and self.can_play_dev_card:
            self.play_dev_card(player_id)
        
        # Move to next player
        # if self.turn_number % 1 == 0:
        #     printBoard(self.board)
        #     for p in self.players:
        #         print(f"player {p.id} resources", p.resources)
        #         print(f"player {p.id} legacy resources", p.legacyResources)
        #         print(f"player {p.id} road spots", p.roadSpots)
        #         print(f"player {p.id} settle spots", p.settlementSpots)
        #         print(f"player {p.id} city spots", p.citySpots)
        #         print(f"player {p.id} victory points", p.victory_points)
        #         print(f"player {p.id} up devs", p.upDevs)
        #         print(f"player {p.id} down devs", p.downDevs)
        #         print(f"player {p.id} longest road", p.longest_road)
        #         print(f"player {p.id} largest army", p.largest_army)
        #         print("")
        #     # time.sleep(3)
        self.current_player = (self.current_player + 1) % self.num_players
        self.turn_number += 1
    
    def get_game_state(self):
        """Return the current game state."""
        return {
            "players": [
                {
                    "id": p.id,
                    "resources": p.resources,
                    "legacyResources": p.legacyResources,
                    "victory_points": p.victory_points,
                    "upDevs": p.upDevs 
                    # "longest_road": p.longest_road,
                    # "largest_army": p.largest_army
                }
                for p in self.players
            ],
            "current_player": self.current_player,
            "turn_number": self.turn_number,
            "game_over": self.game_over,
            "winner": self.winner
        }
    