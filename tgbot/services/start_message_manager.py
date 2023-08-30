user_start_message_txt_path='tgbot/misc/message_storage/users/start_message'

def set_user_start_message(new_message: str):
    with open(user_start_message_txt_path, "w") as _file:
        _file.write(new_message)


def get_user_start_message() -> str:
    with open(user_start_message_txt_path, "r") as _file:
        text = _file.read()
        return text
