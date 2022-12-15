"""
All these algorithms are based on the paper: Two-player fair division of indivisible items: Comparison of algorithms
By: D. Marc Kilgour, Rudolf Vetschera

programmers: Itay Hasidi & Amichai Bitan
"""
from typing import List, Any, Dict
from fairpy.fairpy.agentlist import AgentList


def allocate(agents: AgentList, items: List[Any], allocations: List[Any], a_item = None, b_item = None):
    """
    Allocates the first ite, to agent A and the second item to agent B.
    :param agents A list that represent each of the players
    :param items A list of all existing items (U).
    :param allocations is the allocation for each player so far
    :param a_item the item that agent A gets
    :param b_item the item that agent B gets
    """
    if a_item:
        allocations[0].append(a_item)
        items.remove(a_item)
        agents[0].remove(a_item)
        agents[1].remove(a_item)
    if b_item:
        allocations[1].append(b_item)
        items.remove(b_item)
        agents[0].remove(b_item)
        agents[1].remove(b_item)
    return items, allocations


def H_M_l(agents: AgentList, items: List[Any] = None, level: int = 1):
    """
    Returns the items each player wants until level.
    """
    desired_items = []
    for player in agents:
        player_items = []
        for item in player:
            if item.value <= level and item.key in items:
                player_items.append(item.key)
        desired_items.append(player_items)
    return desired_items


def have_different_elements(items_A: List[Any], items_B: List[Any]):
    """
    Returns True if both lists different at at least one item.
    :param items_A the list of items of player A
    :param items_B the list of items of player B
    """
    if len(items_A) != len(items_B):
        return True
    for i in items_A:
        for j in items_B:
            if i != j:
                return True
    return False


def sequential(agents: AgentList, items: List[Any] = None) -> Dict:
    """
    a.k.a OS. The algorithm returns envy-free allocations if they exist, does not return max-min allocation
    and returns one Pareto optimality allocation.
    the algorithm receives:
    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param items A list of all existing items (U).

    # test 1 :
    >>> Alice = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'computer': 4, 'phone': 2, 'tv': 3, 'book': 1}, name = 'George')
    >>> print(sequential([Alice, George], ['computer', 'phone', 'tv', 'book']))
    {'a': ['computer', 'phone'], 'b': ['book', 'tv']}
    {'a': ['computer', 'tv'], 'b': ['book', 'phone']}

    # test 2 :
    # >>> h = {'a': {'computer': 1, 'phone': 3, 'tv': 2, 'book': 4}, 'b': {'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}}
    # >>> u = ['computer', 'phone', 'tv', 'book']
    # >>> z: dict = {'a': [], 'b': []}
    # # >>> print(sequential(u, z, h, to_sort=True))
    >>> Alice = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 3, 'tv': 2, 'book': 4}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'George')
    >>> print(sequential([Alice, George], ['computer', 'phone', 'tv', 'book']))
    {'a': ['computer', 'phone'], 'b': ['book', 'tv']}
    {'a': ['computer', 'book'], 'b': ['phone', 'tv']}
    {'a': ['tv', 'phone'], 'b': ['computer', 'book']}
    {'a': ['phone', 'book'], 'b': ['computer', 'tv']}
    """
    return recursive_sequential(agents, items, [])


def recursive_sequential(agents: AgentList, items: List[Any] = None, allocations: List[Any] = None, level: int = 1):
    """
    A recursive helper function to sequential()

    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param items A list of all existing items (U)
    :param allocations is the allocation for each player so far
    :param level is the depth level for item searching for each iteration
    """
    if not items:
        return allocations
    H_A_level, H_B_level = H_M_l(agents, items, level)
    if have_different_elements(H_A_level, H_B_level):
        for i in H_A_level:
            for j in H_B_level:
                if i != j:
                    items, allocations = allocate(allocations, i, j)
                    recursive_sequential(agents, items, allocations, level + 1)
    else:
        recursive_sequential(agents, items, allocations, level + 1)


