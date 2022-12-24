"""
All these algorithms are based on the paper: Two-player fair division of indivisible items: Comparison of algorithms
By: D. Marc Kilgour, Rudolf Vetschera

programmers: Itay Hasidi & Amichai Bitan
"""
from utils_two_player_fair_division import *
from fairpy import fairpy
from fairpy.fairpy.agentlist import AgentList


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
    >>> sequential([Alice, George], ['computer', 'phone', 'tv', 'book'])
    [{'Alice': ['computer', 'phone'], 'George': ['book', 'tv']}, {'Alice': ['computer', 'tv'], 'George': ['book', 'phone']}]

    # test 2 :
    >>> Alice = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 3, 'tv': 2, 'book': 4}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'George')
    >>> sequential([Alice, George], ['computer', 'phone', 'tv', 'book'])
    [{'Alice': ['computer', 'phone'], 'George': ['book', 'tv']}, {'Alice': ['computer', 'tv'], 'George': ['book', 'phone']}, {'Alice': ['computer', 'tv'], 'George': ['phone', 'book']}, {'Alice': ['computer', 'book'], 'George': ['phone', 'tv']}, {'Alice': ['tv', 'phone'], 'George': ['computer', 'book']}, {'Alice': ['tv', 'book'], 'George': ['computer', 'phone']}, {'Alice': ['tv', 'computer'], 'George': ['phone', 'book']}, {'Alice': ['tv', 'book'], 'George': ['phone', 'computer']}]
    """
    return recursive_sequential(agents, items)


def recursive_sequential(agents: AgentList, items: List[Any], allocations: List[Any] = [[], []],
                         end_allocation=[], level: int = 1):
    """
    A recursive helper function to sequential()

    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param items A list of all existing items (U)
    :param allocations is the allocation for each player so far
    :param end_allocation is the end allocation for each player
    :param level is the depth level for item searching for each iteration
    """
    if not items:
        end_allocation.append({agents[0].name(): allocations[0], agents[1].name(): allocations[1]})
        return end_allocation
    H_A_level, H_B_level = H_M_l(agents, items, level)
    if have_different_elements(H_A_level, H_B_level):
        for i in H_A_level:
            for j in H_B_level:
                if i != j:
                    _allocations = deep_copy_2d_list(allocations)
                    _items, _allocations = allocate(items.copy(), _allocations, i, j)
                    recursive_sequential(agents, _items, _allocations, end_allocation, level + 1)
    else:
        recursive_sequential(agents, items, allocations, end_allocation, level + 1)
    return end_allocation


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
    [{'Alice': ['computer', 'tv'], 'George': ['book', 'phone']}, {'Alice': ['computer', 'phone'], 'George': ['book', 'tv']}]


    # test 2:
    >>> Alice = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 3, 'tv': 2, 'book': 4}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'George')
    >>> print(restricted_simple([Alice, George], ['computer', 'phone', 'tv', 'book']))
    [{'Alice': ['computer', 'tv'], 'George': ['book', 'phone']}, {'Alice': ['computer', 'phone'], 'George': ['book', 'tv']}, {'Alice': ['tv', 'book'], 'George': ['computer', 'phone']}, {'Alice': ['tv', 'phone'], 'George': ['computer', 'book']}, {'Alice': ['computer', 'book'], 'George': ['phone', 'tv']}, {'Alice': ['computer', 'tv'], 'George': ['phone', 'book']}]

    """
    return recursive_restricted_simple(agents, items)


