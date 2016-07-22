import random

import microbit


BRIGHTNESS_SNAKE = 9
BRIGHTNESS_APPLE = 6

MAX_X = 4
MAX_Y = 4

ALL_SPOTS = frozenset(
    {(x, y) for x in range(0, MAX_X) for y in range(0, MAX_Y)})


while True:
    snake_x = MAX_X
    snake_y = 0
    snake_tail = []

    # up = 0, right = 1, down = 2, left = 3
    direction = 1

    apple_x = snake_x
    apple_y = snake_y

    score = -1

    microbit.display.clear()

    while True:
        microbit.sleep(500)

        a_was_pressed = microbit.button_a.was_pressed()
        b_was_pressed = microbit.button_b.was_pressed()

        if (snake_x, snake_y) == (apple_x, apple_y):
            score += 1
            spots = list(ALL_SPOTS - set(snake_tail) - {(snake_x, snake_y)})
            if spots:
                apple_x, apple_y = random.choice(spots)
        elif (snake_x, snake_y) in snake_tail:
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

        microbit.display.set_pixel(apple_x, apple_y, BRIGHTNESS_APPLE)
        microbit.display.set_pixel(snake_x, snake_y, BRIGHTNESS_SNAKE)
