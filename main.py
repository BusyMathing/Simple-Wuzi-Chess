from asyncio import sleep
from tkinter import messagebox
import pygame
import sys
import os
from pprint import pprint
messagebox.showinfo('更新日志', "五子棋代码更新日志'\n'1. 优化了 `pre_place` 函数的计算逻辑，简化了代码。'\n'2. 将胜利判断逻辑提取到 `check_win` 函数中，减少了重复代码，提高了代码的可读性和维护性。'\n'3. 使用列表推导式初始化 `dp`，使代码更简洁。'\n'4. 修复了最后一颗棋子无法显示的 bug：'\n'- 在每次绘制棋子后立即调用 `pygame.display.update()` 来刷新屏幕，确保最后一颗棋子能够正确显示。'\n'5. 代码结构优化：'\n'- 将绘制棋子和胜利判断的逻辑分离，使代码更模块化。'\n'- 增加了更多注释，帮助理解代码逻辑。'\n''\n'提示：'\n'- 左键点击棋盘进行下棋，黑白棋自动切换。'\n'- 游戏会自动判断胜利，并弹出提示框显示胜利信息。'\n'感谢使用五子棋1.1版本！")
def draw(dp, canvas):
    for i in range(15):
        for j in range(15):
            if dp[i][j] == 1:
                canvas.blit(black, (j * 54 + 27 - 12.5, i * 54 + 15 - 15))
            elif dp[i][j] == 2:
                canvas.blit(white, (j * 54 + 27 - 12.5, i * 54 + 15 - 15))
    pygame.display.update()  # 每次绘制后立即更新屏幕

def pre_place(x, y):
    result = [-1, -1]
    x -= 27
    y -= 15
    if x >= 0 and y >= 0:
        result[0] = x // 54 + (1 if x % 54 > 27 else 0)
        result[1] = y // 54 + (1 if y % 54 > 27 else 0)
    return tuple(result)

def check_win(dp, player):
    for i in range(15):
        for j in range(15):
            if dp[i][j] == player:
                if all(dp[i + k][j] == player for k in range(-2, 3) if 0 <= i + k < 15): return True
                if all(dp[i][j + k] == player for k in range(-2, 3) if 0 <= j + k < 15): return True
                if all(dp[i + k][j + k] == player for k in range(-2, 3) if 0 <= i + k < 15 and 0 <= j + k < 15): return True
                if all(dp[i + k][j - k] == player for k in range(-2, 3) if 0 <= i + k < 15 and 0 <= j - k < 15): return True
    return False

def win(dp):
    draw(dp, canvas)
    if check_win(dp, 1):
        sleep(1)
        pprint(dp)
        draw(dp, canvas)
        messagebox.showinfo('提示', '黑棋胜利')
        print("黑棋胜利")
        pygame.quit()
        os.system("pause")
        sys.exit()
    elif check_win(dp, 2):
        sleep(1)
        pprint(dp)
        draw(dp, canvas)
        messagebox.showinfo('提示', '白棋胜利')
        print("白棋胜利")
        pygame.quit()
        os.system("pause")
        sys.exit()

print("左键下棋，会自动切换黑白棋，可判断胜利")
dp = [[0] * 15 for _ in range(15)]
pygame.init()
size = width, height = 800, 800
canvas = pygame.display.set_mode(size)
pygame.display.set_caption("五子棋1.0")
canvas.fill((255, 255, 255))
black = pygame.image.load("images/black.png")
white = pygame.image.load("images/white.png")
init = pygame.image.load("images/init.png")
canvas.blit(init, (0, 0))
count = 0

messagebox.showinfo('提示', '黑先白后')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = pre_place(event.pos[0], event.pos[1])
            if dp[y][x] == 0:
                dp[y][x] = 1 if count % 2 == 0 else 2
                count += 1
                draw(dp, canvas)
        elif event.type == pygame.MOUSEMOTION:
            pygame.display.set_caption("五子棋1.0" + str(event.pos))
    win(dp)
    pygame.display.update()
