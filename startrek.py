# This Python file uses the following encoding: utf-8

# Attempt to turn a Python version of a C# version
# of Super Star Trek into something more like the
# version I played on the Commodore PET in 1977.
# based on https://github.com/cosmicr/startrek1971

from math import atan2, pi, sqrt, cos, sin
import random, os, sys
from time import sleep
# PROPERTY OF LEONARD TRAMIEL

commandStrings = [
    "COMMANDS ARE: \033[7mP\033[0mHASERS  \033[7mT\033[0mORP  \033[7mS\033[0mHIELDS",
    "              \033[7mM\033[0mOVE     \033[7mL\033[0mRS   \033[7mH\033[0mELP",
    "              \033[7mQ\033[0mUIT     \033[7mA\033[0mCCESS COMPUTER",
    "              \033[7mC\033[0mOMPUTER MAP",
    ]


computerStrings = [
    "--- Main Computer --------------",
    "tor = Photon Torpedo Calculator",
    "bas = Starbase Calculator",
    "nav = Navigation Calculator",
    ]


class Quadrant():

    def __init__(self):
        self.klingons = 0
        self.stars = 0
        self.starbase = False
        self.scanned = False


class SectorType():

    def __init__(self):
        self.empty, self.star, self.klingon, self.enterprise, self.starbase = 1, 2, 3, 4, 5

sector_type = SectorType()


class KlingonShip():

    def __init__(self):
        self.sector_x = 0
        self.sector_y = 0
        self.shield_level = 0


class Game():

    def __init__(self):
        self.star_date = 0
        self.time_remaining = 0
        self.energy = 0
        self.klingons = 0
        self.starbases = 0
        self.quadrant_x, self.quadrant_y = 0, 0
        self.sector_x, self.sector_y = 0, 0
        self.shield_level = 0
        self.photon_torpedoes = 0
        self.docked = False
        self.destroyed = False
        self.starbase_x, self.starbase_y = 0, 0
        self.quadrants = [[Quadrant() for _ in range(8)] for _ in range(8)]
        self.sector = [[SectorType() for _ in range(8)] for _ in range(8)]
        self.klingon_ships = []

game = Game()


def run():
    global game
    while True:
        initialize_game()
        print_mission()
        print_strings(commandStrings)
        sleep(5)
        generate_sector()
        clearConsole()
        while game.energy > 0 and not game.destroyed and game.klingons > 0 and game.time_remaining > 0:
            short_range_scan()
            command_prompt()
            print_game_status()


def print_game_status():
    global game
    if game.destroyed:
        clearConsole()
        print("THE ENTERPRISE HAS BEEN\nDESTROYED")
        sleep(10)
    elif game.energy == 0:
        print("MISSION FAILED: ENTERPRISE RAN OUT OF ENERGY.")
        sleep(10)
    elif game.klingons == 0:
        print("MISSION ACCOMPLISHED: ALL KLINGON SHIPS DESTROYED. WELL DONE!!!")
        sleep(10)
    elif game.time_remaining == 0:
        print("TIME’S UP.")
        sleep(10)


def command_prompt():
    # clear command line
    print("\033[12;0f") # goto line 12
    command = input("COMMAND ?  ").strip().lower()
    clearStatusLines()
    print("\033[13;0f") # goto line 14
    if command == "m":
        navigation()
    elif command == "l":
        long_range_scan()
    elif command == "p":
        phaser_controls()
    elif command == "t":
        torpedo_control()
    elif command == "s":
        shield_controls()
    elif command == "a":
        computer_controls()
    elif command == "q":
        exit()
    elif command == "h":
        show_help()
    elif command == "c":
        display_galactic_record()
    else:
        print_strings(commandStrings)


def computer_controls():
    global game
    print_strings(computerStrings)
    command = input("Enter computer command: ").strip().lower()
    if command == "tor":
        photon_torpedo_calculator()
    elif command == "bas":
        starbase_calculator()
    elif command == "nav":
        navigation_calculator()
    else:
        print()
        print("Invalid computer command.")
        print()


def compute_direction(x1, y1, x2, y2):
    if x1 == x2:
        if y1 < y2:
            direction = 7
        else:
            direction = 3
    elif y1 == y2:
        if x1 < x2:
            direction = 1
        else:
            direction = 5
    else:
        dy = abs(y2 - y1)
        dx = abs(x2 - x1)
        angle = atan2(dy, dx)
        if x1 < x2:
            if y1 < y2:
                direction = 9.0 - 4.0 * angle / pi
            else:
                direction = 1.0 + 4.0 * angle / pi
        else:
            if y1 < y2:
                direction = 5.0 + 4.0 * angle / pi
            else:
                direction = 5.0 - 4.0 * angle / pi
    return direction


