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

# Set the pixel to a Halloween orange
# The pixel collection is an array of 3-value tuples, representing the Red, Green and Blue (RGB)
# values you want for the pixel. These values are from 0-255, representing off to fully on.
# For example:
# - to have the pixel off, set it to (0, 0, 0)
# - to have the pixel white, set it to (255, 255, 255)
# - to have the pixel red, set it to (255, 0, 0)
# - to have the pixel green, set it to (0, 255, 0)
# - to have the pixel blue, set it to (0, 0, 255)
# You can use sites like the Google color picker to get RGB values: https://g.co/kgs/jNx8AH
#
# The first pixel is at position 0 - Python arrays a 0 based
pixels[0] = (255, 102, 0)

# Show the pixel - this commits all the values set on any pixel since the last show call
# If you don't want to have to remember to call show, you can set auto_write to true when
# creating your NeoPixel collection
pixels.show()
