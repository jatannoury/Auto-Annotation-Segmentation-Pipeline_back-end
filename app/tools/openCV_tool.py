import cv2
import random

def random_bounding_box(image):
    height, width, _ = image.shape

    # Generate random coordinates for the top-left and bottom-right corners of the bounding box
    x1 = random.randint(0, width - 1)
    y1 = random.randint(0, height - 1)
    x2 = random.randint(x1 + 1, width)
    y2 = random.randint(y1 + 1, height)

    # Draw the bounding box on a copy of the original image
    image_with_bbox = image.copy()
    cv2.rectangle(image_with_bbox, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green color, thickness = 2

    return image_with_bbox


# Example usage

