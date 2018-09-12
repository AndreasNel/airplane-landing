import random

# TODO remove the randomness, rather go to average
def move_to_target(airplane):
    """
    Moves the landing time of the airplane closer to its target landing time.
    :param airplane: The airplane to land.
    """
    airplane.landing_time = random.randint(min(airplane.landing_time, airplane.target_time), max(airplane.landing_time, airplane.target_time))


def repel_target(airplane):
    """
    Moves the landing time of the airplane away from its target landing time.
    :param airplane: The airplane to land.
    """
    if airplane.landing_time <= airplane.target_time:
        land_earlier(airplane)
    else:
        land_later(airplane)


def land_earlier(airplane):
    """
    Moves the landing time of the airplane to an earlier time.
    :param airplane: The airplane to land.
    """
    airplane.landing_time = random.randint(airplane.earliest_time, airplane.landing_time)


def land_later(airplane):
    """
    Moves the landing time of the airplane to a later time.
    :param airplane: The airplane to land.
    """
    airplane.landing_time = random.randint(airplane.landing_time, airplane.latest_time)


def stay_put(airplane):
    """
    A no-op. The airplane's landing time isn't changed.
    :param airplane: The airplane.
    """
    pass


HEURISTIC_MAP = {
    "m": move_to_target,
    "r": repel_target,
    "e": land_earlier,
    "l": land_later,
    "s": stay_put,
}
