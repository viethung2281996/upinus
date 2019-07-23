import sys

def get_commands(input):
  commands = []
  command = None
  for char in [*input, None]:
    if char == 'R' or char == 'L' or char == 'W' or char == None:
      if command is not None:
        commands.append(command)
      command = char
    else:
      command = command + char
  return commands

if __name__ == '__main__':
  if len(sys.argv) != 2:
    print("Wrong input, please check again!")
  else:
    x = 0
    y = 0
    direction = 0

    commands = get_commands(sys.argv[1])
    for command in commands:
      if command == 'R':
        direction = direction + 1
      elif command == 'L':
        direction = direction - 1
      else:
        positions = int(command[1:])
        if (direction % 4) == 0:
          y = y + positions
        elif (direction % 4) == 1:
          x = x + positions
        elif (direction % 4) == 2:
          y = y - positions
        else:
          x = x - positions

    if (direction % 4) == 0:
      direction = "North"
    elif (direction % 4) == 1:
      direction = "East"
    elif (direction % 4) == 2:
      direction = "South"
    else:
      direction = "West"
    print("X: {} Y: {} Direction: {}".format(x, y, direction))

