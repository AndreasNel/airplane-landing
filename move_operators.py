import random


def remove(items, choices):
    """
    Removes an items from the items list. Guarantees that there will always be at least one item
    left in the list of items.
    :param items: The items to which the operator should be applied.
    :param choices: Items that the operator can inject into the items if necessary.
    :return: The list of items after the operator was applied.
    """
    if len(items) > 1:
        to_remove = random.randrange(len(items))
        items = items[:to_remove] + items[to_remove + 1:]
    return items


def add(items, choices):
    """
    Adds one randomly picked item from the choices list to the list of items.
    :param items: The items to which the operator should be applied.
    :param choices: Items that the operator can inject into the items if necessary.
    :return: The list of items after the operator was applied.
    """
    to_insert = random.randrange(len(items))
    items = items[:to_insert] + random.choice(choices) + items[to_insert:]
    return items


def change(items, choices):
    """
    Changes one of the items in the item list to a randomly picked item in the choices list.
    :param items: The items to which the operator should be applied.
    :param choices: Items that the operator can inject into the items if necessary.
    :return: The list of items after the operator was applied.
    """
    items = list(items)
    to_change = random.randrange(len(items))
    items[to_change] = random.choice(choices)
    return "".join(items)


def swap(items, choices):
    """
    Swaps one of the items with another one in the item list.
    :param items: The items to which the operator should be applied.
    :param choices: Items that the operator can inject into the items if necessary.
    :return: The list of items after the operator was applied.
    """
    items = list(items)
    idx1, idx2 = random.randrange(len(items)), random.randrange(len(items))
    items[idx1], items[idx2] = items[idx2], items[idx1]
    return "".join(items)


MOVE_OP_MAP = {
    "a": add,
    "r": remove,
    "c": change,
    "s": swap,
}
