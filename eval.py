#!/Users/smanurung/miniconda3/bin/python

def precision(basefile, predictedfile):
    """
    precision return fraction of correct answer compared to all returned values
    """
    with open(basefile, 'r') as fbase, open(predictedfile, 'r') as fpred:
        baselist = fbase.readlines()
        basedict = {}
        tp = 0
        attempt = 0

        # take the first token
        for i in range(len(baselist)):
            k = baselist[i].split()[0]
            basedict[k] = True
        # print(basedict, len(basedict))

        for line in fpred:
            attempt += 1

            line = line.split()[0]
            if line in basedict:
                tp += 1

        print("precision {} ({}/{})".format(tp/attempt, tp, attempt))
    return 0
