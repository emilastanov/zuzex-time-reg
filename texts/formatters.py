from models.User import UserType
from texts.lists import USER_LIST


def format_user_list_message(users, pagination_data):
    return USER_LIST.format(
        total_pages=pagination_data["total_pages"],
        total_count=pagination_data["total_count"],
        current_page=pagination_data["current_page"],
        limit=pagination_data["limit"],
        users="\n".join(
            [
                f"""• <code>{
            f"@{u['name']}" if u["type"] == UserType.private else u['name']
        }</code>"""
                for u in users
            ]
        ),
    )
