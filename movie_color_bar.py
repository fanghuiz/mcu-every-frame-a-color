from PIL import Image, ImageEnhance
import os
import subprocess
import sys

# Requires ffmpeg https://www.ffmpeg.org/ffmpeg.html

# Run script as
# python movie_color_bar.py input_video output_frame_folder output_image

# 1st arg - video
input_video = str(sys.argv[1])
# 2nd arg - directory to save frame images in
output_frame_folder = str(sys.argv[2])
# 3rd arg - name of output
output_image = str(sys.argv[3])

# Save frame images as 0001.jpg, 0002.jpg etc
output_frames = output_frame_folder + "/%04d.jpg"

# Run the following shell command
# ffmpeg -i video.mp4 -vf fps=.25 images/%04d.jpg
subprocess.check_output(["ffmpeg", "-i", input_video,
                         "-vf", "fps=0.25", output_frames])
# The command will call ffmpeg to convert video.mp4 into images
# 0.25fps speed - we get one still image per 4 seconds of video. Can be adjusted
# Images will be saved in folder specied in output_frames arg

# Reading in the image paths
images = [output_frame_folder + "/" +
          x for x in os.listdir(output_frame_folder)]

# Sort the images so they are in chronolocal order, 0001, 0002 ... 0999 etc
images.sort(key=lambda x: os.path.split(x)[1])

# Function to find average RGB values in an image


def getAvgRGB(img):

    # Converting image to rgb
    img = img.convert("RGB")

    # Getting colors used in the image, returns (count, [r,g,b])
    colors = img.getcolors(img.size[0] * img.size[1])

    # Get average RGB of the image - sum(r * Count) / sum(Count)
    r = sum([i[1][0] * i[0] for i in colors]) / sum([i[0] for i in colors])
    g = sum([i[1][1] * i[0] for i in colors]) / sum([i[0] for i in colors])
    b = sum([i[1][2] * i[0] for i in colors]) / sum([i[0] for i in colors])

    r = int(r)
    g = int(g)
    b = int(b)

    avg = tuple((r, g, b))

    return avg


barColors = []

# Get the color for each frame
for img in images:

    img = Image.open(img).resize((50, 20))

    color = getAvgRGB(img)
    barColors.append(color)

# Initialize image
barImg = Image.new(
    "RGB", (len(barColors), max([1, int(len(barColors) / 2.5)])))

# Add bars to the image
barFullData = [x for x in barColors] * barImg.size[1]

# Make image
barImg.putdata(barFullData)

# Uncomment to adjust image saturation.
# converter = ImageEnhance.Color(barImg)
# converter.enhance(1.7).save(output_image)

# Save to path specified in output_image arg
barImg.save(output_image)
