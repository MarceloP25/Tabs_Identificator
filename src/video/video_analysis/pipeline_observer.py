import os
import cv2


class PipelineObserver:
    def __init__(self, base_dir="outputs"):
        self.base_dir = base_dir
        self.frame_id = 0

        self.stages = [
            "raw",
            "fretboard_roi",
            "stabilized",
            "rectified",
            "hand",
            "grid",
            "pressure"
        ]


        for stage in self.stages:
            os.makedirs(os.path.join(base_dir, stage), exist_ok=True)

    def save(self, stage, frame):
        if frame is None:
            return

        path = os.path.join(
            self.base_dir,
            stage,
            f"frame_{self.frame_id:06d}.png"
        )
        cv2.imwrite(path, frame)

    def next_frame(self):
        self.frame_id += 1
