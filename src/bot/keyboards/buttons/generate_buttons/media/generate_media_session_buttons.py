from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.keyboards.buttons.common import DeletionButtons
from src.bot.keyboards.buttons.media.media_session_buttons import (
    MediaSessionActionButtons,
)
from src.bot.keyboards.callback_data.media.media_session_cd import (
    GetMediaSessionCD,
    AddMediaSessionCD,
    EditMediaSessionCD,
    DeleteMediaSessionCD,
)
from src.db.models.media_model import MediaSessionModel, MediaPlatformModel


# ********************************************** Get media session **********************************************


async def get_media_sessions_inline_keyboard(media_sessions: list[MediaSessionModel]):
    def generate_text(media_session: MediaSessionModel) -> str:
        return f"{media_session.name} | {media_session.media_name.value}"

    keyboard_build = InlineKeyboardBuilder()
    for media_session in media_sessions:
        keyboard_build.button(
            text=generate_text(media_session),
            callback_data=GetMediaSessionCD.from_model(media_session),
        )
    return keyboard_build.adjust(1)


# ********************************************** Get media session **********************************************
# ********************************************** Edit media session **********************************************


async def get_media_session_actions_inline_keyboard(media_session: MediaSessionModel):
    keyboard_build = InlineKeyboardBuilder()
    media_session_action_buttons: list[MediaSessionActionButtons] = [
        MediaSessionActionButtons.EDIT_NAME,
        MediaSessionActionButtons.DELETE,
        # MediaSessionActionButtons.EDIT_CREDS,
    ]
    for media_session_action_button in media_session_action_buttons:
        keyboard_build.button(
            text=media_session_action_button,
            callback_data=EditMediaSessionCD.from_model(
                media_session, media_session_action_button
            ),
        )
    return keyboard_build.adjust(2)


# ********************************************** Edit media session **********************************************
# ********************************************** Delete media session **********************************************
async def get_media_session_deletion_inline_keyboard(media_session: MediaSessionModel):
    keyboard_build = InlineKeyboardBuilder()
    deletion_buttons: list[DeletionButtons] = [DeletionButtons.CONFIRM]
    for deletion_button in deletion_buttons:
        keyboard_build.button(
            text=deletion_button,
            callback_data=DeleteMediaSessionCD.from_model(
                media_session, deletion_button
            ),
        )
    return keyboard_build


# ********************************************** Delete media session **********************************************
# ********************************************** Add media session **********************************************


async def get_media_platforms_to_add_inline_keyboard(
    media_platforms: list[MediaPlatformModel],
):
    keyboard_build = InlineKeyboardBuilder()
    for media_platform in media_platforms:
        keyboard_build.button(
            text=media_platform.name,
            callback_data=AddMediaSessionCD.from_model(media_platform),
        )
    return keyboard_build


# ********************************************** Add media session **********************************************
