from collections import namedtuple
from io import BytesIO
import math
import pkgutil
from typing import Tuple

from PIL import Image, ImageOps, ImageEnhance
from cv2.data import haarcascades
import cv2
import os
import numpy

__all__ = ('Colour', 'ColourTuple', 'DefaultColours', 'deepfry')

Colour = Tuple[int, int, int]
ColourTuple = Tuple[Colour, Colour]


class DefaultColours:
    """Default colours provided for deepfrying"""
    red = ((254, 0, 2), (255, 255, 15))
    blue = ((36, 113, 229), (255,) * 3)

face_cascade = cv2.CascadeClassifier(os.getcwd() + '/slacky/plugins/custom/deepfry/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(os.getcwd() + '/slacky/plugins/custom/deepfry/haarcascade_eye.xml')
flare_img = Image.open(BytesIO(pkgutil.get_data(__package__, 'flare.png')))

FlarePosition = namedtuple('FlarePosition', ['x', 'y', 'size'])


def deepfryy(img=None, colours= DefaultColours.red, flares= True):
    """
    Deepfry a given image.

    Parameters
    ----------
    img : `Image`
        Image to manipulate.
    colours : `ColourTuple`, optional
        A tuple of the colours to apply on the image.
    flares : `bool`, optional
        Whether or not to try and detect faces for applying lens flares.

    Returns
    -------
    `Image`
        Deepfried image.
    """
    img = img.copy().convert('RGB')
    flare_positions = []

    if flares:
        opencv_img = cv2.cvtColor(numpy.array(img), cv2.COLOR_RGB2GRAY)

        faces = face_cascade.detectMultiScale(
            opencv_img,
            scaleFactor=1.3,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        for (x, y, w, h) in faces:
            face_roi = opencv_img[y:y+h, x:x+w]  # Get region of interest (detected face)

            eyes = eye_cascade.detectMultiScale(face_roi)

            for (ex, ey, ew, eh) in eyes:
                eye_corner = (ex + ew / 2, ey + eh / 2)
                flare_size = eh if eh > ew else ew
                flare_size *= 4
                corners = [math.floor(x) for x in eye_corner]
                eye_corner = FlarePosition(*corners, flare_size)

                flare_positions.append(eye_corner)

    # Crush image to hell and back
    img = img.convert('RGB')
    width, height = img.width, img.height
    img = img.resize((int(width ** .75), int(height ** .75)), resample=Image.LANCZOS)
    img = img.resize((int(width ** .88), int(height ** .88)), resample=Image.BILINEAR)
    img = img.resize((int(width ** .9), int(height ** .9)), resample=Image.BICUBIC)
    img = img.resize((width, height), resample=Image.BICUBIC)
    img = ImageOps.posterize(img, 4)

    # Generate colour overlay
    r = img.split()[0]
    r = ImageEnhance.Contrast(r).enhance(2.0)
    r = ImageEnhance.Brightness(r).enhance(1.5)

    r = ImageOps.colorize(r, colours[0], colours[1])

    # Overlay red and yellow onto main image and sharpen the hell out of it
    img = Image.blend(img, r, 0.75)
    img = ImageEnhance.Sharpness(img).enhance(100.0)

    # Apply flares on any detected eyes
    for flare in flare_positions:
        flare_transformed = flare_img.copy().resize((flare.size,) * 2, resample=Image.BILINEAR)
        img.paste(flare_transformed, (flare.x, flare.y), flare_transformed)

    return img