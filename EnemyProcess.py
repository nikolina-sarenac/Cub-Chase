import CubMaze
import pygame


def move_enemy(xk, yk, player_x, player_y, other_player_x, other_player_y, q, life1, life2, chase, cought,\
               cought_other, trap1, trap2, trap_caught, wait):
        run = True
        width = 25
        height = 25
        matW = 640 / 22
        matH = 480 / 16
        maze = CubMaze.Maze()
        x = xk.value
        y = yk.value
        player_is_dead = False
        vel = 1
        while run:
            if not q.empty():
                return
            #Neprijatelj ganja svog igraca ukoliko on nije mrtav
            if not player_is_dead and chase.value == 1:
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
            #Ako je njegov igrac mrtav, neprijatelj ganja drugog igraca
            else:
                if y < other_player_y.value:
                    y += vel
                    mx = int(x // matW)
                    my = int((y + height) // matH)
                    val = maze.value(mx, my)
                    mx2 = int((x + width) // matW)
                    val2 = maze.value(mx2, my)
                    if val == 1 or val2 == 1:
                        y -= vel
                    yk.value = y
                if y > other_player_y.value:
                    y -= vel
                    mx = int(x // matW)
                    my = int(y // matH)
                    val = maze.value(mx, my)
                    mx2 = int((x + width) // matW)
                    val2 = maze.value(mx2, my)
                    if val == 1 or val2 == 1:
                        y += vel
                    yk.value = y
                if x < other_player_x.value:
                    x += vel
                    mx = int((x + width) // matW)
                    my = int(y // matH)
                    val = maze.value(mx, my)
                    my2 = int((y + height) // matH)
                    val2 = maze.value(mx, my2)
                    if val == 1 or val2 == 1:
                        x -= vel
                    xk.value = x
                if x > other_player_x.value:
                    x -= vel
                    mx = int(x // matW)
                    my = int(y // matH)
                    val = maze.value(mx, my)
                    my2 = int((y + height) // matH)
                    val2 = maze.value(mx, my2)
                    if val == 1 or val2 == 1:
                        x += vel
                    xk.value = x

            if player_x.value < x + 12 < player_x.value + 25 and player_y.value < y + 12 < \
                    player_y.value + 25:
                pygame.time.delay(1500)
                life1.value -= 1
                cought.value = 1
                pygame.time.delay(3000)

            if other_player_x.value < x + 12 < other_player_x.value + 25 and other_player_y.value < y + 12 < \
                    other_player_y.value + 25:
                pygame.time.delay(1500)
                life2.value -= 1
                cought_other.value = 1
                pygame.time.delay(3000)

            if life1.value == 0:
                player_is_dead = True

            #provera da li je neprijatelj na zamci, ako jeste proveri se da li je zamka aktivna, tj vrednost da li je 2,
            #ako jeste pauzira se neprijatelj na 5 sekundi
            if 87 < x + 12 < 112 and 90 < y + 12 < 115:
                if trap1.value == 2:
                    trap_caught.value = 1
                    pygame.time.wait(5000)
                trap_caught.value = 0

            if 465 < x + 12 < 490 and 420 < y + 12 < 445:
                if trap2.value == 2:
                    trap_caught.value = 1
                    pygame.time.wait(5000)
                trap_caught.value = 0

            pygame.time.wait(wait.value)