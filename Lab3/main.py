import random
import turtle
import time
import math

SEED = 3223
NUM_VERTICES = 12
K = 0.695
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
    return directed_matrix

def make_undirected_matrix():
    directed_matrix = make_directed_matrix()
    undirected_matrix = [[0] * NUM_VERTICES for _ in range(NUM_VERTICES)]
    for i in range(NUM_VERTICES):
        for j in range(NUM_VERTICES):
            if directed_matrix[i][j] == 1:
                undirected_matrix[i][j] = 1
                undirected_matrix[j][i] = 1
    return undirected_matrix

def print_matrices():
    directed = make_directed_matrix()
    print("Directed Matrix:")
    for row in directed:
        print(row)

    undirected = make_undirected_matrix()
    print("\nUndirected Matrix:")
    for row in undirected:
        print(row)


print_matrices()


def draw_vertex(x, y, number):
    turtle.penup()
    turtle.goto(x, y - 20)
    turtle.pendown()
    turtle.begin_fill()
    turtle.color("orange")
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
        turtle.color("black")
        draw_bent_edge(x1, y1, x2, y2)

def draw_normal_edge(x1, y1, x2, y2):
    turtle.color("red")
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
            turtle.color("green")
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
        draw_vertex(x, y, i + 1)

    for i in range(NUM_VERTICES):
        for j in range(NUM_VERTICES):
            if matrix[i][j] == 1:
                draw_edge(positions[i][0], positions[i][1], positions[j][0], positions[j][1], i, j, directed)

def main():
    wn = turtle.Screen()
    wn.title("Graphs")
    wn.bgcolor("white")
    wn.setup(width=800, height=600)
    turtle.speed("fastest")

    directed_matrix = make_directed_matrix()
    undirected_matrix = make_undirected_matrix()

    draw_graph(directed_matrix, True)
    turtle.hideturtle()

    time.sleep(10)
    turtle.reset()
    turtle.speed("fastest")
    drawn_edges.clear()

    draw_graph(undirected_matrix, False)
    turtle.hideturtle()
    turtle.done()


main()
