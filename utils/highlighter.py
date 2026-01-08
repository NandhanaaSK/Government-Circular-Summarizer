import re

def highlight_text(text):
    keywords = ["deadline", "shall", "must", "eligible"]

    text = re.sub(
        r'(\d{1,2}\s\w+\s\d{4})',
        r'<mark>\1</mark>',
        text
    )

    for k in keywords:
        text = re.sub(
            rf'\b({k})\b',
            r'<mark>\1</mark>',
            text,
            flags=re.IGNORECASE
        )

    return text