def recursive_restricted_simple(agents: AgentList, items: List[Any], allocations: List[Any] = [[], []],
                                end_allocation=[], level: int = 1):
    """
    A recursive helper function to restricted_simple()

    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param items A list of all existing items (U)
    :param allocations is the allocation for each player so far
    :param end_allocation is the end allocation for each player
    :param level is the depth level for item searching for each iteration
    """
    if not items:
        end_allocation.append({agents[0].name(): allocations[0], agents[1].name(): allocations[1]})
        return end_allocation
    H_A_level, H_B_level = H_M_l(agents, items, level)
    if have_different_elements(H_A_level, H_B_level):
        if H_A_level[0] != H_B_level[0]:
            _allocations = deep_copy_2d_list(allocations)
            _items, _allocations = allocate(items.copy(), _allocations, H_A_level[0], H_B_level[0])
            recursive_restricted_simple(agents, _items, _allocations, end_allocation=end_allocation, level=level + 1)
        else:
            if len(H_A_level) > 1:
                _allocations = deep_copy_2d_list(allocations)
                _items, _allocations = allocate(items.copy(), _allocations, H_A_level[1], H_B_level[0])
                recursive_restricted_simple(agents, _items, _allocations, end_allocation=end_allocation,
                                            level=level + 1)
            if len(H_B_level) > 1:
                _allocations = deep_copy_2d_list(allocations)
                _items, _allocations = allocate(items.copy(), _allocations, H_A_level[0], H_B_level[1])
                recursive_restricted_simple(agents, _items, _allocations, end_allocation=end_allocation,
                                            level=level + 1)
    else:
        recursive_restricted_simple(agents, items, allocations, end_allocation=end_allocation, level=level + 1)
    return end_allocation


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
    []

    # test 2:
    >>> Alice = fairpy.agents.AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'a': 2, 'b': 4, 'c': 1, 'd': 3, 'e': 6, 'f': 5}, name = 'George')
    >>> print(singles_doubles([Alice, George], ['a', 'b', 'c', 'd', 'e', 'f']))
    [{'Alice': ['e', 'b', 'c'], 'George': ['f', 'd', 'a']}]

    # test 3:
    >>> Alice = fairpy.agents.AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4}, name = 'George')
    >>> print(singles_doubles([Alice, George], ['a', 'b', 'c', 'd']))
    [{'Alice': ['a', 'd'], 'George': ['b', 'c']}, {'Alice': ['b', 'c'], 'George': ['a', 'd']}]
    """
    return singles_doubles_helper(agents, items, allocations=[[], []], end_allocation=[], do_single=True)


def singles_doubles_helper(agents: AgentList, items: List[Any] = None, allocations=[[], []], end_allocation=[],
                           do_single: bool = False) -> Dict:
    """
    A recursive helper function to singles_doubles()

    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param items A list of all existing items (U)
    :param allocations is the allocation for each player so far
    :param end_allocation is the end allocation for each player
    :param do_single is a boolean flag that indicates if the singles() algorithm should be used or not, in this function
     it will only be used the first time the function is called.
    """
    if do_single:
        singles(agents, items, allocations)
    if not items:
        if is_envy_free_partial_allocation(agents, allocations):
            end_allocation.append({agents[0].name(): allocations[0], agents[1].name(): allocations[1]})
            return end_allocation
        return
    H_A_level, H_B_level = H_M_l(agents, items, len(agents[0].all_items()))
    if H_A_level[0] != H_B_level[0]:
        _allocations = deep_copy_2d_list(allocations)
        _items, _allocations = allocate(agents, items.copy(), _allocations, H_A_level[0], H_B_level[0])
        singles_doubles_helper(agents, _items, _allocations, end_allocation)
    temp_allocation_1 = deep_copy_2d_list(allocations)
    temp_allocation_2 = deep_copy_2d_list(allocations)
    items_1, temp_allocation_1 = allocate(items.copy(), temp_allocation_1, H_A_level[0], H_B_level[1])
    items_2, temp_allocation_2 = allocate(items.copy(), temp_allocation_2, H_A_level[1], H_B_level[0])
    singles_doubles_helper(agents, items_1, temp_allocation_1, end_allocation)
    singles_doubles_helper(agents, items_2, temp_allocation_2, end_allocation)
    return end_allocation


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
    []

    # rest2 :
    >>> Alice = fairpy.agents.AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'a': 2, 'b': 4, 'c': 1, 'd': 3, 'e': 6, 'f': 5}, name = 'George')
    >>> print(iterated_singles_doubles([Alice, George], ['a', 'b', 'c', 'd', 'e', 'f']))
    [{'Alice': ['e', 'b', 'c'], 'George': ['f', 'd', 'a']}]

    # test 3:
     >>> Alice = fairpy.agents.AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4}, name = 'George')
    >>> print(iterated_singles_doubles([Alice, George], ['a', 'b', 'c', 'd']))
    [{'Alice': ['a', 'd'], 'George': ['b', 'c']}, {'Alice': ['b', 'c'], 'George': ['a', 'd']}]
    """
    return iterated_singles_doubles_helper(agents, items, allocations=[[], []], end_allocation=[], do_single=True)


