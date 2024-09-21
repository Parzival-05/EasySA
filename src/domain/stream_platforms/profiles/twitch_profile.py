import logging

from src.checker.utils import remove_quotes
from src.domain.stream_platforms.errors import IncorrectProfileFormat
from src.domain.stream_platforms.profiles.base_stream_profile import (
    BaseStreamProfile,
    BaseStreamProfileInfoParser,
    StreamProfileInfo,
    BaseStreamProfileValidator,
)
from src.domain.stream_platforms.sessions.twitch_session import TwitchSession
from src.domain.stream_platforms.stream_platform_names import (
    StreamPlatformNames,
)


class TwitchProfileInfoParser(BaseStreamProfileInfoParser):
    async def parse(self) -> StreamProfileInfo:
        without_quotes = remove_quotes(self.text)
        if without_quotes.startswith(TwitchStreamProfile.TWITCH_URL):
            return StreamProfileInfo(
                profile_id=without_quotes[len(TwitchStreamProfile.TWITCH_URL) :]
            )
        logging.debug("Incorrect profile format")
        raise IncorrectProfileFormat


class TwitchProfileValidate(BaseStreamProfileValidator):
    PLATFORM_SESSION = TwitchSession

    async def validate(self):
        twitch_session = self.stream_platform_session
        await twitch_session.auth()
        _ = await twitch_session.get_user_id(
            self.profile_info.profile_id,
            (await twitch_session.get_platform_session()).access_token,
        )
        return


class TwitchStreamProfile(BaseStreamProfile):

    PLATFORM_NAME = StreamPlatformNames.Twitch
    PROFILE_VALIDATOR = TwitchProfileValidate
    PROFILE_INFO_PARSER = TwitchProfileInfoParser
    TWITCH_URL = "https://www.twitch.tv/"

    @staticmethod
    def help():
        return (
            "Введите данные профиля в следующем формате:\n"
            f"{TwitchStreamProfile.TWITCH_URL}" + "{ID профиля}\n\n"
            "Например, ваш профиль — https://www.twitch.tv/voodoosh. Отправьте то же самое, "
            '"https://www.twitch.tv/voodoosh".'
        )

    @staticmethod
    def generate_profile_url(streamer_profile_info: StreamProfileInfo):
        return TwitchStreamProfile.TWITCH_URL + streamer_profile_info.profile_id
