from aiogram import F
from aiogram.types import CallbackQuery
from sqlalchemy.orm import Session

from src.bot.handlers.media.media_router import media_router
from src.bot.keyboards.buttons.generate_buttons.generate_reply_markup import (
    get_reply_markup,
)
from src.bot.keyboards.buttons.generate_buttons.media.generate_media_platform_buttons import (
    get_media_platforms_inline_keyboard,
)
from src.bot.keyboards.buttons.generate_buttons.media.generate_media_session_buttons import (
    get_media_sessions_inline_keyboard,
    get_media_session_actions_inline_keyboard,
)
from src.bot.keyboards.buttons.generate_buttons.media.media_back_button import (
    get_media_sessions_back_button,
)
from src.bot.keyboards.buttons.menu_buttons import MediaButtons
from src.bot.keyboards.callback_data.media.media_session_cd import GetMediaSessionCD
from src.bot.keyboards.callback_data.menu_cd import MenuCD
from src.domain.media_platforms.get_by_name import get_media_profile_class
from src.db.models.media_model import MediaSessionModel
from src.db.repository.media_repository import (
    MediaPlatformRepository,
    MediaSessionRepository,
)


@media_router.callback_query(MenuCD.filter(F.text == MediaButtons.GET_LIST))
async def return_medias(callback_query: CallbackQuery, db_session: Session):
    media_repository = MediaPlatformRepository(db_session)
    reply_markup = await get_reply_markup(
        await get_media_platforms_inline_keyboard(await media_repository.list())
    )
    await callback_query.message.edit_text(
        text="Список медиа платформ", reply_markup=reply_markup
    )


@media_router.callback_query(MenuCD.filter(F.text == MediaButtons.GET_SESSIONS_LIST))
async def return_media_sessions(callback_query: CallbackQuery, db_session: Session):
    media_session_repository = MediaSessionRepository(db_session)
    reply_markup = await get_reply_markup(
        await get_media_sessions_inline_keyboard(await media_session_repository.list())
    )
    await callback_query.message.edit_text(
        text="Выберите медиа", reply_markup=reply_markup
    )


def generate_media_info(media_session: MediaSessionModel) -> str:
    media_profile = get_media_profile_class(media_session.media_name)
    return (
        f"• Название медиа: {media_session.name}\n"
        f"• Платформа: {media_session.media_name.value}\n"
        f"{media_profile.get_important_for_user_info(media_session)}"
    )


@media_router.callback_query(GetMediaSessionCD.filter())
async def return_media(
    callback_query: CallbackQuery,
    db_session: Session,
    callback_data: GetMediaSessionCD,
):
    media_id = callback_data.media_session_id
    media_session_repository = MediaSessionRepository(db_session)
    media_session: MediaSessionModel = await media_session_repository.get_one(
        id=media_id
    )
    go_back_button = get_media_sessions_back_button()
    if not media_session:
        text = f"Медиа не существует."
        reply_markup = None
    else:
        text = generate_media_info(media_session)
        reply_markup = await get_reply_markup(
            await get_media_session_actions_inline_keyboard(media_session),
            go_back_button,
        )
    await callback_query.message.edit_text(
        text=text,
        reply_markup=reply_markup,
    )