def iterated_singles_doubles_helper(agents: AgentList, items: List[Any] = None, allocations=[[], []], end_allocation=[],
                                    do_single: bool = False) -> Dict:
    """
    A recursive helper function to iterated_singles_doubles()

    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param items A list of all existing items (U)
    :param allocations is the allocation for each player so far
    :param end_allocation is the end allocation for each player
    :param do_single is a boolean flag that indicates if the singles() algorithm should be used or not, in this function
     it will only be used the first time the function is called as many times as possible.
    """
    if do_single:
        flag = True
        while flag:
            flag, allocations = singles(agents, items, allocations)
    if not items:
        if is_envy_free_partial_allocation(agents, allocations):
            end_allocation.append({agents[0].name(): allocations[0], agents[1].name(): allocations[1]})
            return end_allocation
        return
    H_A_level, H_B_level = H_M_l(agents, items, len(agents[0].all_items()))
    if H_A_level[0] != H_B_level[0]:
        _allocations = deep_copy_2d_list(allocations)
        _items, _allocations = allocate(agents, items.copy(), _allocations, H_A_level[0], H_B_level[0])
        singles_doubles_helper(agents, _items, _allocations, end_allocation)
    temp_allocation_1 = deep_copy_2d_list(allocations)
    temp_allocation_2 = deep_copy_2d_list(allocations)
    items_1, temp_allocation_1 = allocate(items.copy(), temp_allocation_1, H_A_level[0], H_B_level[1])
    items_2, temp_allocation_2 = allocate(items.copy(), temp_allocation_2, H_A_level[1], H_B_level[0])
    singles_doubles_helper(agents, items_1, temp_allocation_1, end_allocation)
    singles_doubles_helper(agents, items_2, temp_allocation_2, end_allocation)
    return end_allocation


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
    []

    # test2:
    >>> Alice = fairpy.agents.AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'a': 2, 'b': 4, 'c': 1, 'd': 3, 'e': 6, 'f': 5}, name = 'George')
    >>> print(s1([Alice, George], ['a', 'b', 'c', 'd', 'e', 'f']))
    [{'Alice': ['e', 'b', 'c'], 'George': ['f', 'd', 'a']}]

    # test 3:
    >>> Alice = fairpy.agents.AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4}, name = 'George')
    >>> print(s1([Alice, George], ['a', 'b', 'c', 'd']))
    [{'Alice': ['a', 'd'], 'George': ['b', 'c']}, {'Alice': ['b', 'c'], 'George': ['a', 'd']}]
    """
    return s1_helper(agents, items, allocations=[[], []], end_allocation=[], do_single=True)


def s1_helper(agents: AgentList, items: List[Any] = None, allocations=[[], []], end_allocation=[],
              do_single: bool = False) -> Dict:
    """
    A recursive helper function to s1()

    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param items A list of all existing items (U)
    :param allocations is the allocation for each player so far
    :param end_allocation is the end allocation for each player
    :param do_single is a boolean flag that indicates if the singles() algorithm should be used or not, in this function
     it will only be used the first time the function is called.
    """
    if do_single:
        singles(agents, items, allocations)
    if not items:
        end_allocation.append({agents[0].name(): allocations[0], agents[1].name(): allocations[1]})
        return end_allocation
    H_A_level, H_B_level = H_M_l(agents, items, len(agents[0].all_items()))
    if H_A_level[0] != H_B_level[0]:
        _allocations = deep_copy_2d_list(allocations)
        _items, _allocations = allocate(agents, items.copy(), _allocations, H_A_level[0], H_B_level[0])
        singles_doubles_helper(agents, _items, _allocations, end_allocation)
    temp_allocation_1 = deep_copy_2d_list(allocations)
    temp_allocation_2 = deep_copy_2d_list(allocations)
    items_1, temp_allocation_1 = allocate(items.copy(), temp_allocation_1, H_A_level[0], H_B_level[1])
    items_2, temp_allocation_2 = allocate(items.copy(), temp_allocation_2, H_A_level[1], H_B_level[0])
    singles_doubles_helper(agents, items_1, temp_allocation_1, end_allocation)
    singles_doubles_helper(agents, items_2, temp_allocation_2, end_allocation)
    return end_allocation


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
    []

    # test2:
    >>> Alice = fairpy.agents.AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'a': 2, 'b': 4, 'c': 1, 'd': 3, 'e': 6, 'f': 5}, name = 'George')
    >>> print(l1([Alice, George], ['a', 'b', 'c', 'd', 'e', 'f']))
    [{'Alice': ['e', 'b', 'c'], 'George': ['f', 'd', 'a']}]

    # test3:
    >>> Alice = fairpy.agents.AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4}, name = 'George')
    >>> print(l1([Alice, George], ['a', 'b', 'c', 'd']))
    [{'Alice': ['a', 'd'], 'George': ['b', 'c']}, {'Alice': ['b', 'c'], 'George': ['a', 'd']}]
    """
    return l1_helper(agents, items, allocations=[[], []], end_allocation=[], do_single=True)


