#!/usr/bin/env python3
"""
Practical Robotics Visualization Examples

This file demonstrates common robotics scenarios using the visualization library.
Each example is self-contained and showcases different aspects of robot simulation.
"""

import numpy as np
from byu_robomanip.visualization import VizScene, ArmPlayer
from byu_robomanip import kinematics as kin
from byu_robomanip import transforms as tr


def example_1_basic_robot():
    """Example 1: Basic robot arm visualization"""
    print("Example 1: Basic Robot Arm")

    # Create 3-DOF robot
    dh = [[0, 0, 0.4, 0], [0, 0, 0.4, 0], [0, 0, 0.4, 0]]
    arm = kin.SerialArm(dh, jt=["r", "r", "r"])

    # Create scene
    viz = VizScene()
    viz.add_frame(np.eye(4), label="world", axes_label="w")
    viz.add_arm(arm, q=[np.pi / 4, -np.pi / 2, np.pi / 3], draw_frames=True)

    print("Basic robot with coordinate frames")
    viz.hold()
    viz.close_viz()


def example_2_workspace_analysis():
    """Example 2: Robot workspace analysis"""
    print("Example 2: Workspace Analysis")

    dh = [[0, 0, 0.3, 0], [0, 0, 0.4, 0], [0, 0, 0.3, 0]]
    arm = kin.SerialArm(dh, jt=["r", "r", "r"])

    viz = VizScene()
    viz.add_arm(arm, q=[0, 0, 0])

    # Sample workspace
    print("Sampling workspace points...")
    for _ in range(500):
        q_random = np.random.uniform(-np.pi, np.pi, 3)
        try:
            T = arm.fk(q_random)
            pos = T[:3, 3]
            # Color by height
            height_color = [pos[2] / 1.0, 1 - pos[2] / 1.0, 0.5, 0.6]
            viz.add_marker(pos, color=height_color, radius=0.02)
        except:
            continue

    # Add theoretical workspace boundary
    viz.add_ellipse(
        [0, 0, 0.5], np.eye(3), [1.0, 1.0, 0.7], color=[0, 1, 0], wireframe=True
    )

    print("Green wireframe shows theoretical workspace boundary")
    print("Colored points show actual reachable positions")
    viz.hold()
    viz.close_viz()


def example_3_path_planning():
    """Example 3: Path planning visualization"""
    print("Example 3: Path Planning Scenario")

    dh = [[0, 0, 0.3, np.pi / 2], [0, 0, 0.4, 0], [0, 0, 0.3, 0]]
    arm = kin.SerialArm(dh, jt=["r", "r", "r"])

    viz = VizScene()

    # Add obstacles
    obstacles = [
        ([0.4, 0.2, 0.3], 0.12),
        ([0.2, 0.5, 0.4], 0.10),
        ([-0.2, 0.4, 0.2], 0.08),
    ]

    for pos, radius in obstacles:
        viz.add_obstacle(pos, rad=radius)
        # Safety margin
        viz.add_ellipse(
            pos,
            np.eye(3),
            [radius + 0.05] * 3,
            color=[1, 1, 0, 0.2],
            edge_color=[1, 0.5, 0, 0.6],
        )

    # Start and goal configurations
    q_start = [0, 0, 0]
    q_goal = [np.pi / 2, -np.pi / 4, np.pi / 6]

    # Show start position
    viz.add_arm(arm, q=q_start, joint_colors=[[0, 1, 0, 1]] * 3)  # Green
    start_pos = arm.fk(q_start)[:3, 3]
    viz.add_marker(start_pos, color=[0, 1, 0], radius=0.08)

    # Show goal region
    goal_pos = arm.fk(q_goal)[:3, 3]
    viz.add_ellipse(
        goal_pos, np.eye(3), [0.1, 0.1, 0.05], color=[0, 0, 1, 0.5], show_edges=True
    )

    # Simple path (linear interpolation in joint space)
    path_length = 20
    for i in range(path_length + 1):
        alpha = i / path_length
        q_interp = (1 - alpha) * np.array(q_start) + alpha * np.array(q_goal)
        pos = arm.fk(q_interp)[:3, 3]

        # Color gradient from green to blue
        color = [(1 - alpha), alpha * 0.5, alpha, 0.7]
        viz.add_marker(pos, color=color, radius=0.03)

    print("Green: Start position | Blue ellipse: Goal region")
    print("Yellow: Obstacle safety margins | Colored path: Planned trajectory")
    viz.hold()
    viz.close_viz()


