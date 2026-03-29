import os

from ocr.scanner.master import Master


def main():
    display_path = os.path.expanduser("~/.lastdisplay")
    if os.path.exists(display_path):
        display = open(display_path).readline().strip()
        os.environ["DISPLAY"] = display

    screen_size = (1920, 1200)

    master = Master(screen_size)
    master.start()


if __name__ == '__main__':
    main()
