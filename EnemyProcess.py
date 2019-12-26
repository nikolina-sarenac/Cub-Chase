import CubMaze
import pygame


def move_enemy(xk, yk, player_x, player_y, other_player_x, other_player_y, q, life1, life2, vel):
        run = True
        width = 25
        height = 25
        matW = 640 / 22
        matH = 480 / 16
        maze = CubMaze.Maze()
        x = xk.value
        y = yk.value
        while run:
            if not q.empty():
                return
            if y < player_y.value:
                y += vel
                mx = int(x // matW)
                my = int((y + height) // matH)
                val = maze.value(mx, my)
                mx2 = int((x + width) // matW)
                val2 = maze.value(mx2, my)
                if val == 1 or val2 == 1:
                    y -= vel
                yk.value = y
            if y > player_y.value:
                y -= vel
                mx = int(x // matW)
                my = int(y // matH)
                val = maze.value(mx, my)
                mx2 = int((x + width) // matW)
                val2 = maze.value(mx2, my)
                if val == 1 or val2 == 1:
                    y += vel
                yk.value = y
            if x < player_x.value:
                x += vel
                mx = int((x + width) // matW)
                my = int(y // matH)
                val = maze.value(mx, my)
                my2 = int((y + height) // matH)
                val2 = maze.value(mx, my2)
                if val == 1 or val2 == 1:
                    x -= vel
                xk.value = x
            if x > player_x.value:
                x -= vel
                mx = int(x // matW)
                my = int(y // matH)
                val = maze.value(mx, my)
                my2 = int((y + height) // matH)
                val2 = maze.value(mx, my2)
                if val == 1 or val2 == 1:
                    x += vel
                xk.value = x
            if x == player_x.value and y == player_y.value:
                life1.value -= 1
                #player_x.value = 379
                #player_y.value = 210
            if x == other_player_x.value and y == other_player_y.value:
                life2.value -= 1
                #other_player_x.value = 237
                #other_player_y.value = 210
            pygame.time.wait(30)