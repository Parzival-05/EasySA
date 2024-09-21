from src.bot.keyboards.buttons.post.preview_buttons import PostPreviewButtons
from src.bot.keyboards.callback_data.base_cd import BaseCD


class GetPostPreviewTypeCD(BaseCD, prefix="GetPostPreviewTypeCD"):
    post_preview_button: PostPreviewButtons

    @staticmethod
    def from_post_media_button(post_preview_button: PostPreviewButtons):
        return GetPostPreviewTypeCD(post_preview_button=post_preview_button)
