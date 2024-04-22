import time
import random
import requests
import pyautogui
import urllib.parse
from solver import PuzleSolver
from seleniumwire.undetected_chromedriver.v2 import Chrome


def fetch_puzzle_images(driver):
    for request in driver.requests:
        url = urllib.parse.unquote(request.url)
        if url.endswith(".jpg"):
            background_url = url
        elif url.endswith(".frag.png"):
            piece_url = url

    background_file = "background.jpg"
    piece_file = "piece.png"
    
    response = requests.get(background_url)
    with open(background_file, "wb") as f:
        f.write(response.content)

    response = requests.get(piece_url)
    with open(piece_file, "wb") as f:
        f.write(response.content)

    return background_file, piece_file


def solve_captcha(driver, distance):
    screenshot = pyautogui.screenshot()
    position = pyautogui.locate("arrow.png", screenshot)
    
    x = position.left
    y = position.top
    
    pyautogui.moveTo(position)
    pyautogui.mouseDown()
    pyautogui.dragTo(x + distance, y, duration=round(random.uniform(0.8, 1.6), 2))
    pyautogui.mouseUp()


# def get_screen_multiplier():
#     screen_width, screen_height = pyautogui.size()
#     return screen_width / 1366  # 1366 is a reference screen width


def main():
    url = "https://idealista.com"
    driver = Chrome()
    driver.maximize_window()
    driver.get(url)
    
    background_image, piece_image = fetch_puzzle_images(driver)
    
    solver = PuzleSolver(piece_image, background_image)
    distance = solver.get_position() * 1.27
    
    solve_captcha(driver, distance)
    
    time.sleep(15)
    driver.quit()


if __name__ == "__main__":
    main()