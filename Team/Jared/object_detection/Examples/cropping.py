import Image

MAX_SIZE = 1280
image = Image.open(image_path)
original_size = max(image.size[0], image.size[1])

if original_size >= MAX_SIZE:
    resized_file = open(image_path.split('.')[0] + '_resized.jpg', "w")
    if (image.size[0] > image.size[1]):
        resized_width = MAX_SIZE
        resized_height = int(round((MAX_SIZE/float(image.size[0]))*image.size[1])) 
    else:
        resized_height = MAX_SIZE
        resized_width = int(round((MAX_SIZE/float(image.size[1]))*image.size[0]))

    image = image.resize((resized_width, resized_height), Image.ANTIALIAS)
    image.save(resized_file, 'JPEG')