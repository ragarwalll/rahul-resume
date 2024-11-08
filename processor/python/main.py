"""
Main script to generate resume content from JSON file.
"""

import argparse
import json
from pathlib import Path
from typing import Union
from generator import ResumeContentGenerator

parser = argparse.ArgumentParser()

parser.add_argument("--input", help="path to the JSON file")
parser.add_argument("--output", help="path to the output file")


def get_absolute_path(
    file_path: Union[str, Path], base_dir: Union[str, Path, None] = None
) -> Path:
    """
    Convert any file path to its absolute path, handling relative paths, absolute paths,
    and paths with parent directory references.

    Args:
        file_path (Union[str, Path]): The file path to resolve. Can be:
            - A relative path ("data.json", "./data.json")
            - A path with parent references ("../data.json", "../../data.json")
            - An absolute path ("/home/user/data.json", "C:\\Users\\data.json")
        base_dir (Union[str, Path, None]): Optional base directory to resolve relative paths from.
            If not provided, uses the current working directory.

    Returns:
        Path: Absolute path as a Path object

    Examples:
        >>> get_absolute_path("data.json")  # Relative to current directory
        PosixPath('/current/working/dir/data.json')

        >>> get_absolute_path("../data.json", "/home/user/projects")
        PosixPath('/home/user/data.json')

        >>> get_absolute_path("/absolute/path/data.json")
        PosixPath('/absolute/path/data.json')
    """
    # Convert input to Path object
    path = Path(file_path)

    # If path is absolute, return it directly
    if path.is_absolute():
        return path.resolve()

    # Determine base directory
    base = Path(base_dir) if base_dir else Path.cwd()

    # Handle relative paths (including parent directory references)
    return (base / path).resolve()


if __name__ == "__main__":
    args = parser.parse_args()
    if args.input and args.output:
        # resolve path to the JSON file
        # handle in case of invalid path
        # handle in case of relative path
        # handle in case of absolute path

        with open(get_absolute_path(args.input), "r", encoding="utf-8") as f:
            data = json.loads(f.read())

        generator = ResumeContentGenerator(data)
        RESUME_CONTENT = generator.build_resume()

        with open(args.output, "w", encoding="utf-8") as f:
            f.write(RESUME_CONTENT)

        print("Resume TEX generated successfully.")
    else:
        print("Please provide the path to the JSON file.")
