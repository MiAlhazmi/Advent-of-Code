cave = []
robot_track = []
# energized_tiles
line_length = 110
# line_length = 10
directions = ["n", "s", "e", "w"]
dir_movement = {"n": -line_length, "s": line_length, "e": 1, "w": -1, "ne": -line_length + 1, "nw": -line_length - 1, "se": line_length + 1, "sw": line_length - 1}
beeper_exist_in = {}


class KaliTheRobot:
    position = 0
    direction = ""
    dead_end = False
    track = {}  # a map to save previous positions with the coressponding direction

    def __init__(self, position: int, direction: str):
        self.position = position
        self.direction = direction
        self.dead_end = False

    def __str__(self):
        return f"Kali is at pos: {self.position % line_length} line: {int(self.position / line_length)} facing {self.direction} with dead end = {self.dead_end}"


def front_is_clear(robot: KaliTheRobot):
    print(f"front_is_clear() function: {robot}")

    match robot.direction:
        case "n" | "ne" | "nw":
            if robot.position + dir_movement["n"] < 0:
                return False
            else:
                return True
        case "s" | "se" | "sw":
            if robot.position + dir_movement["s"] > len(cave):
                return False
            else:
                return True
        case "e":
            if robot.position % line_length == line_length - 1:   # example: 9 % 10 == 9
                return False
            else:
                return True
        case "w":
            if robot.position % line_length == 0 or robot.position == 0:
                return False
            else:
                return True


def block_is_clear(robot: KaliTheRobot):
    print(f"block_is_clear() function: {robot}")
    print(f"\tcave[robot.position]: {cave[robot.position]} == .? {cave[robot.position] == "."}")
    return cave[robot.position] == "."


# change the direction 'dir'
def change_direction(robot: KaliTheRobot):
    print(f"change_direction() function: {robot}")
    obstacle = cave[robot.position]
    print(f"\t obstacle is {obstacle}")
    match obstacle:
        # Splitters:
        case "|":
            print(f"\t case is |")
            if robot.direction == "n" or robot.direction == "s":
                put_beeper(robot)
                robot = move(robot)
                start(robot)
            else:
                # split here (fork)
                put_beeper(robot)

                # ---- instead of modifying the current robot we should initialize new robot object ----
                # robot.direction = "n"
                robot_north = KaliTheRobot(robot.position, "n")

                robot_north = move(robot_north)  # this go up
                start(robot_north)

                # ---- instead of modifying the current robot we should initialize new robot object ----
                # robot.direction = "s"
                robot_south = KaliTheRobot(robot.position, "s")

                robot_south = move(robot_south) # this go down
                start(robot_south)
        case "-":
            if robot.direction == "e" or robot.direction == "w":
                put_beeper(robot)
                robot = move(robot)
                start(robot)
            else:
                # split here (fork)
                put_beeper(robot)

                robot_east = KaliTheRobot(robot.position, "e")
                robot_east = move(robot_east)  # this go right
                start(robot_east)

                robot_west = KaliTheRobot(robot.position, "w")
                robot_west = move(robot_west)  # this go left
                start(robot_west)
        # mirrors:
        case "/":
            put_beeper(robot)
            
            if robot.direction == "n":
                robot.direction = "e"
                robot = move(robot)
                start(robot)
            elif robot.direction == "s":
                robot.direction = "w"
                robot = move(robot)
                start(robot)
            elif robot.direction == "e":
                robot.direction = "n"
                robot = move(robot)
                start(robot)
            elif robot.direction == "w":
                robot.direction = "s"
                robot = move(robot)
                start(robot)

    #### I thought we shoud go diagnol :( anyways bellow is the solution if that was the case vvvv ####
            # if robot.direction == "ne" or robot.direction == "sw":
            #     put_beeper(robot)
            #     robot = move(robot)
            #     start(robot)
            # else:
                # change direction here
                # put_beeper(robot)

                # ---- change the direction: ---- #
                # if coming from west towards east:
                # if robot.direction == "e":
                #     robot.direction = "ne"
                # if coming from east towards west:
                # elif robot.direction == "w":
                #     robot.direction = "sw"

                # robot = move(robot)
                # start(robot)
        case "\\":
            put_beeper(robot)
            if robot.direction == "n":
                robot.direction = "w"
                robot = move(robot)
                start(robot)
            elif robot.direction == "s":
                robot.direction = "e"
                robot = move(robot)
                start(robot)
            elif robot.direction == "e":
                robot.direction = "s"
                robot = move(robot)
                start(robot)
            elif robot.direction == "w":
                robot.direction = "n"
                robot = move(robot)
                start(robot)


    #### I thought we shoud go diagnol :( anyways bellow is the solution if that was the case vvvv ####

            # if robot.direction == "nw" or robot.direction == "se":
            #     put_beeper(robot)
            #     robot = move(robot)
            #     start(robot)
            # else:
                # change direction here
                # put_beeper(robot)

                # ---- change the direction: ---- #
                # if coming from west towards east:
                # if robot.direction == "e":
                #     robot.direction = "se"
                # if coming from east towards west:
                # elif robot.direction == "w":
                #     robot.direction = "nw"

                # robot = move(robot)
                # start(robot)


# This function move one block towards the direction
def move(robot: KaliTheRobot):
    print(f"move() function: {robot}")
    if front_is_clear(robot):
        robot.position += dir_movement[robot.direction]
        if robot.track.get(robot.position) == robot.direction:  # if the robot was in the same position and direction before
            robot.dead_end = True
        else:
            robot.track[robot.position] = robot.direction
    else:
        print("\tfront is not clear")
        robot.dead_end = True
    print(f"\t{robot.position}")
    return robot


def put_beeper(robot: KaliTheRobot):
    print(f"put_beeper() function: {robot}")
    # cave.replace(robot.position, "#")
    robot_track[robot.position] = "#"


def start(robot: KaliTheRobot):
    print(f"start() function: {robot}")
    while not robot.dead_end and block_is_clear(robot):
        put_beeper(robot)  # -> put '#'
        robot = move(robot)
        print()
    if not robot.dead_end:
        change_direction(robot)
        print()

    print("--------------------------------------------------------------\n")


if __name__ == '__main__':
    f = open("real.txt", "r")
    while True:
        letter = f.read(1)
        if not letter:
            break
        if letter != '\n':
            cave += letter
    robot_track = cave.copy()

    energized_tiles = 0
    kali = KaliTheRobot(0, "e")
    print("---------------------------------------------------------------\n")
    start(kali)
    print("\n---------------------------------------------------------------\n")
    for i in range(len(cave)):
        if i % line_length == 0:
            print()
        print(cave[i], end=" ")
    print()
    for i in range(len(cave)):
        if i % line_length == 0:
            print()
        print(robot_track[i], end=" ")
        if robot_track[i] == "#":
            energized_tiles += 1

    print(f"\n {energized_tiles}")