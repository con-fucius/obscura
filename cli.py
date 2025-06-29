import os
import argparse
from processor import blur_faces, process_video

def main():
    """
    Command-line interface for the Obscura application.
    """
    parser = argparse.ArgumentParser(description="Blur faces in images and videos.")
    parser.add_argument("--input", required=True, help="Path to the input file or directory.")
    parser.add_argument("--output", required=True, help="Path to the output directory.")
    parser.add_argument("--mode", choices=["single", "batch", "video"], required=True, help="Processing mode.")

    args = parser.parse_args()

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    if args.mode == "single":
        if not os.path.isfile(args.input):
            print(f"Error: Input file not found at {args.input}")
            return

        output_path = os.path.join(args.output, os.path.basename(args.input))
        success, result = blur_faces(args.input, output_path)
        if success:
            print(f"Successfully processed {args.input}. Blurred {result} faces.")
        else:
            print(f"Failed to process {args.input}: {result}")

    elif args.mode == "batch":
        if not os.path.isdir(args.input):
            print(f"Error: Input directory not found at {args.input}")
            return

        for filename in os.listdir(args.input):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                input_path = os.path.join(args.input, filename)
                output_path = os.path.join(args.output, filename)
                success, result = blur_faces(input_path, output_path)
                if success:
                    print(f"Successfully processed {filename}. Blurred {result} faces.")
                else:
                    print(f"Failed to process {filename}: {result}")

    elif args.mode == "video":
        if not os.path.isfile(args.input):
            print(f"Error: Input file not found at {args.input}")
            return

        output_path = os.path.join(args.output, os.path.basename(args.input))
        success, result = process_video(args.input, output_path)
        if success:
            print(f"Successfully processed {args.input}.")
        else:
            print(f"Failed to process {args.input}: {result}")

if __name__ == "__main__":
    main()