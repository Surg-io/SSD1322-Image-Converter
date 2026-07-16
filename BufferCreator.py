import numpy
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

img = Image.open("") #Pass the path to the png as the argument. Don't forget \\!

Greyscale = False #Set to False if you want a pixels value to be either ON(0xF) or OFF (0x0)

if Greyscale:
    img = img.convert("L")  # Convert to greyscale
    img = np.array(img)
    img = img >> 4 #Convert grayscale values to be in the range of 0-15. Same as dividing every value in the array by 16.
    img = 15 - img #White is now 0, blue is now the range
else:
    img = img.convert("1",dither=Image.Dither.NONE) #Convert to 1s and 0s instead of greyscale
    img = np.array(img)
    img = img * 15 #Sets each value to be either 0 or 15
    img = 15 - img  # White is now 0, blue is now the range

#Show your image to see what it looks like by removing the # on line 27
plt.imshow(img, cmap="Blues")
plt.colorbar()
#plt.show()

#Translate the 256x64 array to 128x64 so each entry for our buffer is a hex byte.
#We make this conversion here to avoid it in our embedded system code

#1. Convert the image buffer values to their values in hex

buf = np.array(img)

hexbuf = [[f"{x:X}" for x in row] for row in buf] #Convert each pixel to its respective hex value

newbuf = [[0 for _ in range(128)] for _ in range(64)]

for i in range(64):
    for j in range(128):
        newbuf[i][j] = hexbuf[i][j*2] + hexbuf[i][(j*2)+1] #Couple pairs of single hex values to create bytes of data.

#Reconstruct to double check (Reverse the process, from hex to its original 0-15 value)
reconstruct = np.zeros((64,256), dtype=np.uint8)

for i in range(64):
    for j in range(128):
        x, y = newbuf[i][j]
        if (x != '0' or y != '0') and not check:
            check = True
        reconstruct[i][j*2] = int(x,16)
        reconstruct[i][(j*2)+1] = int(y,16)


if np.array_equal(img, reconstruct):
    print("SUCCESS: Image reconstructed perfectly")
else:
    print("ERROR: Reconstruction mismatch")

output = reconstruct * 17 #Translate the 0-15 value to a 0-255 value so

output_img = Image.fromarray(output, mode="L")

output_img.save("reconstructed.png")

#Hopefully by this step, the image reconstructs! Let's print newbuf in a way that we can copy and paste in a .c file
flat = np.array(newbuf).flatten()

print(np.array(newbuf).size)

print("const uint8_t image[] = {")
print("    " + ", ".join(f"0x{b}" for b in flat))
print("};")

#Copy and paste the output into your code!
