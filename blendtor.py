#!/Users/smanurung/miniconda3/bin/python

import argparse
from ngram import NGram
import smith_waterman as sm
import eval
from pyjarowinkler import distance

def led(w1, w2):
    """
    local edit distance: smith waterman algorithm. Implementation was retrieved from
    https://gist.github.com/nornagon/6326a643fc30339ece3021013ed9b48c
    """
    
    # TODO: analyse what's the difference between this LED algorithm making it return different result from
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

def jw(w1, w2, scale=0.1):
    """
    jw: Jaro-Winkler Similarity
    """
    return distance.get_jaro_distance(w1, w2, False, scale)

def analyseLED(minsim, numpairs, outputfile, step=1):
    """
    analyseLED works with dictionary & candidate file to decide lexical blends using local edit distance.
    """

    # TODO: this algorithm is too slow! Need to tweak this making it faster!

    # read from candidates.txt
    with open(outputfile, 'w') as fout, open('data/candidates.txt', 'r') as fcand, open('data/dict.txt', 'r') as fdict:
        dicts = fdict.readlines() # put into mem for multiple use
        cands = fcand.readlines()

        # strip space character at the end of the word once only
        for i in range(len(dicts)):
            dicts[i] = dicts[i].rstrip()

        i = 0

        while i < len(cands):
            cand = cands[i]
            cand = cand.rstrip()
            count = 0

            i += step

            print(cand)
            
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

def analyseNGram(n, maxdistance, numpairs, outputfile, step=1):
    # read from candidates.txt
    with open(outputfile, 'w') as fout, open('data/candidates.txt', 'r') as fcand, open('data/dict.txt', 'r') as fdict:
        dicts = fdict.readlines() # put into mem for multiple use
        cands = fcand.readlines()

        # strip space character at the end of the word once only
        for i in range(len(dicts)):
            dicts[i] = dicts[i].rstrip()

        i = 0

        while i < len(cands):
            cand = cands[i]
            cand = cand.rstrip()
            count = 0

            i += step
            
            for dic in dicts:
                dist = ngram(cand, dic, n)

                if dist <= maxdistance:
                    count += 1

                    if count > numpairs:
                        msg = "{} {}\n".format(cand, count)
                        print("[writeToOutputFile]", msg)
                        fout.write(msg)
                        break
    return 0

def analyseJW(minsim, numpairs, outputfile, step=1):
    # read from candidates.txt
    with open(outputfile, 'w') as fout, open('data/candidates.txt', 'r') as fcand, open('data/dict.txt', 'r') as fdict:
        dicts = fdict.readlines() # put into mem for multiple use
        cands = fcand.readlines()

        # strip space character at the end of the word once only
        for i in range(len(dicts)):
            dicts[i] = dicts[i].rstrip()

        i = 0

        while i < len(cands):
            cand = cands[i]
            cand = cand.rstrip()
            count = 0

            i += step
            
            for dic in dicts:
                sim = jw(cand, dic)

                if sim > minsim:
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
    parser.add_argument('--step', '-s', type=int, default=1)

    args = parser.parse_args()

    basefile = 'data/blends.txt'

    if args.mode == 'led':
        minsim = 3 # based stats, let's do for 2, 3, 4
        numpairs = 2
        outputfile = 'output/led_minsim{}_numpairs{}_step{}.txt'.format(minsim, numpairs, args.step)

        analyseLED(minsim, numpairs, outputfile, args.step)

        eval.precisionAndRecall(basefile, outputfile)
    elif args.mode == 'ngram':
        gram = 2
        maxdistance = 6
        numpairs = 5
        outputfile = 'output/ngram_gram{}_maxdistance{}_numpairs{}_step{}.txt'.format(gram, maxdistance, numpairs, args.step)
        
        analyseNGram(gram, maxdistance, numpairs, outputfile, args.step)

        eval.precisionAndRecall(basefile, outputfile)
    elif args.mode == 'jw':
        minsim = 0.75 # near to mean
        # minsim = 0.91 # mean + stddev
        numpairs = 2 # TODO: IDK what this is based - how to try this more intelligently?
        
        # TODO: add number of test division also here into output filename
        outputfile = 'output/jw_minsim{}_numpairs{}_step{}.txt'.format(minsim, numpairs, args.step)
        # outputfile = 'output/null.txt'

        analyseJW(minsim, numpairs, outputfile, args.step)

        eval.precisionAndRecall(basefile, outputfile)
    # elif args.mode == 'eval':
    #     basefile = 'data/blends.txt'
    #     predictedfile = 'output/ngram_gram2_maxdistance15_numpairs5.txt'
    #     predictedfile = 'output/jw_minsim0.5_numpairs2.txt'
    #     predictedfile = 'output/led_minsim5_numpairs2.txt'
        
    #     eval.precisionAndRecall(basefile, predictedfile)
    else:
        print("empty or invalid algorithm param:", args.mode)
