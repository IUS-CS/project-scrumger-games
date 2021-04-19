class Timer:
    """
    A simple wrapper class used to hold the timer that the game will use.
    """

    def __init__(self, initial_time=30):
        """
        - :param initial_time:
            Optional. An int to set as the initial time that the timer will hold, measured in seconds. Defaults to 30.
        """
        self.init_time = initial_time
        self.time = initial_time

    def get_time(self):
        """
        Getter method to get the current time held in the timer.
        - :return:
            An int representing the time that the timer currently holds, measured in seconds.
        """
        return self.time

    def set_time(self, new_time):
        """
        Setter method to set the timer to hold a specific time value.
        - :param new_time:
            An int representing the time that the timer should be set to.
        - :return:
            None
        """
        self.time = new_time

    def count_up(self):
        """
        Increment the timer by 1.
        - :return:
            None
        """
        self.time += 1

    def count_down(self):
        """
        Decrement the timer by 1.
        - :return:
            None
        """
        self.time -= 1

    def reset(self):
        """
        Reset the timer to its initial time.
        - :return:
            None
        """
        self.time = self.init_time
