# blendtor
blendtor tries to detect the occurence of blend words by using approximate string matching algorithms.

# Usage

In this example, we execute from a directory outside blendtor.py file.
```
python blendtor/blendtor.py [-m=mode] [-s=step]
```

m (mode): specific mode to run the program, for example jw (for Jaro-Winkler), ngram, and led (for Local Edit Distance)

s (step): parameter used to speed up execution by reducing the number of candidate words used. This value is 1, by default, processing all candidate values.

```
python blendtor/analysis.py
```

The above command will return string containing statistical properties to standard output. Statistical properties include central values (mean, median, mode) and dispersion/variability (variance and standard deviation).

# Example

```
$ python blendtor/blendtor.py -m=jw -s=8000
precision	0.0 (0/3)
recall	0.0 (0/183)
```

```
$ python blendtor/analysis.py 

    statistics for JW:
    mean	: 0.7423989565383008
    median	: 0.7833333333333333
    mode	: 0.8333333333333334
    stdev	: 0.1729905416565893
    pstdev	: 0.17275405413432723
    variance	: 0.029925727502640165
    pvariance	: 0.029843963219846066
    

    statistics for NGram:
    mean	: 6.8743169398907105
    median	: 6.0
    mode	: 4
    stdev	: 2.987746014051291
    pstdev	: 2.983661602006302
    variance	: 8.926626244479376
    pvariance	: 8.90223655528681
    

    statistics for LED:
    mean	: 3.8224043715846996
    median	: 4.0
    mode	: 3.0
    stdev	: 1.7481546310660918
    pstdev	: 1.7457648081701527
    variance	: 3.0560446141178232
    pvariance	: 3.04769476544537
```