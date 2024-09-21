# TODO: Post vars should be associated with StreamPlatforms

import enum
from dataclasses import dataclass


@dataclass
class VariableInfo:
    var: str
    info: str


class PostVariables(enum.Enum):
    STREAMER_URL = VariableInfo(var="STREAMER_URL", info="URL стримера")
    STREAM_TITLE = VariableInfo(var="STREAM_TITLE", info="Название стрима")
    STREAM_CATEGORY = VariableInfo(
        var="STREAM_CATEGORY", info="Категория стрима [Twitch-only]"
    )
