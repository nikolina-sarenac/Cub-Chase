import CubMaze


def player_function(xk, yk, qin, q):
    run = True
    width = 25
    height = 25
    vel = 2
    matW = 640 / 22
    matH = 480 / 16
    maze = CubMaze.Maze()
    x = xk.value
    y = yk.value
    while run:
        x = xk.value
        y = yk.value
        if not q.empty():
            return
        if not qin.empty():
            k = qin.get()
            if k == 1:
                x -= vel
                mx = int(x // matW)
                my = int(y // matH)
                val = maze.value(mx, my)
                my2 = int((y + height) // matH)
                val2 = maze.value(mx, my2)
                if val == 1 or val2 == 1:
                    x += vel
                xk.value = x
            if k == 2:
                x += vel
                mx = int((x + width) // matW)
                my = int(y // matH)
                val = maze.value(mx, my)
                my2 = int((y + height) // matH)
                val2 = maze.value(mx, my2)
                if val == 1 or val2 == 1:
                    x -= vel
                xk.value = x
            if k == 3:
                y -= vel
                mx = int(x // matW)
                my = int(y // matH)
                val = maze.value(mx, my)
                mx2 = int((x + width) // matW)
                val2 = maze.value(mx2, my)
                if val == 1 or val2 == 1:
                    y += vel
                yk.value = y
            if k == 4:
                y += vel
                mx = int(x // matW)
                my = int((y + height) // matH)
                val = maze.value(mx, my)
                mx2 = int((x + width) // matW)
                val2 = maze.value(mx2, my)
                if val == 1 or val2 == 1:
                    y -= vel
                yk.value = y