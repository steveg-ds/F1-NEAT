import keyboard
import time
import win32gui
import win32con
import numpy as np
class ModelFunctions:
    def __init__(self, gamepad):
        self.gamepad = gamepad

        self.target_position = {
            'world_position_x': -421,
            'world_position_y': -10,
            'world_position_z': 338
        }
        self.deviation = 20  # Allowed deviation in each dimension

    @staticmethod
    def sig_soft(input1):
        def softmax(x):
            """Compute softmax values for each row of x."""
            e_x = np.exp(x - np.max(x))
            return e_x / e_x.sum(axis=0)

        def sigmoid(x):
            """Sigmoid activation function with scaling."""
            scaled_x = (x - np.min(x)) / (
                    np.max(x) - np.min(x) + 1e-10)  # Scale x to range [0, 1] with a small epsilon added
            return 1 / (1 + np.exp(-scaled_x))

        alpha = 0.01

        # Process input1
        if isinstance(input1, np.ndarray):
            output1 = np.sum(np.where(input1 > 0, input1, alpha * input1))
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
        intensity_output_activations = output_activations / 100  # Scale intensity to [0, 1] based on the same activations

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
        speed_actions = ["w", "s", "none"]  # Actions for speed  "s",
        speed_action = speed_actions[speed_index - 2]
        speed_prob = categorical_probabilities[speed_index]
        speed_intensity = intensity_values[speed_index]

        steering_output = [steering_action, round(steering_prob, 2), round(steering_intensity, 2)]
        speed_output = [speed_action, round(speed_prob, 2), round(speed_intensity, 2)]

        # Return speed and steering outputs
        return speed_output, steering_output

    def within_deviation(self, current_state):
        return (self.target_position['world_position_x'] - self.deviation <= current_state['world_position_x'] <=
                self.target_position['world_position_x'] + self.deviation) \
            and (self.target_position['world_position_y'] - self.deviation <= current_state['world_position_y'] <=
                 self.target_position['world_position_y'] + self.deviation) \
            and (self.target_position['world_position_z'] - self.deviation <= current_state['world_position_z'] <=
                 self.target_position['world_position_z'] + self.deviation)

    def escape_pits(self):
        keyboard.press('enter')
        time.sleep(0.3)
        keyboard.release('enter')
        time.sleep(0.3)
        keyboard.press('enter')
        time.sleep(0.3)
        keyboard.release('enter')
        time.sleep(6)

    def reset_world(self):
        keyboard.press('esc')
        time.sleep(0.3)
        keyboard.release('esc')
        time.sleep(0.3)
        keyboard.press('enter')
        time.sleep(0.3)
        keyboard.release('enter')
        time.sleep(6)

    def calculate_reward(self, data):
        try:
            reward = 1

            # Surface Type Reward/Penalty
            if data['surface_type'] > 0:
                reward -= 10
            else:
                reward += 1

            if data['speed'] >= 100 and data['gear'] > 0:
                reward += data['speed'] * 0.01  # Adjusted scaling factor
            else:
                reward -= data['speed']
                if data['speed'] == 0:
                    reward -= 1  # Adjusted penalty

            if data['current_lap_invalid'] == 1:
                reward -= 100

            reward += (data['lap_distance'] * 0.001)


            return reward

        except Exception as e:
            print("Error in calculate_reward:", e)

    def perform_action(self, output):
        try:
            output = output[0]
            if output[0][0] == "w":
                self.gamepad.right_trigger_float(output[0][2])
            elif output[0][0] == "s":
                self.gamepad.left_trigger_float(output[0][2])
            else:
                self.gamepad.left_trigger_float(0)

            if output[1] == "a":
                output[1][2] = output[1][2] * -1
            elif output[1] == "none":
                output[1][2] = 0
            self.gamepad.left_joystick_float(output[1][2], 0)
            self.gamepad.update()
            # time.sleep(0.16)
            return output

        except Exception as e:
            print("Error in perform_action:", e)
        finally:
            self.gamepad.reset()

    @staticmethod
    def is_window_open():
        hwnd = win32gui.FindWindow(None, "F1 23")
        if hwnd != 0:
            window_state = win32gui.GetWindowPlacement(hwnd)[1]
            return window_state != 2  # Return True if window is not minimized
        return False

    @staticmethod
    def unminimize_window():
        hwnd = win32gui.FindWindow(None, "F1 23")
        if hwnd != 0:
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            time.sleep(4)
            keyboard.press('esc')
            # time.sleep(0.2)
            # keyboard.release('enter')

    # def calculate_reward(self, data):
    #     try:
    #         reward = 1
    #
    #         # Surface Type Reward/Penalty
    #         if data['surface_type'] > 0:
    #             reward -= 10
    #         else:
    #             reward += 1
    #
    #         # Speed Reward/Penalty
    #         if data['speed'] >= 20 and data['gear'] > 0:
    #             reward += data['speed'] * 0.01  # Adjusted scaling factor
    #         else:
    #             reward -= data['speed']
    #             if data['speed'] == 0:
    #                 reward -= 20  # Adjusted penalty
    #
    #         # Lateral G-Force Reward/Penalty
    #         if data['g_force_lateral'] > 0:
    #             reward += 1
    #         else:
    #             reward -= 1  # Adjusted penalty
    #
    #         # Gear Bonus Reward/Penalty
    #         if data['gear'] <= 0:
    #             reward -= data['speed']
    #         else:
    #             reward += (0.01 * data['gear'])
    #
    #         # Pits Penalty/Reward
    #         if (round(data['world_position_x']), round(data['world_position_y']), round(data['world_position_z'])) == (
    #                 -421, -11, 339.):
    #             reward -= 1
    #         else:
    #             reward += 1  # Adjusted reward
    #
    #         # Lap Distance Reward
    #         reward += (data['lap_distance'] * 0.001)
    #         # print(reward)
    #         return reward
    #
    #     except Exception as e:
    #         print("Error in calculate_reward:", e)