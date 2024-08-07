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
        frame = np.array(ImageGrab.grab(bbox=(0, 0, 1920, 1080)))
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        processed_frame = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)
        processed_frame = cv.GaussianBlur(processed_frame, (5, 5), 5)

        polygons = np.array([[(380, 600), (1640, 600), (1640, 500), (380, 500)]])

        # Apply Canny edge detection to the original grayscale frame
        processed_frame = cv.Canny(processed_frame, 100, 150)

        # Create mask for ROI
        mask = np.zeros_like(processed_frame)
        cv.fillPoly(mask, [polygons], 255)

        # Apply mask to edge-detected frame
        masked_frame = cv.bitwise_and(processed_frame, mask)

        # Detect lines using Hough transform
        lines = cv.HoughLinesP(masked_frame, 2, np.pi / 180, 100, np.array([]), minLineLength=125, maxLineGap=10)

        contours, _ = cv.findContours(masked_frame, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        all_points = []

        if contours is not None:
            for contour in contours:
                contour = np.mean(contour, axis=1)
                all_points.extend(contour)

        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line.reshape(4)
                all_points.extend([(x1, y1), (x2, y2), (x2 - x1, y2 - y1)])

        all_points = np.array(all_points)

        try:
            right_points = [point for point in all_points if 1400 > point[0] > 1020]
            right_points = np.asarray(right_points)

            left_points = [point for point in all_points if 520 < point[0] < 900]
            left_points = np.asarray(left_points)

            if len(right_points) > 2:
                rq1, rq2, rq3, rq4, rq5 = np.percentile(right_points, [0, 25, 50, 75, 100], axis=0).astype(int)
                # cv.line(frame, (1400, 700), rq5, (255, 255, 255), thickness=10)
                # cv.line(frame, rq1, rq2, (255, 255, 255), thickness=10)
                # cv.line(frame, rq2, rq3, (255, 255, 255), thickness=10)
                # cv.line(frame, rq3, rq4, (255, 255, 255), thickness=10)
                # cv.line(frame, rq4, rq5, (255, 255, 255), thickness=10)
            else:
                # cv.line(frame, (1640, 600), (1640, 800), (255, 255, 255), thickness=10)
                rq1 = (1650, 500)

            if len(left_points) > 2:
                lq1, lq2, lq3, lq4, lq5 = np.percentile(left_points, [0, 25,50 ,75, 100], axis=0).astype(int)
                # cv.line(frame, (500, 700), lq5, (255, 255, 255), thickness=10)
                # cv.line(frame, lq1, lq2, (255, 255, 255), thickness=10)
                # cv.line(frame, lq2, lq3, (255, 255, 255), thickness=10)
                # cv.line(frame, lq3, lq4, (255, 255, 255), thickness=10)
                # cv.line(frame, lq4, lq5, (255, 255, 255), thickness=10)
            else:
                # cv.line(frame, (540, 600), (540, 800), (255, 255, 255), thickness=10)
                lq4 = (370, 500)

            on_color = (0, 0, 255)
            off_color = (255, 255, 255)

            data = {"left": 0,
                    'right': 0,
                    "midleft": 0,
                    'midright': 0,
                    # 'center': 0
                    }

            left_point = (380, 540)
            if left_point[0] > lq4[0]:
                color = off_color
            else:
                data['left'] = 1
                color = on_color
            cv.circle(frame, left_point, 10, color, -1)
            cv.line(frame, (960, 820), left_point, color, 2)

            midleft_point = (700, 540)
            if midleft_point[0] > lq4[0]:
                color = off_color
            else:
                data['midleft'] = 1
                color = on_color
            cv.circle(frame, midleft_point, 10, color, -1)
            cv.line(frame, (960, 820), midleft_point, color, 2)

            right_point = (1640, 540)
            if right_point[0] < rq1[0]:
                color = off_color
            else:
                data['right'] = 1
                color = on_color
            cv.circle(frame, right_point, 10, color, -1)
            cv.line(frame, (960, 820), right_point, color, 2)

            midright_point = (1220, 540)
            if midright_point[0] < rq1[0]:
                color = off_color
            else:
                data['midright'] = 1
                color = on_color
            cv.circle(frame, midright_point, 10, color, -1)
            cv.line(frame, (960, 820), midright_point, color, 2)

            # center_point = (960, 540)
            # if center_point[0] < rq1[0]:
            #     color = off_color
            # else:
            #     data['center'] = 1
            #     color = on_color
            # cv.circle(frame, center_point, 10, color, -1)
            # cv.line(frame, (960, 820), center_point, color, 2)



            cv.circle(frame, (960, 820), 10, color, -1)
            # cv.imshow('Processed Frame', cv.resize(masked_frame, (640, 360)))
            cv.imshow('Computer Vision', cv.resize(frame, (1280, 720)))
            # cv.imshow('Computer Vision', frame)
            cv.waitKey(33)

            # print(data)

            return data
        except Exception as e:
            print(e)

# while True:
#     screen_processor = ScreenProcessor()
#     screen_processor.process_frame()
