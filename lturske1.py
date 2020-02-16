import sys
import copy


def forward_checking(planar_map, coloring):
    """
    This will do forward checking to make sure you can make the particular move
    :param planar_map: the planar map
    :param coloring: The currenct coloring
    :return:
    """
    edges = planar_map["edges"]
    for start, end in edges:
        if end > len(coloring)-1:
            continue
        if coloring[start][1] is coloring[end][1]:
            return False
    return True


def backtracking(nodes, coloring, planar_map, colors, trace):
    """
    This is a recursive function that will go through depth first trying to find the perfect map coloring
    :param nodes: nodes left to assign
    :param coloring: the current coloring
    :param planar_map: the planar map
    :param colors: all of the colors
    :param trace: debug
    :return: boolean
    """
    # Base Case, if you have no more nodes to assign, you are done
    if len(nodes) is 0:
        if trace:
            print("Found Answer")
        # Set the gloabl answer and return
        global answer
        answer = coloring
        return True
    # Pop the next node off the nodes stack
    node = nodes.pop(0)
    if trace:
        print("Popping node off: " + str(node))
    # Copy all the colors so far so you dont overwrite something
    coloring_copy = copy.deepcopy(coloring)
    # Test all the options
    for color in colors:
        if trace:
            print("Trying: " + color + "for node: " + str(node))
        # Add color to colors so far
        coloring_copy.append((node, color))
        # Do some forward checking and if you pass the forward check then you continue down the tree backtracking
        # If you get to the end return
        if forward_checking(planar_map, coloring_copy) and backtracking(nodes, coloring_copy, planar_map, colors, trace):
            return True
        else:
            if trace:
                print("Could not find proper path for node color: " + color)
            # If you failed forward checking or the path you followed was wrong, try the next color
            coloring_copy = coloring_copy[:-1]
    # If none of the color options worked, go back up the tree by adding the node back to the stack and return false
    if trace:
        print("Could not find color path for node, returning: " + str(node))
    nodes.insert(0, node)
    return False


def get_minimum_values_node(nodes):
    """
    Gets the next node in the nodes array that has the least amount of values
    :param nodes: the nodes array
    :return: the smallest node
    """
    smallest = None
    # Only look for a node that has not been assigned
    for n in nodes:
        if n[4] is None:
            smallest = n
            break
    # Look for the least amount of values in the nodes that have not been assigned
    for n in nodes:
        if len(n[3]) < len(smallest[3]) and n[4] is None:
            smallest = n
    return smallest


def minimum_remaining_answer_format(coloring):
    """
    This will reverse the list because it is in backwards order usually.
    :param coloring: the coloring
    :return: nothing
    """
    lst = len(coloring)
    for i in range(0, lst):
        for j in range(0, lst-i-1):
            if coloring[j][0] > coloring[j+1][0]:
                temp = coloring[j]
                coloring[j] = coloring[j +1]
                coloring[j+1] = temp
    for n in coloring:
        coloring[n[0]] = (n[1], n[2])


def prune(nodes, edges, color):
    """
    Prune the nodes graph, the edges of the colors
    :param nodes: the nodes
    :param edges: the edges that need to be pruned
    :param color: the color that needs to be pruned
    :return:
    """
    # Make sure you can even color the node
    for edge in edges:
        start = edge[0]
        end = edge[1]
        if nodes[start][4] is nodes[end][4]:
            return False

    # For the edges that need to be updated
    for edge in edges:
        start = edge[0]
        end = edge[1]
        # Get the colors of the starting node
        colors = nodes[start][3]
        # Reset the colors on the starting node
        nodes[start] = (nodes[start][0], nodes[start][1], nodes[start][2], [] , nodes[start][4])
        # For each of the colors in the start node, add all the colors back except the color you just added
        if color in colors:
            temp = colors
            for n in temp:
                if n is color:
                    continue
                nodes[start] = (nodes[start][0], nodes[start][1], nodes[start][2], nodes[start][3] + [n], nodes[start][4])
        # Get the colors from the end node
        colors = nodes[end][3]
        # Reset the colors of the end node
        nodes[end] = (nodes[end][0], nodes[end][1], nodes[end][2], [], nodes[end][4])
        # For each of the colors add them back to the node without the color you just added
        if color in colors:
            temp = colors
            for n in temp:
                if n is color:
                    continue
                nodes[end] = (nodes[end][0], nodes[end][1], nodes[end][2], nodes[end][3] + [n], nodes[end][4])
    return True


