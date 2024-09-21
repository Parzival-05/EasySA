from src.checker.utils import remove_quotes
from src.db.models.media_model import MediaSessionModel, MediaPlatformModel
from src.domain.media_platforms.errors import IncorrectMediaProfileFormatInput
from src.domain.media_platforms.profiles.base_media_profile import (
    BaseMediaProfile,
    BaseMediaProfileInfoParser,
    BaseMediaProfileValidator,
    BaseMediaProfileInfo,
)


class DiscordProfileInfo(BaseMediaProfileInfo):
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


class DiscordProfileInfoParser(BaseMediaProfileInfoParser):
    PROFILE_INFO = DiscordProfileInfo

    async def parse(self) -> PROFILE_INFO:
        try:
            channel_id, bot_token = list(map(remove_quotes, self.text.split("\n")))
            return DiscordProfileInfo(channel_id=channel_id, bot_token=bot_token)
        except ValueError:
            raise IncorrectMediaProfileFormatInput()


class DiscordMediaProfileValidator(BaseMediaProfileValidator):
    PROFILE_INFO = DiscordProfileInfo

    async def validate(self):
        return  # TODO: add validation


class DiscordMediaProfile(BaseMediaProfile):

    PROFILE_INFO = DiscordProfileInfo
    PROFILE_INFO_PARSER = DiscordProfileInfoParser
    VALIDATOR = DiscordMediaProfileValidator

    @staticmethod
    def help():
        return (
            "Введите информацию о Discord-канале в следующем формате, разделяя переносом строки: \n"
            "- ID нужной ветки на сервере\n"
            "- Токен бота\n"
            "\n"
            "----------------------------\n"
            "Как получить эти данные:\n"
            "1. Создайте Application по инструкции: https://discordpy.readthedocs.io/en/stable/discord.html\n"
            'Во вкладке "OAuth2" выберите следующие полномочия для бота:\n'
            '- "Send messages"\n'
            '- "Send messages in Threads"\n'
            '- "Manage messages"\n'
            '- "Mention Everyone" (если нужно)\n'
            "2. Подключите бота к серверу.\n"
            '3. Во вкладке "Bot" скопируйте токен бота (с помощью "Reset Token")\n'
            "4. Как найти ID нужной ветки на сервере: "
            "https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID"
            "#h_01HRSTXPS5FSFA0VWMY2CKGZXA (NB: с desktop приложения может понадобиться включить режим разработчика в "
            "настройках)."
        )

    @staticmethod
    def get_important_for_user_info(media_session: MediaSessionModel) -> str:
        return f"""• ID ветки на сервере: @{media_session.extra_field}\n"""
