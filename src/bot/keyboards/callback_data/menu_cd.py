from src.bot.keyboards.buttons.menu_buttons import BaseMenuButtons
from src.bot.keyboards.callback_data.base_cd import BaseCD


class MenuCD(BaseCD, prefix="MenuCD"):
    text: str

    @staticmethod
    def from_button(button: BaseMenuButtons):
        return MenuCD(text=button.value)
