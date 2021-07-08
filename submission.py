import plotly.express as px
import random

# Do not modify the line below.
countries = ["Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Ecuador", "Falkland Islands", "Guyana", "Paraguay", "Peru", "Suriname", "Uruguay", "Venezuela"]

# Do not modify the line below.
colors = ["blue", "green", "red", "yellow"]


# Write your code here
# Do not modify the line below.
# Do not modify the line above.

def read_graph(filename):
    graph = {}

    last_added = None
    with open("countries.txt") as f:
        for line in f.readlines():
            # TODO(bora): There should not be directional edges. Check for that
            if line.startswith("-") and last_added != None:
                neighbor = line[2:-1]
                graph[last_added].append(neighbor)
            else:
                # TODO(bora): Don't randomly crop. Do it only when last char is a line break
                nodename = line[:-1]
                if nodename not in graph:
                    graph[nodename] = []
                    last_added = nodename

    return graph


def print_r(graph):
    print("graph(%d):" % len(graph))

    for node, edges in graph.items():
        print("  %s" % node)
        for neighbor in edges:
            print("   - %s" % neighbor)

    if len(graph) == 0:
        print("    NONE")


def detect_clusters(graph):
    clusters = []
    checklist = list(graph)

    while len(checklist) > 0:
        current_cluster = []
        next_visits = [random.choice(checklist)]

        while len(next_visits) > 0:
            node = next_visits.pop(0)
            current_cluster.append(node)
            if node in checklist:
                checklist.remove(node)

            for neigh in graph[node]:
                if neigh in checklist:
                    next_visits.append(neigh)

        clusters.append(current_cluster)

    return clusters


def paint_map(graph):
    colormap = {
        "Argentina"        : "white",
        "Bolivia"          : "white", 
        "Brazil"           : "white",
        "Chile"            : "white",
        "Colombia"         : "white",
        "Ecuador"          : "white",
        "Falkland Islands" : "white",
        "Guyana"           : "white",
        "Paraguay"         : "white",
        "Peru"             : "white",
        "Suriname"         : "white",
        "Uruguay"          : "white",
        "Venezuela"        : "white"}

    continents = detect_clusters(graph)

    # NOTE(bora): There could be more than one "continents" as graph 
    # can be disconnected. In that case more than one stating points needed.
    # This is list of process queues, each with a stack trace and a ban list.
    start_locations = [[(random.choice(continent), [])] for continent in continents]
    banlists = {c: [] for c in countries}

    def extract_keys(pending_list):
        return [x[0] for x in pending_list]

    for pending in start_locations:
        visited = []
        
        while pending:
            node, trace = pending.pop()

            available_colors = colors[:]
            for color in banlists[node]:
                if color in available_colors:
                    available_colors.remove(color)
            for neigh in graph[node]:
                if colormap[neigh] in available_colors:
                    available_colors.remove(colormap[neigh])

            if colormap[node] not in colors:
                if available_colors:
                    colormap[node] = random.choice(available_colors)
                    visited.append(node)

                    # NOTE(bora): If this is not the first pass, clearing banned colors
                    # is neccessary. Otherwise there will be no colors available for any
                    # of the nodes.
                    if trace:
                        pending.append((trace[-1], trace[0:-1]))
                        banlists[trace[-1]] = []

                    for neigh in graph[node]:
                        if neigh not in visited + trace + extract_keys(pending):
                            pending.append((neigh, trace[:]))
                else:
                    # NOTE(bora): If it backtracked past the root node, then it means
                    # something gone terribly wrong with the graph construction as we
                    # have an impossible to solve graph now..
                    assert visited

                    prev = visited[-1]
                    del visited[-1]

                    new_trace = trace[:] + [node]
                    banlists[prev] += [colormap[prev]]
                    colormap[prev] = "white"
                    pending.append((prev, new_trace))

    return colormap


def check_colored_map(graph, colormap, print_errors=True):
    clusters = detect_clusters(graph)
    reported_errors = []

    for network in clusters:
        for node in network:
            if colormap[node] not in colors:
                error = set((node,))
                if error not in reported_errors:
                    if print_errors:
                        print("[W] %s\n    is UNCOLORED" % (node))
                    reported_errors.append(error)
            else:
                for neigh in graph[node]:
                    if colormap[node] == colormap[neigh]:
                        error = set((node, neigh))
                        if error not in reported_errors:
                            if print_errors:
                                print("[W] %s and %s\n    are both %s" % (node, neigh, colormap[node]))
                            reported_errors.append(error)

    return (len(reported_errors) == 0)


# Do not modify this method, only call it with an appropriate argument.
# colormap should be a dictionary having countries as keys and colors as values.
def plot_choropleth(colormap):
    fig = px.choropleth(locationmode="country names",
                        locations=countries,
                        color=countries,
                        color_discrete_sequence=[colormap[k] for k in countries],
                        scope="south america")
    fig.show()


if __name__ == "__main__":

    colormap_test = {"Argentina": "blue", "Bolivia": "red", "Brazil": "yellow", "Chile": "yellow", "Colombia": "red",
                     "Ecuador": "yellow", "Falkland Islands": "yellow", "Guyana": "red", "Paraguay": "green",
                     "Peru": "green", "Suriname": "green", "Uruguay": "red", "Venezuela": "green"}

    graph = read_graph("text.txt")
    print_r(graph)
    
    print("\nMap is being painted.")
    colormap = paint_map(graph)

    if check_colored_map(graph, colormap):
        print("\nTest is complete. There are no errors\n")
    else:
        print("\nTest is FAILED. There are errors.\n")

    plot_choropleth(colormap=colormap)

# BIM309 dersi 3. odevidir.
# Bora Ozdogan
# END OF submission.py