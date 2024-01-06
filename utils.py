import base64


def get_user_id_and_school_id_for_authtoken(AUTHORIZATION):
    base64_message = AUTHORIZATION.split(" ")[1]
    base64_bytes = base64_message.encode("ascii")
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode("ascii").split("&")
    message_dict = {}
    for item in message:
        key, value = item.split("=")
        message_dict[key] = value
    print(
        f"This token was created on {message_dict['created_date']} and expires on {message_dict['expiry_date']}"
    )
    return message_dict["user_id"], message_dict["school_id"]
