import random
import turtle
import keyboard
import math
from collections import (deque)

SEED = 3223
NUM_VERTICES = 12
K = 0.815
drawn_edges = set()

def generate_matrix():
    random.seed(SEED)
    matrix = [[random.random() * 2 for _ in range(NUM_VERTICES)] for _ in range(NUM_VERTICES)]
    return matrix

def apply_threshold(matrix):
    for i in range(NUM_VERTICES):
        for j in range(NUM_VERTICES):
            matrix[i][j] = 1 if matrix[i][j] * K >= 1 else 0
    return matrix

def make_directed_matrix():
    matrix = generate_matrix()
    directed_matrix = apply_threshold(matrix)
    print("Directed Matrix:")
    for row in directed_matrix:
        print(row)
    return directed_matrix

def draw_vertex(x, y, number, color):
    turtle.penup()
    turtle.goto(x, y - 20)
    turtle.pendown()
    turtle.begin_fill()
    turtle.color(color)
    turtle.circle(20)
    turtle.end_fill()
    turtle.penup()
    turtle.goto(x, y - 15)
    turtle.color("black")
    turtle.write(number, align="center", font=("Arial", 18, "bold"))

def draw_arrows():
    arrow_size = 10
    turtle.begin_fill()
    turtle.left(150)
    turtle.forward(arrow_size)
    turtle.left(120)
    turtle.forward(arrow_size)
    turtle.left(120)
    turtle.forward(arrow_size)
    turtle.end_fill()
    turtle.penup()

def loop(x1, y1):
    turtle.goto(x1, y1 - 20)
    turtle.setheading(180)
    turtle.pendown()
    turtle.circle(15)
    turtle.penup()

def draw_bent_edge(x1, y1, x2, y2):
    turtle.goto(x1, y1)
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2
    angle = math.atan2(y2 - y1, x2 - x1)
    turtle.setheading(math.degrees(angle))
    turtle.forward(20)
    turtle.pendown()
    bent_x = mid_x * random.uniform(1.15, 1.35)
    bent_y = mid_y * random.uniform(1.15, 1.35)
    turtle.goto(bent_x, bent_y)
    distance = math.sqrt((x2 - bent_x) ** 2 + (y2 - bent_y) ** 2)
    angle = math.atan2(y2 - bent_y, x2 - bent_x)
    turtle.setheading(math.degrees(angle))
    turtle.forward(distance - 20)
    turtle.penup()

def diff_edge(x1, y1, x2, y2, i, j):
    if i - j == 1 or j - i == 1:
        draw_normal_edge(x1, y1, x2, y2)
    else:
        draw_bent_edge(x1, y1, x2, y2)

def draw_normal_edge(x1, y1, x2, y2):
    angle = math.atan2(y2 - y1, x2 - x1)
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    turtle.setheading(math.degrees(angle))
    turtle.forward(20)
    turtle.pendown()
    turtle.forward(distance - 40)
    turtle.penup()

def draw_edge(x1, y1, x2, y2, i, j):
    if (i, j) in drawn_edges or (j, i) in drawn_edges:
        draw_bent_edge(x1, y1, x2, y2)
        draw_arrows()
        return

    drawn_edges.add((i, j))

    turtle.goto(x1, y1)

    if x1 == x2 == -225 or x1 == x2 == 225 or y1 == y2 == 225 or y1 == y2 == -225:
        if i == j:
            loop(x1, y1)
        else:
            diff_edge(x1, y1, x2, y2, i, j)
    else:
        draw_normal_edge(x1, y1, x2, y2)
    draw_arrows()

