"""
This module converts images to webp.
"""

from PIL import Image


def images_to_webp(image_path: str, output_path: str) -> None:
    """
    Main function.
    """
    image = Image.open(image_path)
    image.save(output_path, "webp")


images_to_webp("test.jpg", "test.webp")
