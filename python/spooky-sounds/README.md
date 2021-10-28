# Spooky sounds

This sample shows how to play audio on your Pi.

## Hardware

You will need a speaker. You can either connect a speaker to the 3.5mm jack on the Pi, or connect a USB speaker. Make sure you test your speaker out on the Pi, an easy way to do this is to open a YouTube video in the Chromium browser on the Pi, such as this [audio test video](https://youtu.be/dQw4w9WgXcQ).

This code uses the [pyaudio](https://pypi.org/project/PyAudio/) python package. To use this library, you also need to install the following apt packages:

```sh
sudo apt update
sudo apt install libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev libasound2-plugins --yes 
```

Once your hardware is connected, run the following command in the terminal to get the hardware ID:

```sh
aplay -l
```

This will list all your audio hardware. There will be an entry for the headphone socket, an entry for the HDMI audio out for each monitor attached (if you are 'headless' then there will be no HDMI out), and if you are using USB then an entry for your USB audio device.

```output
pi@pumpkin:~/pumpkin $ aplay -l
**** List of PLAYBACK Hardware Devices ****
card 0: b1 [bcm2835 HDMI 1], device 0: bcm2835 HDMI 1 [bcm2835 HDMI 1]
  Subdevices: 4/4
  Subdevice #0: subdevice #0
  Subdevice #1: subdevice #1
  Subdevice #2: subdevice #2
  Subdevice #3: subdevice #3
card 1: Headphones [bcm2835 Headphones], device 0: bcm2835 Headphones [bcm2835 Headphones]
  Subdevices: 4/4
  Subdevice #0: subdevice #0
  Subdevice #1: subdevice #1
  Subdevice #2: subdevice #2
  Subdevice #3: subdevice #3
card 2: M0 [eMeet M0], device 0: USB Audio [USB Audio]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
```

You need the card number for the device you are planning to use to both test an audio file, and to playback from code. In the output above, I want to use the eMeet M0 USB speaker, so the card number is 2.

## Audio file

You will need an audio file to play, such as a WAV file of spooky sounds. One way to get this is to record a WAV file with a USB microphone connected to the Pi.

> If you don't want to record a spooky audio file, you can use the `spooky-sound.wav` file in this folder. Alternatively you can convert any audio file to a WAV file. You may have to try converting the audio to different sample rates depending on your hardware, for example I use an eMeet M0 which only seems to like audio files at 48KHz

To record an audio file, first get the hardware ID of the microphone you want to use with the following command:

```sh
arecord -l
```

This will list all your audio input devices.

```output
pi@pumpkin:~/pumpkin $ arecord -l
**** List of CAPTURE Hardware Devices ****
card 2: M0 [eMeet M0], device 0: USB Audio [USB Audio]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
```

You need the card number for the device you are planning to use. In the output above, my mic is my eMeet M0 on card 2.

Use the following command to record:

```sh
arecord --device=plughw:<mic card number>,0 --format S16_LE --rate 48000 -c1 spooky-sound.wav
```

Replace `<mic card number>` with the card number from the previous step for your microphone. For example, for me eMeet card I would use:

```sh
arecord --device=plughw:2,0 --format S16_LE --rate 48000 -c1 spooky-sound.wav
```

This records a mono audio file called `spooky-sound.wav` at 48KHz. Make sure to record something really spooky! Press `ctrl+c` when you are done recording.

You can listen to this back with the following command:

```sh
aplay --device=plughw:<speaker card number>,0 spooky-sound.wav
```

Replace `<speaker card number>` with the card number from an earlier step for your speaker. For example, for me eMeet card I would use:

```sh
aplay --device=plughw:2,0 spooky-sound.wav
```

## Instructions

1. Configure your audio device and ensure it works

1. Install the apt packages

1. Install the Pip packages using `sudo`:

    ```sh
    sudo pip3 install -r requirements.txt
    ```

1. Open the `app.py` file, and update the `SPEAKER_CARD_NUMBER` to the card number for your speaker.

1. Read the `app.py` code to understand what it does.

1. Run the `app.py` sample using `sudo`:

    ```sh
    sudo python3 app.py
    ```
