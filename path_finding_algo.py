from queue import PriorityQueue, Queue



class Grid:
    def neighbours(self,current):
        pass

    def cost(self, current, next):
        pass

    def distance(self,next, target):
        pass 

def reconstruct_path(came_from:dict, start, target):
    current = came_from[target]
    path = list()
    path.append(target)
    while current != None:
        path.append(current)

    path.reverse()
    return path
"""
key point:
1.use queue to store to-be-searched nodes
2.implement grid's neighbour() for getting next step nodes
3.use came_from[to_node] = from_node dict to store path
4.after searching done, use reconstruct_path() to restore path
"""
def BFS(grids:Grid, start, target):
    queue = Queue()
    queue.put(start)
    came_from = dict()
    came_from[start] = None

    while not queue.empty():
        current = queue.get()
        if current == target:
            break

        for next in grids.neighbours(current): # type: ignore
            if next not in came_from:
                queue.put(next)
                came_from[next] = current
    
    return reconstruct_path(came_from,start, target)

"""
key point: based on BFS, what's more on Dijkstra's Searching
1.use PriorityQueue which prioritize low cost node to store to-be-searched nodes
2.use cost_so_far[node] = cost to store current lowest cost of node. note that a node may be visited multiple times
"""
def Dijkstra(grids:Grid, came_from:dict, start, target):
    pqueue = PriorityQueue()
    pqueue.put(start)
    came_from = dict()
    came_from[start] = None
    cost_so_far = dict()
    cost_so_far[start] = 0

    while not pqueue.empty():
        current = pqueue.get()
        if current == target:
            break
        
        current_cost = cost_so_far[current]
        for next in grids.neighbours(current): # type: ignore
            # a node might be visited multiples, consider node that is never visited or 
            # node with lower cost only
            new_cost = current_cost + grids.cost(current, next)
            if next not in cost_so_far or new_cost < grids.cost(next): # type: ignore
                cost_so_far[next] = new_cost
                came_from[next] = current
                pqueue.put(next,new_cost)

"""
based on BFS,key difference from Dijkstra's Searching
1.use distance to target as sorting priority of Priority Queue, which determine that we always favour the closest point
2.cost_so_far dict is no need  
"""
def GreedyFirstSearch(grids:Grid, came_from:dict, start, target):
    pqueue = PriorityQueue()
    pqueue.put(start)
    came_from = dict()
    came_from[start] = None


    while not pqueue.empty():
        current = pqueue.get()
        if current == target:
            break
        
        for next in grids.neighbours(current): # type: ignore
            if next not in came_from: # type: ignore
                priority = grids.distance(next, target)
                came_from[next] = current
                pqueue.put(next,priority) # type: ignore

"""
A *: combine GreedyFirstSearch and Dijkstra's Searching
"""

def AStar(grids:Grid, came_from:dict, start, target):
    pqueue = PriorityQueue()
    pqueue.put(start)
    came_from = dict()
    came_from[start] = None
    cost_so_far = dict()
    cost_so_far[start] = 0

    while not pqueue.empty():
        current = pqueue.get()
        if current == target:
            break
        
        current_cost = cost_so_far[current]
        for next in grids.neighbours(current): # type: ignore
            # a node might be visited multiples, consider node that is never visited or 
            # node with lower cost only
            new_cost = current_cost + grids.cost(current, next)
            if next not in cost_so_far or new_cost < grids.cost(next): # type: ignore
                distance = grids.distance(next, target)
                priority = distance + new_cost
                cost_so_far[next] = new_cost
                came_from[next] = current
                pqueue.put(next,priority) # type: ignore