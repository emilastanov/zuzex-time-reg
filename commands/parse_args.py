def parse_args(command_name, text):
    query = text.replace(command_name, "").strip().split()
    args = {}

    cursor = 0
    while cursor < len(query):
        arg = query[cursor]
        if arg.startswith("-"):
            if cursor + 1 < len(query) and not query[cursor + 1].startswith("-"):
                args[arg] = query[cursor + 1]
                cursor += 2
            else:
                args[arg] = True
                cursor += 1
        else:
            cursor += 1

    return args
