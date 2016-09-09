#!/usr/bin/python3

from py import spotlight

result = spotlight.SpotlightClient(None).annotate_text("Barack Obama is the husband of Michelle Obama.")
print(result)

# TODO: both entities get annotated
