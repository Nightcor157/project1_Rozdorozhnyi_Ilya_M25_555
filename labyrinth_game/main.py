#!/usr/bin/env python3

# labyrinth_game/main.py

from .constants import COMMANDS
from .player_actions import (
    get_input,
    move_player,
    show_inventory,
    take_item,
    use_item,
)
from .utils import attempt_open_treasure, describe_current_room, show_help, solve_puzzle


def process_command(game_state: dict, command_line: str) -> None:
    command_line = command_line.strip()
    if not command_line:
        return

    parts = command_line.split(maxsplit=1)
    command = parts[0].lower()
    arg = parts[1].lower() if len(parts) > 1 else ""

    match command:
        case "look":
            describe_current_room(game_state)
        case "inventory":
            show_inventory(game_state)
        case "go":
            if arg:
                move_player(game_state, arg)
            else:
                print("Куда идти? Укажите направление.")
        case "take":
            if arg:
                take_item(game_state, arg)
            else:
                print("Что вы хотите взять?")
        case "use":
            if arg:
                use_item(game_state, arg)
            else:
                print("Что вы хотите использовать?")
        case "solve":
            if game_state["current_room"] == "treasure_room":
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)
        case "help":
            show_help(COMMANDS)
        case "north" | "south" | "east" | "west":
            move_player(game_state, command)
        case "quit" | "exit":
            print("Вы решили покинуть лабиринт. Игра окончена.")
            game_state["game_over"] = True
        case _:
            print("Неизвестная команда. Введите 'help' для списка команд.")


def main() -> None:
    game_state = {
        "player_inventory": [],
        "current_room": "entrance",
        "game_over": False,
        "steps_taken": 0,
    }

    print("Добро пожаловать в Лабиринт сокровищ!")

    describe_current_room(game_state)

    while not game_state["game_over"]:
        command_line = get_input("> ")
        process_command(game_state, command_line)


if __name__ == "__main__":
    main()

