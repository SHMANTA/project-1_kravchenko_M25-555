from .constants import ROOMS


def describe_current_room(game_state):
    room_name = game_state["current_room"]
    room = ROOMS[room_name]

    print(f"\n== {room_name.upper()} ==")
    print(room["description"])

    if room["items"]:
        print("Заметные предметы:", ", ".join(room["items"]))

    exits = ", ".join(room["exits"].keys())
    print("Выходы:", exits)

    if room["puzzle"]:
        print("Кажется, здесь есть загадка (используйте команду solve).")


def get_input(prompt="> "):
    try:
        return input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def solve_puzzle(game_state):
    current_room = game_state["current_room"]
    room = ROOMS[current_room]

    if not room["puzzle"]:
        print("Загадок здесь нет.")
        return

    question, answer = room["puzzle"]
    print(question)
    user_answer = get_input("Ваш ответ: ")

    if user_answer == answer:
        print("Правильно! Вы разгадали загадку.")
        room["puzzle"] = None
        reward = "treasure_key" if current_room == "hall" else "gold coin"
        game_state["player_inventory"].append(reward)
        print(f"В награду вы получили: {reward}")
    else:
        print("Неверно. Попробуйте снова.")


def attempt_open_treasure(game_state):
    current_room = game_state["current_room"]
    room = ROOMS[current_room]

    if "treasure chest" not in room["items"]:
        print("Сундук уже открыт или отсутствует.")
        return

    inventory = game_state["player_inventory"]

    if "treasure_key" in inventory or "rusty key" in inventory:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        room["items"].remove("treasure chest")
        print("В сундуке сокровище! Вы победили!")
        game_state["game_over"] = True
        return

    choice = get_input("Сундук заперт. У вас нет ключа. Ввести код? (да/нет) ")
    if choice == "да":
        if room["puzzle"]:
            _, correct_code = room["puzzle"]
            code = get_input("Введите код: ")
            if code == correct_code:
                print("Код верный! Замок открывается.")
                room["items"].remove("treasure chest")
                print("В сундуке сокровище! Вы победили!")
                game_state["game_over"] = True
            else:
                print("Неверный код. Сундук остаётся запертым.")
        else:
            print("Здесь нет загадки для открытия сундука.")
    else:
        print("Вы отступаете от сундука.")


def show_help():
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")
