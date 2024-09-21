import environs

from config import CommonConfig


def get_bot_token():
    env = environs.Env()
    env.read_env(CommonConfig.ENV_PATH)
    return env.str("BOT_TOKEN_API")
