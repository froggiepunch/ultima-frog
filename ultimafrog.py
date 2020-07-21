#!/usr/bin/env python3
import tcod

from engine import Engine
from entity import Entity
from game_map import GameMap
from player_input import EventHandler

def main() -> None:
    # Declare the size of the window
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 45

    # We need to set what font/tileset we're using
    # The most common is CHARMAP_CP437 (16x16 grid, previously "ASCII_INROW")
    tileset = tcod.tileset.load_tilesheet(
        "fonts/CGA8x8thick.png", # font file
        16, # how many rows across
        16, # how many columns
        tcod.tileset.CHARMAP_CP437
    )

    # Let's process some events! How vague.
    event_handler = EventHandler()

    player = Entity(int(screen_width / 2), int(screen_height / 2), "@", (255,255,255))
    npc = Entity(int(screen_width / 2 + 5), int(screen_height / 5), "@", (255,255,0))
    entities = {npc, player}

    game_map = GameMap(map_width, map_height)

    engine = Engine(
        entities=entities,
        event_handler=event_handler,
        game_map=game_map,
        player=player)

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="ultima frog",
        vsync=True,
    ) as context:
        # The main off-screen console that we'll draw things to.
        # It will only temporarily have everything drawn to it directly.
        root_console = tcod.Console(screen_width, screen_height, order="F")

        while True:
            engine.render(console=root_console, context=context)

            events = tcod.event.wait()

            engine.handle_events(events)


if __name__ == "__main__":
    # This is just a fancy way to tell the script to only run the main()
    # function if the script is run directly.
    main()