def navigation_calculator():
    global game
    print()
    print("Enterprise located in quadrant [%s,%s]." % (game.quadrant_x, game.quadrant_y))
    print()
    try:
        quad_x = input_double("Enter destination quadrant X (1--8): ")
    except:
        print("INVALID X CO-ORDINATE")
        return
    if quad_x is False or quad_x < 1 or quad_x > 8:
        print("INVALID X COORDINATE.")
        print()
        return
    try:
        quad_y = input_double("Enter destination quadrant Y (1--8): ")
    except:
        print("INVALID Y CO-ORDINATE")
        return
    if quad_y is False or quad_y < 1 or quad_y > 8:
        print("INVALID Y COORDINATE.")
        print()
        return
    print()
    qx = int(quad_x) - 1
    qy = int(quad_y) - 1
    if qx == game.quadrant_x and qy == game.quadrant_y:
        print("That is the current location of the Enterprise.")
        print()
        return
    print("Direction: {0:1.2f}".format(compute_direction(game.quadrant_x, game.quadrant_y, qx, qy)))
    print("Distance:  {0:2.2f}".format(distance(game.quadrant_x, game.quadrant_y, qx, qy)))
    print()


def starbase_calculator():
    global game
    print()
    if game.quadrants[game.quadrant_y][game.quadrant_x].starbase:
        print("Starbase in sector [%s,%s]." % (game.starbase_x, game.starbase_y))
        print("Direction: {0:1.2f}".format(
            compute_direction(game.sector_x, game.sector_y, game.starbase_x, game.starbase_y)
        ))
        print("Distance:  {0:2.2f}".format(distance(game.sector_x, game.sector_y, game.starbase_x, game.starbase_y) / 8))
    else:
        print("There are no starbases in this quadrant.")
    print()


def photon_torpedo_calculator():
    global game
    print
    if len(game.klingon_ships) == 0:
        print("There are no Klingon ships in this quadrant.")
        print()
        return

    for ship in game.klingon_ships:
        text = "Direction {2:1.2f}: Klingon ship in sector [{0},{1}]."
        print(text.format(
            ship.sector_x, ship.sector_y,
            compute_direction(game.sector_x, game.sector_y, ship.sector_x, ship.sector_y)))
    print()


def display_galactic_record():
    global game
    game.SRS = False
    clearConsole()
    print()
    sb = ""
    print("   0   1   2   3   4   5   6   7")
    print(" ┌────────────────────────────────┐ ")

    for i in range(8):
        sb = str(i)
        sb += "│"
        for j in range(8):
            klingon_count = 0
            starbase_count = 0
            star_count = 0
            quadrant = game.quadrants[i][j]
            if quadrant.scanned:
                klingon_count = quadrant.klingons
                starbase_count = 1 if quadrant.starbase else 0
                star_count = quadrant.stars
                if i == game.quadrant_y and j == game.quadrant_x:
                    sb += "\033[7m" # inverse video for current quadrant
                sb = sb + "{0}{1}{2}".format(klingon_count, starbase_count, star_count)
                if i == game.quadrant_y and j == game.quadrant_x:
                    sb += "\033[0m" # turn off inverse video
                sb += " "
            else:
                sb += "*** "
        sb += "│"
        print_slow(sb)
        sb = ""
    print(" └────────────────────────────────┘")
    print()
    command_prompt()


