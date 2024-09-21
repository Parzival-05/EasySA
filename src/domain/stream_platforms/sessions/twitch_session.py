import logging
import time
from datetime import datetime
from typing import Optional

import requests
import environs
from sqlalchemy.orm import Session

from config import CommonConfig
from src.checker.utils import download_image
from src.domain.stream_platforms.errors import (
    InvalidClient,
    InvalidOAuthToken,
    ValuesNotMatching,
)
from src.domain.stream_platforms.sessions.base_platform_session import (
    BaseStreamPlatformSession,
    NonActiveStreamer,
    InvalidUser,
    StreamInfo,
)
from src.domain.stream_platforms.stream_platform_names import (
    StreamPlatformNames,
)


class TwitchSession(BaseStreamPlatformSession):
    PLATFORM_NAME = StreamPlatformNames.Twitch

    def __init__(self, db_session: Session):
        env = environs.Env()
        env.read_env(CommonConfig.ENV_PATH)
        self.client_id = env.str("TWITCH_CLIENT_ID")
        self.client_secret = env.str("TWITCH_CLIENT_SECRET")
        super().__init__(db_session)

    async def refresh_session(self, refresh_token: Optional[str]) -> dict:
        return await self._get_session_info()

    @BaseStreamPlatformSession.check_if_expired
    async def get_stream_info(
        self,
        user_name: id,
        preview_width=1920,
        preview_height=1080,
    ) -> Optional[StreamInfo]:
        def get_preview_path():
            return (
                CommonConfig.STATIC_PATH
                + f"{self.PLATFORM_NAME.value}/"
                + f"{user_name}_{preview_width}x{preview_height}.jpg"
            )

        session = await self.get_platform_session()
        try:
            user_id = await self.get_user_id(user_name, session.access_token)
            stream_request_data = self.get_stream_info_request(
                user_id=user_id, access_token=session.access_token
            )
            title = stream_request_data["title"]
            category = stream_request_data["game_name"]
            preview_url = stream_request_data["thumbnail_url"].format(
                width=preview_width, height=preview_height
            )
            stream_id = stream_request_data["id"]
            is_downloaded = download_image(
                image_url=preview_url,
                file_dir=get_preview_path(),
            )
            if is_downloaded:
                preview = get_preview_path()
            else:
                preview = None
            return StreamInfo(
                stream_id=stream_id, preview=preview, title=title, category=category
            )
        except NonActiveStreamer:
            return None

    async def _get_session_info(self) -> dict:
        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
        }
        start_time = time.time()
        response = requests.post("https://id.twitch.tv/oauth2/token", params=params)
        response_json = response.json()
        if response_json == {
            "status": 400,
            "message": "invalid client",
        } or response_json == {"status": 403, "message": "invalid client secret"}:
            raise InvalidClient(response.json()["message"])
        result = {
            "access_token": response_json["access_token"],
            "refresh_token": None,
            "expires_in": datetime.fromtimestamp(
                start_time + response_json["expires_in"]
            ),
        }
        return result

    async def get_user_id(self, user_name: str, access_token: str) -> int:
        params = {"login": user_name}

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Client-Id": self.client_id,
        }

        response = requests.get(
            "https://api.twitch.tv/helix/users", params=params, headers=headers
        )

        if len(response.json()["data"]) == 0:
            raise InvalidUser("Invalid user")

        return response.json()["data"][0]["id"]

    def get_stream_info_request(self, user_id: int, access_token: str) -> dict:
        params = {"user_id": user_id}

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Client-Id": self.client_id,
        }

        response = requests.get(
            "https://api.twitch.tv/helix/streams", params=params, headers=headers
        )
        logging.debug(response.json())
        if response.json() == {
            "error": "Unauthorized",
            "status": 401,
            "message": "OAuth token is missing",
        } or response.json() == {
            "error": "Unauthorized",
            "status": 401,
            "message": "Invalid OAuth token",
        }:
            raise InvalidOAuthToken(response.json()["message"])

        if response.json() == {
            "error": "Unauthorized",
            "status": 401,
            "message": "Client ID and OAuth token do not match",
        }:
            raise ValuesNotMatching(response.json()["message"])

        if response.json() == {"data": [], "pagination": {}}:
            raise NonActiveStreamer
        data = response.json()["data"][0]

        return data
