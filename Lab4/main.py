import random
import turtle
import math
import keyboard

SEED = 3223
NUM_VERTICES = 12
k1 = 0.65
k2 = 0.705
drawn_edges = set()

def generate_matrix():
    random.seed(SEED)
    matrix = [[random.random() * 2 for _ in range(NUM_VERTICES)] for _ in range(NUM_VERTICES)]
    return matrix

def apply_threshold(matrix, k):
    for i in range(NUM_VERTICES):
        for j in range(NUM_VERTICES):
            matrix[i][j] = 1 if matrix[i][j] * k >= 1 else 0
    return matrix

def make_directed_matrix(k, print_matrix):
    matrix = generate_matrix()
    directed_matrix = apply_threshold(matrix, k)
    if print_matrix:
        print("\nDirected Matrix:")
        for row in directed_matrix:
            print(row)
    return directed_matrix

def make_undirected_matrix(dir_matrix, print_matrix):
    undirected_matrix = [[0] * NUM_VERTICES for _ in range(NUM_VERTICES)]
    for i in range(NUM_VERTICES):
        for j in range(NUM_VERTICES):
            if dir_matrix[i][j] == 1:
                undirected_matrix[i][j] = 1
                undirected_matrix[j][i] = 1
    if print_matrix:
        print("\nUndirected Matrix:")
        for row in undirected_matrix:
            print(row)
    return undirected_matrix

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
    turtle.pendown()

def print_arrows():
    arrow_size = 10
    turtle.pendown()
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
            print_arrows()
            return

    drawn_edges.add((i, j))
    drawn_edges.add((j, i))

    turtle.penup()
    turtle.goto(x1, y1)
    if x1 == x2 == -225 or x1 == x2 == 225 or y1 == y2 == 225 or y1 == y2 == -225:
        if i == j:
            loop(x1, y1)
        else:
            diff_edge(x1, y1, x2, y2, i, j)
    else:
        draw_normal_edge(x1, y1, x2, y2)

    if directed:
        print_arrows()

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

def draw_graph(matrix, directed, num_vertices):
    positions = calculate_positions(num_vertices, 150)

    for i, (x, y) in enumerate(positions):
        draw_vertex(x, y, i + 1)

    for i in range(num_vertices):
        for j in range(num_vertices):
            if matrix[i][j] == 1:
                draw_edge(positions[i][0], positions[i][1], positions[j][0], positions[j][1], i, j, directed)

def calculate_vertex_degrees(matrix, directed=False):
    degrees = [sum(row) for row in matrix]
    if directed:
        for i in range(len(matrix)):
            degrees[i] += sum(row[i] for row in matrix)
    return degrees

def calculate_out_in_degrees(matrix):
    out_degrees = [sum(row) for row in matrix]
    in_degrees = [sum(row[i] for row in matrix) for i in range(len(matrix))]
    print("\nНапівстепені виходу вершин напрямленого графа:", out_degrees)
    print("Напівстепені заходу вершин напрямленого графа:", in_degrees)

def check_regular_graph(degrees):
    if all(deg == degrees[0] for deg in degrees):
        print("\nГраф регулярний зі степенню")
    else:
        print("\nГраф не регулярний")

def find_leaf_and_isolated_vertices(degrees):
    leaf_vertices = [i + 1 for i, deg in enumerate(degrees) if deg == 1]
    isolated_vertices = [i + 1 for i, deg in enumerate(degrees) if deg == 0]
    print("\nВисячі вершини:", leaf_vertices)
    print("Ізольовані вершини:", isolated_vertices)

    return leaf_vertices, isolated_vertices

def calculate_graph_parameters(k):
    directed_matrix = make_directed_matrix(k, False)
    undirected_matrix = make_undirected_matrix(directed_matrix, True)
    directed_degrees = calculate_vertex_degrees(directed_matrix, True)
    undirected_degrees = calculate_vertex_degrees(undirected_matrix)
    print("\nСтепені вершин напрямленого графа:", directed_degrees)
    print("Степені вершин ненапрямленого графа:", undirected_degrees)

    calculate_out_in_degrees(directed_matrix)

    check_regular_graph(directed_degrees)

    find_leaf_and_isolated_vertices(undirected_degrees)

def second_part_of_calc():

    print("\nМодифікована матриця:")
    modify_matrix = make_directed_matrix(k2, True)
    calculate_out_in_degrees(modify_matrix)
    calculate_paths(modify_matrix)

    print("\nМатриця досяжності:")
    for row in transitive_closure(modify_matrix):
        print(row)

    components = strong_components(modify_matrix)
    strong_components_matrix = strong_matrix(modify_matrix, components)
    print("\nКомпоненти сильної зв'язності:")
    for i, component in enumerate(components):
        print(f"Компонента {i + 1}: {component}")

    for row in strong_components_matrix:
        print(row)

