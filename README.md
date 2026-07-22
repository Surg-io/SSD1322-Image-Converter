# SSD1322-Image-Converter
Generates a 8192 size buffer array of byte hex values that represent pixel values for outputting an image onto the 2.8 NHD 25664 OLED screen that uses the SSD1322 controller

# Workflow

### 1. Get an image/graphic

The image that you select should be relatively similar, if not perfect, to the resolution of the screen you want to print it on. In the case where an image isn't exactly the resolution of the OLED you are transposing it to, choosing an image that isn't similar in resolution can cause the image to be too deformed to be interpreted when we size it exactly later. As an example, when using the NHD 2.8 25664, try to get images that that are 256x64 pixels, or at the vary least, where the width is longer than the height.
**Screenshotting images can be very helpful when getting an image thats an estimate of your screen**

*Here is an example of a screenshot taken. The screenshot is 371 x 105* </br>
![Example Screenshot](/Images/371105.png)


### 2. Plug your image into an m x n pixel image converter 
Choose a pixel image converter to convert your chosen image into pixelated form. Have m and n be the resolution of your OLED(NHD 2.8 will use a 256x64 converter, for example). Save the resulting image. 
An example of a converter can be found [here](https://www.resizepixel.com/)

*Converted Image*</br>
![Converted Image](/Images/25664.png)

## OR

Simply adjust ```Resize = True``` so your photo will automatically be resized to 256x64, or a dimension of your choosing by specifying  ```resizeWidth``` and ```resizeHeight``` parameters. 

### 3. Run the image through the Python Code

Now that you have the image as the same resolution as your screen, you can run the image through the code to get the respective array buffer full of pixel values. You can choose to have the filter allow respective pixels to be greyscaled based on the original image, or simply have a pixel be marked as on or off. Do this by setting the `Greyscale` boolean.

*Example of Greyscaled and Non Greyscaled Outputs*</br>
![Greyscaled](/Images/Greyscale.png)</br>
![Non Greyscaled](/Images/NonGreyscale.png)

You can also choose to print a bitmap of a graphic. If you would rather have a bitmap of a graphic than a buffer for the whole screen that includes said graphic, simply have ```OnlyGraphic = True```

### 4. Final Steps

Assuming you know how to display to your OLED screen using SSD1322 commands, you can simply have a for loop that runs through the generated buffer to print out to your screen. Some psudocode for the NHD 2.8 25664 would look something along the lines of 

```
buffer[] =  *copied buffer*
SendData(0x5C) //Command: Enable Write Data into RAM
for byte in buffer:
    SendData(buffer[byte]) //Data: Pixel Values
```
