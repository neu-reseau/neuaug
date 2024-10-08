import sys
import os
import random
from PIL import Image, ImageEnhance, ImageFilter

def add_noise(image):
    pixels = image.load()
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            r, g, b = pixels[i, j]
            noise = random.randint(-20, 20)
            pixels[i, j] = (
                max(0, min(r + noise, 255)),
                max(0, min(g + noise, 255)),
                max(0, min(b + noise, 255))
            )
    return image

def mirror_image(image):
    return image.transpose(Image.FLIP_LEFT_RIGHT)

def shift_image(image, shift_x, shift_y):
    return image.transform(image.size, Image.AFFINE, (1, 0, shift_x, 0, 1, shift_y))

def augment_image(image):
    augmentations = [
        lambda img: img.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.5, 1.5))),
        lambda img: ImageEnhance.Brightness(img).enhance(random.uniform(0.8, 1.2)),
        lambda img: ImageEnhance.Contrast(img).enhance(random.uniform(0.8, 1.2)),
        lambda img: add_noise(img),
        lambda img: img.transpose(Image.ROTATE_90 if random.choice([True, False]) else Image.ROTATE_270),
        lambda img: mirror_image(img),
        lambda img: shift_image(img, random.randint(20, 30), random.randint(-10, 10))
    ]
    
    num_augmentations = random.randint(1, 4)
    for _ in range(num_augmentations):
        augmentation = random.choice(augmentations)
        image = augmentation(image)
    return image

def main(input_folder, output_folder, num_copies):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
            input_path = os.path.join(input_folder, filename)
            img = Image.open(input_path)
            
            for i in range(num_copies):
                augmented_img = augment_image(img.copy())
                output_filename = f"{os.path.splitext(filename)[0]}_aug_{i+1}.jpg"
                output_path = os.path.join(output_folder, output_filename)
                augmented_img.save(output_path, 'JPEG')

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python program.py <folder of jpg images> <output folder> <number of augmented copies>")
        sys.exit(1)
    
    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    num_copies = int(sys.argv[3])
    
    main(input_folder, output_folder, num_copies)