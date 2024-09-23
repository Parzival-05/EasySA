from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.orm import Session

from config import CommonConfig
from src.bot.handlers.streamer.post.post_router import post_router
from src.bot.keyboards.buttons.generate_buttons.generate_reply_markup import (
    get_reply_markup,
)
from src.bot.keyboards.buttons.generate_buttons.streamer.post.generate_post_buttons import (
    get_choose_media_type_inline_keyboard,
)
from src.bot.keyboards.buttons.post.preview_buttons import PostPreviewButtons
from src.bot.keyboards.callback_data.streamer.post.post_cd import AddPostCD
from src.bot.keyboards.callback_data.streamer.post.preview_cd import (
    GetPostPreviewTypeCD,
)
from src.bot.keyboards.states.post.post_states import AddPostState
from src.checker.post_info import PostVariables
from src.db.models.association.post_media import PostMediaSessionJoin
from src.db.models.post_model import PostModel, PreviewModel
from src.db.repository.association.post_media_repository import (
    PostMediaSessionJoinRepository,
)
from src.db.repository.post_repository import PostRepository
from src.db.repository.streamer_repository import StreamerRepository


@post_router.callback_query(AddPostCD.filter())
async def add_post(
        callback_query: CallbackQuery, state: FSMContext, callback_data: AddPostCD
):
    await state.update_data(streamer_id=callback_data.streamer_id)
    await state.set_state(AddPostState.ADD_NAME)
    await callback_query.message.edit_text(
        text="Введите название поста. Оно должно быть уникальным."
    )


@post_router.message(AddPostState.ADD_NAME)
async def add_name(message: Message, db_session: Session, state: FSMContext):
    name = message.text
    post_repository = PostRepository(db_session)
    context_data = await state.get_data()
    post = await post_repository.get_one(
        streamer_id=context_data.get("streamer_id"), name=name
    )
    if post:
        await message.answer("Пост с таким названием уже существует. Подберите другое.")
        return
    await state.update_data(name=name)
    await state.set_state(AddPostState.ADD_TEXT)
    await message.answer(
        text="Введите текст поста.\n\n"
             "Доступные переменные:\n"
             + "\n".join(f"• {post.value.var}: {post.value.info}" for post in PostVariables)
             + "\n\nДля доступа к переменным ограничивайте их фигурными скобками. Например, так: {"
             + PostVariables.STREAM_TITLE.value.var
             + "}."
    )


@post_router.message(AddPostState.ADD_TEXT)
async def add_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.set_state(AddPostState.ADD_CUSTOM_PREVIEW)
    reply_markup = await get_reply_markup(await get_choose_media_type_inline_keyboard())
    await message.answer(
        text="Добавьте превью или использовать со стрима?.",
        reply_markup=reply_markup,
    )


async def create_post(
        message: Message,
        db_session: Session,
        state: FSMContext,
        context_data: dict,
):
    file_path = context_data.get("file_path")
    streamer_repository = StreamerRepository(db_session)
    streamer = await streamer_repository.get_one(id=context_data.get("streamer_id"))
    post_repository = PostRepository(db_session)
    post = PostModel(
        streamer=streamer,
        name=context_data.get("name"),
        text=context_data.get("text"),
        media_sessions=[],
    )
    preview = PreviewModel(file_path=file_path, post=post)
    await post_repository.add_all([post, preview])
    await post_repository.commit()
    post_media_session_join_repository = PostMediaSessionJoinRepository(db_session)
    for media_session in streamer.media_sessions:
        post_media_session_join = PostMediaSessionJoin(
            post_id=post.id, media_session_id=media_session.id
        )
        await post_media_session_join_repository.add(post_media_session_join)
    await post_repository.commit()
    await state.clear()
    await message.answer(
        text=f"Пост {post.name} для стримера {post.streamer.name} создан."
    )


@post_router.callback_query(
    GetPostPreviewTypeCD.filter(F.post_preview_button == PostPreviewButtons.ADD_PREVIEW)
)
async def add_custom_media_intent(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(AddPostState.ADD_CUSTOM_PREVIEW)
    await callback_query.message.edit_text(text="Отправьте изображение")


@post_router.message(
    F.photo,
    AddPostState.ADD_CUSTOM_PREVIEW,
)
async def add_custom_media(
        message: Message, db_session: Session, state: FSMContext
):
    context_data = await state.get_data()
    file_path = (
            CommonConfig.POST_PREVIEWS_PATH
            + f"{context_data.get('streamer_id')}"
            + f"{context_data.get('name')}.jpg"
    )
    await message.bot.download(file=message.photo[-1].file_id, destination=file_path)
    await state.update_data(file_path=file_path)
    await create_post(
        message=message,
        db_session=db_session,
        state=state,
        context_data=await state.get_data(),
    )


@post_router.callback_query(
    GetPostPreviewTypeCD.filter(
        F.post_preview_button == PostPreviewButtons.STREAM_PREVIEW
    ),
    AddPostState.ADD_CUSTOM_PREVIEW,
)
async def add_media_preview(
        callback_query: CallbackQuery, db_session: Session, state: FSMContext
):
    await state.update_data(file_path=None)
    await create_post(
        message=callback_query.message,
        db_session=db_session,
        state=state,
        context_data=await state.get_data(),
    )
