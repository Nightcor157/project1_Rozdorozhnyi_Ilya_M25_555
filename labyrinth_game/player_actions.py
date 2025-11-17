# labyrinth_game/player_actions.py

from .constants import ROOMS
from .utils import describe_current_room, random_event


def get_input(prompt: str = "> ") -> str:
    """Безопасно запросить ввод у пользователя."""
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def show_inventory(game_state: dict) -> None:
    """Показать содержимое инвентаря игрока."""
    inventory = game_state["player_inventory"]
    if not inventory:
        print("Ваш инвентарь пуст.")
        return

    print("В вашем инвентаре:")
    for item in inventory:
        print(f"  - {item}")


def move_player(game_state: dict, direction: str) -> None:
    """Переместить игрока в указанном направлении, если это возможно."""
    room_name = game_state["current_room"]
    room = ROOMS[room_name]
    exits = room.get("exits", {})

    if direction not in exits:
        print("Нельзя пойти в этом направлении.")
        return

    new_room = exits[direction]

    if new_room == "treasure_room":
        inventory = game_state["player_inventory"]
        if "rusty_key" in inventory:
            print(
                "Вы используете найденный ключ, чтобы открыть путь "
                "в комнату сокровищ."
            )
        else:
            print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
            return

    game_state["current_room"] = new_room
    game_state["steps_taken"] += 1
    describe_current_room(game_state)
    random_event(game_state)


def take_item(game_state: dict, item_name: str) -> None:
    """Попытаться поднять предмет из текущей комнаты."""
    if item_name == "treasure_chest":
        print("Вы не можете поднять сундук, он слишком тяжелый.")
        return

    room_name = game_state["current_room"]
    room = ROOMS[room_name]
    items = room.get("items", [])

    if item_name in items:
        items.remove(item_name)
        game_state["player_inventory"].append(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")


def use_item(game_state: dict, item_name: str) -> None:
    """Использовать предмет из инвентаря игрока."""
    inventory = game_state["player_inventory"]

    if item_name not in inventory:
        print("У вас нет такого предмета.")
        return

    if item_name == "torch":
        print("Вы поднимаете факел, и вокруг становится гораздо светлее.")
    elif item_name == "sword":
        print("Вы сжимаете меч в руке и чувствуете уверенность.")
    elif item_name == "bronze_box":
        if "rusty_key" in inventory:
            print("Вы открываете бронзовую шкатулку, но внутри уже пусто.")
        else:
            print("Вы открываете бронзовую шкатулку и находите внутри ржавый ключ.")
            inventory.append("rusty_key")
    else:
        print("Вы не знаете, как использовать этот предмет.")

