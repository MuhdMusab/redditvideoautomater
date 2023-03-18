from PIL import Image, ImageOps

class TitleImage:
    def __init__(self, titlepath, headerpath, labelpath, upvotespath, outputpath):
        self.titlepath = titlepath
        self.headerpath = headerpath
        self.labelpath = labelpath
        self.upvotespath = upvotespath
        self.outputpath = outputpath
    
    def save_title_image(self):
        #Open the two images
        image1 = Image.open(self.headerpath)
        image2 = Image.open(self.titlepath)

        # Resize image2 to match the width of image1
        image2 = image2.resize((image1.width, image2.height))

        # Create a new blank image with the same width as the two images and the combined height
        output_image = Image.new("RGB", (image1.width, image1.height + image2.height))

        # Paste the two images onto the blank image
        output_image.paste(image1, (0, 0))
        output_image.paste(image2, (0, image1.height))

        # Save the output image
        output_image.save(self.outputpath)

        # Open the two images
        image1 = Image.open(self.outputpath)
        image2 = Image.open(self.labelpath)

        # Resize image2 to match the width of image1
        image2 = image2.resize((image1.width, image2.height))

        # Create a new blank image with the same width as the two images and the combined height
        output_image = Image.new("RGB", (image1.width, image1.height + image2.height))

        # Paste the two images onto the blank image
        output_image.paste(image1, (0, 0))
        output_image.paste(image2, (0, image1.height))

        # Save the output image
        output_image.save(self.outputpath)

        # Open the two images
        image1 = Image.open(self.upvotespath)
        image2 = Image.open(self.outputpath)

        # Resize image2 to match the height of image1
        image1 = image1.resize((image1.width, image2.height))

        # Create a new blank image with the same height as the two images and the combined width
        output_image = Image.new("RGB", (image1.width + image2.width, image1.height))

        # Paste the two images onto the blank image
        output_image.paste(image1, (0, 0))
        output_image.paste(image2, (image1.width, 0))

        # Save the output image
        output_image.save(self.outputpath)
        

        image = Image.open(self.outputpath)

        # Add padding to the image
        padded_image = ImageOps.expand(image, border=10, fill='white')

        # Save the padded image
        padded_image.save(self.outputpath)