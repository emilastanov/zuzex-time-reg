import json


class ContextManager:

    @staticmethod
    def get_or_create_list(user_data, name):
        """Возвращает список из user_data[name], либо пустой список."""
        return json.loads(user_data.get(name, "[]"))

    @staticmethod
    def save_list(user_data, name, data):
        """Сохраняет список в user_data[name] в виде JSON-строки."""
        user_data[name] = json.dumps(data)

    @staticmethod
    def add_to_list(user_data, name, obj):
        """Добавляет элемент в список user_data[name]."""
        current = ContextManager.get_or_create_list(user_data, name)
        current.append(obj)
        ContextManager.save_list(user_data, name, current)

    @staticmethod
    def exists_in_list(user_data, name, predicate):
        """Проверяет, есть ли элемент удовлетворяющий условию predicate(item) в списке user_data[name]."""
        current = ContextManager.get_or_create_list(user_data, name)
        return any(predicate(item) for item in current)

    @staticmethod
    def remove_from_list(user_data, name, predicate):
        """
        Удаляет первый элемент, удовлетворяющий predicate(obj) из списка.
        predicate — функция, принимающая элемент и возвращающая True/False.
        """
        current = ContextManager.get_or_create_list(user_data, name)
        filtered = [item for item in current if not predicate(item)]
        ContextManager.save_list(user_data, name, filtered)

    @staticmethod
    def clear_list(user_data, name):
        """Очищает список user_data[name]."""
        ContextManager.save_list(user_data, name, [])

    @staticmethod
    async def commit(context, chat_id):
        await context.application.persistence.update_user_data(
            chat_id, context.application.user_data[chat_id]
        )
