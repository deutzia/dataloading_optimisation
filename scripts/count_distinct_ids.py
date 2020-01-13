
datafile = "../dlrm/test_data/day_0_repr_sample_big"

with open(str(datafile)) as f:
    num_of_cats = 26
    sets = [set() for i in range(num_of_cats)]

    for line in f:
        # process a line (data point)
        line = line.split('\t')
        # set missing values to zero
        for j in range(len(line)):
            if (line[j] == '') or (line[j] == '\n'):
                line[j] = '0'
        # categorical features begin at idx=14
        ids = line[14:14+num_of_cats]
        # update distinct ids for every categorical feature
        for id, s in zip(ids, sets):
            s.add(id)

    for k, s in enumerate(sets):
        print("categorical feature {}: num of distinct ids: {}".format(k, len(s)))