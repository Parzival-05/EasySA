import logging
from pathlib import Path
from typing import Optional

import requests

from src.actor.base_media_actor import BaseMediaActor
from src.checker.post_info import PostVariables
from src.domain.stream_platforms.get_by_name import get_stream_platform_profile_class
from src.domain.stream_platforms.profiles.base_stream_profile import StreamProfileInfo


class DiscordActor(BaseMediaActor):

    CHAT_ID_TYPE = int

    def get_chat_id(self) -> Optional[CHAT_ID_TYPE]:
        return int(self.media_session.extra_field)

    def _get_text(self):
        stream_platform_profile_class = get_stream_platform_profile_class(
            self.streamer.stream_platform_name
        )
        d = {
            PostVariables.STREAMER_URL.value.var: stream_platform_profile_class.generate_profile_url(
                StreamProfileInfo(profile_id=self.streamer.profile_id)
            ),
            PostVariables.STREAM_TITLE.value.var: self.stream_info.title,
            PostVariables.STREAM_CATEGORY.value.var: self.stream_info.category,
        }
        return self.post.text.format(**d)

    async def _send_post(
        self, chat_id: CHAT_ID_TYPE, text: str, photo: Optional[str] = None, **kwargs
    ):
        payload = {"content": text}
        headers = {
            "authorization": f"Bot {self.media_session.access_token}",
        }
        photo_name = Path(photo).name

        files = (
            {
                "file": (
                    (
                        photo_name,
                        open(photo, "rb"),
                    )
                )
            }
            if photo
            else {}
        )
        res = requests.post(
            f"https://discord.com/api/v9/channels/{chat_id}/messages",
            data=payload,
            headers=headers,
            files=files,
        ).json()
        logging.info(res)
        return res.get("type", False)
