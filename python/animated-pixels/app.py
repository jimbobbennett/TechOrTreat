import time

import board
import neopixel

# The number of pixels in the LED strip
PIXEL_COUNT = 6

# Define the brightness
BRIGHTNESS = 1.0

# Create a pixels collection using GPIO pin 18 (Board.D18) using the degined pixel count and brightness
# The auto_write is set to off - this means when you update the color of a pixel it won't happen
# immediately, instead you have to commit the colors. This is faster and smoother when updating
# multiple pixels at once
pixels = neopixel.NeoPixel(board.D18, PIXEL_COUNT, brightness=BRIGHTNESS, auto_write=False)

# The animation we want is a red pixel moving back and forward in the style of a Cylon from
# Battlestar Galactica or Kitt from Night Rider

# This animation has a full red pixel moving back and forward, with the pixels each side in red
# but with reduced brightness

# The direction - incremeting is true when the lit pixel increments each frame, so we light
# 0, then 1, then 2 etc. If this is false the lit pixel decrements, so 2, then 1, then 0
incrementing = True

# The current active pixel
active_pixel = 0

# Create an infinite loop so the animation keeps looping
while True:
    # Loop through the pixels by index
    for i in range(0, PIXEL_COUNT):
        # If the pixel is the active pixel, set it to full red
        if i == active_pixel:
            pixels[i] = (255, 0, 0)
        # If the pixel is the one immediately before or after the active one,
        # set it to half red
        elif i == (active_pixel - 1) or i == (active_pixel + 1):
            pixels[i] = (128, 0, 0)
        # Otherwise, set the pixel to off
        else:
            pixels[i] = (0, 0, 0)

    # Update the active pixel - increment it unless it reaches then end, then decrement it
    # until it reaches the start

    # If we are incrementing
    if incrementing:
        # Set the active pixel to the next one
        active_pixel += 1
    
        # If we have gone off the end, go back one and set to decrementing
        if active_pixel == PIXEL_COUNT:
            active_pixel -= 1
            incrementing = False
    # If we are decrementing
    else:
        # Set the active pixel to the previous one
        active_pixel -= 1
    
        # If we have gone off the end, go back one and set to incrementing
        if active_pixel == -1:
            active_pixel += 1
            incrementing = True

    # Show the pixels
    pixels.show()

    # Wait for a bit so we have a smooth animation
    time.sleep(0.1)
