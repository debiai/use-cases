import pandas as pd
import os
import csv
from tqdm import tqdm
from typing import List, Dict

"""
Data loader script for the Valeo Woodscape dataset

This script uses the Woodscape "box_2d_annotations" folder.

box_2d_annotations folder expected content:
    List of `XXXXX_YY.txt` files
    Where XXXXX is the image id and YY is the camera id
    Content of the txt file:
        vehicles,0,89,379,135,442
        person,1,431,302,465,389
        traffic_light,3,379,243,398,277
        traffic_sign,3,905,246,925,297
"""


BOX_2D_ANNOTATIONS_FOLDER_PATH = os.path.join("data", "box_2d_annotations")
EXTRA_FEATURES_CSV_PATH = os.path.join("data", "features.csv")
CLASSES = ["vehicles", "person", "bicycle", "traffic_light", "traffic_sign"]


def parse_annotation_file(file_path: str) -> List[Dict]:
    """Parse a single annotation file and return a list of object data."""
    objects = []
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) != 6:
                print(f"Invalid row: {row}")
                continue

            object = {
                "class": row[0],
                "class_number": int(row[1]),
                "x": int(row[2]),
                "y": int(row[3]),
                "w": int(row[4]),
                "h": int(row[5]),
            }

            if object["class"] not in CLASSES:
                print(f"Unknown class: {object['class']}")
                continue

            objects.append(object)
    return objects


def create_woodscape_dataset() -> pd.DataFrame:
    """Create a dataset with one row per image."""
    images_list = os.listdir(BOX_2D_ANNOTATIONS_FOLDER_PATH)
    data = []

    for image_file in tqdm(
        images_list, desc="Parsing images annotations", unit="image"
    ):
        image_id, _ = os.path.splitext(image_file)
        image_cam = image_id.split("_")[1]
        file_path = os.path.join(BOX_2D_ANNOTATIONS_FOLDER_PATH, image_file)

        annotations = parse_annotation_file(file_path)
        number_of_objects_per_class = {cls: 0 for cls in CLASSES}
        objects = []
        for idx, object in enumerate(annotations):
            x, y, w, h = object["x"], object["y"], object["w"], object["h"]
            objects.append(
                {
                    "object nb": idx,
                    "class": object["class"],
                    "class nb": object["class_number"],
                    "x": x,
                    "y": y,
                    "w": w,
                    "h": h,
                    "center x": (x + w) / 2,
                    "center y": (y + h) / 2,
                    "area": (w - x) * (h - y),
                }
            )

            number_of_objects_per_class[object["class"]] += 1

        data.append(
            {
                "camera": image_cam,
                "image": image_id,
                "objects number": len(objects),
                "per classes number": number_of_objects_per_class,
                "objects": objects,
            }
        )

    return pd.DataFrame(data)


def create_woodscape_dataset_extra_features() -> pd.DataFrame:
    woodscape_df = create_woodscape_dataset()

    # Load extra features
    extra_features_df = pd.read_csv(EXTRA_FEATURES_CSV_PATH)

    # Rows:
    # - image_name
    # - luminance
    # - contrast
    # - brisque
    # - cpbd
    # - shannon_entropy
    # - glcm_entropy

    # Merge the two dataframes
    merged_df = pd.merge(
        woodscape_df,
        extra_features_df,
        left_on="image",
        right_on="image_name",
        how="inner",
    )

    return merged_df


if __name__ == "__main__":
    create_woodscape_dataset_extra_features()
