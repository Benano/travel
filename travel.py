# Imports
import matplotlib.pyplot as plt
import random
import copy


# Functions
def distance_between_cities(city1, city2):
    x = abs(city1[0] - city2[0])
    y = abs(city1[1] - city2[1])

    return x + y


def distance_travelled(path, cities):

    # Adding first city as last city
    total_distance = 0
    path = [0] + path + [0] # Start

    # Calculate whole path
    for n in range(len(cities)):
        current_city = cities[path[n]]
        next_city = cities[path[n+1]]
        dist = distance_between_cities(current_city, next_city)
        total_distance += dist

    return total_distance


def swap_mutation(path):
    new_path = copy.copy(path)
    pos = random.sample(list(range(1,len(path))), 2)
    pos0 = pos[0]
    pos1 = pos[1]
    new_path[pos0], new_path[pos1] = new_path[pos1], new_path[pos0]
    return new_path

def inversion_mutation(path): ##
    new_path = path.copy()
    i, j = sorted(random.sample(range(len(path)), 2))
    new_path[i:j+1] = reversed(new_path[i:j+1])
    return new_path

def create_new_path(num_cities):

    path = list(range(1,num_cities))
    random.shuffle(path)

    return path

def evolve(path, mutations):
    mutation = random.sample(mutations, 1)[0]
    new_path = mutation(path)

    return new_path

# Selecting File
file = 4 # 0-4

# Load the Cities
with open(f'cities{file}.txt', "r") as f:
    cities_raw = f.readlines()
cities = [list(map(int, line.split())) for line in cities_raw]
num_cities = len(cities)

# Create first path
parent_path = create_new_path(num_cities)
mutations = [swap_mutation, inversion_mutation]

# Evolution parameters
evo_steps = 1000

# Natural selection
performance = []
for step in range(evo_steps):

    # Parent performance
    parent_performance = distance_travelled(parent_path, cities)

    # Child path
    child_path = evolve(parent_path, mutations)

    # Child performance
    child_performance = distance_travelled(child_path , cities)

    # Battle to the death
    if child_performance <= parent_performance:
        parent_path = child_path

    # Record performance
    performance.append(min(child_performance, parent_performance))


# Plotting performance
plt.plot(performance)
plt.ylabel('Distance travelled [a.u]')
plt.xlabel('Evolution steps')
plt.title(f'Performance Cities {file}')
plt.show()

# Function to plot the path (ChatGPT FTW)
def plot_path(path, cities):
    # Starting city
    plt.scatter(cities[0][0], cities[0][1], c='r', marker='o', s=100, label='Start/End City')

    # Other cities
    for i in range(1, len(cities)):
        plt.scatter(cities[i][0], cities[i][1], c='b', marker='o', s=50)

    # Plot path
    for i in range(len(path) - 1):
        plt.plot([cities[path[i]][0], cities[path[i+1]][0]],
                 [cities[path[i]][1], cities[path[i+1]][1]], 'k-')

    # Connect end to start
    plt.plot([cities[path[-1]][0], cities[0][0]],
             [cities[path[-1]][1], cities[0][1]], 'k-')

    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title(f'Traveling Salesman Path for Cities {file}')
    plt.legend()
    plt.grid(True)
    plt.show()

# Add this to the end of your code
plot_path([0] + parent_path, cities)


