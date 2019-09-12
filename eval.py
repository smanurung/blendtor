#!/Users/smanurung/miniconda3/bin/python

def precisionAndRecall(basefile, predictedfile):
    """
    precision return fraction of correct attempts compared to all attempts
    """
    with open(basefile, 'r') as fbase, open(predictedfile, 'r') as fpred:
        baselist = fbase.readlines()
        basedict = {}
        tp = 0
        attempt = 0
        numAnswers = len(baselist)

        # take the first token
        for i in range(len(baselist)):
            k = baselist[i].split()[0]
            basedict[k] = True

        for line in fpred:
            attempt += 1

            line = line.split()[0]
            if line in basedict:
                tp += 1

        precision = tp/attempt
        recall = tp/numAnswers

        print("precision\t{} ({}/{})".format(precision, tp, attempt))
        print("recall\t{} ({}/{})".format(recall, tp, numAnswers))
    return 0