def unprune(nodes, edges, color):
    """
    Reset the graph to how you were before with the edges
    :param nodes:
    :param edges:
    :param color:
    :return:
    """
    for edge in edges:
        start = edge[0]
        end = edge[1]
        if color not in nodes[start][3]:
            nodes[start] = (nodes[start][0], nodes[start][1], nodes[start][2], nodes[start][3] + [color], None)
        if color not in nodes[end][3] and nodes[end][4] :
            nodes[end] = (nodes[end][0], nodes[end][1], nodes[end][2], nodes[end][3] + [color], nodes[end][4])


def build_minimum_value_structure(planar_map, colors):
    """
    This will build a structuire for the minimum value algorithm to use
    :param planar_map: the planar map
    :param colors: the colors
    :return: [(index, name, values, colors, assigned color)]
    """
    nodes = copy.deepcopy(planar_map).get('nodes')
    edges = copy.deepcopy(planar_map).get('edges')
    data = []
    i = -1
    for node in nodes:
        i += 1
        data.append((i, node, []))
    for edge in edges:
        temp = data[edge[0]][2]
        temp2 = data[edge[1]][2]
        temp.append(edge)
        temp2.append(edge)
        data[edge[0]] = (data[edge[0]][0], data[edge[0]][1], temp)
        data[edge[1]] = (data[edge[1]][0], data[edge[1]][1], temp2)
    for d in range(len(data)):
        data[d] = (data[d][0], data[d][1], data[d][2], colors, None)
    return data


def minimum_value_remaining(nodes, coloring):
    """
    This is the minimum values remaining algorithm
    :param nodes: the nodes to assign
    :param coloring: the current coloring
    :return: boolean
    """
    # Base case, if all the nodes have been assigned you are done
    if len(coloring) is len(nodes):
        global answer
        minimum_remaining_answer_format(coloring)
        answer = coloring
        return True
    # Get the node with the smallest number of values left
    node = get_minimum_values_node(nodes)
    # Get a copy of the color so far
    coloring_copy = copy.deepcopy(coloring)
    # For each color that you have left in your values
    for color in node[3]:
        # Add the color combination to the coloring
        coloring_copy.append((node[0], node[1], color))
        # Assign the node the color
        nodes[node[0]] = (node[0], node[1], node[2], node[3], color)
        # Prune the graph after the color assignment and if you are able to, keep going on the algorithm
        if prune(nodes, node[2], color) and minimum_value_remaining(nodes, coloring_copy):
            return True
        else:
            # If you went the wrong way, unprune what you have done
            unprune(nodes, node[2], color)
            coloring_copy = coloring_copy[:-1]
    return False


global answer


def color_map( planar_map, colors, trace=False):
    """
    This function takes the planar_map and tries to assign colors to it.

    planar_map: Dict with keys "nodes", "edges", and "coordinates". "nodes" is a List of node names, "edges"
    is a List of Tuples. Each tuple is a pair of indices into "nodes" that describes an edge between those
    nodes. "coorinates" are x,y coordinates for drawing.

    colors: a List of color names such as ["yellow", "blue", "green"] or ["orange", "red", "yellow", "green"]
    these should be color names recognized by Matplotlib.

    If a coloring cannot be found, the function returns None. Otherwise, it returns an ordered list of Tuples,
    (node name, color name), with the same order as "nodes".
    """
    # This will set up the minimum value structure portion of the assignment
    #data = build_minimum_value_structure(planar_map, colors)
    #coloring = []
    #minimum_value_remaining(data, coloring)
    nodes = copy.deepcopy(planar_map).get('nodes')
    coloring = []
    backtracking(nodes, coloring, planar_map, colors, trace)
    global answer

    return answer


connecticut = {"nodes": ["Fairfield", "Litchfield", "New Haven", "Hartford", "Middlesex", "Tolland", "New London", "Windham"],
               "edges": [(0,1), (0,2), (1,2), (1,3), (2,3), (2,4), (3,4), (3,5), (3,6), (4,6), (5,6), (5,7), (6,7)],
               "coordinates": [( 46, 52), ( 65,142), (104, 77), (123,142), (147, 85), (162,140), (197, 94), (217,146)]}

