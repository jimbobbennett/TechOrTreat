import asyncio
import board
import neopixel
import pyaudio
import wave

from azure.iot.device.aio import IoTHubDeviceClient, ProvisioningDeviceClient
from azure.iot.device import MethodResponse, MethodRequest

# Set up the connection details for the IoT Central app
ID_SCOPE = ''
DEVICE_ID = ''
PRIMARY_KEY = '+7QNskIREiFdK1if8WdXMoRuwEm4kYffaQ4='

# The number of pixels in the LED strip
PIXEL_COUNT = 6

# Define the brightness
BRIGHTNESS = 1.0

# This is the card number for your speaker
# You can get this by running aplay -l
SPEAKER_CARD_NUMBER = 2

# Create a pixels collection using GPIO pin 18 (Board.D18) using the defined pixel count and brightness
# The auto_write is set to off - this means when you update the color of a pixel it won't happen
# immediately, instead you have to commit the colors. This is faster and smoother when updating
# multiple pixels at once
pixels = neopixel.NeoPixel(board.D18, PIXEL_COUNT, brightness=BRIGHTNESS, auto_write=False)

# Create an audio device
audio = pyaudio.PyAudio()

# When IoT Central sets the lights, it sends the color as a hex string
# This has 6 characters - the first 2 are the hex value for the red channel,
# the next 2 are for the green channel, the last 2 are for the blue channel
# This function converts the hex string to a tuple of values that matches what
# the pixels need.
def hex_to_rgb(hex_color: str):
    try:
        # split in the color string into the red, green and blue components, and convert these
        # to valid hex strings
        r = '0x' + hex_color[0:2]
        g = '0x' + hex_color[2:4]
        b = '0x' + hex_color[4:6]

        # Convert hex to numerical values
        r_value = int(r, 0)
        g_value = int(g, 0)
        b_value = int(b, 0)

        # Return the color as a tuple
        return (r_value, g_value, b_value)
    except:
        # If this isn't a valid hex string, return 0
        return (0, 0, 0)

# This function sets the color of the pixels based off a hex string sent
# in the payload from a IoT Central command
def set_color(payload: str):
    # Convert the hex string to an RGB tuple
    color = hex_to_rgb(payload)
    # Fill the pixels with the color
    pixels.fill(color)
    # Light up the pixels!
    pixels.show()

# This function plays the spooky sound
def play_audio():
    # Open the spooky-sound.wav audio file
    with wave.open('spooky-sound.wav', 'rb') as wave_file:
        # Create an audio output stream using the audio format from the wave file that has just been opened
        # This will output to the SPEAKER_CARD_NUMBER speaker
        stream = audio.open(format=audio.get_format_from_width(wave_file.getsampwidth()),
                            channels=wave_file.getnchannels(),
                            rate=wave_file.getframerate(),
                            output_device_index=SPEAKER_CARD_NUMBER,
                            output=True)

        # Read data from the wave file
        data = wave_file.readframes(4096)

        # All the while we have data, write it to the audio stream
        while len(data) > 0:
            # Write the data to the output stream. This blocks until the stream has been played
            stream.write(data)
            # Read more data. Once the end of the stream is reached the data will be empty and
            # the loop will exit
            data = wave_file.readframes(4096)

        # Stop and close the audio stream
        stream.stop_stream()
        stream.close()

# The asynchronous main function
async def main():
    # Create a provisioning device client to connect this device to the IoT Hub used by
    # IoT Central
    provisioning_device_client = ProvisioningDeviceClient.create_from_symmetric_key(
        provisioning_host="global.azure-devices-provisioning.net",
        registration_id=DEVICE_ID,
        id_scope=ID_SCOPE,
        symmetric_key=PRIMARY_KEY)
    
    # Register the device to get it's hub
    registration_result = await provisioning_device_client.register()

    # Build the connection string - this is used to connect to IoT Central
    conn_str="HostName=" + registration_result.registration_state.assigned_hub + \
                ";DeviceId=" + DEVICE_ID + \
                ";SharedAccessKey=" + PRIMARY_KEY

    # Create the client object using the connection string
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    # Connect the client.
    print("Connecting")
    await device_client.connect()
    print("Connected")

    # This function is called when an IoT Central command is run
    async def command_listener(method_request: MethodRequest):
        # Check the comand that was run
        if method_request.name == 'Scare':
            # If the scare command was run, play the spooky audio
            play_audio()
        elif method_request.name == 'Light':
            # If the light request was run, light the lisghts using the provided hex color
            set_color(method_request.payload)

        # Commands require a response, so create an OK response
        method_response = MethodResponse.create_from_method_request(method_request, 200, {"result": True})

        # Send the response to IoT Central
        await device_client.send_method_response(method_response)

    # Wire up the command listener to be called when a command is received
    device_client.on_method_request_received = command_listener

    # THe main loop - this does nothing, it just keeps the app alive whilst we listen for commands
    async def main_loop():
        # Loop for ever
        while True:
            # Sleep for 1 second every loop
            await asyncio.sleep(1)
    
    # Run the async main loop forever
    await main_loop()

    # Finally, disconnect
    await device_client.disconnect()

# Start the main function running
asyncio.run(main())
