import glob
import argparse
import os.path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str, help='source file or directory')

    args = parser.parse_args()
    path = args.path


if __name__ == '__main__':
    main()