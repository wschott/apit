def padded_number(number: int, total: int) -> str:
    return str(number).rjust(len(str(total)), "0")
