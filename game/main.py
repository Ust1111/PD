#!/usr/bin/env python3
import traceback
import tcod
import color
import exceptions
import setup_game
import input_handlers


def save_game(handler: input_handlers.BaseEventHandler, filename: str) -> None:
    """Save the game if the current handler has an active Engine."""
    if isinstance(handler, input_handlers.EventHandler):
        try:
            handler.engine.save_as(filename)
            print(f"Game saved successfully. Gold: {handler.engine.player.inventory.gold}")
        except Exception as save_error:
            print(f"Failed to save game: {save_error}")
            if hasattr(handler, 'engine') and hasattr(handler.engine, 'message_log'):
                handler.engine.message_log.add_message(
                    f"Save failed: {save_error}",
                    color.error
                )


def main() -> None:
    screen_width = 80
    screen_height = 50

    try:
        tileset = tcod.tileset.load_tilesheet(
            "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
        )
    except Exception as tileset_error:
        print(f"Failed to load tileset: {tileset_error}")
        raise

    handler: input_handlers.BaseEventHandler = setup_game.MainMenu()

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Roguelike-Game",
        vsync=True,
    ) as context:
        root_console = tcod.console.Console(screen_width, screen_height, order="F")
        try:
            while True:
                try:
                    root_console.clear()
                    handler.on_render(console=root_console)
                    context.present(root_console)

                    for event in tcod.event.wait():
                        context.convert_event(event)
                        handler = handler.handle_events(event)
                except exceptions.QuitWithoutSaving:
                    raise
                except SystemExit:
                    save_game(handler, "savegame.sav")
                    raise
                except Exception as game_error:
                    traceback.print_exc()
                    if isinstance(handler, input_handlers.EventHandler):
                        handler.engine.message_log.add_message(
                            f"Error: {str(game_error)}",
                            color.error
                        )
                        handler.engine.message_log.add_message(
                            f"Debug - Gold: {handler.engine.player.inventory.gold}",
                            color.gold
                        )
                    # Try to recover by returning to main menu
                    handler = setup_game.MainMenu()

        except Exception as fatal_error:
            print(f"Fatal error: {fatal_error}")
            save_game(handler, "autosave.sav")
            raise


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Application crashed: {e}")
        input("Press Enter to exit...")