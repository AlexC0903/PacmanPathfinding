import pygame
import queue


WIDTH = 720
pygame.init()
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Pathfinding Visualizer")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.width = width
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbours = []
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == PURPLE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))


    def update_neighbours(self, grid):
        self.neighbours = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
            self.neighbours.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbours.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT
            self.neighbours.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbours.append(grid[self.row][self.col - 1])


    def __lt__(self, other):
        return False

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def dfs(draw, start, end):
    count = 0
    open_set = queue.LifoQueue()
    open_set.put(start)
    came_from = {}
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    return False, 0


        current = open_set.get()

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True, count

        for n in current.neighbours:
            if n not in open_set_hash:
                came_from[n] = current
                open_set.put(n)
                open_set_hash.add(n)
                count += 1

        draw()

        if current != start:
             current.make_closed()

    return False, 0

def bfs(draw, start, end):
    count = 0
    open_set = queue.Queue()
    open_set.put(start)
    came_from = {}
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    return False, 0


        current = open_set.get()

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True, count

        for n in current.neighbours:
            if n not in open_set_hash:
                came_from[n] = current
                open_set.put(n)
                open_set_hash.add(n)
                count += 1

        draw()

        if current != start:
             current.make_closed()

    return False, 0

def astar(draw, grid, start, end):
    count = 0
    open_set = queue.PriorityQueue()
    open_set.put(item=(0, count, start))
    came_from = {}
    g = {node: float("inf") for row in grid for node in row}
    g[start] = 0
    f = {node: float("inf") for row in grid for node in row}
    f[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    return False, 0


        current = open_set.get()[2]

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True, count

        for neighbour in current.neighbours:
            temp_g = g[current] + 1

            if temp_g < g[neighbour]:
                came_from[neighbour] = current
                g[neighbour] = temp_g
                f[neighbour] = temp_g + h(neighbour.get_pos(), end.get_pos())
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    if neighbour != end:
                        neighbour.make_open()

        draw()

        if current != start:
             current.make_closed()

    return False, 0

def ucs(draw, grid, start, end):
    count = 0
    open_set = queue.PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    c = {node: float("inf") for row in grid for node in row}
    c[start] = 0

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    return False, 0


        current = open_set.get()[1]

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True, count

        for n in current.neighbours:
            if n not in open_set_hash:
                came_from[n] = current
                c[n] = c[current] + 1
                open_set.put((c[n], n))
                open_set_hash.add(n)
                count += 1


        draw()

        if current != start:
             current.make_closed()

    return False, 0

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        # If rows = 5, then grid would be [[], [], [], [], []]
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            if i == 0 or j == 0 or i == 59 or j == 59:
                node.make_barrier()
            grid[i].append(node)

    return grid

def draw_grid(win, rows, width):
     gap = width // rows
     for i in range(rows):
         pygame.draw.line(win, GREY, (0, i*gap), (width, i*gap))
         for j in range(rows):
            pygame.draw.line(win, GREY, (j*gap, 0), (j*gap, width))

def draw_text(win, text, fontSize, colour, offsetX, offsetY):
    font = pygame.font.Font(None, fontSize)
    text = font.render(text, 1, colour)
    textpos = text.get_rect()
    textpos.centerx = win.get_rect().centerx+offsetX
    textpos.centery = win.get_rect().centery+offsetY

    win.blit(text, textpos)


def draw(win, grid, rows, width, score):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    draw_text(win, "Depth First Search - D", 20, (255, 255, 255), -290, -353)
    draw_text(win, "Breadth First Search - B", 20, (255, 255, 255), -80, -353)
    draw_text(win, "AStar Search - A", 20, (255, 255, 255), 100, -353)
    draw_text(win, "Uniform Cost Search - U", 20, (255, 255, 255), 280, -353)
    draw_text(win, score, 20, (255, 255, 255), 0, 355)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

def main(win, width):
    ROWS = 60
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False
    score = "Success: False  Count: 0"


    while run:
        draw(win, grid, ROWS, width, score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if not start and node != end and node.is_barrier() == False:
                    start = node
                    start.make_start()

                elif not end and node != start and node.is_barrier() == False:
                    end = node
                    end.make_end()

                elif node != end and node != start:
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]: # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and start and end and started == False:
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)
                    started = True
                    Success, Count = astar(lambda: draw(win, grid, ROWS, width, score), grid, start, end)
                    score = "Success: " + str(Success) + "  Count:" + str(Count)

                elif event.key == pygame.K_d and start and end and started == False:
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)
                    started = True
                    Success, Count = dfs(lambda: draw(win, grid, ROWS, width, score), start, end)
                    score = "Success: " + str(Success) + "  Count:" + str(Count)

                elif event.key == pygame.K_b and start and end and started == False:
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)
                    started = True
                    Success, Count = bfs(lambda: draw(win, grid, ROWS, width, score), start, end)
                    score = "Success: " + str(Success) + "  Count:" + str(Count)

                elif event.key == pygame.K_u and start and end and started == False:
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)
                    started = True
                    Success, Count = ucs(lambda: draw(win, grid, ROWS, width, score), grid, start, end)
                    score = "Success: " + str(Success) + "  Count:" + str(Count)

                if event.key == pygame.K_c and started:
                    start = None
                    end = None
                    started = False
                    grid = make_grid(ROWS, width)



    pygame.quit()

main(WIN, WIDTH)