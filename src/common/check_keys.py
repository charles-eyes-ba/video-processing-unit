def check_keys(dictionary: dict, keys: list[str]) -> bool:
    for key in keys:
        if not key in dictionary:
            return False
    return True