# F1-NEAT



Data Collection

The DataProcessor class manages the collection and processing of telemetry data from a UDP packet sent by the game. It uses the collect_packet method to listen for UDP packets, process data based on packet IDs, and yield structured dictionaries. The listen_udp helper function handles UDP socket communication for various packet types, including car motion, lap data, telemetry data, and car status. The class converts raw binary data into attributes using predefined data classes. 

Data Processing

This module provides a structured approach to unpacking telemetry data. Each class interprets specific binary data packets from the game and converts them into dictionaries. The PacketHeader class extracts general information from the packet header, while CarMotionData, LapData, CarTelemetryData, and CarStatusData handle motion data, lap metrics, telemetry details, and car status indicators, respectively. 

Computer Vision (CV)

The ScreenProcessor class captures and processes screen frames to detect edges, key points, and lines within a specified region of interest (ROI). This functionality simulates sensors that respond to their position relative to detected lines, helping the model navigate the track. The process_frame method captures screen content, converts it to grayscale, applies Gaussian blur, and uses Canny edge detection. It then defines a polygonal ROI, applies a mask, detects lines using Hough Line Transform, and identifies contours. Key points are calculated and visual indicators are drawn on the frame, which is displayed in a resizable window. The method returns a dictionary with the status of detected points. The idea is to give the model some level of reference as to its positioning on the track.

Database

The MongoDB class offers an interface for managing a MongoDB database. It allows connection to a MongoDB server, creation and truncation of collections, and document insertion or retrieval. Key methods include open_connection, close_connection, insert_document, insert_documents, find_documents, and aggregate. All data from the telemetry processor, screen processor, and NEAT status are stored in the database.

Model Functions

The ModelFunctions class provides utility functions for interacting with the game using a simulated gamepad and keyboard inputs. It includes methods for handling activation functions (sig_soft), checking car position relative to a target (within_deviation), simulating keyboard inputs for game state management (escape_pits and reset_world), and calculating rewards based on game data (calculate_reward). The class also includes methods to perform actions based on computed outputs (perform_action), check if the game window is open (is_window_open), and unminimize the game window if needed (unminimize_window). These functions ensure the program continues running smoothly, even if the game window is minimized.

Plotting

The App class provides a graphical user interface for real-time data visualization using PyQt5 and PyQtGraph. It displays two line plots: one for the model's reward and another for its speed, updating dynamically based on data from a multiprocessing-safe queue. The application resets plot data when the genome ID changes and updates plot titles with information about the current generation, genome ID, and population number. The mean frame rate is shown in a label for performance monitoring. 

Main Loop

The main script integrates the components to create a system for training and evaluating NEAT algorithms in a simulated environment. It uses multiprocessing for concurrent data collection, screen processing, and NEAT training. 

Results

This project explores the feasibility of using unsupervised machine learning for self-driving within a video game. The model successfully trained for extended periods, but encountered challenges with game control dynamics, exploration vs. exploitation balance, and lighting variations. Notably, a supervised learning approach taken by a team of researchers at the University of Virginia (https://youtu.be/abdOnoe2f0A?si=tB0JFFl-ZyPLSPPL) demonstrated that success is possible by creating a model capable of doing pretty consistent laps. The next iteration will focus on using Assetto Corsa, a racing simulator with customizable tracks and more consistent lighting, inspired by successful applications in TrackMania (https://www.youtube.com/@yoshtm). 


Here's a link to one of its better runs on the Las Vegas Grand Prix circuit:  https://drive.google.com/file/d/1K67EZyzcwK1NMd-efDgeFeBLFa9zTYZs/view?usp=drive_link

