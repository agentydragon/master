from src.prototype.entity_recognition import spotlight

spotlight_client = spotlight.SpotlightClient(spotlight.DEFAULT_PUBLIC_SPOTLIGHT_ENDPOINT)
result = spotlight_client.annotate_text("Barack Obama is the husband of Michelle Obama.")
print(result)

# TODO: both entities get annotated
