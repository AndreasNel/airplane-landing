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
    #     TODO implement fitness function

    def valid(self):
        """
        Determines whether the state of the airplane is currently valid.
        :return: Boolean, indicating whether the current state is valid.
        """
        # TODO extend to check for other constraints
        return self.earliest_time <= self.landing_time <= self.latest_time

    def next_available_time(self, airplane_id):
        """
        Gets the next available landing time for the given airplane wrt to this airplane.
        :param airplane_id: The ID (index) of the plane to check for.
        :return: The next available landing time for the specified airplane.
        """
        return self.landing_time + self.separation_time[airplane_id]
