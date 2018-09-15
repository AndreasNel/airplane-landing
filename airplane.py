class Airplane:
    def __init__(self, plane_id, arrival, early, target, last, separation, early_penalty, late_penalty):
        self.plane_id = plane_id
        self.arrival_time = arrival
        self.earliest_time = early
        self.target_time = target
        self.latest_time = last
        self.separation_time = separation
        self.early_penalty = early_penalty
        self.late_penalty = late_penalty
        self.landing_time = self.earliest_time

    def fitness(self):
        """
        Gives the fitness value of the plane based on its landing time, target time and penalty coefficients.
        :return: float
        """
        return (self.early_penalty if self.landing_time < self.target_time else self.late_penalty) *\
            abs(self.landing_time - self.target_time)

    def valid(self):
        """
        Determines whether the state of the airplane is currently valid.
        :return: Boolean, indicating whether the current state is valid.
        """
        return self.earliest_time <= self.landing_time <= self.latest_time

    def next_available_time(self, airplane_id):
        """
        Gets the next available landing time for the given airplane wrt to this airplane.
        :param airplane_id: The ID (index) of the plane to check for.
        :return: The next available landing time for the specified airplane.
        """
        return self.landing_time + self.separation_time[airplane_id]

    def is_after(self, plane):
        """
        Determines whether this plane lands after the specified plane.
        :param plane: The plane to check.
        :return: bool
        """
        return plane.is_before(self)

    def is_before(self, plane):
        """
        Determines whether this plane lands before the specified plane.
        :param plane: The plane to check.
        :return: bool
        """
        return self.next_available_time(plane.plane_id) <= plane.landing_time
