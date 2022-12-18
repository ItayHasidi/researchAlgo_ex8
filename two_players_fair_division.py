"""
All these algorithms are based on the paper: Two-player fair division of indivisible items: Comparison of algorithms
By: D. Marc Kilgour, Rudolf Vetschera

programmers: Itay Hasidi & Amichai Bitan
"""
from typing import List, Any, Dict

from fairpy import fairpy
from fairpy.fairpy.agentlist import AgentList


def find_last_item(agent, items, item_list):
    min_score = -1
    min_item = ""
    for item in item_list:
        score = agent.value(item)
        if min_score > score or min_score < 0:
            min_score = score
            min_item = item
    return min_item


def is_envy_free_partial_allocation(agents: AgentList, allocations: List[Any]):
    A_sum = 0
    B_sum = 0
    for idx in range(len(allocations[0])):
        A_sum += agents[0].value(allocations[0][idx])
        B_sum += agents[1].value(allocations[1][idx])
    if A_sum == B_sum:
        return True
    return False


def deep_copy_2d_list(lst: list):
    """
    Deep copies a 2D list and returns it
    """
    lst_copy = []
    for i in range(len(lst)):
        lst_temp = []
        for j in range(len(lst[0])):
            lst_temp.append(lst[i][j])
        lst_copy.append(lst_temp)
    return lst_copy


def allocate(agents: AgentList, items: List[Any], allocations: List[Any] = None, a_item=None, b_item=None):
    """
    Allocates the first ite, to agent A and the second item to agent B.
    :param agents A list that represent each of the players
    :param items A list of all existing items (U).
    :param allocations is the allocation for each player so far
    :param a_item the item that agent A gets
    :param b_item the item that agent B gets
    """
    # if a_item is not None:
    # if allocations[0]:
    #     allocations[0] = [a_item]
    # else:
    if a_item:
        allocations[0].append(a_item)
        items.remove(a_item)
    # agents[0].remove(agents[0].value(a_item))
    # agents[1].remove(agents[1].value(a_item))
    # if b_item is not None:
    # if allocations[1]:
    #     allocations[1] = [b_item]
    # else:
    if b_item:
        allocations[1].append(b_item)
        items.remove(b_item)
    # agents[0].remove(b_item)
    # agents[1].remove(b_item)
    return items, allocations


def H_M_l(agents: AgentList, items: List[Any] = None, level: int = 1):
    """
    Returns the items each player wants until level.
    """
    desired_items = []
    for player in agents:
        player_items = []
        # print(player.value(1))
        # for i in range(1, level+1):
        #     item = player.__getitem__(i)
        #     if item in items:
        #         player_items.append(item)
        # desired_items.append(player_items)

        # i = 0
        for item in player.all_items():
            # i += 1
            if player.value(item) <= level and item in items:
                player_items.append(item)
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
    return recursive_sequential(agents, items)


def recursive_sequential(agents: AgentList, items: List[Any] = None, allocations: List[Any] = [[], []], end_allocation: List[List] = [], level: int = 1):
    """
    A recursive helper function to sequential()

    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param items A list of all existing items (U)
    :param allocations is the allocation for each player so far
    :param level is the depth level for item searching for each iteration
    """
    if not items:
        print(allocations)
        end_allocation.append(allocations)
        return end_allocation
    H_A_level, H_B_level = H_M_l(agents, items, level)
    if have_different_elements(H_A_level, H_B_level):
        for i in H_A_level:
            for j in H_B_level:
                if i != j:
                    _allocations = deep_copy_2d_list(allocations)
                    _items, _allocations = allocate(agents, items.copy(), _allocations, i, j)
                    recursive_sequential(agents, _items, _allocations, end_allocation, level + 1)
    else:
        recursive_sequential(agents, items, allocations, end_allocation, level + 1)


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
            items, allocations = allocate(agents, allocations, H_A_level[0], H_B_level[0])
            recursive_restricted_simple(agents, items, allocations, level + 1)
        else:
            if len(H_A_level) > 1:
                items, allocations = allocate(agents, allocations, H_A_level[1], H_B_level[0])
                recursive_restricted_simple(agents, items, allocations, level + 1)
            if len(H_B_level) > 1:
                items, allocations = allocate(agents, allocations, H_A_level[0], H_B_level[1])
                recursive_restricted_simple(agents, items, allocations, level + 1)
    else:
        recursive_restricted_simple(agents, items, allocations, level + 1)


def singles(agents: AgentList, items: List[Any] = None, allocations: List[Any] = None):
    A_items = {}
    B_items = {}
    A_allocations = []
    B_allocations = []
    for item in items:
        A_items[agents[0].value(item)] = item
        B_items[agents[1].value(item)] = item
    for i in range(len(items)):
        idx = len(items) - i
        if A_items[idx] != B_items[idx]:
            A_allocations.append(B_items[idx])
            B_allocations.append(A_items[idx])
    if not A_allocations and not B_allocations:
        return False
    for j in range(len(A_allocations)):
        if A_allocations[j] in items and B_allocations[j] in items:
            allocate(agents, items, allocations, A_allocations[j], B_allocations[j])
    return True


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
    return singles_doubles_helper(agents, items, True)