def phaser_controls():
    global game
    if len(game.klingon_ships) == 0:
        print("There are no Klingon ships in this quadrant.")
        print()
        return
    print("PHASERS LOCKED ON TARGET.")
    try:
        phaser_energy = input_double("Enter phaser energy (1--{0}): ".format(game.energy))
        if not phaser_energy or phaser_energy < 1 or phaser_energy > game.energy:
            print("INVALID ENERGY LEVEL.")
            print()
            return
        print()
        print("FIRING PHASERS...")
        destroyed_ships = []
        for ship in game.klingon_ships:
            game.energy -= int(phaser_energy)
            if game.energy < 0:
                game.energy = 0
                break
            dist = distance(game.sector_x, game.sector_y, ship.sector_x, ship.sector_y)
            delivered_energy = phaser_energy * (1.0 - dist / 11.3)
            ship.shield_level -= int(delivered_energy)
            if ship.shield_level <= 0:
                print("KLINGON SHIP DESTROYED AT SECTOR [{0},{1}].".format(ship.sector_x, ship.sector_y))
                explosion(ship.sector_x,ship.sector_y)
                destroyed_ships.append(ship)
            else:
                print("HIT SHIP AT SECTOR [{0},{1}].\nKLINGON SHIELD STRENGTH DROPPED TO {2}.".format(
                    ship.sector_x, ship.sector_y, ship.shield_level
                ))
        for ship in destroyed_ships:
            game.quadrants[game.quadrant_y][game.quadrant_x].klingons -= 1
            game.klingons -= 1
            game.sector[ship.sector_y][ship.sector_x] = sector_type.empty
            game.klingon_ships.remove(ship)
        if len(game.klingon_ships) > 0:
            print()
            klingons_attack()
        print()
    except:
        print("INVALID PHASER ENERGY")


def shield_controls():
    global game
    max_transfer = game.energy + game.shield_level
    print("YOU HAVE {0} UNITS AVAILABLE.".format(max_transfer))
    try:
        transfer = int(input("HOW MANY UNITS TO SHIELDS? "))
    except:
        print("INVALID AMOUNT OF ENERGY.")
        return
    if transfer < 0 or transfer > max_transfer:
        print("INVALID AMOUNT OF ENERGY.")
        return
    game.energy += game.shield_level
    game.shield_level = transfer
    game.energy -= transfer


def klingons_attack():
    global game
    if len(game.klingon_ships) > 0:
        for ship in game.klingon_ships:
            if game.docked:
                print("Enterprise hit by ship at sector [{0},{1}]. No damage due to starbase shields.".format(
                    ship.sector_x, ship.sector_y
                ))
            else:
                dist = distance(
                    game.sector_x, game.sector_y, ship.sector_x, ship.sector_y)
                delivered_energy = 300 * \
                    random.uniform(0.0, 1.0) * (1.0 - dist / 11.3)
                game.shield_level -= int(delivered_energy)
                if game.shield_level < 0:
                    game.shield_level = 0
                    game.destroyed = True
                print("ENTERPRISE HIT:SHIELDS DOWN {0} UNITS!".format(int(delivered_energy)))
                if game.shield_level == 0:
                    return True
        return True
    return False


def distance(x1, y1, x2, y2):
    x = x2 - x1
    y = y2 - y1
    return sqrt(x * x + y * y)


def long_range_scan():
    global game
    sb = "              "
    for i in range(game.quadrant_y - 1, game.quadrant_y+2):  # quadrantY + 1 ?
        for j in range(game.quadrant_x - 1, game.quadrant_x+2):  # quadrantX + 1?
            klingon_count = 0
            starbase_count = 0
            star_count = 0
            if 0 <= i < 8 and 0 <= j < 8:
                quadrant = game.quadrants[i][j]
                quadrant.scanned = True
                klingon_count = quadrant.klingons
                starbase_count = 1 if quadrant.starbase else 0
                star_count = quadrant.stars
            sb = sb + \
                "{0}{1}{2} ".format(klingon_count, starbase_count, star_count)
        print_slow(sb)
        sb = "              "


