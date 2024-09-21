from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.keyboards.buttons.common import DeletionButtons
from src.bot.keyboards.buttons.streamer_buttons import (
    StreamerActionButtons,
    StreamerInfoButtons,
)
from src.bot.keyboards.callback_data.streamer.streamer_cd import (
    GetStreamerCD,
    EditStreamerCD,
    DeleteStreamerCD,
    GetPlatformNameCD,
)
from src.db.models.streamer_model import StreamerModel
from src.domain.stream_platforms.stream_platform_names import (
    StreamPlatformNames,
)


# ********************************************** Get streamers **********************************************


async def get_streamers_inline_keyboard(streamers: list[StreamerModel]):
    def generate_text(streamer: StreamerModel):
        activity_status = (
            "🟢 Постинг активен" if streamer.is_active else "🔴 Постинг не активен"
        )
        return f"{streamer.name} | {activity_status} | {streamer.stream_platform_name.value}"

    keyboard_build = InlineKeyboardBuilder()
    for streamer in streamers:
        keyboard_build.button(
            text=generate_text(streamer),
            callback_data=GetStreamerCD.from_model(
                streamer, StreamerInfoButtons.STREAMER
            ),
        )
    return keyboard_build.adjust(1)


# ********************************************** Get streamers **********************************************
# ********************************************** Edit streamer **********************************************


async def get_streamer_actions_inline_keyboard(streamer: StreamerModel):
    keyboard_build = InlineKeyboardBuilder()
    streamer_buttons: list[StreamerActionButtons | StreamerInfoButtons] = [
        StreamerInfoButtons.POSTS,
        StreamerInfoButtons.MEDIAS,
        StreamerActionButtons.EDIT_NAME,
        StreamerActionButtons.DELETE,
        (
            StreamerActionButtons.SET_AS_INACTIVE
            if streamer.is_active
            else StreamerActionButtons.SET_AS_ACTIVE
        ),
    ]
    for streamer_button in streamer_buttons:
        text = streamer_button
        if isinstance(streamer_button, StreamerActionButtons):
            callback_data = EditStreamerCD.from_model(streamer, streamer_button)
        else:
            callback_data = GetStreamerCD.from_model(streamer, streamer_button)
        keyboard_build.button(
            text=text,
            callback_data=callback_data,
        )
    return keyboard_build.adjust(2)


# ********************************************** Edit streamer **********************************************
# ********************************************** Delete streamer **********************************************
async def get_streamer_deletion_inline_keyboard(streamer: StreamerModel):
    keyboard_build = InlineKeyboardBuilder()
    streamer_deletion_buttons: list[DeletionButtons] = [DeletionButtons.CONFIRM]
    for streamer_button in streamer_deletion_buttons:
        keyboard_build.button(
            text=streamer_button,
            callback_data=DeleteStreamerCD.from_model(streamer, streamer_button),
        )
    return keyboard_build


# ********************************************** Delete streamer **********************************************
# ********************************************** Add streamer **********************************************


async def get_streamer_platforms_inline_keyboard():
    keyboard_build = InlineKeyboardBuilder()
    for streamer_platform_name in StreamPlatformNames:
        keyboard_build.button(
            text=streamer_platform_name.value,
            callback_data=GetPlatformNameCD.from_platform_name(streamer_platform_name),
        )
    return keyboard_build
