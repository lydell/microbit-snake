import math
import random

import microbit


BRIGHTNESS_SNAKE_MIN = 6
BRIGHTNESS_SNAKE_MAX = 9

BRIGHTNESS_APPLE_MIN = 1
BRIGHTNESS_APPLE_MAX = 9
BRIGHTNESS_APPLE_MAX_BIAS = 0.25
BRIGHTNESS_APPLE_PERIOD = 1000

SLEEP_APPLE = 10
SLEEP_SNAKE = 500

DEATH_BLINK_NUM = 3
DEATH_BLINK_OFF_SLEEP = 300
DEATH_BLINK_ON_SLEEP = 600

MAX_X = 4
MAX_Y = 4

ALL_SPOTS = frozenset(
    {(x, y) for x in range(0, MAX_X) for y in range(0, MAX_Y)})


while True:
    snake_x = 0
    snake_y = 0
    snake_tail = []

    # up = 0, right = 1, down = 2, left = 3
    direction = 1

    apple_x = snake_x
    apple_y = snake_y
    apple_time = microbit.running_time()

    score = -1

    microbit.display.clear()

    while True:
        a_was_pressed = microbit.button_a.was_pressed()
        b_was_pressed = microbit.button_b.was_pressed()

        if (snake_x, snake_y) == (apple_x, apple_y):
            score += 1
            spots = list(ALL_SPOTS - set(snake_tail) - {(snake_x, snake_y)})
            if spots:
                apple_x, apple_y = random.choice(spots)
                apple_time = microbit.running_time()
        elif (snake_x, snake_y) in snake_tail:
            for i in range(0, DEATH_BLINK_NUM * 2):
                if i % 2 == 0:
                    microbit.display.off()
                    microbit.sleep(DEATH_BLINK_OFF_SLEEP)
                else:
                    microbit.display.on()
                    microbit.sleep(DEATH_BLINK_ON_SLEEP)
            microbit.display.scroll(str(score))
            break
        elif snake_tail:
            popped_x, popped_y = snake_tail.pop(0)
            microbit.display.set_pixel(popped_x, popped_y, 0)
        snake_tail.append((snake_x, snake_y))

        diff = int(a_was_pressed) - int(b_was_pressed)
        direction = (direction + diff) % 4

        if direction % 2 == 0:
            snake_y = (snake_y + 1 - direction) % (MAX_Y + 1)
        else:
            snake_x = (snake_x + 2 - direction) % (MAX_X + 1)

        microbit.display.set_pixel(snake_x, snake_y, BRIGHTNESS_SNAKE_MAX)
        tail_length = len(snake_tail)
        for i, (tail_x, tail_y) in enumerate(snake_tail):
            brightness = BRIGHTNESS_SNAKE_MIN + math.floor(
                (BRIGHTNESS_SNAKE_MAX - BRIGHTNESS_SNAKE_MIN) *
                (i / tail_length)
            )
            microbit.display.set_pixel(tail_x, tail_y, brightness)

        for _ in range(0, SLEEP_SNAKE + 1, SLEEP_APPLE):
            if (apple_x, apple_y) != (snake_x, snake_y):
                time = microbit.running_time() - apple_time
                frequency = 2 * math.pi / BRIGHTNESS_APPLE_PERIOD
                brightness = min(
                    BRIGHTNESS_APPLE_MAX,
                    BRIGHTNESS_APPLE_MIN + math.floor(
                        (BRIGHTNESS_APPLE_MAX - BRIGHTNESS_APPLE_MIN) *
                        (math.sin(time * frequency) + 1) *
                        (0.5 + BRIGHTNESS_APPLE_MAX_BIAS)
                    )
                )
                microbit.display.set_pixel(apple_x, apple_y, brightness)
            microbit.sleep(SLEEP_APPLE)