def torpedo_control():
    global game
    if game.photon_torpedoes == 0:
        print("YOU ARE OUT OF TORPEDOES.")
        print()
        return
    if len(game.klingon_ships) == 0:
        print("There are no Klingon ships in this quadrant.")
        print()
        return
    try:
        show_angles()
        direction = input_double("ANGLE (1-9)? ")
        if not direction or direction < 1.0 or direction > 9.0:
            print("INVALID DIRECTION")
            return
    except:
        print("INVALID DIRECTION")
        return
    clearStatusLines()
    print("\033[14;0f")
    print("PHOTON TORPEDO FIRED...")
    game.photon_torpedoes -= 1
    angle = -(pi * (direction - 1.0) / 4.0)
    if random.randint(0, 2) == 0:
        angle += (1.0 - 2.0 * random.uniform(0.0, 1.0) * pi * 2.0) * 0.03
    x = game.sector_x
    y = game.sector_y
    vx = cos(angle) / 20
    vy = sin(angle) / 20
    last_x = last_y = -1
    # new_x = game.sector_x
    # new_y = game.sector_y
    hit = False
    while x >= 0 and y >= 0 and round(x) < 8 and round(y) < 8:
        new_x = int(round(x))
        new_y = int(round(y))
        if last_x != new_x or last_y != new_y:
            print("  [{0},{1}]".format(new_x, new_y))
            last_x = new_x
            last_y = new_y
        for ship in game.klingon_ships:
            if ship.sector_x == new_x and ship.sector_y == new_y:
                print("KLINGON SHIP DESTROYED AT SECTOR [{0},{1}].".format(ship.sector_x, ship.sector_y))
                explosion(ship.sector_x,ship.sector_y)
                game.sector[ship.sector_y][ship.sector_x] = sector_type.empty
                game.klingons -= 1
                game.klingon_ships.remove(ship)
                game.quadrants[game.quadrant_y][game.quadrant_x].klingons -= 1
                hit = True
                break  # break out of the for loop
        if hit:
            break  # break out of the while loop
        if game.sector[new_y][new_x] == sector_type.starbase:
            game.starbases -= 1
            game.quadrants[game.quadrant_y][game.quadrant_x].starbase = False
            game.sector[new_y][new_x] = sector_type.empty
            explosion(new_x,new_y)
            print("CONGRATULATIONS,\nYOU DESTROYED A STARBASE AT [{0},{1}]!".format(new_x, new_y))
            print("YOU HAVE {0} STARBASES LEFT. GOOD LUCK!!".format(game.starbases))
            sleep(3)
            hit = True
            break
        elif game.sector[new_y][new_x] == sector_type.star:
            print("TORPEDO CAPTURED BY STAR'S\nGRAVITATIONAL FIELD AT SECTOR [{0},{1}].".format(
                new_x, new_y
            ))
            hit = True
            break
        x += vx
        y += vy
    if not hit:
        print("PHOTON TORPEDO FAILED TO HIT ANYTHING.")
    if len(game.klingon_ships) > 0:
        print()
        klingons_attack()
    print()


def navigation():
    global game
    max_warp_factor = 8.0
    if not game.SRS:
        short_range_scan()

    try:
        show_angles()
        direction = input_double("ANGLE (1-9)? ")
        if not direction or direction < 1.0 or direction > 9.0:
            print()
            print("INVALID COURSE")
            return
        clearStatusLines()
    except:
        print()
        print("INVALID COURSE")
        return

    try:
        print("\033[14;0f")
        dist = input_double(
            "DISTANCE (0.1-{0})? ".format(max_warp_factor))
        if not dist or dist < 0.1 or dist > max_warp_factor:
            print("INVALID WARP FACTOR")
            return
    except:
        print("INVALID WARP FACTOR")
        return

    print()

    dist *= 8
    energy_required = int(dist)
    if energy_required >= game.energy:
        print("Unable to comply. Insufficient energy to travel that speed.")
        print()
        return
    else:
        print("Warp engines engaged.")
        print()
        game.energy -= energy_required

    last_quad_x = game.quadrant_x
    last_quad_y = game.quadrant_y
    angle = -(pi * (direction - 1.0) / 4.0)
    x = game.quadrant_x * 8 + game.sector_x
    y = game.quadrant_y * 8 + game.sector_y
    dx = dist * cos(angle)
    dy = dist * sin(angle)
    vx = dx / 1000
    vy = dy / 1000
    # quad_x = quad_y = sect_x = sect_y = 0
    last_sect_x = game.sector_x
    last_sect_y = game.sector_y
    game.sector[game.sector_y][game.sector_x] = sector_type.empty
    obstacle = False
    for i in range(999):
        x += vx
        y += vy
        quad_x = int(round(x)) / 8
        quad_y = int(round(y)) / 8
        if quad_x == game.quadrant_x and quad_y == game.quadrant_y:
            sect_x = int(round(x)) % 8
            sect_y = int(round(y)) % 8
            if game.sector[sect_y][sect_x] != sector_type.empty:
                game.sector_x = last_sect_x
                game.sector_y = last_sect_y
                game.sector[game.sector_y][game.sector_x] = sector_type.enterprise
                print("Encountered obstacle within quadrant.")
                obstacle = True
                break
            last_sect_x = sect_x
            last_sect_y = sect_y

    if not obstacle:
        if x < 0:
            x = 0
        elif x > 63:
            x = 63
        if y < 0:
            y = 0
        elif y > 63:
            y = 63
        quad_x = int(round(x)) / 8
        quad_y = int(round(y)) / 8
        game.sector_x = int(round(x)) % 8
        game.sector_y = int(round(y)) % 8
        if quad_x != game.quadrant_x or quad_y != game.quadrant_y:
            game.quadrant_x = int(quad_x)
            game.quadrant_y = int(quad_y)
            generate_sector()
        else:
            game.quadrant_x = int(quad_x)
            game.quadrant_y = int(quad_y)
            game.sector[game.sector_y][game.sector_x] = sector_type.enterprise
    if is_docking_location(game.sector_y, game.sector_x):
        game.energy = 5000
        game.photon_torpedoes = 10
        game.shield_level = 0
        game.docked = True
    else:
        game.docked = False

    if last_quad_x != game.quadrant_x or last_quad_y != game.quadrant_y:
        game.time_remaining -= 1
        game.star_date += 1

    short_range_scan()

    if game.docked:
        print("Lowering shields as part of docking sequence...")
        print("Enterprise successfully docked with starbase.")
        print()
    else:
        if game.quadrants[game.quadrant_y][game.quadrant_x].klingons > 0 \
                and last_quad_x == game.quadrant_x and last_quad_y == game.quadrant_y:
            klingons_attack()
            print()


