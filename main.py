import time
import os
import multiprocessing
import atexit
import sys
from bson import ObjectId
import numpy as np
import vgamepad as vg
from model_functions import ModelFunctions
from data_processing import DataProcessor
from CV import ScreenProcessor
import keyboard
from db import MongoDB

from plotting import App
from PyQt5.QtWidgets import QApplication
import neat

def cleanup_processes(collect, screen, neat):
    """
    Terminate the given processes and perform cleanup.

    Args:
        collect (multiprocessing.Process): The process collecting packet data.
        screen (multiprocessing.Process): The process processing screen data.
        neat (multiprocessing.Process): The process running the NEAT algorithm.
    """
    print("Cleaning up processes...")
    collect.terminate()  # Terminate the packet collection process
    screen.terminate()   # Terminate the screen processing process
    neat.terminate()     # Terminate the NEAT algorithm process

def collect_packet_process(result_queue, data_processor):
    """
    Process to collect packet data from the DataProcessor and put it into a queue.

    Args:
        result_queue (multiprocessing.Queue): The queue to put collected data into.
        data_processor (DataProcessor): The instance of DataProcessor to collect packet data.
    """
    while True:
        # Collect game data from DataProcessor and put it into the result queue
        for game_data in data_processor.collect_packet():
            result_queue.put(game_data)
            # Maintain a maximum queue size to avoid excessive memory usage
            if result_queue.qsize() == 99:
                result_queue.get()

def process_screen_process(result_queue, screen_processor):
    """
    Process to capture and process screen data from ScreenProcessor and put it into a queue.

    Args:
        result_queue (multiprocessing.Queue): The queue to put screen data into.
        screen_processor (ScreenProcessor): The instance of ScreenProcessor to process screen data.
    """
    while True:
        try:
            # Capture and process a single frame from the screen
            screen_data = screen_processor.process_frame()
            result_queue.put(screen_data)
            # Maintain a maximum queue size to avoid excessive memory usage
            if result_queue.qsize() == 99:
                result_queue.get()
        except Exception as e:
            print(f"Error in process_screen_process: {e}")

