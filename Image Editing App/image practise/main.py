from PIL import Image, ImageFilter, ImageEnhance
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, "HSE.png")

with Image.open(image_path) as picture:
    # picture.show()

    # Convert to black and white
    black_white = picture.convert("L")
    black_white.save('grayHSE.png')

    # Mirror image
    mirror = picture.transpose(Image.FLIP_LEFT_RIGHT)
    mirror.save('mirrorHSE.png')

    # Blur image
    blur = picture.filter(ImageFilter.BLUR)
    blur.save('blurHSE.png')

    # Image Enhance
    contrast = ImageEnhance.Contrast(picture)
    contrast = contrast.enhance(2.5)
    contrast.save('contrastHSE.png')

    color = ImageEnhance.Color(picture).enhance(1.2)
    color.save('colorHSE.png')

    