def l1_helper(agents: AgentList, items: List[Any] = None, allocations=[[], []], end_allocation=[],
              do_single: bool = False) -> Dict:
    """
     A recursive helper function to l1()

     :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
     player's name.
     :param items A list of all existing items (U)
     :param allocations is the allocation for each player so far
     :param end_allocation is the end allocation for each player
     :param do_single is a boolean flag that indicates if the singles() algorithm should be used or not, in this function
      it will only be used the first time the function is called as many times as possible.
     """
    if do_single:
        flag = True
        while flag:
            flag, allocations = singles(agents, items, allocations)
    if not items:
        end_allocation.append({agents[0].name(): allocations[0], agents[1].name(): allocations[1]})
        return end_allocation
    H_A_level, H_B_level = H_M_l(agents, items, len(agents[0].all_items()))
    if H_A_level[0] != H_B_level[0]:
        _allocations = deep_copy_2d_list(allocations)
        _items, _allocations = allocate(agents, items.copy(), _allocations, H_A_level[0], H_B_level[0])
        singles_doubles_helper(agents, _items, _allocations, end_allocation)
    temp_allocation_1 = deep_copy_2d_list(allocations)
    temp_allocation_2 = deep_copy_2d_list(allocations)
    items_1, temp_allocation_1 = allocate(items.copy(), temp_allocation_1, H_A_level[0], H_B_level[1])
    items_2, temp_allocation_2 = allocate(items.copy(), temp_allocation_2, H_A_level[1], H_B_level[0])
    singles_doubles_helper(agents, items_1, temp_allocation_1, end_allocation)
    singles_doubles_helper(agents, items_2, temp_allocation_2, end_allocation)
    return end_allocation


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
    {'Alice': ['computer', 'phone'], 'George': ['book', 'tv']}

    # test2:
    >>> Alice = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 3, 'tv': 2, 'book': 4}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'George')
    >>> print(top_down([Alice, George], ['computer', 'phone', 'tv', 'book']))
    {'Alice': ['computer', 'tv'], 'George': ['phone', 'book']}
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
    length = int(len(items) / 2)
    allocations = [[], []]
    valuations = sorted_valuations(agents, items)
    for i in range(length):
        if valuations[0][0] in items:
            items, allocations = allocate(items, allocations, a_item=valuations[0][0], valuation_list=valuations)
        if valuations[1][0] in items:
            items, allocations = allocate(items, allocations, b_item=valuations[1][0], valuation_list=valuations)
    end_allocation = {agents[0].name(): allocations[0], agents[1].name(): allocations[1]}
    return end_allocation


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
    {'Alice': ['computer', 'tv'], 'George': ['book', 'phone']}

    # test2:
    >>> Alice = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 3, 'tv': 2, 'book': 4}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'George')
    >>> print(top_down_alternating([Alice, George], ['computer', 'phone', 'tv', 'book']))
    {'Alice': ['computer', 'book'], 'George': ['phone', 'tv']}
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
    allocations = [[], []]
    valuations = sorted_valuations(agents, items)
    length = int(len(items) / 2)
    for _ in range(length):
        if flag:
            if valuations[0][0] in items:
                items, allocations = allocate(items, allocations, a_item=valuations[0][0], valuation_list=valuations)
            if valuations[1][0] in items:
                items, allocations = allocate(items, allocations, b_item=valuations[1][0], valuation_list=valuations)
            flag = False
        elif not flag:
            if valuations[1][0] in items:
                items, allocations = allocate(items, allocations, b_item=valuations[1][0], valuation_list=valuations)
            if valuations[0][0] in items:
                items, allocations = allocate(items, allocations, a_item=valuations[0][0], valuation_list=valuations)
            flag = True
    end_allocation = {agents[0].name(): allocations[0], agents[1].name(): allocations[1]}
    return end_allocation


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
    {'Alice': ['computer', 'phone'], 'George': ['book', 'tv']}

    # test2:
    >>> Alice = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 3, 'tv': 2, 'book': 4}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'George')
    >>> print(bottom_up([Alice, George], ['computer', 'phone', 'tv', 'book']))
    {'Alice': ['tv', 'computer'], 'George': ['book', 'phone']}
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
    length = int(len(items) / 2)
    allocations = [[], []]
    valuations = sorted_valuations(agents, items)
    for i in range(length):
        if valuations[0][len(valuations[0]) - 1] in items:
            items, allocations = allocate(items, allocations, b_item=valuations[0][len(valuations[0]) - 1],
                                          valuation_list=valuations)
        if valuations[1][len(valuations[1]) - 1] in items:
            items, allocations = allocate(items, allocations, a_item=valuations[1][len(valuations[1]) - 1],
                                          valuation_list=valuations)
    end_allocation = {agents[0].name(): allocations[0], agents[1].name(): allocations[1]}
    return end_allocation


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
    {'Alice': ['computer', 'tv'], 'George': ['book', 'phone']}

    # test 2:
    >>> Alice = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 3, 'tv': 2, 'book': 4}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'George')
    >>> print(bottom_up_alternating([Alice, George], ['computer', 'phone', 'tv', 'book']))
    {'Alice': ['tv', 'phone'], 'George': ['book', 'computer']}
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
    allocations = [[], []]
    valuations = sorted_valuations(agents, items)
    length = int(len(items) / 2)
    for _ in range(length):
        if flag:
            if valuations[0][len(valuations[0]) - 1] in items:
                items, allocations = allocate(items, allocations, b_item=valuations[0][len(valuations[0]) - 1], valuation_list=valuations)
            if valuations[1][len(valuations[1]) - 1] in items:
                items, allocations = allocate(items, allocations, a_item=valuations[1][len(valuations[1]) - 1], valuation_list=valuations)
            flag = False
        elif not flag:
            if valuations[1][len(valuations[1]) - 1] in items:
                items, allocations = allocate(items, allocations, a_item=valuations[1][len(valuations[1]) - 1], valuation_list=valuations)
            if valuations[0][len(valuations[0]) - 1] in items:
                items, allocations = allocate(items, allocations, b_item=valuations[0][len(valuations[0]) - 1], valuation_list=valuations)
            flag = True
    end_allocation = {agents[0].name(): allocations[0], agents[1].name(): allocations[1]}
    return end_allocation


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
    {'Alice': ['computer', 'tv'], 'George': ['book', 'phone']}

    # test2:
    >>> Alice = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 3, 'tv': 2, 'book': 4}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'George')
    >>> print(trump([Alice, George], ['computer', 'phone', 'tv', 'book']))
    {'Alice': [], 'George': []}
    """
    i = 1
    allocations = [[], []]
    length = len(items)
    while i < length:
        for m in range(len(agents)):
            hm = H_M_l(agents, items, i)
            if not hm[0] and not hm[1]:
                print({agents[0].name(): [], agents[1].name(): []})
                return
            if m == 0:
                item = find_last_item(agents[1], items)
                allocate(items, allocations, a_item=item)
            if m == 1:
                item = find_last_item(agents[0], items)
                allocate(items, allocations, b_item=item)
        i += 2
    end_allocation = {agents[0].name(): allocations[0], agents[1].name(): allocations[1]}
    return end_allocation
