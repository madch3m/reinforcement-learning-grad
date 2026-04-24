"""
Comprehensive test suite for the Traffic Signal RL project.
Tests cover: Vehicle, TrafficGenerator, TrafficSignalEnv, Controllers, and Gradio app functions.
"""

import pytest
import numpy as np

from traffic_rl_project import (
    ActuatedController,
    FixedTimeController,
    MaxPressureController,
    TrafficSignalEnv,
    Vehicle,
    compare_controllers,
)
from gradio_app.gradio_traffic_app import (
    create_intersection_visualization,
    create_performance_plots,
    run_comparison,
    run_simulation,
)


class TestVehicle:
    def test_init(self):
        v = Vehicle(arrival_time=10.0, lane=2)
        assert v.arrival_time == 10.0
        assert v.lane == 2
        assert v.waiting_time == 0.0
        assert v.has_passed is False

    def test_update_waiting_time(self):
        v = Vehicle(0.0, 0)
        v.update_waiting_time(1.0)
        assert v.waiting_time == 1.0
        v.update_waiting_time(2.5)
        assert v.waiting_time == 3.5

    def test_update_waiting_time_after_passed(self):
        v = Vehicle(0.0, 0)
        v.update_waiting_time(1.0)
        v.has_passed = True
        v.update_waiting_time(5.0)
        assert v.waiting_time == 1.0

    def test_lane_values(self):
        for lane in range(4):
            v = Vehicle(0.0, lane)
            assert v.lane == lane


class TestTrafficSignalEnv:
    def test_init_defaults(self):
        env = TrafficSignalEnv()
        assert env.arrival_rates == [0.2, 0.2, 0.2, 0.2]
        assert env.min_green_time == 10
        assert env.dt == 1.0
        assert env.max_queue_length == 50

    def test_init_custom(self):
        env = TrafficSignalEnv(arrival_rates=[0.1, 0.3, 0.2, 0.4], min_green_time=15)
        assert env.arrival_rates == [0.1, 0.3, 0.2, 0.4]
        assert env.min_green_time == 15

    def test_reset(self):
        env = TrafficSignalEnv()
        # Run a few steps to change state
        for _ in range(10):
            env.step(0)
        obs, info = env.reset()
        assert env.current_time == 0
        assert env.current_phase == 0
        assert env.phase_time == 0
        assert env.total_vehicles_passed == 0
        assert env.total_vehicles_arrived == 0
        assert all(len(q) == 0 for q in env.queues)
        assert len(obs) == 10
        assert info == {}

    def test_observation_shape(self):
        env = TrafficSignalEnv()
        obs, _ = env.reset()
        assert obs.shape == (10,)
        assert obs.dtype == np.float32

    def test_observation_contents_at_reset(self):
        env = TrafficSignalEnv()
        obs, _ = env.reset()
        # Queue lengths should be 0
        np.testing.assert_array_equal(obs[:4], [0, 0, 0, 0])
        # Avg waiting times should be 0
        np.testing.assert_array_equal(obs[4:8], [0, 0, 0, 0])
        # Phase should be 0, phase_time should be 0
        assert obs[8] == 0
        assert obs[9] == 0

    def test_step_returns_correct_tuple(self):
        env = TrafficSignalEnv()
        env.reset()
        result = env.step(0)
        assert len(result) == 5
        obs, reward, terminated, truncated, info = result
        assert obs.shape == (10,)
        assert isinstance(reward, float)
        assert isinstance(terminated, bool)
        assert isinstance(truncated, bool)
        assert isinstance(info, dict)
        assert 'vehicles_passed' in info
        assert 'avg_waiting_time' in info
        assert 'throughput' in info

    def test_step_action_maintain(self):
        env = TrafficSignalEnv()
        env.reset()
        env.step(0)  # maintain phase
        assert env.current_phase == 0
        assert env.phase_time == 1.0

    def test_step_action_switch_before_min_green(self):
        env = TrafficSignalEnv(min_green_time=10)
        env.reset()
        # Try to switch immediately - should be ignored
        env.step(1)
        assert env.current_phase == 0  # Still phase 0

    def test_step_action_switch_after_min_green(self):
        env = TrafficSignalEnv(min_green_time=5)
        env.reset()
        # Advance past min green time
        for _ in range(6):
            env.step(0)
        assert env.phase_time >= 5
        # Now switch should work
        env.step(1)
        assert env.current_phase == 1

    def test_phase_cycles(self):
        env = TrafficSignalEnv(min_green_time=1)
        env.reset()
        # Advance past min_green then switch 4 times to cycle all phases
        phases_seen = [0]
        for _ in range(4):
            env.step(0)  # advance one step
            env.step(1)  # switch
            phases_seen.append(env.current_phase)
        assert 0 in phases_seen
        assert 1 in phases_seen

    def test_time_advances(self):
        env = TrafficSignalEnv()
        env.reset()
        for i in range(10):
            env.step(0)
        assert env.current_time == 10.0

    def test_max_queue_length_enforced(self):
        env = TrafficSignalEnv(arrival_rates=[1.0, 1.0, 1.0, 1.0], min_green_time=1000)
        env.reset()
        # Run many steps so queues fill up; no vehicles pass because phase never switches green properly
        for _ in range(200):
            env.step(0)
        for q in env.queues:
            assert len(q) <= env.max_queue_length

    def test_vehicles_pass_on_green(self):
        """With high traffic and enough steps, vehicles should pass on green phases."""
        np.random.seed(42)
        env = TrafficSignalEnv(arrival_rates=[0.5, 0.5, 0.5, 0.5])
        env.reset()
        for _ in range(100):
            env.step(0)
        # Phase 0 = NS green, so some NS vehicles should pass
        assert env.total_vehicles_passed > 0

    def test_phases_dictionary(self):
        assert len(TrafficSignalEnv.PHASES) == 4
        for phase_id, info in TrafficSignalEnv.PHASES.items():
            assert 'ns' in info
            assert 'ew' in info
            assert info['ns'] in ('green', 'yellow', 'red')
            assert info['ew'] in ('green', 'yellow', 'red')

    def test_reward_is_finite(self):
        env = TrafficSignalEnv()
        env.reset()
        for _ in range(50):
            _, reward, _, _, _ = env.step(np.random.choice([0, 1]))
            assert np.isfinite(reward)

    def test_info_values_non_negative(self):
        env = TrafficSignalEnv()
        env.reset()
        for _ in range(50):
            _, _, _, _, info = env.step(0)
        assert info['vehicles_passed'] >= 0
        assert info['avg_waiting_time'] >= 0
        assert info['throughput'] >= 0


