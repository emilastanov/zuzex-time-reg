from models.User import UserType, User


async def find_or_create_user(chat, message):
    is_new = False

    user = await User.find_one(chat_id=chat.id)
    if not user:
        is_new = True
        user = await User.create(
            chat_id=chat.id,
            chat_type=UserType(chat.type),
            language_code=getattr(message.from_user, "language_code", None),
            group_title=getattr(chat, "title", None),
            first_name=getattr(message.from_user, "first_name", None),
            last_name=getattr(message.from_user, "last_name", None),
            username=getattr(message.from_user, "username", None),
        )

    return user, is_new