def restricted_simple(agents: AgentList, items: List[Any] = None) -> Dict:
    """
    a.k.a RS. The algorithm does not return envy-free allocations, does not return max-min allocations
    and does not return one Pareto optimality allocations.
    the algorithm receives:
    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param items A list of all existing items (U).

    # test1:
    >>> Alice = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'computer': 4, 'phone': 2, 'tv': 3, 'book': 1}, name = 'George')
    >>> print(restricted_simple([Alice, George], ['computer', 'phone', 'tv', 'book']))
    {'a': ['computer', 'tv'], 'b': ['book', 'phone']}
    {'a': ['computer', 'phone'], 'b': ['book', 'tv']}

    # rest 2:
    # >>> h = {'a': {'computer': 1, 'phone': 3, 'tv': 2, 'book': 4}, 'b': {'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}}
    # >>> u = ['computer', 'phone', 'tv', 'book']
    # >>> z: dict = {'a': [], 'b': []}
    # >>> print(restricted_simple(u, z, h, to_sort=True))

    >>> Alice = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 3, 'tv': 2, 'book': 4}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'George')
    >>> print(restricted_simple([Alice, George], ['computer', 'phone', 'tv', 'book']))

    {'a': ['tv', 'phone'], 'b': ['computer', 'book']}
    {'a': ['phone', 'book'], 'b': ['computer', 'tv']}
    {'a': ['computer', 'phone'], 'b': ['book', 'tv']}
    {'a': ['computer', 'book'], 'b': ['phone', 'tv']}
    """
    return recursive_restricted_simple(agents, items, [])


def recursive_restricted_simple(agents: AgentList, items: List[Any] = None, allocations: List[Any] = None, level: int = 1):
    """
    A recursive helper function to restricted_simple()

    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param items A list of all existing items (U)
    :param allocations is the allocation for each player so far
    :param level is the depth level for item searching for each iteration
    """
    if not items:
        return allocations
    H_A_level, H_B_level = H_M_l(agents, items, level)
    if have_different_elements(H_A_level, H_B_level):
        if H_A_level[0] != H_B_level[0]:
            items, allocations = allocate(allocations, H_A_level[0], H_B_level[0])
            recursive_restricted_simple(agents, items, allocations, level + 1)
        else:
            if len(H_A_level) > 1:
                items, allocations = allocate(allocations, H_A_level[1], H_B_level[0])
                recursive_restricted_simple(agents, items, allocations, level + 1)
            if len(H_B_level) > 1:
                items, allocations = allocate(allocations, H_A_level[0], H_B_level[1])
                recursive_restricted_simple(agents, items, allocations, level + 1)
    else:
        recursive_restricted_simple(agents, items, allocations, level + 1)


def singles_doubles(agents: AgentList, items: List[Any] = None) -> Dict:
    """
    a.k.a SD. The algorithm returns envy-free allocations, returns max-min allocations
    and returns one Pareto optimality allocations.
    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param items A list of all existing items (U).

    # test 1:
    >>> Alice = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'computer': 4, 'phone': 2, 'tv': 3, 'book': 1}, name = 'George')
    >>> print(singles_doubles([Alice, George], ['computer', 'phone', 'tv', 'book']))
    {'a': ['computer', 'phone'], 'b': ['book', 'tv']}
    {'a': ['computer', 'tv'], 'b': ['book', 'phone']}
    # test 2:
    # >>> h = {'a': {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}, 'b': {'a': 2, 'b': 4, 'c': 1, 'd': 3, 'e': 6, 'f': 5}}
    # >>> u = ['a', 'b', 'c', 'd', 'e', 'f']
    # >>> z: dict = {'a': [], 'b': []}
    # >>> print(singles_doubles(u, z, h, to_sort=True))

    >>> Alice = fairpy.agents.AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'a': 2, 'b': 4, 'c': 1, 'd': 3, 'e': 6, 'f': 5}, name = 'George')
    >>> print(singles_doubles([Alice, George], ['a', 'b', 'c', 'd', 'e', 'f']))
    {'a': ['a', 'b', 'e], 'b': ['c', 'd', 'f']}

    # test 3:

    # >>> h = {'a': {'a': 1, 'b': 2, 'c': 3, 'd': 4}, 'b': {'a': 1, 'b': 2, 'c': 3, 'd': 4}}
    # >>> u = ['a', 'b', 'c', 'd']
    # >>> z: dict = {'a': [], 'b': []}
    # >>> print(singles_doubles(u, z, h, to_sort=True))
    >>> Alice = fairpy.agents.AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4}, name = 'George')
    >>> print(singles_doubles([Alice, George], ['a', 'b', 'c', 'd']))
    {'a': [], 'b': []}
    """
    pass