class TestFixedTimeController:
    def test_init(self):
        c = FixedTimeController(green_time=25)
        assert c.green_time == 25
        assert c.name == "Fixed-Time"

    def test_maintain_before_green_time(self):
        c = FixedTimeController(green_time=30)
        obs = np.zeros(10, dtype=np.float32)
        obs[9] = 10  # phase_time = 10 < 30
        action, _ = c.predict(obs)
        assert action == 0

    def test_switch_at_green_time(self):
        c = FixedTimeController(green_time=30)
        obs = np.zeros(10, dtype=np.float32)
        obs[9] = 30  # phase_time = 30 >= 30
        action, _ = c.predict(obs)
        assert action == 1

    def test_switch_after_green_time(self):
        c = FixedTimeController(green_time=30)
        obs = np.zeros(10, dtype=np.float32)
        obs[9] = 50
        action, _ = c.predict(obs)
        assert action == 1


class TestActuatedController:
    def test_init(self):
        c = ActuatedController(min_green=10, max_green=60)
        assert c.min_green == 10
        assert c.max_green == 60
        assert c.name == "Actuated"

    def test_maintain_before_min_green(self):
        c = ActuatedController(min_green=10, max_green=60)
        obs = np.zeros(10, dtype=np.float32)
        obs[9] = 5  # phase_time < min_green
        action, _ = c.predict(obs)
        assert action == 0

    def test_switch_at_max_green(self):
        c = ActuatedController(min_green=10, max_green=60)
        obs = np.zeros(10, dtype=np.float32)
        obs[9] = 60  # phase_time >= max_green
        action, _ = c.predict(obs)
        assert action == 1

    def test_switch_when_waiting_queues_longer(self):
        c = ActuatedController(min_green=10, max_green=60)
        obs = np.zeros(10, dtype=np.float32)
        obs[8] = 0  # NS green phase
        obs[9] = 15  # phase_time > min_green
        obs[0] = 2   # North queue (active) = 2
        obs[2] = 2   # South queue (active) = 2 -> active total = 4
        obs[1] = 10  # East queue (waiting) = 10
        obs[3] = 10  # West queue (waiting) = 10 -> waiting total = 20
        action, _ = c.predict(obs)
        assert action == 1  # should switch

    def test_maintain_when_active_queues_longer(self):
        c = ActuatedController(min_green=10, max_green=60)
        obs = np.zeros(10, dtype=np.float32)
        obs[8] = 0   # NS green phase
        obs[9] = 15  # phase_time > min_green
        obs[0] = 10  # North queue (active)
        obs[2] = 10  # South queue (active) -> active total = 20
        obs[1] = 2   # East queue (waiting)
        obs[3] = 2   # West queue (waiting) -> waiting total = 4
        action, _ = c.predict(obs)
        assert action == 0  # should maintain


