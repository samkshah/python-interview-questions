
# Graph algorithm debugging
# Fix this code!


def path_search(start, end, graph):
    ''' Finds any valid path from a to b in the provided graph.
    Each node is identified by an integer.
    The graph is directed : a->b does not imply b->a.
    Args:
        - graph is provided as an adjacency list, where graph[x] is
          a list of integers representing all nodes accessible from x.
        - node_a and node_b are integers representing the start and end.
    Return:
        A list of nodes representing any path from node_a to node_b.
        The path does not have to be the shortest one.
        If no path exists, return None.
    '''
    if start == end:
        # Trivial path, return
        return [start]
    if graph[start] == []:
        # No neighbors = no path
        return None
    for neighbor_node in graph[start]:
        # Search neighbors recursively
        path = path_search(neighbor_node, end, graph)
        if path is not None:
          return [start] + path

GRAPH = {
    1: [2, 4],
    2: [5, 4, 1],
    3: [],
    4: [6, 3],
    5: [],
    6: [1, 3]
}

def verify(start, end, graph, path_exists):
    print(f'Testing the path from {start} to {end}: ', end='')
    try:
        result = path_search(start, end, graph)
        if path_exists:
            assert result is not None
            assert result[0] == start
            assert result[-1] == end
            for a, b in zip(result, result[1:]):
                # Iterate over all consecutive pairs
                # Super helpful Python trick using zip :)
                assert b in graph[a]
        else:
            assert result is None
    except:
        print('ERROR...')
        return False
    print('OK!')

verify(6, 5, GRAPH, True)
verify(1, 4, GRAPH, True)
verify(3, 2, GRAPH, False)
verify(2, 1, GRAPH, True)
verify(6, 3, GRAPH, True)
verify(5, 3, GRAPH, False)
verify(1, 3, GRAPH, True)