def iterated_singles_doubles(agents: AgentList, items: List[Any] = None) -> Dict:
    """
    a.k.a IS. The algorithm returns envy-free allocations, returns max-min allocations
    and returns one Pareto optimality allocations.
    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param items A list of all existing items (U).

    the algorithm receives:
        z_a - partial allocation for player a.
        z_b - partial allocation for player b.
        u - all un-allocated objects.
    # test 1:
    >>> Alice = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'computer': 4, 'phone': 2, 'tv': 3, 'book': 1}, name = 'George')
    >>> print(iterated_singles_doubles([Alice, George], ['computer', 'phone', 'tv', 'book']))
    {'a': ['computer', 'phone'], 'b': ['book', 'tv']}
    {'a': ['computer', 'tv'], 'b': ['book', 'phone']}

    # rest2 :
    # >>> h = {'a': {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}, 'b': {'a': 2, 'b': 4, 'c': 1, 'd': 3, 'e': 6, 'f': 5}}
    # >>> u = ['a', 'b', 'c', 'd', 'e', 'f']
    # >>> z: dict = {'a': [], 'b': []}
    # >>> print(iterated_singles_doubles(u, z, h, to_sort=True))
    >>> Alice = fairpy.agents.AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'a': 2, 'b': 4, 'c': 1, 'd': 3, 'e': 6, 'f': 5}, name = 'George')
    >>> print(iterated_singles_doubles([Alice, George], ['a', 'b', 'c', 'd', 'e', 'f']))
    {'a': ['a', 'b', 'e], 'b': ['c', 'd', 'f']}

    # test 3:
    # >>> h = {'a': {'a': 1, 'b': 2, 'c': 3, 'd': 4}, 'b': {'a': 1, 'b': 2, 'c': 3, 'd': 4}}
    # >>> u = ['a', 'b', 'c', 'd']
    # >>> z: dict = {'a': [], 'b': []}
    # >>> print(iterated_singles_doubles(u, z, h, to_sort=True))
     >>> Alice = fairpy.agents.AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4}, name = 'George')
    >>> print(iterated_singles_doubles([Alice, George], ['a', 'b', 'c', 'd']))
    {'a': [], 'b': []}
    """
    pass


def s1(agents: AgentList, items: List[Any] = None) -> Dict:
    """
    The algorithm returns envy-free allocations if they exist and returns max-min allocations.
    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param items A list of all existing items (U).

    # test1:
    >>> Alice = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'computer': 4, 'phone': 2, 'tv': 3, 'book': 1}, name = 'George')
    >>> print(s1([Alice, George], ['computer', 'phone', 'tv', 'book']))
    {'a': ['computer', 'phone'], 'b': ['book', 'tv']}
    {'a': ['computer', 'tv'], 'b': ['book', 'phone']}

    # test2:

    # >>> h = {'a': {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}, 'b': {'a': 2, 'b': 4, 'c': 1, 'd': 3, 'e': 6, 'f': 5}}
    # >>> u = ['a', 'b', 'c', 'd', 'e', 'f']
    # >>> z: dict = {'a': [], 'b': []}
    # >>> print(s1(u, z, h, to_sort=True))
    >>> Alice = fairpy.agents.AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'a': 2, 'b': 4, 'c': 1, 'd': 3, 'e': 6, 'f': 5}, name = 'George')
    >>> print(s1([Alice, George], ['a', 'b', 'c', 'd', 'e', 'f']))
    {'a': ['a', 'b', 'e], 'b': ['c', 'd', 'f']}

    # test 3:

    # >>> h = {'a': {'a': 1, 'b': 2, 'c': 3, 'd': 4}, 'b': {'a': 1, 'b': 2, 'c': 3, 'd': 4}}
    # >>> u = ['a', 'b', 'c', 'd']
    # >>> z: dict = {'a': [], 'b': []}
    # >>> print(s1(u, z, h, to_sort=True)
    >>> Alice = fairpy.agents.AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4}, name = 'George')
    >>> print(s1([Alice, George], ['a', 'b', 'c', 'd']))
    {'a': ['b', 'd'], 'b': ['a', 'c']}
    """
    pass


def l1(agents: AgentList, items: List[Any] = None) -> Dict:
    """
    The algorithm returns envy-free allocations if they exist and returns max-min allocations.
    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param items A list of all existing items (U).

    # test1:
    >>> Alice = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'computer': 4, 'phone': 2, 'tv': 3, 'book': 1}, name = 'George')
    >>> print(l1([Alice, George], ['computer', 'phone', 'tv', 'book']))
    {'a': ['computer', 'phone'], 'b': ['book', 'tv']}
    {'a': ['computer', 'tv'], 'b': ['book', 'phone']}

    # test2:
    # >>> h = {'a': {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}, 'b': {'a': 2, 'b': 4, 'c': 1, 'd': 3, 'e': 6, 'f': 5}}
    # >>> u = ['a', 'b', 'c', 'd', 'e', 'f']
    # >>> z: dict = {'a': [], 'b': []}
    # >>> print(l1(u, z, h, to_sort=True))
    >>> Alice = fairpy.agents.AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'a': 2, 'b': 4, 'c': 1, 'd': 3, 'e': 6, 'f': 5}, name = 'George')
    >>> print(l1([Alice, George], ['a', 'b', 'c', 'd', 'e', 'f']))
    {'a': ['a', 'b', 'e], 'b': ['c', 'd', 'f']}

    # test3:
    # >>> h = {'a': {'a': 1, 'b': 2, 'c': 3, 'd': 4}, 'b': {'a': 1, 'b': 2, 'c': 3, 'd': 4}}
    # >>> u = ['a', 'b', 'c', 'd']
    # >>> z: dict = {'a': [], 'b': []}
    # >>> print(l1(u, z, h, to_sort=True))
    >>> Alice = fairpy.agents.AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4}, name = 'George')
    >>> print(l1([Alice, George], ['a', 'b', 'c', 'd']))
    {'a': ['b', 'd'], 'b': ['a', 'c']}
    """
    pass


