import numpy
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from numpy.f2py.auxfuncs import throw_error

screensizewidth = 256
screensizeheight = 64

img = Image.open(
    "C:\\Users\\Sergio Mendieta\\Pictures\\Screenshots\\Screenshot 2026-07-21 005323.png")  # Pass the path to the png as the argument. Don't forget \\!

width, height = img.size

# --------Variables to control the flow of the program----------
Greyscale = False  # Set to False if you want a pixels value to be either ON(0xF) or OFF (0x0). Set to True for greyscale values

Resize = True  # When False, the photo will stay the same size, so long as it is/under 256 x 64. Otherwise, it will scale down to fit 256x64

# When True, the program will automatically resize the photo to be the dimension closest specified by resizeWidth or resizeHeight
# such that it keeps the aspect ratio. Default values are screensizewidth and screensizeheight
resizeWidth = 240
resizeHeight = 47

OnlyGraphic = True  # If you only have one graphic, you can choose to return of bitmap of said graphic than the entire screen buffer

# Optional: Make a setting that gives a min buffer for a graphic.
# For example, if trying to extract bitmaps, you may want the buffer for each graphic to have the same dimensions.


# May not be needed as we might do this anyway if an image isn't 256 by 64
# Center = True #Buffer the image such that it is centered in the middle screen.
# -------------------------------------------------------------

if resizeWidth > screensizewidth or resizeHeight > screensizeheight:
    throw_error("Cannot resize an image bigger than the target screen size")

if Resize:  # CURRENLTY ONLY WORKS WHEN SIZING DOWN
    img.thumbnail((resizeWidth, resizeHeight), Image.Resampling.NEAREST)
else:
    if width > screensizewidth or height > screensizeheight:
        print("Adjusting")
        img.thumbnail((screensizewidth, screensizeheight), Image.Resampling.NEAREST)

# If the image is not 256x64(becuase it was smaller res, and we never rescaled it up, not that I have added this functionality yet), we can paste it to a 256x64 canvas, or whatever your screensize happens to be
if img.width != screensizewidth or img.height != screensizeheight:
    canvas = Image.new("L", (screensizewidth, screensizeheight), 255)  # 136
    x = (screensizewidth - img.width) // 2  # Centers the image
    y = (screensizeheight - img.height) // 2
    canvas.paste(img, (x, y))
    img = canvas

print(img.size)

if Greyscale:
    img = img.convert("L")  # Convert to greyscale
    img = np.array(img)
    img = img >> 4  # Convert grayscale values to be in the range of 0-15. Same as dividing every value in the array by 16.
    img = 15 - img  # White is now 0, blue is now the range
else:
    img = img.convert("1", dither=Image.Dither.NONE)  # Convert to 1s and 0s instead of greyscale
    img = np.array(img)
    img = img * 15  # Sets each value to be either 0 or 15
    img = 15 - img  # White is now 0, blue is now the range

# Show your image to see what it looks like up to this point by removing the # on line 27
plt.imshow(img, cmap="Blues")
plt.colorbar()
# plt.show()

bufferw = screensizewidth // 2
bufferh = screensizeheight

# Doens't work if width if graphic is an odd number. The string buffer we end up printing later assumes an even number width size so each two columns can be assigned to a byte
if OnlyGraphic:
    ys, xs = np.where(img != 0)  # Get rows and columns that are populated with values
    bbox = (  # Of populated rows and columns, get the min and max of each
        xs.min(),  # left
        ys.min(),  # top
        xs.max() + 1,  # right
        ys.max() + 1  # bottom
    )
    left, top, right, bottom = bbox
    img = img[top:bottom,
          left:right]  # Cropped version of the screen buffer such that it only contains the graphic with no padding
    # In the case that graphic is an odd pixel width, lets add a copy of the middle row to the middle to make it vertically symmetrical
    if img.shape[1] % 2 == 1:
        middle = img.shape[1] // 2
        img = np.insert(img, middle, img[:, middle],
                        axis=1)  # img[:,middle], means get all rows at column 'middle'. Axis is insert as column.
    bufferw = img.shape[1] // 2
    bufferh = img.shape[0]

# Translate the m x n array to m/2 x n so each entry for our buffer is a hex byte.
# We make this conversion here to avoid it in our embedded system code
# 1. Convert the image buffer values to their values in hex

buf = np.array(img)

hexbuf = [[f"{x:X}" for x in row] for row in buf]  # Convert each pixel in the img to its respective hex value

newbuf = [[0 for _ in range(bufferw)] for _ in range(bufferh)]

for i in range(bufferh):
    for j in range(bufferw):
        newbuf[i][j] = hexbuf[i][j * 2] + hexbuf[i][
            (j * 2) + 1]  # Combine pairs of single hex values to create hex bytes of data.

# Reconstruct to double check (Reverse the process, from hex to its original 0-15 value)
reconstruct = np.zeros((bufferh, bufferw * 2), dtype=np.uint8)

for i in range(bufferh):
    for j in range(bufferw):
        x, y = newbuf[i][j]
        reconstruct[i][j * 2] = int(x, 16)
        reconstruct[i][(j * 2) + 1] = int(y, 16)

if np.array_equal(img, reconstruct):
    print("SUCCESS: Image reconstructed perfectly")
else:
    print("ERROR: Reconstruction mismatch")

output = reconstruct * 17  # Translate the 0-15 value to a 0-255 value so the library can generate the png correctly

output_img = Image.fromarray(output, mode="L")

output_img.save("reconstructed.png")

# Hopefully by this step, the image reconstructs! Let's print newbuf in a way that we can copy and paste in a .c file
flat = np.array(newbuf).flatten()

# Should be 8192 for 256x64. Will vary when generating bitmaps for graphics
print(np.array(newbuf).size)

if OnlyGraphic:
    print(f"const char image[{bufferh}][{bufferw}] = ", "{")
    for i in range(bufferh):
        print("  {" + ", ".join(f"0x{b}" for b in newbuf[i]) + "},")
    print("};")
else:
    print("const char image[] = {")
    print("    " + ", ".join(f"0x{b}" for b in flat))
    print("};")




# Copy and paste the output into your code!