def process_neat_process(result_queue_neat, result_queue_collect, result_queue_screen):
    """
    Process to run the NEAT algorithm, evaluating genomes and interacting with the game.

    Args:
        result_queue_neat (multiprocessing.Queue): The queue to put NEAT results into.
        result_queue_collect (multiprocessing.Queue): The queue containing collected game data.
        result_queue_screen (multiprocessing.Queue): The queue containing screen data.
    """
    def eval_genomes(genomes, config):
        """
        Evaluate NEAT genomes and update their fitness.

        Args:
            genomes (list of tuple): A list of genome ID and genome pairs.
            config (neat.Config): The NEAT configuration object.
        """
        pop = 0

        for genome_id, genome in genomes:
            total_reward = [0]  # Initialize list to keep track of total rewards
            pop += 1
            start_time = time.time()  # Record the start time
            run_time = 15 + (p.generation * 5) if p.generation < 20 else 120  # Set runtime based on generation

            while time.time() - start_time <= run_time and np.mean(total_reward) >= -2:
                it_time = time.time()  # Record iteration time
                if not mf.is_window_open():  # Ensure the game window is open
                    mf.unminimize_window()

                try:
                    # Create a neural network from the genome
                    individual = neat.nn.RecurrentNetwork.create(genome, config)
                    screen_data = result_queue_screen.get()  # Retrieve screen data from the queue
                    game_data = result_queue_collect.get()  # Retrieve game data from the queue
                    game_data.update(screen_data)  # Combine game data with screen data
                    action = individual.activate(list(game_data.values()))  # Compute action using the neural network
                    press = mf.perform_action(action)  # Perform the action in the game
                    total_reward.append(mf.calculate_reward(game_data))  # Calculate and append reward

                    # Update game data with additional information
                    game_data.update({
                        'steer_action': press[0][0],
                        "steer_prop": press[0][1],
                        "steer_intensity": press[0][2],
                        'speed_action': press[1][0],
                        "speed_prop": press[1][1],
                        "speed_intensity": press[1][2],
                        'reward': np.mean(total_reward),
                        'elapsed_time': time.time() - start_time
                    })
                    data = {"_id": ObjectId(), "generation": p.generation, 'genome_id': genome_id,
                            "pop_num": pop,
                            **game_data}
                    data_collection.insert_document(data)  # Insert data into MongoDB
                    result_queue_neat.put(data)  # Put data into the NEAT results queue

                    # Maintain a maximum queue size to avoid excessive memory usage
                    if result_queue_neat.qsize() == 5:
                        result_queue_neat.get()

                    # Ensure the agent stays within deviation limits and handles special cases
                    if mf.within_deviation(data):
                        mf.escape_pits()
                    time.sleep(0.1)  # Small delay to avoid overloading the system

                except Exception as e:
                    print(f"Error in main neat loop: {e}")
                    break
            else:
                # Set the fitness of the genome based on rewards and elapsed time
                genome.fitness = np.mean(total_reward) + ((time.time() - start_time) * 0.1)
                if not mf.within_deviation(data):
                    # Handle cases where the agent is not within deviation limits
                    keyboard.press('esc')
                    time.sleep(0.3)
                    keyboard.release('esc')
                    time.sleep(0.3)
                    keyboard.press('enter')
                    time.sleep(0.3)
                    keyboard.release('enter')
                    time.sleep(10)

    # Initialize gamepad and model functions
    gamepad = vg.VX360Gamepad()
    mf = ModelFunctions(gamepad)

    # Initialize MongoDB connection
    data_collection = MongoDB(host='localhost', port=27017, db_name='Goatifi', collection_name=f"Goatifi")
    local_dir = os.path.dirname(__file__)
    config_file = os.path.join(local_dir, 'neat_config.cfg')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    config.genome_config.add_activation("sig_soft_act", mf.sig_soft)
    p = neat.Population(config)

    # Add reporters for logging and checkpointing NEAT process
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1, filename_prefix="neat_models/"))

    try:
        data_collection.open_connection()  # Open connection to MongoDB
        winner = p.run(eval_genomes, 100)  # Run NEAT algorithm
        return winner
    except Exception as e:
        print(f"Error running NEAT: {e}")
    except KeyboardInterrupt:
        # Handle keyboard interrupt gracefully
        data_collection.close_connection()
        collect_process.terminate()
        screen_process.terminate()
        neat_process.terminate()
        sys.exit(0)
    finally:
        # Ensure all resources are cleaned up properly
        data_collection.close_connection()
        collect_process.terminate()
        screen_process.terminate()
        neat_process.terminate()
        sys.exit(0)

if __name__ == "__main__":
    # Create instances of data processors
    screen_processor = ScreenProcessor()
    data_processor = DataProcessor()

    # Create queues for inter-process communication
    result_queue_collect = multiprocessing.Queue(maxsize=100)
    result_queue_screen = multiprocessing.Queue(maxsize=100)
    result_queue_neat = multiprocessing.Queue(maxsize=100)

    # Create and start processes for collecting data, processing screen, and running NEAT
    collect_process = multiprocessing.Process(target=collect_packet_process,
                                              args=(result_queue_collect, data_processor))
    screen_process = multiprocessing.Process(target=process_screen_process,
                                             args=(result_queue_screen, screen_processor))
    neat_process = multiprocessing.Process(target=process_neat_process,
                                           args=(result_queue_neat, result_queue_collect, result_queue_screen))

    # Register cleanup function to ensure proper resource release
    atexit.register(lambda: cleanup_processes(collect_process, screen_process, neat_process))

    collect_process.start()
    screen_process.start()
    neat_process.start()

    # Start the PyQt5 application for plotting results
    app = QApplication(sys.argv)
    thisapp = App(result_queue_neat)
    thisapp.show()
    sys.exit(app.exec_())