def calculate_positions(num_vertices, distance):
    positions = []
    x, y = -225, 225
    for i in range(4):
        for _ in range(num_vertices // 4):
            positions.append((x, y))
            if i % 2 == 0:
                x += distance if i == 0 else -distance
            else:
                y += -distance if i == 1 else distance
    return positions

def draw_graph(matrix):
    positions = calculate_positions(NUM_VERTICES, 150)

    for i, (x, y) in enumerate(positions):
        draw_vertex(x, y, i + 1, 'Orange')

    for i in range(NUM_VERTICES):
        for j in range(NUM_VERTICES):
            if matrix[i][j] == 1:
                draw_edge(positions[i][0], positions[i][1], positions[j][0], positions[j][1], i, j)

def bfs(start_node, adjacency_list):
    print('\n*****BFS*****\n')

    visited = [False] * NUM_VERTICES
    bfs_matrix = [[0] * NUM_VERTICES for _ in range(NUM_VERTICES)]
    bfs_order = []
    positions = calculate_positions(NUM_VERTICES, 150)

    def bfs_recursive(queue):
        if not queue:
            return

        current_vertex = queue.popleft()
        bfs_order.append(current_vertex + 1)

        print("Active vertex:", current_vertex + 1)
        x1, y1 = positions[current_vertex]
        turtle.home()
        draw_vertex(x1, y1, current_vertex + 1, 'Blue')

        for neighbor in adjacency_list[current_vertex]:
            if not visited[neighbor]:
                x2, y2 = positions[neighbor]
                keyboard.wait('space')

                turtle.width(3)
                turtle.color('Red')
                draw_edge(x1, y1, x2, y2, current_vertex, neighbor)
                turtle.home()
                draw_vertex(x2, y2, neighbor + 1, 'Green')

                bfs_matrix[current_vertex][neighbor] = 1
                visited[neighbor] = True
                queue.append(neighbor)

        turtle.home()
        draw_vertex(x1, y1, current_vertex + 1, 'Magenta')
        bfs_recursive(queue)

    queue = deque([start_node])
    visited[start_node] = True
    bfs_recursive(queue)

    for i in range(NUM_VERTICES):
        if not visited[i]:
            queue = deque([i])
            visited[i] = True
            bfs_recursive(queue)

    print("\nBFS adjacency matrix:")
    for row in bfs_matrix:
        print(row)

    print("\nBFS list:", bfs_order)


def build_adjacency_list(matrix):
    adjacency_list = [[] for _ in range(NUM_VERTICES)]

    for i in range(NUM_VERTICES):
        for j in range(NUM_VERTICES):
            if matrix[i][j] == 1:
                adjacency_list[i].append(j)
    return adjacency_list

def dfs(start_node, adjacency_list):
    print('\n*****DFS*****\n')

    visited = [False] * NUM_VERTICES
    dfs_matrix = [[0] * NUM_VERTICES for _ in range(NUM_VERTICES)]
    dfs_order = []
    positions = calculate_positions(NUM_VERTICES, 150)

    def dfs_recursive(current_vertex):
        visited[current_vertex] = True
        dfs_order.append(current_vertex + 1)
        print("Active vertex:", current_vertex + 1)
        x1, y1 = positions[current_vertex]
        turtle.home()
        draw_vertex(x1, y1, current_vertex + 1, 'Blue')

        for neighbor in adjacency_list[current_vertex]:
            if not visited[neighbor]:
                x2, y2 = positions[neighbor]
                keyboard.wait('space')
                draw_vertex(x1, y1, current_vertex + 1, 'Green')

                turtle.home()
                turtle.width(3)
                turtle.color('Red')
                draw_edge(x1, y1, x2, y2, current_vertex, neighbor)
                dfs_matrix[current_vertex][neighbor] = 1

                dfs_recursive(neighbor)

        draw_vertex(x1, y1, current_vertex + 1, 'Magenta')

    dfs_recursive(start_node)

    for i in range(NUM_VERTICES):
        if not visited[i]:
            dfs_recursive(i)

    print("\nDFS adjacency matrix:")
    for row in dfs_matrix:
        print(row)

    print("\nDFS list:", dfs_order)

def main():
    wn = turtle.Screen()
    wn.title("Graphs")
    wn.bgcolor("white")
    wn.setup(width=650, height=650)
    turtle.speed(0)

    directed_matrix = make_directed_matrix()
    draw_graph(directed_matrix)
    turtle.home()
    drawn_edges.clear()

    adjacency_list = build_adjacency_list(directed_matrix)

    bfs(0, adjacency_list)

    keyboard.wait("x")
    drawn_edges.clear()
    turtle.clear()
    turtle.width(1)
    draw_graph(directed_matrix)
    drawn_edges.clear()

    dfs(0, adjacency_list)

    turtle.done()


main()
