import board
import neopixel

from grove.i2c import Bus
from rpi_vl53l0x.vl53l0x import VL53L0X

# Create a time of flight sensor instance
distance_sensor = VL53L0X(bus = Bus().bus)
distance_sensor.begin()    

# The number of pixels in the LED strip
PIXEL_COUNT = 6

# Define the brightness
BRIGHTNESS = 1.0

# Create a pixels collection using GPIO pin 18 (Board.D18) using the defined pixel count and brightness
# The auto_write is set to off - this means when you update the color of a pixel it won't happen
# immediately, instead you have to commit the colors. This is faster and smoother when updating
# multiple pixels at once
pixels = neopixel.NeoPixel(board.D18, PIXEL_COUNT, brightness=BRIGHTNESS, auto_write=False)

# Loop forever
while True:
    # Wait for the sensor to get a distance
    distance_sensor.wait_ready()

    # Get the sdistance measurement in mm
    distance = distance_sensor.get_distance()

    # We want the LED to start lighting up when someone is 1m (1000mm) away
    # and be fully lit when they are 50cm (500mm) away

    # Start with > 1m (1000mm)
    if distance >= 1000:
        brightness = 0.0
    
    # Check for <= 500mm
    elif distance <= 500:
        brightness = 1.0

    else:
        # Now do brightness on a scale of 0-1 by dividing the distance from the 1m mark by 500mm
        brightness = (1000.0 - distance) / 500.0

    # Our base color is orange, so multiple the red and green components by the brightness.
    # Orange has no blue component, so this is always 0
    base_r = 255
    base_g = 102

    # Pixel colors are integers, so convert to an int
    adjusted_r = int(base_r * brightness)
    adjusted_g = int(base_g * brightness)

    # The fill method sets the color on all the pixels
    pixels.fill((adjusted_r, adjusted_g, 0))

    # Show the pixels - this commits all the values set on any pixel since the last show call
    # If you don't want to have to remember to call show, you can set auto_write to true when
    # creating your NeoPixel collection
    pixels.show()
