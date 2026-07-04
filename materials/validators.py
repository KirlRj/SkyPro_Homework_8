import re

from rest_framework.serializers import ValidationError


class YouTubeLinkValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        link = value.get(self.field)
        if link:
            if not re.match(r"^https?://(www\.)?youtube\.com/", link):
                raise ValidationError("Ссылка должна вести на youtube.com")
