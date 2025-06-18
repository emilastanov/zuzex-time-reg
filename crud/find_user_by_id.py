from models.User import User


async def find_user_by_id(user_id):
    return await User.find_one(chat_id=user_id)  # eager_load=["limits"]
