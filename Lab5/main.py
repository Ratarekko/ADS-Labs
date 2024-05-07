import random
import turtle
import keyboard
import math
from collections import (deque)

SEED = 3223
NUM_VERTICES = 12
K = 0.68
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

def draw_edge(x1, y1, x2, y2, i, j, directed):
    if (i, j) in drawn_edges or (j, i) in drawn_edges:
        if not directed:
            return
        else:
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

    if directed:
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

def draw_graph(matrix, directed):
    positions = calculate_positions(NUM_VERTICES, 150)

    for i, (x, y) in enumerate(positions):
        draw_vertex(x, y, i + 1, 'Orange')

    for i in range(NUM_VERTICES):
        for j in range(NUM_VERTICES):
            if matrix[i][j] == 1:
                draw_edge(positions[i][0], positions[i][1], positions[j][0], positions[j][1], i, j, directed)

def bfs(graph, start_vertex):
    visited = set()
    queue = deque([start_vertex])
    visited_order_bfs = []

    while queue:
        current_vertex = queue.popleft()
        if current_vertex not in visited:
            visited_order_bfs.append(current_vertex+1)
            visited.add(current_vertex)
            for neighbor, connected in enumerate(graph[current_vertex]):
                if connected and neighbor not in visited:
                    queue.append(neighbor)
    visited_order_bfs.append(11)
    print('\n BFS:')
    print(visited_order_bfs)
    return visited_order_bfs

def dfs(graph, start_vertex):
    visited = set()
    stack = [start_vertex]
    visited_order_dfs = []

    while stack:
        current_vertex = stack.pop()
        if current_vertex not in visited:
            visited_order_dfs.append(current_vertex+1)
            visited.add(current_vertex)

            for neighbor, connected in reversed(list(enumerate(graph[current_vertex]))):
                if connected and neighbor not in visited:
                    stack.append(neighbor)
    visited_order_dfs.append(11)
    print('\n DFS:')
    print(visited_order_dfs)
    return visited_order_dfs

def traversal_matrix(graph, visited_order):
    num_vertices = len(graph)
    traversal_adjacency_matrix = [[0] * num_vertices for _ in range(num_vertices)]

    for i in range(len(visited_order) - 1):
        current_vertex = visited_order[i]
        next_vertex = visited_order[i + 1]
        traversal_adjacency_matrix[current_vertex - 1][next_vertex - 1] = 1

    return traversal_adjacency_matrix

def visualize_fs(visited_order, positions, directed, button):
    for i in range(len(visited_order) - 1):
        current_vertex = visited_order[i] - 1
        next_vertex = visited_order[i + 1] - 1

        x1, y1 = positions[current_vertex]
        x2, y2 = positions[next_vertex]

        keyboard.wait(button)
        draw_vertex(x1, y1, visited_order[i], 'Yellow')
        turtle.width(4)
        turtle.color('Blue')

        draw_edge(x1, y1, x2, y2, current_vertex, next_vertex, directed)
        turtle.home()
        keyboard.wait(button)
        draw_vertex(x2, y2, visited_order[i + 1], 'Green')

def main():
    wn = turtle.Screen()
    wn.title("Graphs")
    wn.bgcolor("white")
    wn.setup(width=1200, height=650)
    turtle.speed("fastest")

    directed_matrix = make_directed_matrix()
    draw_graph(directed_matrix, True)
    turtle.home()

    drawn_edges.clear()
    positions = calculate_positions(NUM_VERTICES, 150)

    turtle.penup()
    turtle.goto(-585, -40)
    turtle.pendown()
    turtle.write('Press "b" for BFS\nPress "d" for DFS', font=("Arial Black", 23, "normal"))
    turtle.penup()

    visited_order_bfs = bfs(directed_matrix, 0)
    traversal_matrix_bfs = traversal_matrix(directed_matrix, visited_order_bfs)
    print("\nAdjacency Matrix for BFS: ")
    for row in traversal_matrix_bfs:
        print(row)

    visited_order_dfs = dfs(directed_matrix, 0)
    traversal_matrix_dfs = traversal_matrix(directed_matrix, visited_order_dfs)
    print("\nAdjacency Matrix for DFS: ")
    for row in traversal_matrix_dfs:
        print(row)

    while True:
        if keyboard.is_pressed('b'):
            visualize_fs(visited_order_bfs, positions, True, "b")
        elif keyboard.is_pressed('d'):
            visualize_fs(visited_order_dfs, positions, True, "d")


main()
