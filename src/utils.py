

def format_number(number) -> str:
    if int(number) >= 1e6:
        return f"{number / 1e6:.2f}".rstrip('0').rstrip('.') + 'M'
    elif number >= 1e3:
        return f"{number / 1e3:.2f}".rstrip('0').rstrip('.') + 'K'
    else:
        return number


if __name__ == "__main__":
    pass
