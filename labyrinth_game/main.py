#!/usr/bin/env python3
from .player_actions import (
    move_player,
    show_inventory,
    take_item,
    use_item,
)
from .utils import (
    attempt_open_treasure,
    describe_current_room,
    get_input,
    solve_puzzle,
)


def process_command(game_state, command):
    parts = command.split()
    if not parts:
        return

    cmd = parts[0]
    arg = parts[1] if len(parts) > 1 else None

    match cmd:
        case "look":
            describe_current_room(game_state)
        case "go":
            if arg:
                move_player(game_state, arg)
            else:
                print("Куда идти? Используйте: go <направление>")
        case "take":
            if arg:
                take_item(game_state, arg)
            else:
                print("Что взять? Используйте: take <предмет>")
        case "use":
            if (
                arg == "treasure_chest"
                and game_state["current_room"] == "treasure_room"
            ):
                attempt_open_treasure(game_state)
            elif arg:
                use_item(game_state, arg)
            else:
                print("Что использовать? Используйте: use <предмет>")
        case "solve":
            solve_puzzle(game_state)
        case "inventory":
            show_inventory(game_state)
        case "quit" | "exit":
            print("Вы покинули игру.")
            game_state["game_over"] = True
        case _:
            print(
                "Неизвестная команда. Доступные: look, go, take, use, solve, inventory, quit"
            )


def main():
    game_state = {
        "current_room": "entrance",
        "player_inventory": [],
        "steps": 0,
        "game_over": False,
    }

    print("Добро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state)

    while not game_state["game_over"]:
        command = get_input("> ")
        process_command(game_state, command)


if __name__ == "__main__":
    main()
