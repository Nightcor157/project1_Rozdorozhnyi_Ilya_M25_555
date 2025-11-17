# labyrinth_game/utils.py

import math

from .constants import (
    COMMANDS,
    EVENT_PROBABILITY_MODULO,
    ROOMS,
    TRAP_DAMAGE_MODULO,
    TRAP_DEATH_THRESHOLD,
)


def pseudo_random(seed: int, modulo: int) -> int:
    """Простейший псевдослучайный генератор на основе синуса."""
    if modulo <= 0:
        return 0

    x = math.sin(seed * 12.9898) * 43758.5453
    frac = x - math.floor(x)
    value = int(math.floor(frac * modulo))
    return value


def describe_current_room(game_state: dict) -> None:
    """Вывести описание текущей комнаты и доступные действия."""
    room_name = game_state["current_room"]
    room = ROOMS[room_name]

    print(f"\n== {room_name.upper()} ==")
    print(room["description"])

    if room.get("items"):
        print("Заметные предметы:")
        for item in room["items"]:
            print(f"  - {item}")

    exits = room.get("exits", {})
    if exits:
        print("Выходы:")
        for direction, target_room in exits.items():
            print(f"  {direction} -> {target_room}")

    if room.get("puzzle") is not None:
        print("Кажется, здесь есть загадка (используйте команду solve).")


def show_help(commands: dict | None = None) -> None:
    """Показать доступные команды игроку."""
    if commands is None:
        commands = COMMANDS

    print("\nДоступные команды:")
    for pattern, description in commands.items():
        print(f"  {pattern.ljust(16)} - {description}")


def trigger_trap(game_state: dict) -> None:
    """Сымитировать срабатывание ловушки с негативными последствиями."""
    print("Ловушка активирована! Пол начинает дрожать...")

    inventory = game_state["player_inventory"]
    if inventory:
        index = pseudo_random(game_state["steps_taken"], len(inventory))
        lost_item = inventory.pop(index)
        print(f"Вы теряете предмет: {lost_item}")
        return

    # Инвентарь пуст — возможен смертельный исход
    roll = pseudo_random(game_state["steps_taken"], TRAP_DAMAGE_MODULO)
    if roll < TRAP_DEATH_THRESHOLD:
        print("Пол разверзается под вами. Вы падаете в пропасть. Игра окончена.")
        game_state["game_over"] = True
    else:
        print("Пол трескается, но вы чудом удерживаетесь на краю.")


def random_event(game_state: dict) -> None:
    """Генерация небольших случайных событий при перемещении игрока."""
    seed = game_state["steps_taken"]
    chance = pseudo_random(seed, EVENT_PROBABILITY_MODULO)

    # Низкая вероятность события
    if chance != 0:
        return

    room_name = game_state["current_room"]
    room = ROOMS[room_name]
    inventory = game_state["player_inventory"]

    event_type = pseudo_random(seed + 1, 3)

    if event_type == 0:
        # Находка
        print("Вы замечаете на полу блестящую монетку.")
        room.setdefault("items", []).append("coin")
    elif event_type == 1:
        # Испуг
        print("Где-то рядом слышится тревожный шорох...")
        if "sword" in inventory:
            print("Вы крепче сжимаете меч, и существо в темноте отступает.")
    elif event_type == 2:
        # Ловушка в trap_room без факела
        if room_name == "trap_room" and "torch" not in inventory:
            print("Вы наступаете на подозрительную плиту — это может быть ловушка!")
            trigger_trap(game_state)


def solve_puzzle(game_state: dict) -> None:
    """Позволить игроку попытаться решить загадку в текущей комнате."""
    room_name = game_state["current_room"]
    room = ROOMS[room_name]
    puzzle = room.get("puzzle")

    if puzzle is None:
        print("Загадок здесь нет.")
        return

    question, correct_answer = puzzle
    print(question)
    answer = input("Ваш ответ: ").strip()

    user_answer = answer.lower()
    correct = correct_answer.lower()

    alternatives = {correct}
    if correct_answer == "10":
        alternatives.add("десять")
    if correct_answer == "4":
        alternatives.add("четыре")

    if user_answer in alternatives:
        print("Верно! Вы успешно решили загадку.")
        room["puzzle"] = None

        if room_name == "library":
            inventory = game_state["player_inventory"]
            if "treasure_key" not in inventory:
                inventory.append("treasure_key")
                print("Вы находите сокровищный ключ (treasure_key)!")
    else:
        print("Неверно. Попробуйте снова.")
        if room_name == "trap_room":
            trigger_trap(game_state)


def attempt_open_treasure(game_state: dict) -> None:
    """Попытаться открыть сундук с сокровищами и завершить игру победой."""
    room_name = game_state["current_room"]
    if room_name != "treasure_room":
        print("Здесь нет сокровищного сундука.")
        return

    room = ROOMS[room_name]
    items = room.get("items", [])
    inventory = game_state["player_inventory"]

    if "treasure_chest" not in items:
        print("Сундук уже открыт или его здесь нет.")
        return

    if "treasure_key" in inventory:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        items.remove("treasure_chest")
        print("В сундуке сокровище! Вы победили!")
        game_state["game_over"] = True
        return

    print("Сундук заперт. Похоже, его можно открыть кодом.")
    choice = input("Ввести код? (да/нет) ").strip().lower()

    if choice != "да":
        print("Вы отступаете от сундука.")
        return

    code = input("Введите код: ").strip()
    puzzle = room.get("puzzle")
    correct_answer = puzzle[1] if puzzle is not None else ""

    if code == correct_answer:
        print("Код верный! Замок открывается.")
        items.remove("treasure_chest")
        print("В сундуке сокровище! Вы победили!")
        game_state["game_over"] = True
    else:
        print("Неверный код. Сундук остаётся закрытым.")

