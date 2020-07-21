#!/usr/bin/env python3
import tcod

from actions import EscapeAction, MovementAction
from entity import Entity
from player_input import EventHandler

def main() -> None:
    # Declare the size of the window
    screen_width = 80
    screen_height = 50

    # We need to set what font/tileset we're using
    # The most common is CHARMAP_CP437 (16x16 grid, previously "ASCII_INROW")
    tileset = tcod.tileset.load_tilesheet("fonts/CGA8x8thick.png", 16, 16,
        tcod.tileset.CHARMAP_CP437
    )

    # Let's process some events! How vague.
    event_handler = EventHandler()

    player = Entity(int(screen_width / 2), int(screen_height / 2), "@", (255,255,255))
    npc = Entity(int(screen_width / 2 + 5), int(screen_height / 5), "@", (255,255,0))
    entities = {npc, player}

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
            root_console.print(x=player.x, y=player.y, string=player.char, fg=player.colour)

            # This was previously the "flush" call
            context.present(root_console)

            # Clean up junk left behind by stuff that gets drawn in new places
            root_console.clear()

            for event in tcod.event.wait():
                action = event_handler.dispatch(event)

                # Self explanitory, if nothing happens just keep moving
                if action is None:
                    continue

                # If the event is a movement action...move!
                if isinstance(action, MovementAction):
                    player.move(dx=action.dx, dy=action.dy)

                # If user presses "esc", blow up!
                elif isinstance(action, EscapeAction):
                    raise SystemExit()


if __name__ == "__main__":
    # This is just a fancy way to tell the script to only run the main()
    # function if the script is run directly.
    main()
