import keyboard
import time
import win32gui
import win32con
import numpy as np

class ModelFunctions:
    def __init__(self, gamepad):
        """
        Initialize ModelFunctions with a gamepad and set target positions and deviation.

        Args:
            gamepad (vgamepad.VX360Gamepad): The gamepad instance used for controlling the game.
        """
        self.gamepad = gamepad

        # Target position for the game object with allowed deviation
        self.target_position = {
            'world_position_x': -421,
            'world_position_y': -10,
            'world_position_z': 338
        }
        self.deviation = 20  # Allowed deviation in each dimension

    @staticmethod
    def sig_soft(input1):
        """
        Apply a custom activation function combining softmax and sigmoid functions.

        Args:
            input1 (np.ndarray or float): The input value(s) to be processed.

        Returns:
            tuple: Speed output and steering output, each consisting of action, probability, and intensity.
        """
        def softmax(x):
            """Compute softmax values for each row of x."""
            e_x = np.exp(x - np.max(x))
            return e_x / e_x.sum(axis=0)

        def sigmoid(x):
            """Sigmoid activation function with scaling."""
            scaled_x = (x - np.min(x)) / (np.max(x) - np.min(x) + 1e-10)  # Scale x to range [0, 1] with a small epsilon
            return 1 / (1 + np.exp(-scaled_x))

        alpha = 0.01  # Small constant for handling negative inputs

        # Process input1
        if isinstance(input1, np.ndarray):
            output1 = np.sum(np.where(input1 > 0, input1, alpha * input1))  # Apply ReLU with alpha
        else:
            output1 = max(0, input1) if input1 > 0 else alpha * input1

        combined_input = np.array([output1])  # Only one input

        # Initialize weights and biases for the output layer
        output_layer_weights = np.random.randn(4, 1)  # 4 output nodes, 1 input node
        output_layer_biases = np.zeros(4)  # Initialize biases with zeros

        # Calculate activations of the output layer
        output_activations = np.dot(output_layer_weights, combined_input) + output_layer_biases

        # Split the output activations into categorical outputs and intensities
        categorical_output_activations = output_activations
        intensity_output_activations = output_activations / 100  # Scale intensity to [0, 1]

        # Apply softmax activation function to categorical outputs
        categorical_probabilities = softmax(categorical_output_activations)

        # Apply sigmoid activation function to scaled intensity output activations
        intensity_values = sigmoid(intensity_output_activations)

        # Choose action with highest probability for steering
        steering_index = np.argmax(categorical_probabilities[:2])  # Selecting from the first two outputs
        steering_actions = ["a", "d", "none"]  # Actions for steering
        steering_action = steering_actions[steering_index]
        steering_prob = categorical_probabilities[steering_index]
        steering_intensity = intensity_values[steering_index]

        # Choose action with highest probability for speed
        speed_index = np.argmax(categorical_probabilities[2:]) + 2  # Selecting from the last two outputs
        speed_actions = ["w", "s", "none"]  # Actions for speed
        speed_action = speed_actions[speed_index - 2]
        speed_prob = categorical_probabilities[speed_index]
        speed_intensity = intensity_values[speed_index]

        steering_output = [steering_action, round(steering_prob, 2), round(steering_intensity, 2)]
        speed_output = [speed_action, round(speed_prob, 2), round(speed_intensity, 2)]

        # Return speed and steering outputs
        return speed_output, steering_output

    def within_deviation(self, current_state):
        """
        Check if the current state is within the allowed deviation from the target position.

        Args:
            current_state (dict): Dictionary containing current world positions.

        Returns:
            bool: True if current state is within deviation, False otherwise.
        """
        return (self.target_position['world_position_x'] - self.deviation <= current_state['world_position_x'] <=
                self.target_position['world_position_x'] + self.deviation) \
            and (self.target_position['world_position_y'] - self.deviation <= current_state['world_position_y'] <=
                 self.target_position['world_position_y'] + self.deviation) \
            and (self.target_position['world_position_z'] - self.deviation <= current_state['world_position_z'] <=
                 self.target_position['world_position_z'] + self.deviation)

    def escape_pits(self):
        """
        Simulate key presses to escape pits or reset situations in the game.
        """
        keyboard.press('enter')
        time.sleep(0.3)
        keyboard.release('enter')
        time.sleep(0.3)
        keyboard.press('enter')
        time.sleep(0.3)
        keyboard.release('enter')
        time.sleep(6)

    def reset_world(self):
        """
        Simulate key presses to reset the world or game state.
        """
        keyboard.press('esc')
        time.sleep(0.3)
        keyboard.release('esc')
        time.sleep(0.3)
        keyboard.press('enter')
        time.sleep(0.3)
        keyboard.release('enter')
        time.sleep(6)

    def calculate_reward(self, data):
        """
        Calculate the reward based on the provided game data.

        Args:
            data (dict): Dictionary containing various game metrics.

        Returns:
            float: Calculated reward based on the data.
        """
        try:
            reward = 1  # Initialize reward

            # Surface Type Reward/Penalty
            if data['surface_type'] > 0:
                reward -= 10
            else:
                reward += 1

            # Reward or penalty based on speed and gear
            if data['speed'] >= 100 and data['gear'] > 0:
                reward += data['speed'] * 0.01  # Positive reward for high speed
            else:
                reward -= data['speed']  # Penalty for low speed
                if data['speed'] == 0:
                    reward -= 1  # Additional penalty for zero speed

            # Penalty for invalid lap
            if data['current_lap_invalid'] == 1:
                reward -= 100

            # Reward based on lap distance
            reward += (data['lap_distance'] * 0.001)

            return reward

        except Exception as e:
            print(f"Error in calculate_reward: {e}")

    def perform_action(self, output):
        """
        Perform an action based on the given output using the gamepad.

        Args:
            output (list): List containing actions for speed and steering.

        Returns:
            list: The same output as received, with actions performed.
        """
        try:
            output = output[0]
            # Perform actions based on speed output
            if output[0][0] == "w":
                self.gamepad.right_trigger_float(output[0][2])
            elif output[0][0] == "s":
                self.gamepad.left_trigger_float(output[0][2])
            else:
                self.gamepad.left_trigger_float(0)

            # Perform actions based on steering output
            if output[1] == "a":
                output[1][2] = output[1][2] * -1
            elif output[1] == "none":
                output[1][2] = 0
            self.gamepad.left_joystick_float(output[1][2], 0)
            self.gamepad.update()

            return output

        except Exception as e:
            print(f"Error in perform_action: {e}")
        finally:
            self.gamepad.reset()

    @staticmethod
    def is_window_open():
        """
        Check if the game window is open and not minimized.

        Returns:
            bool: True if the game window is open, False otherwise.
        """
        hwnd = win32gui.FindWindow(None, "F1 23")
        if hwnd != 0:
            window_state = win32gui.GetWindowPlacement(hwnd)[1]
            return window_state != 2  # Return True if window is not minimized
        return False

    @staticmethod
    def unminimize_window():
        """
        Restore and bring the game window to the foreground if it is minimized.
        """
        hwnd = win32gui.FindWindow(None, "F1 23")
        if hwnd != 0:
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            time.sleep(4)
            keyboard.press('esc')
