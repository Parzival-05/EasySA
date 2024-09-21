from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.keyboards.callback_data.media.media_platform_cd import (
    GetMediaPlatformCD,
)
from src.db.models.media_model import MediaPlatformModel


# ********************************************** Get media **********************************************


async def get_media_platforms_inline_keyboard(medias: list[MediaPlatformModel]):
    def generate_text(media: MediaPlatformModel) -> str:
        return f"{media.name.value}"

    keyboard_build = InlineKeyboardBuilder()
    for media in medias:
        keyboard_build.button(
            text=generate_text(media),
            callback_data=GetMediaPlatformCD.from_model(media),
        )
    return keyboard_build.adjust(1)


# ********************************************** Get media **********************************************
