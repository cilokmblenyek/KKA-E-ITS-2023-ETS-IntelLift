# Kelompok    : Bocil AI
# Kelas       : KKA E
# Dosen       : Bu Chastine
# Programmer  : Faa'iz Haikal Hilmi 
#             : Ahmad Fatih Ramadhani 
#             : Yoga Firman Syahputra 

class TreeNode:
    def __init__(self, floor, weight, heuristic):
        self.floor = floor
        self.w = weight
        self.heuristic = heuristic
        self.f = weight + heuristic
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)

# PRINT PATH
def print_path(path):
    for i in range(len(path)):
        if (i == len(path) - 1):
            print(path[i])
        else:
            print(path[i], end=" -> ")

# FIND PATH USING A STAR
def Astar(root_node):
    current_node = root_node
    list = []
    last_floor = None
    list.append(root_node)
    while (len(list) > 0):
        list.sort(key=lambda x: x.f)
        current_node = list.pop(0)
        if (current_node.heuristic == 0):
            last_floor = current_node.floor
            break
        for child in current_node.children:
            f = child.f
            if (f < initial_f[child.floor]):
                initial_f[child.floor] = f
                list.append(child)
                prev[child.floor] = current_node.floor

    path = []
    path.append(last_floor)
    while (last_floor != initial_floor):
        last_floor = prev[last_floor]
        path.append(last_floor)

    path.reverse()

    return path

# FIND PATH USING Iterative-Deepening A*
def IDAstar(root_node, heuristic):
    def DFS(node, bound, path):
        f = node.f

        if f > bound:
            return f, None
        if node.heuristic == 0:
            return "FOUND", path + [node.floor]

        min = float("inf")
        best_path = None

        for child in node.children:
            new_bound = child.f
            search_temporary, child_path = DFS(child, bound, path + [node.floor])
            if search_temporary == "FOUND":
                return "FOUND", child_path
            if search_temporary < min:
                min = search_temporary
                best_path = child_path
        return min, best_path

    f_bound = root_node.f
    path = []

    while True:
        search_temporary, path = DFS(root_node, f_bound, [])
        if search_temporary == "FOUND":
            return path
        if search_temporary == float("inf"):
            return None
        f_bound = search_temporary

# PERMUTATIONS OF FLOORS
def create_elevator_orders(arr):
    if len(arr) == 0:
        return [[]]
    elif len(arr) == 1:
        return [arr]

    result = []
    for i in range(len(arr)):
        first_elem = arr[i]
        rest = arr[:i] + arr[i+1:]

        # CHECK IF DESTINATION IS PICKED BEFORE SOURCE
        if first_elem in destination_to_source:
            source = destination_to_source[first_elem]
            if source in rest:
                continue

        for p in create_elevator_orders(rest):
            temp = [first_elem] + p
            result.append(temp)
    return result

def build_tree_from_paths(paths):
    # CREATE ROOT NODE
    root = TreeNode(initial_floor, 0 , total_people)

    for path in paths:
        current_node = root
        for value in path:
            child_node = None
            for child in current_node.children:
                if child.floor == value:
                    child_node = child
                    break
            if not child_node:
                w = abs(value - current_node.floor)         # WEIGHT

                # HEURISTIC
                h = current_node.heuristic
                if value in destination_to_source:
                    s = destination_to_source[value]
                    h -= source_with_people[s]

                child_node = TreeNode(value, w, h)
                current_node.add_child(child_node)
            current_node = child_node

    return root

if __name__ == "__main__":
    initial_floor = int(input("Masukkan lantai awal: "))        # ELEVATOR INITIAL FLOOR
    request = int(input("Masukkan banyaknya permintaan: "))     # CALLS / REQUESTS FOR ELEVATOR
    floors = []
    source_with_people = {}
    destination_to_source = {}
    total_people = 0
    initial_f = {}
    initial_f[initial_floor] = 0
    prev = {}
    prev[initial_floor] = initial_floor

    # INPUT
    for i in range(request):
        source_floor, target_floor, people = input("Masukkan lantai asal, lantai tujuan, dan jumlah orang: ").split()
        source_floor = int(source_floor)
        target_floor = int(target_floor)
        people = int(people)

        floors.extend([source_floor, target_floor])         # LIST OF FLOORS
        prev[source_floor] = source_floor
        prev[target_floor] = target_floor
        source_with_people[source_floor] = people           # SOURCE FLOOR WITH PEOPLE
        destination_to_source[target_floor] = source_floor  # DESTINATION FLOOR WITH SOURCE FLOOR
        initial_f[source_floor] = float('inf')
        initial_f[target_floor] = float('inf')
        total_people += people                              # TOTAL PEOPLE

    # CREATE VALID ELEVATOR ORDERS
    elevator_orders = create_elevator_orders(floors)

    # CLEAN UP
    del floors

    # BUILD TREE
    root_node = build_tree_from_paths(elevator_orders)

    # A STAR
    print("A* Algorithm...")
    print_path(Astar(root_node))

    # IDA STAR
    print("IDA* Algorithm...")
    print_path(IDAstar(root_node, total_people))