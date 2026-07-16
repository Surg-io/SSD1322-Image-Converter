# SSD1322-Image-Converter
Generates a 256x64 buffer array of half-byte hex values that represent pixel values for outputting an image onto the 2.8 NHD 25664 OLED screen that uses the SSD1322 controller

# Workflow

### 1. Get an image

The image that you select should be relatively similar, if not perfect, to the resolution of the screen you want to print it on. In the case where an image isn't exactly the resolution of the OLED you are transposing it to, choosing an image that isn't similar in resolution can cause the image to be too deformed to be interpreted when we size it exactly later. As an example, when using the NHD 2.8 25664, try to get images that that are 256x64 pixels, or at the vary least, where the width is longer than the height.
**Screenshotting images can be very helpful when getting an image thats an estimate of your screen**

*Here is an example of a screenshot taken. The screenshot is 371 x 105* CREATE IMAGE FOLDER AND PUT IMAGE IN THERE FOR REFERENCE
![Example Screenshot]()

### 2. Plug your image into an m x n pixel image converter

Choose a pixel image converter to convert your chosen image into pixelated form. Have m and n be the resolution of your OLED(NHD 2.8 will use a 256x64 converter, for example). Save the resulting image. 
An example of a converter can be found [here](https://www.resizepixel.com/)

### 3. Run the image through the Python Code

Now that you have the image as the same resolution as your screen, you can run the image through the code to get the respective array buffer full of pixel values. You can choose to have the filter allow certain pixels to be greyscaled based on the original image, or simply have a pixel be marked as on or off. The choice is up to you

### 4. Final Steps

Assuming you know how to display to your OLED screen using SSD1322 commands, you can simply have a for loop that runs through the generated buffer to print out to your screen. Some psudocode for the NHD 2.8 25664 would look something along the lines of 

```
m = 128 // m is 256/2 as the SSD1322 sends a byte at a time. A byte = 2 pixels, 4 bits per pixel. So we will be sending 128 bytes for 256 columns
n = 64
buffer[n][m] =  *copied buffer*
SendData(0x5C) //Command: Enable Write Data into RAM
for i in range(0,n):
  for j in range(0,m):
    SendData(buffer[i][j]) //Data: Pixel Values
```
