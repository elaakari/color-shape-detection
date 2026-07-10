import numpy as np

COLOR_RANGES = {
    "Red": [
        (
            np.array([0, 120, 70]),
            np.array([10, 255, 255])
        ),
        (
            np.array([170, 120, 70]),
            np.array([180, 255, 255])
        )
    ],

    "Green": [
        (
            np.array([35, 80, 80]),
            np.array([85, 255, 255])
        )
    ],

    "Blue": [
        (
            np.array([100, 150, 50]),
            np.array([140, 255, 255])
        )
    ],

    "Yellow": [
        (
            np.array([20, 100, 100]),
            np.array([35, 255, 255])
        )
    ],

    "Orange": [
        (
            np.array([10, 100, 100]),
            np.array([20, 255, 255])
        )
    ],

    "Purple": [
        (
            np.array([140, 80, 80]),
            np.array([165, 255, 255])
        )
    ]
}

# Rectangle colors (BGR)

BOX_COLORS = {
    "Red": (0, 0, 255),
    "Green": (0, 255, 0),
    "Blue": (255, 0, 0),
    "Yellow": (0, 255, 255),
    "Orange": (0, 165, 255),
    "Purple": (255, 0, 255)
}