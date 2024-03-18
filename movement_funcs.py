import pyautogui
import keyboard
import sys
import time
import os
from pathlib import Path


def move_click(xposition, yposition):
    pyautogui.moveTo(xposition, yposition)
    time.sleep(0.1)
    pyautogui.click()

def move_click_write(xposition, yposition, text):
    pyautogui.moveTo(xposition, yposition)
    time.sleep(0.1)
    pyautogui.click()
    pyautogui.write(text)


def get_image_coords(image_path, error_message):
    """
    Looks for an image on screen and returns the center coords.
    It keeps looking until either, finds the image or 'esc' key is pressed
    """
    while keyboard.is_pressed('esc') == False:
        try:
            pyautogui.locateOnScreen(image_path, confidence=0.9)
        except pyautogui.ImageNotFoundException:
            print(error_message)
            time.sleep(1)
        else:
            print(f"{image_path} found")
            coords = pyautogui.locateCenterOnScreen(image_path, grayscale=0.7, confidence=0.7)
            return(coords)


if __name__ == "__main__":
    pyautogui.displayMousePosition()
