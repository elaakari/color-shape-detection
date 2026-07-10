import cv2
import math


def detect_shape(contour):
    """
    Detect the geometric shape of a contour.

    Returns
    -------
    str
        Shape name.
    """

    # Ignore tiny contours
    area = cv2.contourArea(contour)

    if area < 100:
        return "Unknown"

    # Convex Hull -> more robust contour
    hull = cv2.convexHull(contour)

    perimeter = cv2.arcLength(hull, True)

    if perimeter == 0:
        return "Unknown"

    # Polygon approximation
    approx = cv2.approxPolyDP(
        hull,
        0.02 * perimeter,
        True
    )

    vertices = len(approx)

    # Circularity
    circularity = (4 * math.pi * area) / (perimeter * perimeter)
    

    # -----------------------------
    # Triangle
    # -----------------------------
    if vertices == 3:
        return "Triangle"

    # -----------------------------
    # Square / Rectangle
    # -----------------------------
    elif vertices == 4:

        x, y, w, h = cv2.boundingRect(approx)

        aspect_ratio = w / float(h)

        if 0.95 <= aspect_ratio <= 1.05:
            return "Square"
        else:
            return "Rectangle"

    # -----------------------------
    # Pentagon
    # -----------------------------
    elif vertices == 5:
        return "Pentagon"

    # -----------------------------
    # Hexagon
    # -----------------------------
    elif vertices == 6:
        return "Hexagon"

    # -----------------------------
    # Circle Detection
    # -----------------------------
    else:

        if circularity > 0.80:
            return "Circle"

        elif vertices >= 8:
            return "Ellipse"

        return "Polygon"