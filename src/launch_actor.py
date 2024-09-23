import logging

from flask import Flask, request
from waitress import serve

from config import ActorConfig
from src.actor.get_by_name import get_media_actor_class
from src.connection.messages import PostStreamInfoMessage
from src.db.models.all_models import *
from src.db.models.engine import db_session
from src.db.repository.post_repository import PublishedPostRepository
from src.db.repository.streamer_repository import StreamerRepository

app = Flask(__name__)


@app.route("/send_message")
async def send_message():
    json = request.json
    post_stream_info = PostStreamInfoMessage.model_validate(json)
    logging.info(post_stream_info)
    stream_info = post_stream_info.stream_info
    published_post_repository = PublishedPostRepository(db_session)
    published_posts = await published_post_repository.list(
        stream_id=stream_info.stream_id
    )
    streamer_id = post_stream_info.streamer_id
    streamer_repository = StreamerRepository(db_session)
    streamer = await streamer_repository.get_one(id=streamer_id)
    for media_session in streamer.media_sessions:
        for post in streamer.posts:
            need_to_post = False
            for published_post in published_posts:
                if (
                    published_post.media_session == media_session
                    and published_post.post == post
                ):
                    resp = {
                        "code": 1,
                        "message": f"{post.name} of streamer {streamer.name} is already posted in "
                        f"{media_session.media_name.value}",
                    }
                    logging.info(resp)
                    break
            else:
                need_to_post = True
            if not need_to_post:
                continue
            media_actor_class = get_media_actor_class(media_session.media_name)
            media_actor = media_actor_class(post, streamer, media_session, stream_info)
            is_posted = await media_actor.send_post()
            if is_posted:
                logging_message = (
                    f"Successfully posted {post.name} of streamer {streamer.name} in media {media_session.media_name} "
                    f"with id {media_actor.get_chat_id()}"
                )
            else:
                logging_message = (
                    f"Fail to post {post.name} of streamer {streamer.name} in media {media_session.media_name} with "
                    f"id {media_actor.get_chat_id()}"
                )
            logging.info(logging_message)
            published_post = PublishedPostModel(
                stream_id=stream_info.stream_id,
                post=post,
                media_session=media_session,
            )
            await published_post_repository.add(published_post)
    await published_post_repository.commit()
    resp = {"code": 0, "message": "posted"}
    logging.info(resp)
    return resp


def main():
    serve(app, host="127.0.0.1", port=ActorConfig.PORT)


if __name__ == "__main__":
    main()
