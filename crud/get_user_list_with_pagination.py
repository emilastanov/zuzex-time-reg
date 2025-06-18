from models.User import User
from utils.pagination.get_pagination_data import get_pagination_data


async def get_user_list_with_pagination(limit, page_number):
    _, total_count = await User.find()
    pagination_data = get_pagination_data(total_count, limit, page_number)

    users, _ = await User.find(limit=limit, offset=pagination_data["offset"])

    data = list(
        map(
            lambda user: {
                "name": user.group_title or user.username,
                "type": user.chat_type,
            },
            users,
        )
    )

    return data, pagination_data
