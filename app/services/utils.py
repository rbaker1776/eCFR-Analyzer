from datetime import datetime, timedelta


def format_number(number) -> str:
    if int(number) >= 1e6:
        return f"{number / 1e6:.2f}".rstrip('0').rstrip('.') + 'M'
    elif number >= 1e3:
        return f"{number / 1e3:.2f}".rstrip('0').rstrip('.') + 'K'
    else:
        return number


def get_completion_date(word_count):
    words_per_day = 250 * 60 * 24
    days = word_count / words_per_day
    finish_date = datetime.now() + timedelta(days=days)
    return finish_date.strftime("%B %d, %Y")


if __name__ == "__main__":
    pass
