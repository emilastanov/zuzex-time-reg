def to_callback_data_format(type, *args):
    callback_data = f"{type}:" + ";".join(map(str, args))

    byte_length = len(callback_data.encode("utf-8"))

    if byte_length > 64:
        raise ValueError(
            f"⚠️ callback_data слишком длинный! Telegram не примет >64 байт. Длина callback_data: {byte_length} байт"
        )

    return callback_data
