from .constants import ROOMS
from .utils import describe_current_room


def show_inventory(game_state):
    inventory = game_state["player_inventory"]
    if inventory:
        print("Ваш инвентарь:", ", ".join(inventory))
    else:
        print("Ваш инвентарь пуст.")


def move_player(game_state, direction):
    current_room = game_state["current_room"]
    exits = ROOMS[current_room]["exits"]

    if direction in exits:
        game_state["current_room"] = exits[direction]
        game_state["steps"] += 1
        describe_current_room(game_state)
    else:
        print("Нельзя пойти в этом направлении.")


def take_item(game_state, item_name):
    current_room = game_state["current_room"]
    room_items = ROOMS[current_room]["items"]

    if item_name in room_items:
        game_state["player_inventory"].append(item_name)
        room_items.remove(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")


def use_item(game_state, item_name):
    inventory = game_state["player_inventory"]

    if item_name not in inventory:
        print("У вас нет такого предмета.")
        return

    if item_name == "torch":
        print("Вы зажгли факел. Вокруг стало светлее!")
    elif item_name == "sword":
        print("Вы сжали меч и почувствовали уверенность.")
    elif item_name == "bronze box":
        print("Вы открыли бронзовую шкатулку...")
        if "rusty key" not in inventory:
            inventory.append("rusty key")
            print("Внутри лежит ржавый ключ. Вы добавили его в инвентарь.")
        else:
            print("Но внутри уже пусто.")
    else:
        print("Вы не знаете, как использовать этот предмет.")
