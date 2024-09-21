from src.bot.keyboards.buttons.menu_buttons import MediaButtons, StreamerButtons
from src.bot.keyboards.main_menu import MainMenuButtons

ALL_MENU_BUTTONS = [MainMenuButtons, StreamerButtons, MediaButtons]


async def check_is_button_pressed(text):
    for button_container in ALL_MENU_BUTTONS:
        for button in button_container:
            if button == text:
                return True
    return False
