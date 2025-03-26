import sys
import matplotlib.pyplot as plt


def read_features(csv_file):
    features = []
    with open(csv_file) as csv:
        next(csv)  # skip header
        for line in csv:
            line = line.split(sep=",")
            features.append(line[1])
    return features


def main():
    if len(sys.argv) < 2:
        print("Usage: common_features <csv1> <csv2>")
        exit(1)

    csv1 = sys.argv[1]
    csv2 = sys.argv[2]

    features1 = set(read_features(csv1))
    features2 = set(read_features(csv2))
    common_features = features1.intersection(features2)
    print(f"Number of common features: {len(common_features)}")


if __name__ == '__main__':
    main()
