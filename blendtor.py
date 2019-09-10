#!/Users/smanurung/miniconda3/bin/python

import argparse
from ngram import NGram
import smith_waterman as sm
import eval

def led(w1, w2):
    """
    local edit distance: smith waterman algorithm. Implementation was retrieved from
    https://gist.github.com/nornagon/6326a643fc30339ece3021013ed9b48c
    """
    
    # TODO: analyse what's the difference between this LED algorithm making it return different result from
    # manual LED calculation (for "deaden" and "lended")
    sim = sm.smith_waterman(w1, w2)
    return sim

def ngram(w1, w2, n):
    """
    ngram distance
    """
    pad = lambda x : "#{}#".format(x)
    w1, w2 = pad(w1), pad(w2)

    g1 = [w1[i:i+n] for i in range(len(w1)-n+1)]
    g2 = [w2[i:i+n] for i in range(len(w2)-n+1)]


    # compute ngram similarity
    # d(a, b) = |a| + |b| + 2|a intersection b|
    n = NGram(g1)
    n.intersection_update(g2)

    d = len(g1) + len(g2) - 2 * len(list(n))
    return d

def jw():
    """
    jw: Jaro-Winkler Similarity
    """

def analyseLED(minsim, numpairs, outputfile, test):
    """
    analyseLED works with dictionary & candidate file to decide lexical blends using local edit distance.
    """
    # read from candidates.txt
    with open(outputfile, 'w') as fout, open('data/candidates.txt', 'r') as fcand, open('data/dict.txt', 'r') as fdict:
        dicts = fdict.readlines() # put into mem for multiple use
        cands = fcand.readlines()

        # strip space character at the end of the word once only
        for i in range(len(dicts)):
            dicts[i] = dicts[i].rstrip()

        # if test is True, only iterate half of candidate list
        r = len(cands)
        if test:
            r = int(r/2)

        for i in range(r):
            cand = cands[i]
            cand = cand.rstrip()
            count = 0
            
            for dic in dicts:
                sim = led(cand, dic)

                if sim > minsim:
                    count += 1

                    if count > numpairs:
                        msg = "{} {}\n".format(cand, count)
                        print("[writeToOutputFile]", msg)
                        fout.write(msg)
                        break
    return 0

def analyseNGram(n, maxdistance, numpairs, outputfile, test):
    # read from candidates.txt
    with open(outputfile, 'w') as fout, open('data/candidates.txt', 'r') as fcand, open('data/dict.txt', 'r') as fdict:
        dicts = fdict.readlines() # put into mem for multiple use
        cands = fcand.readlines()

        # strip space character at the end of the word once only
        for i in range(len(dicts)):
            dicts[i] = dicts[i].rstrip()

        r = len(cands)
        if test:
            r = int(r/2)

        for i in range(r):
            cand = cands[i]
            cand = cand.rstrip()
            count = 0
            
            for dic in dicts:
                dist = ngram(cand, dic, 2)

                if dist <= maxdistance:
                    count += 1

                    if count > numpairs:
                        msg = "{} {}\n".format(cand, count)
                        print("[writeToOutputFile]", msg)
                        fout.write(msg)
                        break
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="lexical blend params")
    parser.add_argument('--mode', '-m')
    parser.add_argument('--test', '-t', type=bool, default=False)

    args = parser.parse_args()

    if args.mode == 'led':
        minsim = 5
        numpairs = 2
        outputfile = 'output/led_minsim5_numpairs2.txt'

        analyseLED(minsim, numpairs, outputfile, args.test)
    elif args.mode == 'ngram':
        gram = 2
        maxdistance = 15
        numpairs = 5
        outputfile = 'output/ngram_gram2_maxdistance15_numpairs5.txt'
        
        analyseNGram(gram, maxdistance, numpairs, outputfile, args.test)
    elif args.mode == 'prec':
        basefile = 'data/blends.txt'
        predictedfile = 'output/ngram_gram2_maxdistance15_numpairs5.txt'
        
        eval.precision(basefile, predictedfile)
    else:
        print("empty or invalid algorithm param:", args.mode)
