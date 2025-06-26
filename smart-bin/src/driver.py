from smartbin import SmartBin
import readchar

from gpiozero import LED
from time import sleep


def show_info(text):
    print("\033[H\033[J", end='')  # clear terminal windows
    print(text)


def main():
    # show_info("Press any key to start")
    # while True:
    #     if readchar.readkey():
    #         bin = SmartBin()
    #         break
    bin = SmartBin()
    print(bin.check_fullness())
    bin.get_distance()
    show_info("Press 0/1/2/3 to open a partition")
    key = readchar.readkey()
    if key == "0":
        bin.open(0)
    elif key == "1":
        bin.open(1)
    elif key == "2":
        bin.open(2)
    elif key == "3":
        bin.open(3)

    show_info("Press s to close the bin")
    while True:
        key = readchar.readkey()
        if key == "s":
            bin.close_all()
            break


if __name__ == "__main__":
    main()
