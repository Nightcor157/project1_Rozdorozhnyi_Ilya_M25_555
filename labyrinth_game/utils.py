# labyrinth_game/utils.py

from .constants import ROOMS


def describe_current_room(game_state: dict) -> None:
    """Описание текущей комнаты."""
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


def show_help() -> None:
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")


def solve_puzzle(game_state: dict) -> None:
    """Решение загадки в текущей комнате."""
    room_name = game_state["current_room"]
    room = ROOMS[room_name]
    puzzle = room.get("puzzle")

    if puzzle is None:
        print("Загадок здесь нет.")
        return

    question, correct_answer = puzzle
    print(question)
    answer = input("Ваш ответ: ").strip()

    if answer == correct_answer:
        print("Верно! Вы успешно решили загадку.")
        # Убираем загадку, чтобы нельзя было решить её дважды
        room["puzzle"] = None

        # Награда: ключ в библиотеке
        if room_name == "library":
            inventory = game_state["player_inventory"]
            if "treasure_key" not in inventory:
                inventory.append("treasure_key")
                print("Вы находите сокровищный ключ (treasure_key)!")
    else:
        print("Неверно. Попробуйте снова.")


def attempt_open_treasure(game_state: dict) -> None:
    """Попытка открыть сундук с сокровищами и логика победы."""
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

    # Проверка ключа
    if "treasure_key" in inventory:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        items.remove("treasure_chest")
        print("В сундуке сокровище! Вы победили!")
        game_state["game_over"] = True
        return

    # Предложение ввести код
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
