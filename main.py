import cv2
import numpy as np
import time

from colors import COLOR_RANGES, BOX_COLORS
from shape_detector import detect_shape



cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

MIN_AREA = 5000

cv2.namedWindow(
    "Real-Time Color & Shape Detection",
    cv2.WINDOW_NORMAL
)

cv2.resizeWindow(
    "Real-Time Color & Shape Detection",
    1280,
    720
)

previous_time = time.time()


while True:

    ret, frame = cap.read()

    if not ret:
        break

    current_time = time.time()
    fps = 1 / (current_time - previous_time)
    previous_time = current_time

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    color_counter = {
        name: 0 for name in COLOR_RANGES
    }

    total_objects = 0


    for color_name, ranges in COLOR_RANGES.items():

        mask = None

        for lower, upper in ranges:

            current_mask = cv2.inRange(
                hsv,
                lower,
                upper
            )

            if mask is None:
                mask = current_mask
            else:
                mask = cv2.bitwise_or(mask, current_mask)

        kernel = np.ones((5, 5), np.uint8)

        mask = cv2.morphologyEx(
            mask,
            cv2.MORPH_OPEN,
            kernel
        )

        mask = cv2.morphologyEx(
            mask,
            cv2.MORPH_CLOSE,
            kernel
        )

        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        for contour in contours:

            area = cv2.contourArea(contour)

            if area < MIN_AREA:
                continue

            color_counter[color_name] += 1
            total_objects += 1

            shape = detect_shape(contour)

            x, y, w, h = cv2.boundingRect(contour)

            center_x = x + w // 2
            center_y = y + h // 2

            color = BOX_COLORS[color_name]

            # Bounding Box
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                color,
                2
            )

            # Center
            cv2.circle(
                frame,
                (center_x, center_y),
                5,
                color,
                -1
            )

            # Color + Shape
            cv2.putText(
                frame,
                f"{color_name} {shape}",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,
                2
            )

            # Coordinates
            cv2.putText(
                frame,
                f"Center: ({center_x}, {center_y})",
                (x, y + h + 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                color,
                2
            )

            # Area
            cv2.putText(
                frame,
                f"Area: {int(area)}",
                (x, y + h + 45),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                color,
                2
            )



    overlay = frame.copy()

    cv2.rectangle(
        overlay,
        (10, 10),
        (320, 260),
        (40, 40, 40),
        -1
    )

    frame = cv2.addWeighted(
        overlay,
        0.75,
        frame,
        0.25,
        0
    )

    cv2.putText(
        frame,
        "Color & Shape Detection",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"FPS : {int(fps)}",
        (20, 70),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (0, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Objects : {total_objects}",
        (20, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 255),
        2
    )

    y = 135

    for name, count in color_counter.items():

        cv2.putText(
            frame,
            f"{name:<8}: {count}",
            (20, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.60,
            BOX_COLORS[name],
            2
        )

        y += 28


    cv2.imshow(
        "Real-Time Color & Shape Detection",
        frame
    )

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()