def example_4_uncertainty_visualization():
    """Example 4: Uncertainty and error visualization"""
    print("Example 4: Uncertainty Visualization")

    dh = [[0, 0, 0.4, 0], [0, 0, 0.4, 0], [0, 0, 0.4, 0]]
    arm = kin.SerialArm(dh, jt=["r", "r", "r"])

    viz = VizScene()

    # Nominal configuration
    q_nominal = [np.pi / 6, -np.pi / 4, np.pi / 3]
    viz.add_arm(arm, q=q_nominal, draw_frames=True)

    # Joint angle uncertainties (standard deviations in radians)
    joint_std = [0.05, 0.03, 0.04]  # Different uncertainty per joint

    # Monte Carlo sampling to visualize uncertainty propagation
    print("Computing uncertainty propagation via Monte Carlo...")
    ee_positions = []

    for _ in range(200):
        # Sample joint angles with noise
        q_sample = q_nominal + np.random.normal(0, joint_std, 3)
        try:
            T_sample = arm.fk(q_sample)
            ee_positions.append(T_sample[:3, 3])
        except:
            continue

    # Plot uncertainty cloud
    for pos in ee_positions:
        viz.add_marker(pos, color=[1, 0, 0, 0.3], radius=0.02)

    # Compute and show uncertainty ellipse
    if ee_positions:
        ee_array = np.array(ee_positions)
        mean_pos = np.mean(ee_array, axis=0)
        cov_matrix = np.cov(ee_array.T)

        # Eigendecomposition for ellipse orientation and size
        eigenvals, eigenvecs = np.linalg.eig(cov_matrix)
        ellipse_radii = 2 * np.sqrt(eigenvals)  # 2-sigma bounds

        viz.add_ellipse(
            mean_pos,
            eigenvecs,
            ellipse_radii,
            color=[1, 0, 0, 0.2],
            show_edges=True,
            edge_color=[0.8, 0, 0, 0.8],
        )

        # Add nominal end effector position
        T_nominal = arm.fk(q_nominal)
        nominal_pos = T_nominal[:3, 3]
        viz.add_marker(nominal_pos, color=[0, 0, 1], radius=0.05)

    print("Blue: Nominal end effector position")
    print("Red cloud: Monte Carlo uncertainty samples")
    print("Red ellipse: 2-sigma uncertainty bounds")
    viz.hold()
    viz.close_viz()


def example_5_multi_robot_coordination():
    """Example 5: Multi-robot coordination"""
    print("Example 5: Multi-Robot Coordination")

    # Create two different robots
    dh1 = [[0, 0, 0.3, 0], [0, 0, 0.4, 0], [0, 0, 0.2, 0]]
    dh2 = [[0, 0, 0.25, np.pi / 2], [0, 0, 0.35, 0], [0, 0, 0.3, 0]]

    arm1 = kin.SerialArm(dh1, jt=["r", "r", "r"])
    arm2 = kin.SerialArm(dh2, jt=["r", "r", "r"])

    viz = VizScene()

    # Position robots at different bases
    base1 = tr.se3(t=[-0.5, 0, 0])
    base2 = tr.se3(t=[0.5, 0, 0], R=tr.rotz(np.pi))

    viz.add_frame(base1, label="robot1_base", axes_label="1")
    viz.add_frame(base2, label="robot2_base", axes_label="2")

    # Add robots with different colors
    q1 = [np.pi / 4, -np.pi / 6, np.pi / 3]
    q2 = [np.pi / 3, -np.pi / 4, np.pi / 6]

    viz.add_arm(arm1, q=q1, joint_colors=[[1, 0, 0, 1]] * 3)  # Red robot
    viz.add_arm(arm2, q=q2, joint_colors=[[0, 0, 1, 1]] * 3)  # Blue robot

    # Shared workspace
    viz.add_ellipse(
        [0, 0, 0.4],
        np.eye(3),
        [0.8, 0.6, 0.5],
        color=[0.5, 0.5, 0.5, 0.1],
        wireframe=True,
    )

    # Shared task object
    task_pos = [0, 0.3, 0.4]
    viz.add_marker(task_pos, color=[0, 1, 0], radius=0.05)

    # Safety zones around each robot
    ee1_pos = arm1.fk(q1)[:3, 3] + base1[:3, 3]
    ee2_pos = arm2.fk(q2)[:3, 3] + base2[:3, 3]

    viz.add_ellipse(
        ee1_pos,
        np.eye(3),
        [0.15, 0.15, 0.1],
        color=[1, 0, 0, 0.2],
        edge_color=[1, 0, 0, 0.5],
    )
    viz.add_ellipse(
        ee2_pos,
        np.eye(3),
        [0.15, 0.15, 0.1],
        color=[0, 0, 1, 0.2],
        edge_color=[0, 0, 1, 0.5],
    )

    print("Red robot (left) and Blue robot (right)")
    print("Gray wireframe: Shared workspace")
    print("Green marker: Shared task object")
    print("Colored ellipses: Robot safety zones")
    viz.hold()
    viz.close_viz()


