import pandas as pd
import cv2 as cv
import numpy as np
from PIL import ImageGrab
import time


class ScreenProcessor:
    """
    Class for processing screen recordings.
    """

    @staticmethod
    def process_frame():
        """
        Processes a single frame from the screen recording, detects edges, applies a region of interest (ROI),
        and identifies key points and lines. Visual indicators are drawn based on the detected features.
        
        Returns:
            dict: A dictionary containing the status of detected points (left, right, midleft, midright).
        """
        # Capture the screen within the specified bounding box
        frame = np.array(ImageGrab.grab(bbox=(0, 0, 1920, 1080)))
        
        # Convert the frame to RGB format
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        
        # Convert the frame to grayscale
        processed_frame = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)
        
        # Apply Gaussian blur to the grayscale frame
        processed_frame = cv.GaussianBlur(processed_frame, (5, 5), 5)

        # Define the region of interest (ROI) as a polygon
        polygons = np.array([[(380, 600), (1640, 600), (1640, 500), (380, 500)]])

        # Apply Canny edge detection to the blurred frame
        processed_frame = cv.Canny(processed_frame, 100, 150)

        # Create a mask for the ROI
        mask = np.zeros_like(processed_frame)
        cv.fillPoly(mask, [polygons], 255)

        # Apply the mask to the edge-detected frame
        masked_frame = cv.bitwise_and(processed_frame, mask)

        # Detect lines using Hough transform
        lines = cv.HoughLinesP(masked_frame, 2, np.pi / 180, 100, np.array([]), minLineLength=125, maxLineGap=10)

        # Find contours in the masked frame
        contours, _ = cv.findContours(masked_frame, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        all_points = []

        # Collect mean points from contours
        if contours is not None:
            for contour in contours:
                contour = np.mean(contour, axis=1)
                all_points.extend(contour)

        # Collect points and vectorized lines from the detected lines
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line.reshape(4)
                all_points.extend([(x1, y1), (x2, y2), (x2 - x1, y2 - y1)])

        all_points = np.array(all_points)

        try:
            # Filter points for the right and left sections
            right_points = [point for point in all_points if 1400 > point[0] > 1020]
            right_points = np.asarray(right_points)

            left_points = [point for point in all_points if 520 < point[0] < 900]
            left_points = np.asarray(left_points)

            # Calculate percentiles for right points
            if len(right_points) > 2:
                rq1, rq2, rq3, rq4, rq5 = np.percentile(right_points, [0, 25, 50, 75, 100], axis=0).astype(int)
            else:
                rq1 = (1650, 500)

            # Calculate percentiles for left points
            if len(left_points) > 2:
                lq1, lq2, lq3, lq4, lq5 = np.percentile(left_points, [0, 25, 50, 75, 100], axis=0).astype(int)
            else:
                lq4 = (370, 500)

            # Colors for visual indicators
            on_color = (0, 0, 255)
            off_color = (255, 255, 255)

            # Initialize data dictionary
            data = {
                "left": 0,
                'right': 0,
                "midleft": 0,
                'midright': 0,
            }

            # Process and draw left point indicator
            left_point = (380, 540)
            if left_point[0] > lq4[0]:
                color = off_color
            else:
                data['left'] = 1
                color = on_color
            cv.circle(frame, left_point, 10, color, -1)
            cv.line(frame, (960, 820), left_point, color, 2)

            # Process and draw mid-left point indicator
            midleft_point = (700, 540)
            if midleft_point[0] > lq4[0]:
                color = off_color
            else:
                data['midleft'] = 1
                color = on_color
            cv.circle(frame, midleft_point, 10, color, -1)
            cv.line(frame, (960, 820), midleft_point, color, 2)

            # Process and draw right point indicator
            right_point = (1640, 540)
            if right_point[0] < rq1[0]:
                color = off_color
            else:
                data['right'] = 1
                color = on_color
            cv.circle(frame, right_point, 10, color, -1)
            cv.line(frame, (960, 820), right_point, color, 2)

            # Process and draw mid-right point indicator
            midright_point = (1220, 540)
            if midright_point[0] < rq1[0]:
                color = off_color
            else:
                data['midright'] = 1
                color = on_color
            cv.circle(frame, midright_point, 10, color, -1)
            cv.line(frame, (960, 820), midright_point, color, 2)

            # Draw a circle at the center
            cv.circle(frame, (960, 820), 10, color, -1)

            # Display the frame with visual indicators
            cv.imshow('Computer Vision', cv.resize(frame, (1280, 720)))
            cv.waitKey(33)

            return data
        except Exception as e:
            print(e)