def multiply_matrix(matrix1, matrix2):
    result = []
    for i in range(len(matrix1)):
        row = []
        for j in range(len(matrix2[0])):
            row.append(sum(matrix1[i][k] * matrix2[k][j] for k in range(len(matrix2))))
        result.append(row)
    return result

def calculate_paths(matrix):

    def route_points(matrix, row_num, col_num):
        points_list = []
        for i in range(len(matrix)):
            if matrix[i][col_num] and matrix[row_num][i]:
                points_list.append(i + 1)
        return points_list

    def find_third(matrix, end):
        third_list = []
        for k in range(len(matrix)):
            if matrix[k][end]:
                third_list.append(k + 1)
        return third_list

    squared_matrix = multiply_matrix(matrix, matrix)
    cubic_matrix = multiply_matrix(squared_matrix, matrix)

    paths = {}

    paths[2] = []
    for row in range(len(squared_matrix)):
        for col in range(len(squared_matrix)):
            if squared_matrix[row][col]:
                points_list = route_points(matrix, row, col)
                for point in points_list:
                    paths[2].append((row + 1, point, col + 1))

    paths[3] = []
    for row in range(len(cubic_matrix)):
        for col in range(len(cubic_matrix)):
            if cubic_matrix[row][col]:
                third_list = find_third(matrix, col)
                for third in third_list:
                    points_list = route_points(matrix, row, third - 1)
                    for point in points_list:
                        paths[3].append((row + 1, point, third, col + 1))

    print("\nRoutes of length 2:")
    print(paths[2])
    print(f"Number of routes of length 2: {len(paths[2])}\n")

    print("Routes of length 3:")
    print(paths[3])
    print(f"Number of routes of length 3: {len(paths[3])}\n")

    return paths

def transitive_closure(matrix):
    num_vertices = len(matrix)

    for k in range(num_vertices):
        for i in range(num_vertices):
            for j in range(num_vertices):
                if matrix[i][k] and matrix[k][j]:
                    matrix[i][j] = 1
    return matrix

def strong_components(matrix):
    num_vertices = len(matrix)

    reachability_matrix = transitive_closure(matrix)

    transpose_matrix = [[matrix[j][i] for j in range(num_vertices)] for i in range(num_vertices)]

    transpose_reachability_matrix = transitive_closure(transpose_matrix)

    components = []
    visited = [False] * num_vertices
    for i in range(num_vertices):
        if not visited[i]:
            component = []
            for j in range(num_vertices):
                if reachability_matrix[i][j] and transpose_reachability_matrix[j][i]:
                    visited[j] = True
                    component.append(j)
            components.append(component)
    return components

def strong_matrix(matrix, components):
    num_components = len(components)
    num_vertices = len(matrix)
    strong_components_matrix = [[0] * num_components for _ in range(num_components)]

    component_vertices = {}
    for i, component in enumerate(components):
        for vertex in component:
            component_vertices[vertex] = i

    for i in range(num_vertices):
        for j in range(num_vertices):
            if matrix[i][j]:
                if component_vertices[i] != component_vertices[j]:
                    strong_components_matrix[component_vertices[i]][component_vertices[j]] = 1

    return strong_components_matrix

def default_turtle():
    keyboard.wait('space')
    turtle.reset()
    turtle.speed(0)
    drawn_edges.clear()

def main():
    wn = turtle.Screen()
    wn.title("Graphs")
    wn.bgcolor("white")
    wn.setup(width=800, height=650)
    turtle.speed(0)

    directed_matrix = make_directed_matrix(k1, False)
    undirected_matrix = make_undirected_matrix(directed_matrix, False)
    modify_matrix = make_directed_matrix(k2, True)

    calculate_graph_parameters(k1)
    second_part_of_calc()

    draw_graph(directed_matrix, True, len(directed_matrix))

    default_turtle()
    draw_graph(undirected_matrix, False, len(undirected_matrix))

    default_turtle()
    draw_graph(modify_matrix, True, len(directed_matrix))

    default_turtle()
    components = strong_components(modify_matrix)
    strong_components_matrix = strong_matrix(modify_matrix, components)
    draw_vertex(0, 0, len(strong_components_matrix))

    turtle.hideturtle()
    turtle.done()


main()
