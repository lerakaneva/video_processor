import argparse
from video_processor.data_processor import DataProcessor

def main():
    parser = argparse.ArgumentParser(description="Process microscopy video and segmentation data.")
    parser.add_argument("--config", required=True, help="Path to the JSON config file.")
    args = parser.parse_args()

    processor = DataProcessor(args.config)
    processor.process_data()

if __name__ == "__main__":
    main()
