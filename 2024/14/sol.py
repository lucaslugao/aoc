import sys
import re
import dataclasses
import collections

WIDTH = 101
HEIGHT = 103


@dataclasses.dataclass
class Robot:
    p: complex
    v: complex

    def at(self, t=100):
        r = self.p + t * self.v
        return Robot(complex(r.real % WIDTH, r.imag % HEIGHT), self.v)

    def quadrant(self):
        if self.p.real == WIDTH // 2 or self.p.imag == HEIGHT // 2:
            return None, None
        return self.p.real < WIDTH // 2, self.p.imag < HEIGHT // 2


def prod(iterable):
    result = 1
    for x in iterable:
        result *= x
    return result


def get_dispersion_at(robots, t):
    x = [robot.at(t).p.real for robot in robots]
    y = [robot.at(t).p.imag for robot in robots]
    center_x = sum(x) / len(robots)
    center_y = sum(y) / len(robots)
    return sum(
        abs(complex(x[i], y[i]) - complex(center_x, center_y))
        for i in range(len(robots))
    )


if __name__ == "__main__":
    robots = []
    for line in sys.stdin:
        line = line.strip()
        match = re.match(r"p=([+-]?\d+),([+-]?\d+) v=([+-]?\d+),([+-]?\d+)", line)
        p_x = int(match.group(1))
        p_y = int(match.group(2))
        v_x = int(match.group(3))
        v_y = int(match.group(4))
        robot = Robot(complex(p_x, p_y), complex(v_x, v_y))
        robots.append(robot)

    quadrants = collections.defaultdict(int)
    for robot in robots:
        q = robot.at(100).quadrant()
        if q != (None, None):
            quadrants[q] += 1
    print(prod(quadrants.values()))

    min_dispersion = get_dispersion_at(robots, 0)
    for t in range(1, 10000):
        dispersion = get_dispersion_at(robots, t)
        if dispersion < min_dispersion:
            min_dispersion = dispersion
            print(t, min_dispersion)
