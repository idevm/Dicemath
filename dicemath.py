'Арифметика с игральными костями'

import random, time

DICE_WIDTH: int = 9
DICE_HEIGHT: int = 5
CANVAS_WIDTH: int = 79
CANVAS_HEIGHT: int = 24 - 4
QUIZ_DURATION: float = 60
MIN_DICE: int = 2
MAX_DICE: int = 6
REWARD: int = 5
PENALTY: int = 2

assert MAX_DICE <= 14

D1 = (['+-------+',
       '|       |',
       '|   *   |',
       '|       |',
       '+-------+'], 1)

D2a = (['+-------+',
        '| *     |',
        '|       |',
        '|     * |',
        '+-------+'], 2)

D2b = (['+-------+',
        '|     * |',
        '|       |',
        '| *     |',
        '+-------+'], 2)

D3a = (['+-------+',
        '| *     |',
        '|   *   |',
        '|     * |',
        '+-------+'], 3)

D3b = (['+-------+',
        '|     * |',
        '|   *   |',
        '| *     |',
        '+-------+'], 3)

D4 = (['+-------+',
       '| *   * |',
       '|       |',
       '| *   * |',
       '+-------+'], 4)

D5 = (['+-------+',
       '| *   * |',
       '|   *   |',
       '| *   * |',
       '+-------+'], 5)

D6a = (['+-------+',
        '| *   * |',
        '| *   * |',
        '| *   * |',
        '+-------+'], 6)

D6b = (['+-------+',
        '| * * * |',
        '|       |',
        '| * * * |',
        '+-------+'], 6)

ALL_DICE: 'list[tuple]' = [D1, D2a, D2b, D3a, D3b, D4, D5, D6a, D6b]

print('Арифметика с игральными костями')
print(f'''Сложите все очки, выпавшие на костях на экране. У вас {QUIZ_DURATION} секунд, чтобы решить как можно больше. Вы получите {REWARD} очков за каждый правильный ответ и потеряете {PENALTY} очка за неправильный.''')
input('Нажмите Enter чтобы начать...')

correctAnswers: int = 0
incorrectAnswers: int = 0
startTime: float = time.time()

while time.time() < startTime + QUIZ_DURATION:
    sumAnswer: int = 0
    diceFaces: 'list[list[str]]' = []

    for i in range(random.randint(MIN_DICE, MAX_DICE)):
        die: tuple = random.choice(ALL_DICE)
        diceFaces.append(die[0])
        sumAnswer += die[1]

    topLeftDiceCorners: list = []

    for i in range(len(diceFaces)):
        while True:
            left: int = random.randint(0, CANVAS_WIDTH-1-DICE_WIDTH)
            top: int = random.randint(0, CANVAS_HEIGHT-1-DICE_HEIGHT)
            topLeftX: int = left
            topLeftY: int = top
            topRightX: int = left + DICE_WIDTH
            topRightY: int = top
            bottomLeftX: int = left
            bottomLeftY: int = top + DICE_HEIGHT
            bottomRightX: int = left + DICE_WIDTH
            bottomRightY: int = top + DICE_HEIGHT
            overlaps: bool = False

            for prevDieLeft, prevDieTop in topLeftDiceCorners:
                prevDieRight: int = prevDieLeft + DICE_WIDTH
                prevDieBottom: int = prevDieTop + DICE_HEIGHT

                for cornerX, cornerY in ((topLeftX, topLeftY), (topRightX, topRightY), (bottomLeftX, bottomLeftY), (bottomRightX, bottomRightY)):
                    if (prevDieLeft <= cornerX < prevDieRight and prevDieTop <= cornerY < prevDieBottom):
                        overlaps = True

            if not overlaps:
                topLeftDiceCorners.append((left, top))
                break

    canvas: dict = {}

    for i, (dieLeft, dieTop) in enumerate(topLeftDiceCorners):
        dieFace: 'list[str]' = diceFaces[i]

        for dx in range(DICE_WIDTH):
            for dy in range(DICE_HEIGHT):
                canvasX: int = dieLeft + dx
                canvasY: int = dieTop + dy
                canvas[(canvasX, canvasY)] = dieFace[dy][dx]

    for cy in range(CANVAS_HEIGHT):
        for cx in range(CANVAS_WIDTH):
            print(canvas.get((cx, cy), ' '), end='')

        print()

    response: str = input('Введите сумму: ').strip()
    
    if response.isdecimal() and int(response) == sumAnswer:
        correctAnswers += 1
    else:
        print('Ошибка. Правильный ответ: ', sumAnswer)
        time.sleep(2)
        incorrectAnswers += 1

    print('\n' * 50)

score: int = (correctAnswers * REWARD) - (incorrectAnswers * PENALTY)

print('Время вышло')
print('Правильных ответов: ', correctAnswers)
print('Неправильных ответов: ', incorrectAnswers)
print('Счет: ', score)