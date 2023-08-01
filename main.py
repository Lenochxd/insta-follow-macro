import pyautogui
from pynput import keyboard
import threading
from PIL import ImageGrab
import pygetwindow as gw
import time

SCROLL_SPEED = -10
TARGET_COLOR = [(24, 119, 242), (0, 149, 246)]

scrolling = False
last_timestamp = time.time()

def on_press(key):
    global scrolling
    try:
        key_char = key.char
        if key_char == 'q':
            if not scrolling:
                scrolling = True
                # Démarrer le défilement dans un thread séparé
                scrolling_thread = threading.Thread(target=start_scrolling)
                scrolling_thread.start()
            else:
                scrolling = False

    except AttributeError:
        # Certaines touches spéciales n'ont pas d'attribut "char"
        pass

def get_pixel_color(x, y):
    current_screen = gw.getWindowsAt(x, y)[0]
    # Capture d'écran au niveau du curseur de la souris et récupération de la couleur du pixel
    screen = ImageGrab.grab(bbox=(x - current_screen.left, y - current_screen.top, x - current_screen.left + 1, y - current_screen.top + 1))
    return screen.getpixel((0, 0))

def start_scrolling():
    global scrolling, last_timestamp
    while scrolling:
        pyautogui.scroll(SCROLL_SPEED)
        cursor_x, cursor_y = pyautogui.position()
        pixel_color = get_pixel_color(cursor_x, cursor_y)
        print(pixel_color)
        if pixel_color in TARGET_COLOR:
            current_timestamp = time.time()
            if current_timestamp - last_timestamp > 0.5:  # Vérifier qu'il s'est écoulé au moins 0.5 seconde depuis le dernier clic
                last_timestamp = current_timestamp
                pyautogui.scroll(SCROLL_SPEED-8)
                pyautogui.click()
                print('click')
                pyautogui.scroll(SCROLL_SPEED-25)  # Scroll supplémentaire après le clic

# Démarrer le programme
if __name__ == "__main__":
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
