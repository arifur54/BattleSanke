# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com



import random
import typing
from scipy import spatial

# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "Team 4",  # TODO: Your Battlesnake Username
        "color": "#ffc34d",  # TODO: Choose color
        "head": "dragon",  # TODO: Choose head
        "tail": "flame",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")

# Avoid Walls 
def avoid_walls(board_height, board_width, possible_moves):
  remove = []

  for direction, location in possible_moves.items():
    x_out_of_range = (location["x"] < 0 or location['x'] == board_width)
    y_out_of_range = (location["y"] < 0 or location['y'] == board_height)

    if x_out_of_range or y_out_of_range:
      remove.append(direction)

  for direction in remove:
    del possible_moves[direction]

  return possible_moves

# Avoid Body
def avoid_body(my_body, possible_moves):
  remove = []

  for direction, location in possible_moves.items():
    if location in my_body:
      remove.append(direction)
  for direction in remove:
    del possible_moves[direction]

  print(f"possible_moveis {possible_moves}")
  return possible_moves

# Avoid Other Snakes
def avoid_other_snakes(other_snakes, possible_moves):
  remove = []
  for snake in other_snakes:
    for direction, location, in possible_moves.items():
      if location in snake['body']:
        remove.append(direction)
  
  for direction in remove:
    del possible_moves[direction]

  return possible_moves

def food_location(foods, my_head):
  coordinates = []

  if len(foods) == 0:
    return None

  for food in foods:
    coordinates.append((food["x"], food["y"]))

  tree = spatial.KDTree(coordinates)
  
  results = tree.query([(my_head["x"], my_head["y"])])[1]
  return foods[results[0]]

def move_twoard_target(possible_moves, my_head, target):
  distance_x = abs(my_head["x"] - target["x"])
  distance_y = abs(my_head["y"] - target["y"])

  for direction, location in possible_moves.items():
    new_distance_x = abs(location["x"] - target["x"])
    new_distance_y = abs(location["y"] - target["y"])

    if new_distance_x < distance_x or new_distance_y < distance_y:
      return direction

  return list(possible_moves.keys())[0]

def move_away_from_target_and_loop(possible_moves, my_head, target):
  distance_x = abs(target["x"] - my_head["x"])
  distance_y = abs(target["y"] - my_head["y"])

  for direction, location in possible_moves.items():
    new_distance_x = abs(target["x"] - location["x"])
    new_distance_y = abs(target["y"] - location["y"])

    if new_distance_x > distance_x or new_distance_y > distance_y:
      return direction

  return list(possible_moves.keys())[0]

def stupid_Move(possible_moves, my_head, target):
  distance_x = abs(my_head["x"] + target["x"])
  distance_y = abs(my_head["y"] + target["y"])

  for direction, location in possible_moves.items():
    new_distance_x = abs(location["x"] + target["x"])
    new_distance_y = abs(location["y"] + target["y"])

    if new_distance_x > distance_x or new_distance_y > distance_y:
      return direction

  return list(possible_moves.keys())[0]
  
# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
    my_health = game_state['you']['health']
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"
    my_body = game_state['you']['body']
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']
    other_snakes = game_state['board']['snakes']
    food = game_state['board']['food']
    turn = game_state['turn']
  
    other_snakes_body = []
    other_snakes_head = {}
    other_snakes_neck = {}
  
    for snake in other_snakes:
      other_snakes_body =  snake['body']
      other_snakes_head = snake['body'][0]
      other_snakes_neck = snake['body'][1]

    print(f"Body: {other_snakes_body} Head: {other_snakes_head}")
    print(f"turn: {turn}")
    possible_moves = {
      "up": {
        "x": my_head["x"],
        "y": my_head["y"] + 1,
      }, 
      "down": {
        "x": my_head["x"] ,
        "y": my_head["y"] - 1,
      }, 
      "left": {
        "x": my_head["x"] - 1,
        "y": my_head["y"],
      }, 
      "right": {
        "x": my_head["x"] + 1,
        "y": my_head["y"],
      }
    }

    # We've included code to prevent your Battlesnake from moving backwards
    
    possible_moves = avoid_body(my_body, possible_moves)
    possible_moves = avoid_walls(board_width, board_height, possible_moves)
    possible_moves = avoid_other_snakes(other_snakes, possible_moves)
    food_loc = food_location(food, my_head)
   
    if len(possible_moves) > 0:
      if turn > 0:
        if food_loc is not None:
          if len(my_body) < 9 or my_health < 35:
            if(len(other_snakes_body) < len(my_body)):
              move = move_twoard_target(possible_moves, my_head, other_snakes_head)
            # elif(len(other_snakes_body) >= len(my_body) and my_health > 80):
            #   move = move_away_from_target_and_loop(possible_moves, my_head, other_snakes_head)
            else:
              move = move_twoard_target(possible_moves, my_head, food_loc)
          else:
            possible_moves = list(possible_moves.keys())
            move = random.choice(possible_moves)
        else:
          possible_moves = list(possible_moves.keys())
          move = random.choice(possible_moves)
      else: 
        move = move_away_from_target_and_loop(possible_moves, my_head, other_snakes_head)
    else:
      move = "down"
    # Choose a random move from the safe ones
    #next_move = random.choice(safe_moves)

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    # food = game_state['board']['food']

    print(f"MOVE {game_state['turn']}: {move}")
    return {"move": move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({
        "info": info, 
        "start": start, 
         "move": move, 
        "end": end
    })
