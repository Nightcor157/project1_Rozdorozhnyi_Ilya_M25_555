# labyrinth_game/player_actions.py

from .constants import ROOMS
from .utils import describe_current_room


def get_input(prompt: str = "> ") -> str:
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def show_inventory(game_state: dict) -> None:
    inventory = game_state["player_inventory"]
    if not inventory:
        print("Ваш инвентарь пуст.")
        return

    print("В вашем инвентаре:")
    for item in inventory:
        print(f"  - {item}")


def move_player(game_state: dict, direction: str) -> None:
    room_name = game_state["current_room"]
    room = ROOMS[room_name]
    exits = room.get("exits", {})

    if direction in exits:
        new_room = exits[direction]
        game_state["current_room"] = new_room
        game_state["steps_taken"] += 1
        describe_current_room(game_state)
    else:
        print("Нельзя пойти в этом направлении.")


def take_item(game_state: dict, item_name: str) -> None:
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
