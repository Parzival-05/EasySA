from dataclasses import dataclass


@dataclass
class Button:
    text: str
    url: str


class Buttons(list[list[Button]]):
    def __str__(self):
        res = ""
        for row in self:
            row_str = ""
            for button in row:
                row_str += f"{button.text}: {button.url} | "
            else:
                row_str = row_str[0:-3]
            res += row_str + "\n"
        else:
            res = res[0:-1]
        return res


class ButtonsParser:
    def __init__(self, buttons_in_text: str):
        self.buttons_in_text = buttons_in_text

    async def parse(self) -> Buttons:
        rows = self.buttons_in_text.split("\n")

        def convert_str_to_button(button_info: str) -> Button:
            first_semicolon_index = button_info.find(":")
            text, url = list(
                map(str.strip, [button_info[0: first_semicolon_index], button_info[first_semicolon_index + 1:]]))
            return Button(text=text, url=url)

        def convert_str_to_row(row_info: str) -> list[Button]:
            buttons_info = list(map(str.strip, row_info.split("|")))
            buttons_info = list(map(convert_str_to_button, buttons_info))
            return buttons_info

        return Buttons(list(map(convert_str_to_row, rows)))
