from PIL import Image

# Create a 10x10 red image
img = Image.new('RGB', (10, 10), color = 'red')
img.save('jules-scratch/verification/test_image.png')