def input_double(prompt):
    text = input(prompt)
    value = float(text)
    if type(value) == float:
        return value
    else:
        return False


def generate_sector():
    global game
    quadrant = game.quadrants[game.quadrant_y][game.quadrant_x]
    starbase = quadrant.starbase
    stars = quadrant.stars
    klingons = quadrant.klingons
    game.klingon_ships = []
    for i in range(8):
        for j in range(8):
            game.sector[i][j] = sector_type.empty
    game.sector[game.sector_y][game.sector_x] = sector_type.enterprise
    while starbase or stars > 0 or klingons > 0:
        i = random.randint(0, 7)
        j = random.randint(0, 7)
        if is_sector_region_empty(i, j):
            if starbase:
                starbase = False
                game.sector[i][j] = sector_type.starbase
                game.starbase_y = i
                game.starbase_x = j
            elif stars > 0:
                game.sector[i][j] = sector_type.star
                stars -= 1
            elif klingons > 0:
                game.sector[i][j] = sector_type.klingon
                klingon_ship = KlingonShip()
                klingon_ship.shield_level = 300 + random.randint(0, 199)
                klingon_ship.sector_y = i
                klingon_ship.sector_x = j
                game.klingon_ships.append(klingon_ship)
                klingons -= 1


def is_docking_location(i, j):
    for y in range(i - 1, i+1):  # i + 1?
        for x in range(j - 1, j+1):  # j + 1?
            if read_sector(y, x) == sector_type.starbase:
                return True
    return False


def is_sector_region_empty(i, j):
    for y in range(i - 1, i+1):  # i + 1?
        if read_sector(y, j - 1) != sector_type.empty and read_sector(y, j + 1) != sector_type.empty:
            return False
    return read_sector(i, j) == sector_type.empty


def read_sector(i, j):
    global game
    if i < 0 or j < 0 or i > 7 or j > 7:
        return sector_type.empty
    return game.sector[i][j]


def short_range_scan():
    global game
    game.SRS = True
    clearScreenTop()
    print("\033[H")   #cursor home
    quadrant = game.quadrants[game.quadrant_y][game.quadrant_x]
    quadrant.scanned = True
    print_sector(quadrant)


def print_sector(quadrant):
    global game
    game.condition = "G"
    if quadrant.klingons > 0:
        game.condition = "\033[7m\033[5mR\033[0m"  # reverse blink
    elif game.energy < 300:
        game.condition = "Y"
    elif game.docked:
        game.condition = "\033[7mD\033[0m"  # reverse

    sb = "│"
    print("   0  1  2  3  4  5  6  7")
    print(" ┌────────────────────────┐ ")
    print_sector_row("0"+sb, 0, "│ STARDATE {0}".format(game.time_remaining))
    print_sector_row("1"+sb, 1, "│ CONDITION {0}".format(game.condition))
    print_sector_row("2"+sb, 2, "│ QUAD.   {0},{1}".format(game.quadrant_x, game.quadrant_y))
    print_sector_row("3"+sb, 3, "│ SECTOR  {0},{1}".format(game.sector_x, game.sector_y))
    print_sector_row("4"+sb, 4, "│ ENERGY {0}".format(game.energy))
    print_sector_row("5"+sb, 5, "│ P.TORP  {0}".format(game.photon_torpedoes))
    print_sector_row("6"+sb, 6, "│ SHIELDS {0}".format(game.shield_level))
    print_sector_row("7"+sb, 7, "│ KLINGONS {0}".format(game.klingons))
    print(" └────────────────────────┘")

    if quadrant.klingons > 0:
        print()