class TestMaxPressureController:
    def test_init(self):
        c = MaxPressureController()
        assert c.min_phase_time == 10
        assert c.name == "Max-Pressure"

    def test_maintain_before_min_phase_time(self):
        c = MaxPressureController()
        obs = np.zeros(10, dtype=np.float32)
        obs[9] = 5  # phase_time < min_phase_time
        action, _ = c.predict(obs)
        assert action == 0

    def test_switch_when_opposing_pressure_higher(self):
        c = MaxPressureController()
        obs = np.zeros(10, dtype=np.float32)
        obs[8] = 0   # NS green
        obs[9] = 15  # phase_time > min
        obs[0] = 2   # North
        obs[2] = 2   # South -> NS pressure = 4
        obs[1] = 10  # East
        obs[3] = 10  # West -> EW pressure = 20 > 4 * 1.2
        action, _ = c.predict(obs)
        assert action == 1

    def test_maintain_when_current_pressure_higher(self):
        c = MaxPressureController()
        obs = np.zeros(10, dtype=np.float32)
        obs[8] = 0   # NS green
        obs[9] = 15
        obs[0] = 10  # North
        obs[2] = 10  # South -> NS pressure = 20
        obs[1] = 2   # East
        obs[3] = 2   # West -> EW pressure = 4
        action, _ = c.predict(obs)
        assert action == 0

    def test_hysteresis(self):
        """EW pressure must exceed NS * 1.2 to trigger switch."""
        c = MaxPressureController()
        obs = np.zeros(10, dtype=np.float32)
        obs[8] = 0   # NS green
        obs[9] = 15
        obs[0] = 5   # NS pressure = 10
        obs[2] = 5
        obs[1] = 6   # EW pressure = 12 = 10 * 1.2, NOT greater
        obs[3] = 6
        action, _ = c.predict(obs)
        assert action == 0  # should NOT switch due to hysteresis

    def test_ew_phase_switch_to_ns(self):
        c = MaxPressureController()
        obs = np.zeros(10, dtype=np.float32)
        obs[8] = 2   # EW green
        obs[9] = 15
        obs[0] = 10  # NS pressure = 20
        obs[2] = 10
        obs[1] = 2   # EW pressure = 4
        obs[3] = 2
        action, _ = c.predict(obs)
        assert action == 1


class TestControllerIntegration:
    """Test controllers running against the actual environment."""

    @pytest.mark.parametrize("controller_cls,kwargs", [
        (FixedTimeController, {"green_time": 30}),
        (ActuatedController, {"min_green": 10, "max_green": 60}),
        (MaxPressureController, {}),
    ])
    def test_controller_runs_full_episode(self, controller_cls, kwargs):
        np.random.seed(0)
        env = TrafficSignalEnv(arrival_rates=[0.2, 0.2, 0.2, 0.2])
        controller = controller_cls(**kwargs)
        obs, _ = env.reset()
        total_steps = 200
        for _ in range(total_steps):
            action, _ = controller.predict(obs, env)
            assert action in (0, 1)
            obs, reward, terminated, truncated, info = env.step(action)
        assert info['vehicles_passed'] >= 0
        assert info['throughput'] >= 0

    def test_compare_controllers_returns_expected_rows(self):
        np.random.seed(0)
        env = TrafficSignalEnv(arrival_rates=[0.2, 0.2, 0.2, 0.2], episode_length=100)
        controllers = [
            FixedTimeController(green_time=30),
            ActuatedController(min_green=10, max_green=60),
            MaxPressureController(),
        ]
        results = compare_controllers(controllers, env, n_episodes=2)
        assert len(results) == 3
        assert {result["controller"] for result in results} == {
            "Fixed-Time",
            "Actuated",
            "Max-Pressure",
        }