def example_6_dynamic_simulation():
    """Example 6: Dynamic robot simulation"""
    print("Example 6: Dynamic Simulation")

    dh = [[0, 0, 0.3, 0], [0, 0, 0.4, 0], [0, 0, 0.3, 0]]
    arm = kin.SerialArm(dh, jt=["r", "r", "r"])

    viz = VizScene()
    viz.add_arm(arm, draw_frames=True)

    # Add a moving target
    target_pos = [0.5, 0, 0.5]
    viz.add_marker(target_pos, color=[1, 0, 0], radius=0.05)

    # Add trajectory trace
    trace_positions = []

    print("Running dynamic simulation... (10 seconds)")
    print("Robot follows sinusoidal motion pattern")

    t_start = 0
    dt = 0.05
    duration = 10.0

    for i in range(int(duration / dt)):
        t = t_start + i * dt

        # Sinusoidal joint motion
        q = [
            0.5 * np.sin(0.5 * t),
            0.3 * np.cos(0.7 * t) - 0.2,
            0.4 * np.sin(0.9 * t + np.pi / 4),
        ]

        # Update robot
        viz.update(qs=[q])

        # Add trace point
        T = arm.fk(q)
        ee_pos = T[:3, 3]
        trace_positions.append(ee_pos)

        # Show recent trace (last 50 points)
        if len(trace_positions) > 1:
            recent_trace = trace_positions[-50:]
            for j, pos in enumerate(recent_trace):
                alpha = j / len(recent_trace)  # Fade effect
                viz.add_marker(pos, color=[0, 1, 1, alpha * 0.5], radius=0.01)

        # Update moving target
        target_new = [
            0.5 * np.cos(0.3 * t),
            0.3 * np.sin(0.4 * t),
            0.5 + 0.1 * np.sin(0.6 * t),
        ]
        viz.update(poss=[target_new])

        viz.hold(dt)

    print("Simulation complete!")
    viz.hold(3)  # Hold final state for 3 seconds
    viz.close_viz()


def main():
    """Run interactive example selection"""
    examples = [
        ("Basic Robot Arm", example_1_basic_robot),
        ("Workspace Analysis", example_2_workspace_analysis),
        ("Path Planning", example_3_path_planning),
        ("Uncertainty Visualization", example_4_uncertainty_visualization),
        ("Multi-Robot Coordination", example_5_multi_robot_coordination),
        ("Dynamic Simulation", example_6_dynamic_simulation),
    ]

    print("Robotics Visualization Examples")
    print("=" * 40)
    for i, (name, _) in enumerate(examples):
        print(f"{i+1}. {name}")
    print("0. Run all examples")
    print("=" * 40)

    try:
        choice = input("Select example (0-6): ").strip()
        choice = int(choice)

        if choice == 0:
            print("Running all examples...")
            for name, func in examples:
                print(f"\nRunning: {name}")
                func()
        elif 1 <= choice <= len(examples):
            examples[choice - 1][1]()
        else:
            print("Invalid choice")
    except (ValueError, KeyboardInterrupt, EOFError):
        print("Exiting...")


if __name__ == "__main__":
    main()
