# Obscura

Obscura is a flexible application for automatically detecting and blurring faces in images and videos. Implemented as a web application for single-file processing and as a command-line tool for batch processing of entire directories.

## Features

-  Powered by a YOLOv8 deep learning model for accurate and reliable face detection.
-  An intuitive web interface for blurring faces in single images.
-  A robust CLI for batch processing of image directories and video files.
-  Modular design allows for extension and customization.

## Live Demo

The web interface can be run locally by following the installation instructions.

## Installation & Setup

1.  **Clone the repository:**
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    *   **Web Interface:**
        ```bash
        python app.py
        ```
    *   **Command-Line Interface:**
        ```bash
        python cli.py --mode <mode> --input <input_path> --output <output_path>
        ```

## Screenshots

To be uploaded

## Technology Stack

- **Backend:** Flask (Python)
- **Computer Vision:** OpenCV, YOLOv8
- **Frontend:** HTML, CSS, JavaScript