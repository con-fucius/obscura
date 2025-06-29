# Changelog

This document tracks all changes and progress for the Obscura feature extension project.

## Summary of Changes

*   **Refactored for Modularity:** The core processing logic has been separated from the web application, making the project more maintainable and extensible.
*   **Batch and Video Processing:** The application now supports processing of image directories and video files through a command-line interface.
*   **Upgraded Face Detection:** The face detection model has been upgraded to YOLOv8 model for significantly improved accuracy.

### Usage Instructions

The application can now be run from the command line to process single images, directories of images, and video files.

**Single Image Processing:**
```bash
python cli.py --mode single --input /path/to/your/image.jpg --output /path/to/output/directory
```

**Batch Image Processing:**
```bash
python cli.py --mode batch --input /path/to/your/image/directory --output /path/to/output/directory
```

**Video Processing:**
```bash
python cli.py --mode video --input /path/to/your/video.mp4 --output /path/to/output/directory
```