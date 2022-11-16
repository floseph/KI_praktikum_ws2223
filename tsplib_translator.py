import re


def xy_coords(file_path):
  f = open(file_path, "r")
  x = []
  y = []

  current_line = f.readline()

  # read until NODE_COORD_SECTION
  while("NODE_COORD_SECTION" not in current_line):
    current_line = f.readline()

  # read all the raw data
  while("EOF" not in current_line):
    
    current_line = f.readline()

    current_line = re.split("[\s]", current_line)
    
    # list with [node#, x, y]
    data_row = list(filter(lambda e : e.isdigit() is True, current_line))

    # x.append(data_row[1])
    if(data_row != []):
      x.append(int(data_row[1]))
      y.append(int(data_row[2]))


  f.close()
  print("done")
  return x,y