#        print("Condition RED: Klingon ship{0} detected.".format("" if quadrant.klingons == 1 else "s")
        if game.shield_level == 0 and not game.docked:
            print("* WARNING: SHIELDS ARE DOWN! *                             ")
        elif game.shield_level < 100 and not game.docked:
            print("* SHIELDS DANGEROUSLY LOW! *                               ")
    elif game.energy < 300:
        print()
        print("CONDITION YELLOW: LOW ENERGY LEVEL.")
        game.condition = "Y"


def print_sector_row(sb, row, suffix):
    global game
    for column in range(8):
        if game.sector[row][column] == sector_type.empty:
            sb += "   "
        elif game.sector[row][column] == sector_type.enterprise:
            sb += " E "
        elif game.sector[row][column] == sector_type.klingon:
            sb += " K "
        elif game.sector[row][column] == sector_type.star:
            sb += " ● "
        elif game.sector[row][column] == sector_type.starbase:
            sb += " B "
    if suffix is not None:
        sb = sb + suffix
    print(sb)


def print_mission():
    clearConsole()
    global game
    print("\n\n\n\nYOU MUST DESTROY {0} KLINGONS\nIN  {1}  STARDATES.\n\n\nYOU HAVE {2} STARBASES.\n\n".format(
        game.klingons, game.time_remaining, game.starbases))


def initialize_game():
    # gah, globals
    clearConsole()
    print("\n\n\n\nONE MOMENT PLEASE, WHILE I ARRANGE\n\nTHE GALAXY...\n")
    sleep(3)
    global game
    game.quadrant_x = random.randint(0, 7)
    game.quadrant_y = random.randint(0, 7)
    game.sector_x = random.randint(0, 7)
    game.sector_y = random.randint(0, 7)
    game.star_date = random.randint(0, 50) + 2250
    game.energy = 5000
    game.photon_torpedoes = 10
    game.time_remaining = 40 + random.randint(0, 9)
    game.klingons = 15 + random.randint(0, 5)
    game.starbases = 2 + random.randint(0, 2)
    game.destroyed = False
    game.shield_level = 500
    game.docked = False
    game.SRS = True

    for i in range(8):
        for j in range(8):
            quadrant = Quadrant()
            quadrant.stars = 1 + random.randint(0, 7)
            game.quadrants[i][j] = quadrant

    klingon_count = game.klingons
    starbase_count = game.starbases
    while klingon_count > 0 or starbase_count > 0:
        i = random.randint(0, 7)
        j = random.randint(0, 7)
        quadrant = game.quadrants[i][j]
        if not quadrant.starbase:
            quadrant.starbase = True
            starbase_count -= 1
        if quadrant.klingons < 3:
            quadrant.klingons += 1
            klingon_count -= 1


def print_strings(string_list):
    for string in string_list:
        print(string)
    print()


def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

def clearScreenTop():
    print("\033[H")
    for i in range(12):
        print("                                                     ")
    print("\033[H")

def clearStatusLines():
    print("\033[13;0f")
    for i in range(16):
        print("                                                     ")

def show_help():
    print_strings(commandStrings)

def show_angles():
    print('''
    \033[14;0f
    4  3  2
    5  *  1
    6  7  8
    ''')
    print("\033[13;0f")

def print_slow(str):
    for letter in str:
        sys.stdout.write(letter)
        sys.stdout.flush()
        sleep(0.015)
    sys.stdout.write('\n')
    sys.stdout.flush()

def explosion(x,y):
    print("\033[{0};{1}f\033[7mK\033[0m".format(y + 4, x*3 + 4))
    sleep(0.2)
    print("\033[{0};{1}f○".format(y + 4, x*3 + 4))
    sleep(0.2)
    print("\033[{0};{1}f●".format(y + 4, x*3 + 4))
    sleep(0.2)
    print("\033[{0};{1}f╋".format(y + 4, x*3 + 4))
    sleep(0.2)
    print("\033[{0};{1}f▦".format(y + 4, x*3 + 4))
    sleep(0.2)
    print("\033[{0};{1}f╳".format(y + 4, x*3 + 4))
    sleep(0.2)
    print("\033[{0};{1}f*".format(y + 4, x*3 + 4))
    sleep(0.2)
    print("\033[{0};{1}f\033[7m \033[0m".format(y + 4, x*3 + 4))
    sleep(0.2)


if __name__ == '__main__':
    run()
