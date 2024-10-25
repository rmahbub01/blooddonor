from PIL import Image

STATIC_DIR = "./blooddonor/static"


async def save_image(file, user_id: str):
    output_size = (150, 150)
    img = Image.open(file.file)
    img.thumbnail(output_size)
    img.save(f"{STATIC_DIR}/images/{user_id}.png")
