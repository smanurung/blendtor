#!/Users/smanurung/miniconda3/bin/python

from pyjarowinkler import distance
import statistics
import blendtor

def stat(name, d):
    """
    stat with input elements array
    """
    mean = statistics.mean(d)
    median = statistics.median(d)
    mode = statistics.mode(d)
    stdev = statistics.stdev(d)
    pstdev = statistics.pstdev(d)
    var = statistics.variance(d)
    pvar = statistics.pvariance(d)

    print("""
    statistics for {}:
    mean\t: {}
    median\t: {}
    mode\t: {}
    stdev\t: {}
    pstdev\t: {}
    variance\t: {}
    pvariance\t: {}
    """.format(name, mean, median, mode, stdev, pstdev, var, pvar))
    # TODO: look into median and the whole data distribution

def statNGram():
    d = []

    with open('data/blends.txt') as f:
        for line in f:

            t, tt, ttt = line.split()
            gram = 2

            d1 = blendtor.ngram(t, tt, gram)
            d2 = blendtor.ngram(t, ttt, gram)

            d.extend([d1, d2])
    stat('NGram', d)

def statJW():
    d = []

    with open('data/blends.txt') as f:
        for line in f:

            t, tt, ttt = line.split()

            jw1 = distance.get_jaro_distance(t, tt, False)
            jw2 = distance.get_jaro_distance(t, ttt, False)

            d.extend([jw1, jw2])
    stat('JW', d)

def statLED():
    d = []

    with open('data/blends.txt') as f:
        for line in f:

            t, tt, ttt = line.split()

            s1 = blendtor.led(t, tt)
            s2 = blendtor.led(t, ttt)

            d.extend([s1, s2])
    stat('LED', d)

if __name__ == "__main__":
    statJW()
    statNGram()
    statLED()