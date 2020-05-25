import sys
from datetime import timedelta
from timeit import default_timer


class ProgressBar(object):
    def __init__(self, max_value, width=60):
        self.max_value = max_value
        self.width = width
        self.current_value = 0
        self.current_progress = 0
        self.start = None

    def setup(self):
        output = "[{spaces}] 0 in 0 s - 0%".format(spaces=" " * self.width)
        sys.stdout.write(output)
        sys.stdout.flush()
        sys.stdout.write("\r")
        self.start = default_timer()

    def update(self, new_value=0, chunk=0):
        if new_value:
            self.current_value = new_value
        else:
            self.current_value += chunk

        self.current_progress = int(self.current_value * self.width / self.max_value)
        elapsed = default_timer() - self.start
        seconds_left = (self.max_value * elapsed / self.current_value) - elapsed

        output = "[{dashes}{spaces}] {current} in {elapsed}, {left} left - {percentage}%".format(
            elapsed=self._format_time(elapsed),
            dashes="-" * self.current_progress,
            spaces=" " * (self.width - self.current_progress),
            current=self.current_value,
            left=self._format_time(seconds_left),
            percentage=str(self.current_value * 100 / self.max_value),
        )
        sys.stdout.write(output)
        sys.stdout.write("\r")
        sys.stdout.flush()

    def finish(self):
        if self.current_progress < self.width:
            self.update(new_value=self.max_value)

        sys.stdout.write("\n")

    def _format_time(self, seconds):
        return str(timedelta(seconds=seconds)).split(".")[0]
