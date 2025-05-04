import os


def get_save_path(filename: str, subdir: str = "data") -> str:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(BASE_DIR, "..", subdir)
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, filename)
    return output_path