class TestVisualization:
    def test_create_intersection_visualization(self):
        """Test that intersection visualization returns a PIL Image."""
        from PIL import Image
        env = TrafficSignalEnv()
        env.reset()
        for _ in range(10):
            env.step(0)
        img = create_intersection_visualization(env, 10)
        assert isinstance(img, Image.Image)
        assert img.width > 0
        assert img.height > 0

    def test_create_performance_plots(self):
        """Test that performance plots return a PIL Image."""
        from PIL import Image
        history = {
            'queue_lengths': [[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6]],
            'waiting_times': [[0.5, 1.0, 1.5, 2.0], [1.0, 1.5, 2.0, 2.5], [1.5, 2.0, 2.5, 3.0]],
            'throughput': [5, 10, 15],
        }
        img = create_performance_plots(history)
        assert isinstance(img, Image.Image)
        assert img.width > 0
        assert img.height > 0


class TestGradioFunctions:
    def test_run_simulation_fixed_time(self):
        np.random.seed(42)
        intersection_img, performance_img, summary = run_simulation(
            "Fixed-Time", 0.2, 0.2, 0.2, 0.2, 100, 30, 15, 45
        )
        from PIL import Image
        assert isinstance(intersection_img, Image.Image)
        assert isinstance(performance_img, Image.Image)
        assert "Simulation Complete" in summary
        assert "Fixed-Time" in summary

    def test_run_simulation_actuated(self):
        np.random.seed(42)
        _, _, summary = run_simulation(
            "Actuated", 0.25, 0.25, 0.25, 0.25, 100, 30, 15, 45
        )
        assert "Actuated" in summary

    def test_run_simulation_max_pressure(self):
        np.random.seed(42)
        _, _, summary = run_simulation(
            "Max-Pressure", 0.3, 0.2, 0.3, 0.2, 100, 30, 15, 45
        )
        assert "Max-Pressure" in summary

    def test_run_comparison(self):
        np.random.seed(42)
        result = run_comparison(0.25, 0.25, 0.25, 0.25, 100)
        assert "Controller Comparison" in result
        assert "Fixed-Time" in result
        assert "Actuated" in result
        assert "Max-Pressure" in result
        assert "|" in result

    def test_run_simulation_with_asymmetric_traffic(self):
        np.random.seed(42)
        _, _, summary = run_simulation(
            "Actuated", 0.4, 0.1, 0.4, 0.1, 200, 30, 10, 60
        )
        assert "Total Vehicles Passed" in summary
        assert "Throughput Rate" in summary


class TestEdgeCases:
    def test_zero_arrival_rate(self):
        """Environment with zero traffic should still work."""
        env = TrafficSignalEnv(arrival_rates=[0.0, 0.0, 0.0, 0.0])
        obs, _ = env.reset()
        for _ in range(50):
            obs, reward, _, _, info = env.step(0)
        assert info['vehicles_passed'] == 0
        assert all(len(q) == 0 for q in env.queues)

    def test_max_arrival_rate(self):
        """Environment with very high traffic should not crash."""
        env = TrafficSignalEnv(arrival_rates=[0.5, 0.5, 0.5, 0.5])
        obs, _ = env.reset()
        for _ in range(100):
            obs, reward, _, _, info = env.step(np.random.choice([0, 1]))
        assert np.isfinite(reward)

    def test_single_step(self):
        env = TrafficSignalEnv()
        obs, _ = env.reset()
        obs, reward, terminated, truncated, info = env.step(0)
        assert not terminated
        assert not truncated

    def test_repeated_resets(self):
        env = TrafficSignalEnv()
        for _ in range(5):
            obs, _ = env.reset()
            assert obs.shape == (10,)
            for _ in range(10):
                env.step(0)

    def test_all_actions_valid(self):
        env = TrafficSignalEnv()
        env.reset()
        for action in [0, 1]:
            obs, reward, _, _, _ = env.step(action)
            assert obs.shape == (10,)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
