"""Write your method below. Run this file to watch the resulting motion."""

import time
import numpy as np
from collections import deque
from exam_robot import arm


def compute_robot_path(q_init, goal, obst_location, obst_radius):
    # Use arm and your own homework library to compute the path.
    # Return a list of joint configurations (or a NumPy array with one per row).
    # Include q_init first. Use radians for revolute joints and meters for prismatic joints.
    
    # Save the initial row with q_s.append(q_init.copy()); use q = q_init.copy() to work.
    # q_s.append(q_init.copy())
    # q = q_init.copy()

    q_max = q_init + np.pi
    q_min = q_init - np.pi

    # 5 deg steps
    rad_jump = 0.0872665
    tolerance = 0.05

    # BFS, You just said it had to work, not work well
    start = (0,) * arm.n
    queue = deque([start])
    parent = {start: None}
    
    while queue:
        c = queue.popleft()
        q = q_init + rad_jump * np.array(c)

        #Check win
        tip = arm.fk(q)[:3, 3]

        #loop through joints
        if np.linalg.norm(tip - goal) <= tolerance:
            q_s = []
            node = c

            while node is not None:
                q_s.append((q_init + rad_jump * np.array(node)).tolist())
                node = parent[node]

            q_s.reverse()
            return q_s

        #moving each joint
        for joint in range(arm.n):
            for direction in (-1, 1):
                neighbor = list(c)
                neighbor[joint] += direction
                neighbor = tuple(neighbor)

                if neighbor in parent:
                    continue

                q_next = q_init + rad_jump * np.array(neighbor)

                # check for invalid configs
                if np.any(q_next < q_min - 0.00000000001):
                    continue
                if np.any(q_next > q_max + 0.00000000001):
                    continue

                if not check_motion(q, q_next, obst_location, obst_radius):
                    continue

                parent[neighbor] = c
                queue.append(neighbor)

    #not able to find a valid path
    return []


# helper function to see if we have crashed
def collition(point, obst_location, obst_radius) -> bool:
    return np.linalg.norm(point - obst_location) <= obst_radius

def robo_pos(q):
    return [
        arm.fk(q, index=i)[:3, 3]
        for i in range(arm.n + 1)
    ]

def check_config(q, obst_location, obst_radius):
    points = robo_pos(q)

    for a, b in zip(points[:-1], points[1:]):
        segment = b - a
        length = np.dot(segment, segment)

        if length == 0:
            closest = a
        else:
            t = np.dot(obst_location - a, segment) / length
            t = np.clip(t, 0.0, 1.0)
            closest = a + t * segment

        if collition(closest, obst_location, obst_radius):
            return False

    return True

def check_motion(q_from, q_to, obst_location, obst_radius):
    for q in np.linspace(q_from, q_to, 6):
        if not check_config(q, obst_location, obst_radius):
            return False
    return True

if __name__ == "__main__":
    # These values are for your own testing. The instructor will also use other cases.
    from byu_robomanip.visualization import VizScene

    q_0 = np.zeros(arm.n)
    goal = np.array([0.0, 2.0, 4.0])
    obst_position = np.array([0.0, 3.0, 2.0])
    obst_rad = 1.0

    q_s = compute_robot_path(q_0, goal, obst_position, obst_rad)
    if len(q_s) == 0:
        raise ValueError(
            "No path returned. Implement compute_robot_path before running it."
        )

    viz = VizScene()
    viz.add_arm(arm)
    viz.add_marker(goal, radius=0.1)
    viz.add_obstacle(obst_position, rad=obst_rad)
    viz.update(qs=[q_0.tolist()])
    for q in q_s:
        viz.update(qs=[np.asarray(q).tolist()])
        time.sleep(0.02)
    viz.hold()
