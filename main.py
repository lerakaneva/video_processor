import argparse
from visualizer.data_visualizer import DataVisualizer

def main():
    parser = argparse.ArgumentParser(description="Visualize microscopy data with masks and trajectories.")
    parser.add_argument("--config", required=True, help="Path to the JSON config file.")
    args = parser.parse_args()

    processor = DataVisualizer(args.config)
    processor.process_data()

if __name__ == "__main__":
    main()
