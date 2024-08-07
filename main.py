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
from CV_2 import ScreenProcessor
import keyboard
from db import MongoDB

from plotting import App
from PyQt5.QtWidgets import QApplication
import neat


def cleanup_processes(collect, screen, neat):
    print("Cleaning up processes...")
    collect.terminate()
    screen.terminate()
    neat.terminate()

def collect_packet_process(result_queue, data_processor):
    while True:
        for game_data in data_processor.collect_packet():
            result_queue.put(game_data)
            if result_queue.qsize() == 99:
                result_queue.get()


def process_screen_process(result_queue, screen_processor):
    while True:
        try:
            screen_data = screen_processor.process_frame()
            result_queue.put(screen_data)
            if result_queue.qsize() == 99:
                result_queue.get()
        except Exception as e:
            print("Error in process_screen_process: %s", e)


def process_neat_process(result_queue_neat, result_queue_collect, result_queue_screen):
    """
    Train the NEAT algorithm using your evaluation function.
    """

    def eval_genomes(genomes, config):
        """

        Evaluate genomes using your existing while loop.
        """
        pop = 0

        for genome_id, genome in genomes:
            total_reward = [0]
            pop += 1
            start_time = time.time()
            run_time = 15 + (p.generation * 5) if p.generation < 20 else 120
            while time.time() - start_time <= run_time and np.mean(total_reward) >= -2:
                it_time = time.time()
                if not mf.is_window_open():
                    mf.unminimize_window()

                try:
                    individual = neat.nn.RecurrentNetwork.create(genome, config)
                    screen_data = result_queue_screen.get()
                    game_data = result_queue_collect.get()
                    game_data.update(screen_data)
                    action = individual.activate(list(game_data.values()))
                    press = mf.perform_action(action)
                    total_reward.append(mf.calculate_reward(game_data))

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
                    data_collection.insert_document(data)
                    result_queue_neat.put(data)


                    if result_queue_neat.qsize() == 5:
                        result_queue_neat.get()

                    if mf.within_deviation(data):
                        mf.escape_pits()
                    time.sleep(0.1)
                    # print(round(np.mean(total_reward), 2))
                    # print(f"Screen Queue: {result_queue_screen.qsize()}, "
                    #       f"Game Queue: {result_queue_collect.qsize()}, NEAT Queue: {result_queue_neat.qsize()},"
                    #       f"Iteration Time: {time.time() - it_time}")

                except Exception as e:
                    print("Error in main neat loop: %s", e)
                    break
            else:
                genome.fitness = np.mean(total_reward) + ((time.time() - start_time) * 0.1)
                if not mf.within_deviation(data):
                    keyboard.press('esc')
                    time.sleep(0.3)
                    keyboard.release('esc')
                    time.sleep(0.3)
                    keyboard.press('enter')
                    time.sleep(0.3)
                    keyboard.release('enter')
                    time.sleep(10)

    gamepad = vg.VX360Gamepad()
    mf = ModelFunctions(gamepad)

    data_collection = MongoDB(host='localhost', port=27017, db_name='Goatifi_3', collection_name=f"Goatifi")
    local_dir = os.path.dirname(__file__)
    config_file = os.path.join(local_dir, 'neat_config.cfg')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    config.genome_config.add_activation("sig_soft_act", mf.sig_soft)
    p = neat.Population(config)

    # p = neat.Checkpointer.restore_checkpoint("neat_models/29")
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1, filename_prefix="neat_models/"))



    try:
        data_collection.open_connection()
        # client.start_stream()
        winner = p.run(eval_genomes, 100)
        return winner
    except Exception as e:
        print("error running neat:", e)
    except KeyboardInterrupt:
        data_collection.close_connection()
        collect_process.terminate()
        screen_process.terminate()
        neat_process.terminate()
        sys.exit(0)
    finally:
        data_collection.close_connection()
        data_collection.close_connection()
        collect_process.terminate()
        screen_process.terminate()
        neat_process.terminate()
        sys.exit(0)


if __name__ == "__main__":
    screen_processor = ScreenProcessor()
    data_processor = DataProcessor()

    result_queue_collect = multiprocessing.Queue(maxsize=100)
    result_queue_screen = multiprocessing.Queue(maxsize=100)
    result_queue_neat = multiprocessing.Queue(maxsize=100)

    collect_process = multiprocessing.Process(target=collect_packet_process,
                                              args=(result_queue_collect, data_processor))
    screen_process = multiprocessing.Process(target=process_screen_process,
                                             args=(result_queue_screen, screen_processor))
    neat_process = multiprocessing.Process(target=process_neat_process,
                                           args=(result_queue_neat, result_queue_collect, result_queue_screen))

    atexit.register(lambda: cleanup_processes(collect_process, screen_process, neat_process))

    collect_process.start()
    screen_process.start()
    neat_process.start()

    # TODO: everything else seems to be working okay but the plot is fucked
    app = QApplication(sys.argv)
    thisapp = App(result_queue_neat)
    thisapp.show()
    sys.exit(app.exec_())
