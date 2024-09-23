from src.checker.utils import remove_quotes
from src.db.models.media_model import MediaSessionModel, MediaPlatformModel
from src.domain.media_platforms.errors import IncorrectMediaProfileFormatInput
from src.domain.media_platforms.profiles.base_media_profile import (
    BaseMediaProfile,
    BaseMediaProfileInfoParser,
    BaseMediaProfileValidator,
    BaseMediaProfileInfo,
)


class TelegramProfileInfo(BaseMediaProfileInfo):
    channel_id: str
    bot_token: str

    def create_model(
            self, name: str, media_platform: MediaPlatformModel, is_active: bool = True
    ) -> MediaSessionModel:
        return MediaSessionModel(
            name=name,
            media_platform=media_platform,
            access_token=self.bot_token,
            extra_field=self.channel_id,
            is_active=is_active,
        )


class TelegramProfileInfoParser(BaseMediaProfileInfoParser):
    PROFILE_INFO = TelegramProfileInfo

    async def parse(self) -> PROFILE_INFO:
        try:
            channel_id, bot_token = list(map(remove_quotes, self.text.split("\n")))
            channel_id: str = channel_id
            if channel_id.startswith("@"):
                channel_id = channel_id[1:]
            return TelegramProfileInfo(channel_id=channel_id, bot_token=bot_token)
        except ValueError:
            raise IncorrectMediaProfileFormatInput()


class TelegramMediaProfileValidator(BaseMediaProfileValidator):
    PROFILE_INFO = TelegramProfileInfo

    async def validate(self):
        return  # TODO: add validation


class TelegramMediaProfile(BaseMediaProfile):
    PROFILE_INFO = TelegramProfileInfo
    PROFILE_INFO_PARSER = TelegramProfileInfoParser
    VALIDATOR = TelegramMediaProfileValidator

    @staticmethod
    def help():
        return (
            "Введите информацию о TG-канале в следующем формате, разделяя переносом строки: \n"
            "- Уникальный user id канала (тэг)\n"
            "- Токен бота из BotFather\n"
            "\n"
            "----------------------------\n"
            "Как получить эти данные:\n"
            "1. Создайте бота через BotFather: https://t.me/BotFather\n"
            '2. Зайдите в канал, найдите "управление каналом", "Администраторы", добавьте созданного бота в качестве '
            'администратора.'
        )

    @staticmethod
    def get_important_for_user_info(media_session: MediaSessionModel) -> str:
        return f"""• ID канала: @{media_session.extra_field}\n"""
