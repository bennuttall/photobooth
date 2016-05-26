from picamera import PiCamera
from gpiozero import Button
from datetime import datetime
from time import sleep
from twython import Twython
from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

camera = PiCamera()
left = Button(23)
right = Button(24)

effects = ['negative', 'emboss', 'colorswap', 'sketch', 'none']
i = 0

def change_effect():
    global i
    i += 1
    effect = effects[i % len(effects)]
    camera.image_effect = effect

def capture():
    global last_capture
    dt = datetime.now().isoformat()
    filename = '/home/pi/photobooth/{}.jpg'.format(dt)
    camera.capture(filename)
    last_capture = filename

def tweet(message, img):
    with open(img, 'rb') as photo:
        twitter.update_status_with_media(status=message, media=photo)

left.when_pressed = change_effect

while True:
    camera.start_preview()
    camera.annotate_text = "Press left button to change the effect"
    sleep(2)
    camera.annotate_text = "Press right button to take a picture"
    sleep(2)
    camera.annotate_text = None
    right.wait_for_press()
    capture()
    camera.annotate_text = "Press right button to tweet the photo"
    right.wait_for_press()
    camera.stop_preview()
    handle = input("Enter your Twitter handle: @")
    message = "Welcome to @Raspberry_Pi Towers, @{}".format(handle)
    tweet(message, last_capture)
    camera.start_preview()
    camera.annotate_text = "Tweeted!"
    sleep(2)
