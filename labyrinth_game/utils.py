import math

from .constants import COMMANDS, ROOMS


def describe_current_room(game_state):
    """Печатает описание текущей комнаты и её содержимое."""    
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
    """Считывает и нормализует ввод пользователя."""
    try:
        return input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def solve_puzzle(game_state):
    """Обрабатывает решение загадки в текущей комнате."""
    current_room = game_state["current_room"]
    room = ROOMS[current_room]

    if not room["puzzle"]:
        print("Загадок здесь нет.")
        return

    question, answer = room["puzzle"]
    print(question)
    user_answer = get_input("Ваш ответ: ")

    normalized = user_answer.strip().lower()
    correct = {answer}
    if answer == "10":
        correct.update({"десять"})
    elif answer == "все":
        correct.update({"все месяцы", "каждый"})

    if normalized in correct:
        print("Правильно! Вы разгадали загадку.")
        room["puzzle"] = None

        # награда зависит от комнаты
        if current_room == "hall":
            reward = "treasure_key"
        elif current_room == "library":
            reward = "rusty key"
        else:
            reward = "gold coin"

        game_state["player_inventory"].append(reward)
        print(f"В награду вы получили: {reward}")
    else:
        print("Неверно. Попробуйте снова.")
        if current_room == "trap_room":
            from .utils import trigger_trap

            trigger_trap(game_state)


def attempt_open_treasure(game_state):
    """Пытается открыть сундук с сокровищами."""
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


def show_help(commands=COMMANDS):
    """Показывает список доступных команд."""
    print("\nДоступные команды:")
    for cmd, desc in commands.items():
        print(f"  {cmd:<16} - {desc}")


def pseudo_random(seed: int, modulo: int) -> int:
    """Генерирует псевдослучайное число от 0 до modulo."""
    x = math.sin(seed * 12.9898) * 123.5453
    frac = x - math.floor(x)
    return int(frac * modulo)


def trigger_trap(game_state):
    """Активирует ловушку в комнате."""
    print("Ловушка активирована! Пол стал дрожать...")

    inventory = game_state["player_inventory"]

    if inventory:
        idx = pseudo_random(game_state["steps"], len(inventory))
        lost_item = inventory.pop(idx)
        print(f"Вы потеряли предмет: {lost_item}")
    else:
        chance = pseudo_random(game_state["steps"], 10)
        if chance < 3:
            print("Ловушка сработала смертельно! Вы проиграли.")
            game_state["game_over"] = True
        else:
            print("Вам повезло! Ловушка едва не погубила вас, но вы уцелели.")


def random_event(game_state):
    """Запускает случайное событие при перемещении игрока."""
    seed = game_state["steps"]

    if pseudo_random(seed, 10) != 0:
        return

    event_type = pseudo_random(seed + 1, 3)

    if event_type == 0:
        print("Вы заметили что-то блестящее на полу — это монетка!")
        current_room = ROOMS[game_state["current_room"]]
        current_room["items"].append("coin")

    elif event_type == 1:
        print("Вы услышали странный шорох из темноты...")
        if "sword" in game_state["player_inventory"]:
            print("К счастью, ваш меч отпугнул неизвестное существо.")

    elif event_type == 2:
        if (
            game_state["current_room"] == "trap_room"
            and "torch" not in game_state["player_inventory"]
        ):
            print("Темнота скрывает опасность... ловушка может сработать!")
            trigger_trap(game_state)