def top_down(agents: AgentList, items: List[Any] = None) -> Dict:
    """
    a.k.a TD. The algorithm does not return envy-free allocations and returns max-min allocations.
    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param items A list of all existing items (U).

    # test1:
    >>> Alice = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'computer': 4, 'phone': 2, 'tv': 3, 'book': 1}, name = 'George')
    >>> print(top_down([Alice, George], ['computer', 'phone', 'tv', 'book']))
    {'a': ['computer', 'phone'], 'b': ['book', 'tv']}

    # test2:
    # >>> h = {'a': {'computer': 1, 'phone': 3, 'tv': 2, 'book': 4}, 'b': {'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}}
    # >>> u = ['computer', 'phone', 'tv', 'book']
    # >>> z: dict = {'a': [], 'b': []}
    # >>> print(top_down(u, z, h, to_sort=True))
    >>> Alice = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 3, 'tv': 2, 'book': 4}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'George')
    >>> print(top_down([Alice, George], ['computer', 'phone', 'tv', 'book']))
    {'a': ['computer', 'tv'], 'b': ['phone', 'book']}
    """
    return top_down_helper(agents, items, [])


def top_down_helper(agents: AgentList, items: List[Any] = None, allocations: List[Any] = None):
    """
    A helper function to top_down()

    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param items A list of all existing items (U)
    :param allocations is the allocation for each player so far
    """
    for _ in range(len(items) / 2):
        items, allocations = allocate(agents, items, allocations, a_item=agents[0][0])
        items, allocations = allocate(agents, items, allocations, b_item=agents[1][0])
    return allocations


def top_down_alternating(agents: AgentList, items: List[Any] = None) -> Dict:
    """
    a.k.a TA. The algorithm does not return envy-free allocations and returns max-min allocations.
    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param items A list of all existing items (U).

    # test1:
    >>> Alice = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'computer': 4, 'phone': 2, 'tv': 3, 'book': 1}, name = 'George')
    >>> print(top_down_alternating([Alice, George], ['computer', 'phone', 'tv', 'book']))
    {'a': ['computer', 'book'], 'b': ['phone', 'tv']}

    # test2:

    # >>> h = {'a': {'computer': 1, 'phone': 3, 'tv': 2, 'book': 4}, 'b': {'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}}
    # >>> u = ['computer', 'phone', 'tv', 'book']
    # >>> z: dict = {'a': [], 'b': []}
    # >>> print(top_down_alternating(u, z, h, to_sort=True))
    >>> Alice = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 3, 'tv': 2, 'book': 4}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'George')
    >>> print(top_down([Alice, George], ['computer', 'phone', 'tv', 'book']))
    {'a': ['computer', 'book'], 'b': ['phone', 'tv']}
    """
    return top_down_alternating_helper(agents, items, [])


def top_down_alternating_helper(agents: AgentList, items: List[Any] = None, allocations: List[Any] = None):
    """
    A helper function to top_down_alternating()

    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param items A list of all existing items (U)
    :param allocations is the allocation for each player so far
    """
    flag = True
    for _ in range(len(items) / 2):
        if flag:
            items, allocations = allocate(agents, items, allocations, a_item=agents[0][0])
            items, allocations = allocate(agents, items, allocations, b_item=agents[1][0])
            flag = False
        elif not flag:
            items, allocations = allocate(agents, items, allocations, b_item=agents[1][0])
            items, allocations = allocate(agents, items, allocations, a_item=agents[0][0])
            flag = True
    return allocations


