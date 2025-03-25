import sys
from collections import Counter
import matplotlib.pyplot as plt


def read_features(csv_file):
    features = []
    with open(csv_file) as csv:
        next(csv) # skip header
        for line in csv:
            line = line.split(sep=",")
            features.append(line[1])
    return features


def compute_stats(features):
    counts = {x: 0 for x in range(1, 25)}
    for feature in features:
        feature = feature.split(".")[0]
        chromosome_number = int(feature[-2:])
        counts[chromosome_number] += 1

    # Sort by value
    sorted_items = sorted(counts.items())  # List of tuples [(1,1), (2,2), ...]

    # Separate into x and y
    x_vals, y_vals = zip(*sorted_items)
    return x_vals, y_vals


def plot_stat(x_vals, y_vals, png_out='chromosomes_stat.png', csv_out=None):
    plt.bar(x_vals, y_vals, color='skyblue', edgecolor='black')
    plt.title('Value Distribution (Sorted)')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.xticks(x_vals)
    plt.savefig(png_out)

    if csv_out is not None:
        with open(csv_out):
            for x_val, y_val in zip(x_vals, y_vals):
                csv_out.write("{},{}\n".format(x_val, y_val))


def main():
    if len(sys.argv) < 2:
        print("Usage: chromosomes_stat <csv-in> <csv-out>")
        exit(1)

    csv_in = sys.argv[1]
    if len(sys.argv) == 3:
        csv_out = sys.argv[2]
    else:
        csv_out = None

    features = read_features(csv_in)
    plot_stat(*compute_stats(features))


if __name__ == '__main__':
    main()
