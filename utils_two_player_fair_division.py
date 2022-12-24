from typing import List, Any, Dict
from fairpy import fairpy
from fairpy.fairpy.agentlist import AgentList


def find_last_item(agent, item_list):
    """
    returns the last item a player wants

    >>> Alice = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'Alice')
    >>> find_last_item(Alice, ['computer', 'phone', 'tv', 'book'])
    'book'
    """
    max_score = -1
    max_item = ""
    for item in item_list:
        score = agent.value(item)
        if max_score < score:
            max_score = score
            max_item = item
    return max_item


def is_envy_free_partial_allocation(agents: AgentList, allocations: List[Any]):
    """
    Gets an allocation and determines if its env free

    >>> Alice = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'computer': 4, 'phone': 2, 'tv': 3, 'book': 1}, name = 'George')
    >>> is_envy_free_partial_allocation([Alice, George], [['computer', 'phone'], ['book', 'tv']])
    False

    >>> Alice = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'computer': 4, 'phone': 3, 'tv': 2, 'book': 1}, name = 'George')
    >>> is_envy_free_partial_allocation([Alice, George], [['computer', 'phone'], ['book', 'tv']])
    True

    """
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

    >>> deep_copy_2d_list([[1, 2, 3], [4, 5, 6]])
    [[1, 2, 3], [4, 5, 6]]
    """
    lst_copy = []
    for i in range(len(lst)):
        lst_temp = []
        for j in range(len(lst[0])):
            lst_temp.append(lst[i][j])
        lst_copy.append(lst_temp)
    return lst_copy


def allocate(items: List[Any], allocations: List[Any] = None, a_item=None, b_item=None, valuation_list=None):
    """
    Allocates the first item, to agent A and the second item to agent B.
    :param items A list of all existing items (U).
    :param allocations is the allocation for each player so far
    :param a_item the item that agent A gets
    :param b_item the item that agent B gets
    :param valuation_list a list with valuations for each agent, only used in BU BA TD TA algorithms

    >>> itm, alloc = allocate(['a', 'b', 'c', 'd'], [[], []], 'a', 'b')
    >>> itm
    ['c', 'd']
    >>> alloc
    [['a'], ['b']]

    >>> itm, alloc = allocate(['a', 'b', 'c', 'd'], [[], []], 'a')
    >>> itm
    ['b', 'c', 'd']
    >>> alloc
    [['a'], []]
    """
    if a_item:
        allocations[0].append(a_item)
        items.remove(a_item)
        if valuation_list:
            valuation_list[0].remove(a_item)
            valuation_list[1].remove(a_item)
    if b_item:
        allocations[1].append(b_item)
        items.remove(b_item)
        if valuation_list:
            valuation_list[0].remove(b_item)
            valuation_list[1].remove(b_item)
    return items, allocations


def H_M_l(agents: AgentList, items: List[Any] = None, level: int = 1):
    """
    Returns the items each player wants until level.

    >>> Alice = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'computer': 4, 'phone': 2, 'tv': 3, 'book': 1}, name = 'George')
    >>> H_M_l([Alice, George], ['computer', 'phone', 'tv', 'book'])
    [['computer'], ['book']]
    >>> H_M_l([Alice, George], ['computer', 'phone', 'tv', 'book'], 2)
    [['computer', 'phone'], ['phone', 'book']]
    """
    desired_items = []
    for player in agents:
        player_items = []
        for item in player.all_items():
            if player.value(item) <= level and item in items:
                player_items.append(item)
        desired_items.append(player_items)
    return desired_items


def have_different_elements(items_A: List[Any], items_B: List[Any]):
    """
    Returns True if both lists different at at least one item.
    :param items_A the list of items of player A
    :param items_B the list of items of player B

    >>> have_different_elements(['a', 'b'], ['a', 'c'])
    True
    >>> have_different_elements(['a', 'b'], ['a', 'b'])
    True
    >>> have_different_elements(['a'], ['a'])
    False
    """
    if len(items_A) != len(items_B):
        return True
    for i in items_A:
        for j in items_B:
            if i != j:
                return True
    return False


def singles(agents: AgentList, items: List[Any] = None, allocations: List[Any] = None):
    """
    Goes over both valuation list of the players and returns allocates all the singles to each player.
    Singles are object at the end of each lst that occur only in one player's list until a certain level.
    For instance: A = [1, 2, 3, 4], B = [1, 4, 3, 2] we see that 2 is single in B and 4 in A, but 3 is in both A and B
    so that means 3 is not a single.

    >>> Alice = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'computer': 4, 'phone': 2, 'tv': 3, 'book': 1}, name = 'George')
    >>> singles([Alice, George], ['computer', 'phone', 'tv', 'book'], [[], []])
    (True, [['computer'], ['book']])

    >>> Alice = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 3, 'tv': 2, 'book': 4}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'computer': 4, 'phone': 2, 'tv': 3, 'book': 1}, name = 'George')
    >>> singles([Alice, George], ['computer', 'phone', 'tv', 'book'], [[], []])
    (True, [['computer', 'tv'], ['book', 'phone']])

    >>> Alice = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'George')
    >>> singles([Alice, George], ['computer', 'phone', 'tv', 'book'], [[], []])
    (False, [[], []])
    """
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
        else:
            break
    if not A_allocations and not B_allocations:
        return False, allocations
    for j in range(len(A_allocations)):
        if A_allocations[j] in items and B_allocations[j] in items:
            allocate(items, allocations, A_allocations[j], B_allocations[j])
    return True, allocations


def sorted_valuations(agents: AgentList, items: List[Any]):
    """
    Returns the valuation of the agents in a sorted List format, where the first sub-list is the first agent,
    and the first item in a sub-list is the most valued item for that agent.

    >>> Alice = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'Alice')
    >>> George = fairpy.agents.AdditiveAgent({'computer': 4, 'phone': 2, 'tv': 3, 'book': 1}, name = 'George')
    >>> sorted_valuations([Alice, George], ['computer', 'phone', 'tv', 'book'])
    [['computer', 'phone', 'tv', 'book'], ['book', 'phone', 'tv', 'computer']]
    """
    sorted_lst = [[], []]
    for agent in range(len(agents)):
        for i in range(1, len(items) + 1):
            for item in items:
                if agents[agent].value(item) == i:
                    sorted_lst[agent].append(item)
                    break
    return sorted_lst