def singles_doubles_helper(agents: AgentList, items: List[Any] = None, do_single: bool = False) -> Dict:
    allocations = [[], []]
    if do_single:
        singles(agents, items, allocations)
    if not items:
        print(allocations)
        return allocations
    H_A_level, H_B_level = H_M_l(agents, items, len(agents[0].all_items()))
    if H_A_level[0] != H_B_level[0]:
        _allocations = deep_copy_2d_list(allocations)
        _items, _allocations = allocate(agents, items.copy(), _allocations, H_A_level[0], H_B_level[0])
        singles_doubles_helper(agents, _items, _allocations)
    temp_allocation_1 = deep_copy_2d_list(allocations)
    temp_allocation_2 = deep_copy_2d_list(allocations)
    items_1, temp_allocation_1 = allocate(agents, items.copy(), temp_allocation_1, H_A_level[0], H_B_level[1])
    items_2, temp_allocation_2 = allocate(agents, items.copy(), temp_allocation_2, H_A_level[1], H_B_level[0])
    if is_envy_free_partial_allocation(agents, temp_allocation_1):
        singles_doubles_helper(agents, items_1, temp_allocation_1)
    if is_envy_free_partial_allocation(agents, temp_allocation_2):
        singles_doubles_helper(agents, items_2, temp_allocation_2)


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
    return iterated_singles_doubles_helper(agents, items, True)


def iterated_singles_doubles_helper(agents: AgentList, items: List[Any] = None, do_single: bool = False) -> Dict:
    allocations = [[], []]
    if do_single:
        flag = True
        while flag:
            flag = singles(agents, items, allocations)
    if not items:
        print(allocations)
        return allocations
    H_A_level, H_B_level = H_M_l(agents, items, len(agents[0].all_items()))
    if H_A_level[0] != H_B_level[0]:
        _allocations = deep_copy_2d_list(allocations)
        _items, _allocations = allocate(agents, items.copy(), _allocations, H_A_level[0], H_B_level[0])
        iterated_singles_doubles_helper(agents, _items, _allocations)
    temp_allocation_1 = deep_copy_2d_list(allocations)
    temp_allocation_2 = deep_copy_2d_list(allocations)
    items_1, temp_allocation_1 = allocate(agents, items.copy(), temp_allocation_1, H_A_level[0], H_B_level[1])
    items_2, temp_allocation_2 = allocate(agents, items.copy(), temp_allocation_2, H_A_level[1], H_B_level[0])
    if is_envy_free_partial_allocation(agents, temp_allocation_1):
        iterated_singles_doubles_helper(agents, items_1, temp_allocation_1)
    if is_envy_free_partial_allocation(agents, temp_allocation_2):
        iterated_singles_doubles_helper(agents, items_2, temp_allocation_2)


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
    return s1_helper(agents, items, True)


def s1_helper(agents: AgentList, items: List[Any] = None, do_single: bool = False) -> Dict:
    allocations = [[], []]
    if do_single:
        singles(agents, items, allocations)
    if not items:
        print(allocations)
        return allocations
    H_A_level, H_B_level = H_M_l(agents, items, len(agents[0].all_items()))
    if H_A_level[0] != H_B_level[0]:
        _allocations = deep_copy_2d_list(allocations)
        _items, _allocations = allocate(agents, items.copy(), _allocations, H_A_level[0], H_B_level[0])
        s1_helper(agents, _items, _allocations)
    temp_allocation_1 = deep_copy_2d_list(allocations)
    temp_allocation_2 = deep_copy_2d_list(allocations)
    items_1, temp_allocation_1 = allocate(agents, items.copy(), temp_allocation_1, H_A_level[0], H_B_level[1])
    items_2, temp_allocation_2 = allocate(agents, items.copy(), temp_allocation_2, H_A_level[1], H_B_level[0])
    # if is_envy_free_partial_allocation(agents, temp_allocation_1):
    s1_helper(agents, items_1, temp_allocation_1)
    # if is_envy_free_partial_allocation(agents, temp_allocation_2):
    s1_helper(agents, items_2, temp_allocation_2)


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
    return l1_helper(agents, items, True)


def l1_helper(agents: AgentList, items: List[Any] = None, do_single: bool = False) -> Dict:
    allocations = [[], []]
    if do_single:
        flag = True
        while flag:
            flag = singles(agents, items, allocations)
    if not items:
        print(allocations)
        return allocations
    H_A_level, H_B_level = H_M_l(agents, items, len(agents[0].all_items()))
    if H_A_level[0] != H_B_level[0]:
        _allocations = deep_copy_2d_list(allocations)
        _items, _allocations = allocate(agents, items.copy(), _allocations, H_A_level[0], H_B_level[0])
        l1_helper(agents, _items, _allocations)
    temp_allocation_1 = deep_copy_2d_list(allocations)
    temp_allocation_2 = deep_copy_2d_list(allocations)
    items_1, temp_allocation_1 = allocate(agents, items.copy(), temp_allocation_1, H_A_level[0], H_B_level[1])
    items_2, temp_allocation_2 = allocate(agents, items.copy(), temp_allocation_2, H_A_level[1], H_B_level[0])
    # if is_envy_free_partial_allocation(agents, temp_allocation_1):
    l1_helper(agents, items_1, temp_allocation_1)
    # if is_envy_free_partial_allocation(agents, temp_allocation_2):
    l1_helper(agents, items_2, temp_allocation_2)


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

    i = 1
    allocations = [[], []]
    length = len(items)
    while i < length:
        for m in range(len(agents)):
            hm = H_M_l(agents, items, i)
            if not hm:
                print("No EV allocation")
                return
            if m == 0:
                item = find_last_item(agents[1], items, hm[0])
                allocate(agents, items, allocations, a_item=item)
            if m == 1:
                item = find_last_item(agents[0], items, hm[1])
                allocate(agents, items, allocations, b_item=item)
        i += 2
    print(allocations)


if __name__ == '__main__':
    Alice = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 3, 'tv': 2, 'book': 4}, name='Alice')
    George = fairpy.agents.AdditiveAgent({'computer': 4, 'phone': 2, 'tv': 3, 'book': 1}, name='George')
    trump([Alice, George], ['computer', 'phone', 'tv', 'book'])
