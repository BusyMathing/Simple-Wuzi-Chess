# -*- coding:utf-8 -*-
from asyncio import sleep
from tkinter import messagebox
import pygame
import sys
import os
from pprint import pprint
import random

# 显示更新日志
messagebox.showinfo('更新日志', "五子棋代码更新日志'\n'1. 优化了 `pre_place` 函数的计算逻辑，简化了代码。'\n'2. 将胜利判断逻辑提取到 `check_win` 函数中，减少了重复代码，提高了代码的可读性和维护性。'\n'3. 使用列表推导式初始化 `dp`，使代码更简洁。'\n'4. 修复了最后一颗棋子无法显示的 bug：'\n'- 在每次绘制棋子后立即调用 `pygame.display.update()` 来刷新屏幕，确保最后一颗棋子能够正确显示。'\n'5. 代码结构优化：'\n'- 将绘制棋子和胜利判断的逻辑分离，使代码更模块化。'\n'- 增加了更多注释，帮助理解代码逻辑。'\n'6. 新增功能：'\n'- 加入了AI对战功能，玩家可以选择单人对战或线下多人对战。'\n'- 在单人对战模式下，AI将作为白棋进行对战。'\n''\n'提示：'\n'- 左键点击棋盘进行下棋，黑白棋自动切换。'\n'- 游戏会自动判断胜利，并弹出提示框显示胜利信息。'\n'感谢使用五子棋1.2版本！")

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
                # 检查水平
                if j <= 10 and all(dp[i][j + k] == player for k in range(5)):
                    return True
                # 检查垂直
                if i <= 10 and all(dp[i + k][j] == player for k in range(5)):
                    return True
                # 检查对角线（左上到右下）
                if i <= 10 and j <= 10 and all(dp[i + k][j + k] == player for k in range(5)):
                    return True
                # 检查对角线（左下到右上）
                if i >= 4 and j <= 10 and all(dp[i - k][j + k] == player for k in range(5)):
                    return True
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

def ai_move(dp):
    def is_winning_move(dp, player, x, y):
        dp[x][y] = player
        win = check_win(dp, player)
        dp[x][y] = 0
        return win

    def evaluate_position(dp, player, x, y):
        score = 0
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            count = 0
            for k in range(-4, 5):
                nx, ny = x + k * dx, y + k * dy
                if 0 <= nx < 15 and 0 <= ny < 15:
                    if dp[nx][ny] == player:
                        count += 1
                    elif dp[nx][ny] != 0:
                        count -= 1
            score += count
        return score

    def find_nearby_black(dp):
        black_positions = [(i, j) for i in range(15) for j in range(15) if dp[i][j] == 1]
        nearby_positions = []
        for x, y in black_positions:
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < 15 and 0 <= ny < 15 and dp[nx][ny] == 0:
                        nearby_positions.append((nx, ny))
        return nearby_positions

    best_score = -1
    best_move = None

    # 优先阻止玩家的连珠
    for i in range(15):
        for j in range(15):
            if dp[i][j] == 0:
                if is_winning_move(dp, 1, i, j):
                    dp[i][j] = 2
                    draw(dp, canvas)
                    return

    # 优先完成自己的连珠
    for i in range(15):
        for j in range(15):
            if dp[i][j] == 0:
                if is_winning_move(dp, 2, i, j):
                    dp[i][j] = 2
                    draw(dp, canvas)
                    return

    # 在第3颗子连珠时进行堵截
    for i in range(15):
        for j in range(15):
            if dp[i][j] == 0:
                if evaluate_position(dp, 1, i, j) >= 3:
                    dp[i][j] = 2
                    draw(dp, canvas)
                    return

    # 评估每个空位置的得分
    for i in range(15):
        for j in range(15):
            if dp[i][j] == 0:
                score = evaluate_position(dp, 2, i, j)
                if score > best_score:
                    best_score = score
                    best_move = (i, j)

    # 如果找到最佳位置，则下棋
    if best_move:
        dp[best_move[0]][best_move[1]] = 2
        draw(dp, canvas)
    else:
        # 如果没有找到最佳位置，则在黑棋附近随机下棋
        nearby_positions = find_nearby_black(dp)
        if nearby_positions:
            move = random.choice(nearby_positions)
        else:
            # 如果没有黑棋附近的空位，则随机下棋
            empty_positions = [(i, j) for i in range(15) for j in range(15) if dp[i][j] == 0]
            move = random.choice(empty_positions)
        dp[move[0]][move[1]] = 2  # AI always plays as white
        draw(dp, canvas)

# 默认在中央下棋
    if  dp[7][7] == 0:
        dp[7][7] = 2
        draw(dp, canvas)


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

mode = messagebox.askquestion('选择模式', '请选择游戏模式：\n是：单人对战\n否：线下多人对战')

messagebox.showinfo('提示', '黑先白后')

player_turn = True  # 用于控制玩家和AI的轮次

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and player_turn:
            x, y = pre_place(event.pos[0], event.pos[1])
            if dp[y][x] == 0:
                if mode == 'yes' and count % 2 == 1:
                    continue  # 单人对战时，玩家只能下黑棋
                dp[y][x] = 1  # 玩家只能下黑棋
                count += 1
                draw(dp, canvas)
                if mode == 'yes':  # 单人对战且轮到AI
                    player_turn = False  # 禁用玩家点击，等待AI下棋
                    ai_move(dp)
                    count += 1
                    player_turn = True  # AI下棋完成，重新启用玩家点击
        elif event.type == pygame.MOUSEMOTION:
            pygame.display.set_caption("五子棋1.0" + str(event.pos))
    win(dp)
    pygame.display.update()