europe = {
    "nodes":  ["Iceland", "Ireland", "United Kingdom", "Portugal", "Spain",
                 "France", "Belgium", "Netherlands", "Luxembourg", "Germany",
                 "Denmark", "Norway", "Sweden", "Finland", "Estonia",
                 "Latvia", "Lithuania", "Poland", "Czech Republic", "Austria",
                 "Liechtenstein", "Switzerland", "Italy", "Malta", "Greece",
                 "Albania", "Macedonia", "Kosovo", "Montenegro", "Bosnia Herzegovina",
                 "Serbia", "Croatia", "Slovenia", "Hungary", "Slovakia",
                 "Belarus", "Ukraine", "Moldova", "Romania", "Bulgaria",
                 "Cyprus", "Turkey", "Georgia", "Armenia", "Azerbaijan",
                 "Russia" ],
    "edges": [(0,1), (0,2), (1,2), (2,5), (2,6), (2,7), (2,11), (3,4),
                 (4,5), (4,22), (5,6), (5,8), (5,9), (5,21), (5,22),(6,7),
                 (6,8), (6,9), (7,9), (8,9), (9,10), (9,12), (9,17), (9,18),
                 (9,19), (9,21), (10,11), (10,12), (10,17), (11,12), (11,13), (11,45),
                 (12,13), (12,14), (12,15), (12,17), (13,14), (13,45), (14,15),
                 (14,45), (15,16), (15,35), (15,45), (16,17), (16,35), (17,18),
                 (17,34), (17,35), (17,36), (18,19), (18,34), (19,20), (19,21),
                 (19,22), (19,32), (19,33), (19,34), (20,21), (21,22), (22,23),
                 (22,24), (22,25), (22,28), (22,29), (22,31), (22,32), (24,25),
                 (24,26), (24,39), (24,40), (24,41), (25,26), (25,27), (25,28),
                 (26,27), (26,30), (26,39), (27,28), (27,30), (28,29), (28,30),
                 (29,30), (29,31), (30,31), (30,33), (30,38), (30,39), (31,32),
                 (31,33), (32,33), (33,34), (33,36), (33,38), (34,36), (35,36),
                 (35,45), (36,37), (36,38), (36,45), (37,38), (38,39), (39,41),
                 (40,41), (41,42), (41,43), (41,44), (42,43), (42,44), (42,45),
                 (43,44), (44,45)],
    "coordinates": [( 18,147), ( 48, 83), ( 64, 90), ( 47, 28), ( 63, 34),
                   ( 78, 55), ( 82, 74), ( 84, 80), ( 82, 69), (100, 78),
                   ( 94, 97), (110,162), (116,144), (143,149), (140,111),
                   (137,102), (136, 95), (122, 78), (110, 67), (112, 60),
                   ( 98, 59), ( 93, 55), (102, 35), (108, 14), (130, 22),
                   (125, 32), (128, 37), (127, 40), (122, 42), (118, 47),
                   (127, 48), (116, 53), (111, 54), (122, 57), (124, 65),
                   (146, 87), (158, 65), (148, 57), (138, 54), (137, 41),
                   (160, 13), (168, 29), (189, 39), (194, 32), (202, 33),
                   (191,118)]}


COLOR = 1

def test_coloring(planar_map, coloring):
    edges = planar_map["edges"]
    nodes = planar_map[ "nodes"]

    for start, end in edges:
        try:
            assert coloring[ start][COLOR] != coloring[ end][COLOR]
        except AssertionError:
            print("%s and %s are adjacent but have the same color." % (nodes[ start], nodes[ end]))

def assign_and_test_coloring(name, planar_map, colors, trace=False):
    print(f"Trying to assign {len(colors)} colors to {name}")
    coloring = color_map(planar_map, colors, trace=trace)
    if coloring:
        print(f"{len(colors)} colors assigned to {name}.")
        test_coloring(planar_map, coloring)
    else:
        print(f"{name} cannot be colored with {len(colors)} colors.")


if __name__ == "__main__":
    debug = len(sys.argv) > 1 and sys.argv[1].lower() == 'debug'

    # Edit these to indicate what you implemented.
    print("Backtracking...", "yes")
    print("Forward Checking...", "yes")
    print("Minimum Remaining Values...", "yes")
    print("Degree Heuristic...", "no")
    print("Least Constraining Values...", "no")
    print("")

    three_colors = ["red", "blue", "green"]
    four_colors = ["red", "blue", "green", "yellow"]

    # Easy Map
    assign_and_test_coloring("Connecticut", connecticut, four_colors, trace=debug)
    assign_and_test_coloring("Connecticut", connecticut, three_colors, trace=debug)
    # Difficult Map
    assign_and_test_coloring("Europe", europe, four_colors, trace=debug)
    assign_and_test_coloring("Europe", europe, three_colors, trace=debug)