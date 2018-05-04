import time
from CarMove import CarMove

if __name__ == '__main__':

    c = CarMove()

    print("moveFront(325)")
    c.moveFront(325)
    time.sleep(2)

    print("turnRight!")
    c.turnRight(380)
    time.sleep(2)

    print("turnLeft!")
    c.turnLeft(220)
    time.sleep(2)

    print("stop")
    c.turnRight(307)
    c.moveFront(307)

    c.stop()

