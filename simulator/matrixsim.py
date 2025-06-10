from PIL import Image, ImageDraw
import numpy as np
import math

def crop_to_aspect(image, target_width, target_height):
    img_width, img_height = image.size
    target_aspect = target_width / target_height
    img_aspect = img_width / img_height

    if img_aspect > target_aspect:
        # Image is wider than target: crop sides
        new_width = int(img_height * target_aspect)
        offset = (img_width - new_width) // 2
        return image.crop((offset, 0, offset + new_width, img_height))
    else:
        # Image is taller than target: crop top/bottom
        new_height = int(img_width / target_aspect)
        offset = (img_height - new_height) // 2
        return image.crop((0, offset, img_width, offset + new_height))

def simulate_led_matrix(image_path, led_width, led_height, fill_factor, output_path='led_simulation.png'):
    # Load and prepare image
    image = Image.open(image_path).convert('RGB')
    image = crop_to_aspect(image, led_width, led_height)
    image = image.resize((led_width, led_height), Image.LANCZOS)

    pixels = np.array(image)

    # Determine box sizes
    # Choose smallest integer base size so whole image is not too large
    max_canvas_width = 1000  # in pixels
    base_size = max_canvas_width // led_width
    outer_size = base_size
    inner_size = max(1, round(base_size * fill_factor))

    offset = (outer_size - inner_size) // 2

    canvas_width = led_width * outer_size
    canvas_height = led_height * outer_size

    canvas = Image.new('RGB', (canvas_width, canvas_height), 'black')
    draw = ImageDraw.Draw(canvas)

    for y in range(led_height):
        for x in range(led_width):
            color = tuple(pixels[y, x])
            x0 = x * outer_size + offset
            y0 = y * outer_size + offset
            x1 = x0 + inner_size
            y1 = y0 + inner_size
            draw.rectangle([x0, y0, x1, y1], fill=color)

    canvas.save(output_path)
    print(f"Saved simulated LED image to {output_path}")

# Example usage:
simulate_led_matrix("input3.png", led_width=192, led_height=192, fill_factor=0.3)
