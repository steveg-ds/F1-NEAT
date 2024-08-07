# F1-NEAT



Data Collection

The DataProcessor class manages the collection and processing of telemetry data from a UDP packet sent by the game. It uses the collect_packet method to listen for UDP packets, process data based on packet IDs, and yield structured data dictionaries. The listen_udp helper function handles UDP socket communication for various packet types, including car motion, lap data, telemetry data, and car status. The class converts raw binary data into meaningful attributes using predefined data classes (e.g., CarMotionData, LapData, CarTelemetryData, and CarStatusData), and supports data aggregation, such as summing surface type values for analysis. It also includes error handling for robust real-time telemetry analysis.

Data Processing

This module provides a structured approach to unpacking telemetry data. Each class interprets specific binary data packets from the game and converts them into dictionaries. The PacketHeader class extracts general information from the packet header, while CarMotionData, LapData, CarTelemetryData, and CarStatusData handle motion data, lap metrics, telemetry details, and car status indicators, respectively. PacketLapData and PacketCarMotionData aggregate these details for multiple cars, facilitating easy analysis and visualization. Each class includes a to_dict method for straightforward data conversion.

CV

The ScreenProcessor class captures and processes screen frames to detect edges, key points, and lines within a specified region of interest (ROI). This functionality simulates sensors that respond to their position relative to detected lines, helping the model navigate the track. The process_frame method captures screen content, converts it to grayscale, applies Gaussian blur, and uses Canny edge detection. It then defines a polygonal ROI, applies a mask, detects lines using Hough Line Transform, and identifies contours. Key points are calculated and visual indicators are drawn on the frame, which is displayed in a resizable window. The method returns a dictionary with the status of detected points.

Database

The MongoDB class offers an interface for managing a MongoDB database. It allows connection to a MongoDB server, creation and truncation of collections, and document insertion or retrieval. Key methods include open_connection, close_connection, insert_document, insert_documents, find_documents, and aggregate. The class supports flexible operations on specified collections and various query and aggregation tasks, making it a valuable tool for integrating MongoDB functionality into applications. All data from the telemetry processor, screen processor, and NEAT status are stored in the database.

Model Functions

The ModelFunctions class provides utility functions for interacting with the game using a simulated gamepad and keyboard inputs. It includes methods for handling activation functions (sig_soft), checking car position relative to a target (within_deviation), simulating keyboard inputs for game state management (escape_pits and reset_world), and calculating rewards based on game data (calculate_reward). The class also includes methods to perform actions based on computed outputs (perform_action), check if the game window is open (is_window_open), and unminimize the game window if needed (unminimize_window). These functions ensure the program continues running smoothly, even if the game window is minimized.

Plotting
The App class provides a graphical user interface for real-time data visualization using PyQt5 and PyQtGraph. It displays two line plots: one for the model's reward and another for its speed, updating dynamically based on data from a multiprocessing-safe queue. The application resets plot data when the genome ID changes and updates plot titles with information about the current generation, genome ID, and population number. The mean frame rate is shown in a label for performance monitoring. The GUI components are styled and updated periodically to refresh the plots and label.

Main Loop
The main script integrates the components to create a system for training and evaluating NEAT algorithms in a simulated environment. It uses multiprocessing for concurrent data collection, screen processing, and NEAT training. Key functions include collect_packet_process for game data collection, process_screen_process for screen data capture, and process_neat_process for NEAT algorithm management. Data is stored in a MongoDB database, and genome rewards and speeds are visualized using the PyQt5 application. The script includes robust process management and exception handling.

Results
This project explores the feasibility of using unsupervised machine learning for self-driving within a video game context. The model successfully trained for extended periods, but encountered challenges with game control dynamics, exploration vs. exploitation balance, and lighting variations. Notably, a related supervised learning approach at the University of Virginia demonstrated effective results in a similar game version. Future efforts will focus on using Assetto Corsa, a racing simulator with customizable tracks and more consistent lighting, inspired by successful applications in TrackMania.