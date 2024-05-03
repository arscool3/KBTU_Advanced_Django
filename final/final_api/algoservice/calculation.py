from typing import List, Dict

from schemas import Message


def count_messages_per_user_chat(messages: List[Message]) -> Dict[int, Dict[int, int]]:
    message_count = {}
    for message in messages:
        user_id = message.sender_id
        chat_id = message.chat_id

        if user_id not in message_count:
            message_count[user_id] = {}

        if chat_id not in message_count[user_id]:
            message_count[user_id][chat_id] = 0
        message_count[user_id][chat_id] += 1

    return message_count