def bottom_up(agents: AgentList, items: List[Any] = None) -> Dict:
    """
    a.k.a BU. The algorithm does not return envy-free allocations and does not return max-min allocations.
    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param items A list of all existing items (U).

    # test1:
    >>> Alice = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'computer': 4, 'phone': 2, 'tv': 3, 'book': 1}, name = 'George')
    >>> print(bottom_up([Alice, George], ['computer', 'phone', 'tv', 'book']))
    {'a': ['computer', 'phone'], 'b': ['book', 'tv']}

    # test2:
    # >>> h = {'a': {'computer': 1, 'phone': 3, 'tv': 2, 'book': 4}, 'b': {'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}}
    # >>> u = ['computer', 'phone', 'tv', 'book']
    # >>> z: dict = {'a': [], 'b': []}
    # >>> print(bottom_up(u, z, h, to_sort=True))
    >>> Alice = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 3, 'tv': 2, 'book': 4}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'George')
    >>> print(top_down([Alice, George], ['computer', 'phone', 'tv', 'book']))
    {'a': ['tv', 'computer'], 'b': ['phone', 'tv']}
    """
    return bottom_up_helper(agents, items, [])


def bottom_up_helper(agents: AgentList, items: List[Any] = None, allocations: List[Any] = None):
    """
    A helper function to bottom_up()

    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param items A list of all existing items (U)
    :param allocations is the allocation for each player so far
    """
    for _ in range(len(items) / 2):
        items, allocations = allocate(agents, items, allocations, a_item=agents[1][len(items) - 1])
        items, allocations = allocate(agents, items, allocations, b_item=agents[0][len(items) - 1])
    return allocations


def bottom_up_alternating(agents: AgentList, items: List[Any] = None) -> Dict:
    """
    a.k.a BA. The algorithm does not return envy-free allocations and does not return max-min allocations.
    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param items A list of all existing items (U).

    # test1:
    >>> Alice = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'computer': 4, 'phone': 2, 'tv': 3, 'book': 1}, name = 'George')
    >>> print(bottom_up_alternating([Alice, George], ['computer', 'phone', 'tv', 'book']))
    {'a': ['computer', 'tv'], 'b': ['book', 'phone']}

    # test 2:
    # >>> h = {'a': {'computer': 1, 'phone': 3, 'tv': 2, 'book': 4}, 'b': {'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}}
    # >>> u = ['computer', 'phone', 'tv', 'book']
    # >>> z: dict = {'a': [], 'b': []}
    # >>> print(bottom_up_alternating(u, z, h, to_sort=True))
    >>> Alice = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 3, 'tv': 2, 'book': 4}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'George')
    >>> print(top_down([Alice, George], ['computer', 'phone', 'tv', 'book']))
    {'a': ['tv', 'phone'], 'b': ['book', 'computer']}
    """
    return bottom_up_alternating_helper(agents, items, [])


def bottom_up_alternating_helper(agents: AgentList, items: List[Any] = None, allocations: List[Any] = None):
    """
    A helper function to bottom_up_alternating()

    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param items A list of all existing items (U)
    :param allocations is the allocation for each player so far
    """
    flag = True
    for _ in range(len(items) / 2):
        if flag:
            items, allocations = allocate(agents, items, allocations, a_item=agents[1][len(items) - 1])
            items, allocations = allocate(agents, items, allocations, b_item=agents[0][len(items) - 1])
            flag = False
        elif not flag:
            items, allocations = allocate(agents, items, allocations, b_item=agents[0][len(items) - 1])
            items, allocations = allocate(agents, items, allocations, a_item=agents[1][len(items) - 1])
            flag = True
    return allocations


def trump(agents: AgentList, items: List[Any] = None) -> Dict:
    """
    a.k.a TR. The algorithm returns envy-free allocations, does not return max-min allocations
    and returns one Pareto optimality allocations.
    the algorithm receives:
    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param items A list of all existing items (U).

    # test1:
    >>> Alice = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'computer': 4, 'phone': 2, 'tv': 3, 'book': 1}, name = 'George')
    >>> print(trump([Alice, George], ['computer', 'phone', 'tv', 'book']))
    {'a': ['computer', 'tv'], 'b': ['book', 'phone']}

    # test2:
    # >>> h = {'a': {'computer': 1, 'phone': 3, 'tv': 2, 'book': 4}, 'b': {'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}}
    # >>> u = ['computer', 'phone', 'tv', 'book']
    # >>> z: dict = {'a': [], 'b': []}
    # >>> print(trump(u, z, h, to_sort=True))
    >>> Alice = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 3, 'tv': 2, 'book': 4}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'George')
    >>> print(top_down([Alice, George], ['computer', 'phone', 'tv', 'book']))
    {'a': [], 'b': []}
    """
    pass
