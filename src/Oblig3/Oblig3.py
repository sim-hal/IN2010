import oblig3runner
import sys
from plot_results import plot_results


def main(filename):
    with open(filename, 'r') as f:
        A = [int(x) for x in f.readlines()]
    oblig3runner.run_algs_part1(A, filename)
    oblig3runner.run_algs_part2(A, filename)
    plot_results(filename+"_results.csv")


if __name__ == '__main__':
    main(sys.argv[1])


