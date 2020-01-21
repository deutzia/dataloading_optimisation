# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#
# Description: generate inputs and targets for the DLRM benchmark
#
# Utility function(s) to download and pre-process public data sets
#   - Criteo Kaggle Display Advertising Challenge Dataset
#     https://labs.criteo.com/2014/02/kaggle-display-advertising-challenge-dataset
#   - Criteo Terabyte Dataset
#     https://labs.criteo.com/2013/12/download-terabyte-click-logs
#
# After downloading dataset, run:
#   getCriteoAdData(
#       datafile="<path-to-train.txt>",
#       o_filename=kaggleAdDisplayChallenge_processed.npz,
#       max_ind_range=-1,
#       sub_sample_rate=0.0,
#       days=7,
#       data_split='train',
#       randomize='total',
#       criteo_kaggle=True,
#       memory_map=False
#   )
#   getCriteoAdData(
#       datafile="<path-to-day_{0,...,23}>",
#       o_filename=terabyte_processed.npz,
#       max_ind_range=-1,
#       sub_sample_rate=0.0,
#       days=24,
#       data_split='train',
#       randomize='total',
#       criteo_kaggle=False,
#       memory_map=False
#   )

from __future__ import absolute_import, division, print_function, unicode_literals

import sys
# import os
from os import path
# import io
# from io import StringIO
# import collections as coll

import numpy as np
import time
import pandas


def logPerfMeasurement(name):
    end_time = time.time()
    print(f"[{name}] elapsed {end_time - logPerfMeasurement.start_time}", file=sys.stderr)
    logPerfMeasurement.start_time = end_time
logPerfMeasurement.start_time = time.time()


def processCriteoAdData(d_path, d_file, npzfile, split, convertDicts, pre_comp_counts):
    # Process Kaggle Display Advertising Challenge or Terabyte Dataset
    # by converting unicode strings in X_cat to integers and
    # converting negative integer values in X_int.
    #
    # Loads data in the form "{kaggle|terabyte}_day_i.npz" where i is the day.
    #
    # Inputs:
    #   d_path (str): path for {kaggle|terabyte}_day_i.npz files
    #   split (int): total number of splits in the dataset (typically 7 or 24)

    # process data if not all files exist
    for i in range(split):
        filename_i = npzfile + "_{0}_processed.npz".format(i)

        if path.exists(filename_i):
            print("Using existing " + filename_i, end="\r")
        else:
            with np.load(npzfile + "_{0}.npz".format(i)) as data:
                # categorical features
                # Approach 2a: using pre-computed dictionaries
                X_cat_t_original = data["X_cat"].transpose()
                X_cat_t = np.zeros(X_cat_t_original.shape)
                for j in range(26):
                    for k, x in enumerate(X_cat_t_original[j, :]):
                        X_cat_t[j, k] = convertDicts[j][x]
                # continuous features
                X_int = data["X_int"]
                X_int[X_int < 0] = 0
                # targets
                y = data["y"]

            np.savez_compressed(
                filename_i,
                # X_cat = X_cat,
                X_cat=np.transpose(X_cat_t),  # transpose of the data
                X_int=X_int,
                y=y,
            )
            print("Processed " + filename_i, end="\r")
    print("")
    # sanity check (applicable only if counts have been pre-computed & are re-computed)
    # for j in range(26):
    #    if pre_comp_counts[j] != counts[j]:
    #        sys.exit("ERROR: Sanity check on counts has failed")
    # print("\nSanity check on counts passed")

    return


def concatCriteoAdData(
        d_path,
        d_file,
        npzfile,
        trafile,
        days,
        data_split,
        randomize,
        total_per_file,
        total_count,
        memory_map,
        o_filename
):
    # Concatenates different days and saves the result.
    #
    # Inputs:
    #   days (int): total number of days in the dataset (typically 7 or 24)
    #   d_path (str): path for {kaggle|terabyte}_day_i.npz files
    #   o_filename (str): output file name
    #
    # Output:
    #   o_file (str): output file path

    if memory_map:
        # dataset break up per fea
        # tar_fea = 1   # single target
        den_fea = 13  # 13 dense  features
        spa_fea = 26  # 26 sparse features
        # tad_fea = tar_fea + den_fea
        # tot_fea = tad_fea + spa_fea
        # create offset per file
        offset_per_file = np.array([0] + [x for x in total_per_file])
        for i in range(days):
            offset_per_file[i + 1] += offset_per_file[i]

        # Approach 4: Fisher-Yates-Rao (FYR) shuffle algorithm
        # 1st pass of FYR shuffle
        # check if data already exists
        recreate_flag = False
        for j in range(days):
            filename_j_y = npzfile + "_{0}_intermediate_y.npy".format(j)
            filename_j_d = npzfile + "_{0}_intermediate_d.npy".format(j)
            filename_j_s = npzfile + "_{0}_intermediate_s.npy".format(j)
            if (
                path.exists(filename_j_y)
                and path.exists(filename_j_d)
                and path.exists(filename_j_s)
            ):
                print(
                    "Using existing\n"
                    + filename_j_y + "\n"
                    + filename_j_d + "\n"
                    + filename_j_s
                )
            else:
                recreate_flag = True
        # reorder across buckets using sampling
        if recreate_flag:
            # init intermediate files (.npy appended automatically)
            for j in range(days):
                filename_j_y = npzfile + "_{0}_intermediate_y".format(j)
                filename_j_d = npzfile + "_{0}_intermediate_d".format(j)
                filename_j_s = npzfile + "_{0}_intermediate_s".format(j)
                np.save(filename_j_y, np.zeros((total_per_file[j])))
                np.save(filename_j_d, np.zeros((total_per_file[j], den_fea)))
                np.save(filename_j_s, np.zeros((total_per_file[j], spa_fea)))
            # start processing files
            total_counter = [0] * days
            for i in range(days):
                filename_i = npzfile + "_{0}_processed.npz".format(i)
                with np.load(filename_i) as data:
                    X_cat = data["X_cat"]
                    X_int = data["X_int"]
                    y = data["y"]
                size = len(y)
                # sanity check
                if total_per_file[i] != size:
                    sys.exit("ERROR: sanity check on number of samples failed")
                # debug prints
                print("Reordering (1st pass) " + filename_i)

                # create buckets using sampling of random ints
                # from (discrete) uniform distribution
                buckets = []
                for _j in range(days):
                    buckets.append([])
                counter = [0] * days
                days_to_sample = days if data_split == "none" else days - 1
                if randomize == "total":
                    rand_u = np.random.randint(low=0, high=days_to_sample, size=size)
                    for k in range(size):
                        # sample and make sure elements per buckets do not overflow
                        if data_split == "none" or i < days - 1:
                            # choose bucket
                            p = rand_u[k]
                            # retry of the bucket is full
                            while total_counter[p] + counter[p] >= total_per_file[p]:
                                p = np.random.randint(low=0, high=days_to_sample)
                        else:  # preserve the last day/bucket if needed
                            p = i
                        buckets[p].append(k)
                        counter[p] += 1
                else:  # randomize is day or none
                    for k in range(size):
                        # do not sample, preserve the data in this bucket
                        p = i
                        buckets[p].append(k)
                        counter[p] += 1

                # sanity check
                if np.sum(counter) != size:
                    sys.exit("ERROR: sanity check on number of samples failed")
                # debug prints
                # print(counter)
                # print(str(np.sum(counter)) + " = " + str(size))
                # print([len(x) for x in buckets])
                # print(total_counter)

                # partially feel the buckets
                for j in range(days):
                    filename_j_y = npzfile + "_{0}_intermediate_y.npy".format(j)
                    filename_j_d = npzfile + "_{0}_intermediate_d.npy".format(j)
                    filename_j_s = npzfile + "_{0}_intermediate_s.npy".format(j)
                    start = total_counter[j]
                    end = total_counter[j] + counter[j]
                    # target buckets
                    fj_y = np.load(filename_j_y, mmap_mode='r+')
                    # print("start=" + str(start) + " end=" + str(end)
                    #       + " end - start=" + str(end - start) + " "
                    #       + str(fj_y[start:end].shape) + " "
                    #       + str(len(buckets[j])))
                    fj_y[start:end] = y[buckets[j]]
                    del fj_y
                    # dense buckets
                    fj_d = np.load(filename_j_d, mmap_mode='r+')
                    # print("start=" + str(start) + " end=" + str(end)
                    #       + " end - start=" + str(end - start) + " "
                    #       + str(fj_d[start:end, :].shape) + " "
                    #       + str(len(buckets[j])))
                    fj_d[start:end, :] = X_int[buckets[j], :]
                    del fj_d
                    # sparse buckets
                    fj_s = np.load(filename_j_s, mmap_mode='r+')
                    # print("start=" + str(start) + " end=" + str(end)
                    #       + " end - start=" + str(end - start) + " "
                    #       + str(fj_s[start:end, :].shape) + " "
                    #       + str(len(buckets[j])))
                    fj_s[start:end, :] = X_cat[buckets[j], :]
                    del fj_s
                    # update counters for next step
                    total_counter[j] += counter[j]

        # 2nd pass of FYR shuffle
        # check if data already exists
        for j in range(days):
            filename_j = npzfile + "_{0}_reordered.npz".format(j)
            if path.exists(filename_j):
                print("Using existing " + filename_j)
            else:
                recreate_flag = True
        # reorder within buckets
        if recreate_flag:
            for j in range(days):
                filename_j_y = npzfile + "_{0}_intermediate_y.npy".format(j)
                filename_j_d = npzfile + "_{0}_intermediate_d.npy".format(j)
                filename_j_s = npzfile + "_{0}_intermediate_s.npy".format(j)
                fj_y = np.load(filename_j_y)
                fj_d = np.load(filename_j_d)
                fj_s = np.load(filename_j_s)

                indices = range(total_per_file[j])
                if randomize == "day" or randomize == "total":
                    if data_split == "none" or j < days - 1:
                        indices = np.random.permutation(range(total_per_file[j]))

                filename_r = npzfile + "_{0}_reordered.npz".format(j)
                print("Reordering (2nd pass) " + filename_r)
                np.savez_compressed(
                    filename_r,
                    X_cat=fj_s[indices, :],
                    X_int=fj_d[indices, :],
                    y=fj_y[indices],
                )

    else:
        print("Concatenating multiple days into %s.npz file" % str(d_path + o_filename))

        # load and concatenate data
        for i in range(days):
            filename_i = npzfile + "_{0}_processed.npz".format(i)
            with np.load(filename_i) as data:
                if i == 0:
                    X_cat = data["X_cat"]
                    X_int = data["X_int"]
                    y = data["y"]
                else:
                    X_cat = np.concatenate((X_cat, data["X_cat"]))
                    X_int = np.concatenate((X_int, data["X_int"]))
                    y = np.concatenate((y, data["y"]))
            print("Loaded day:", i, "y = 1:", len(y[y == 1]), "y = 0:", len(y[y == 0]))

        with np.load(d_path + d_file + "_fea_count.npz") as data:
            counts = data["counts"]
        print("Loaded counts!")

        np.savez_compressed(
            d_path + o_filename + ".npz",
            X_cat=X_cat,
            X_int=X_int,
            y=y,
            counts=counts,
        )

    return d_path + o_filename + ".npz"


def transformCriteoAdData(X_cat, X_int, y, days, data_split, randomize, total_per_file):
    # Transforms Criteo Kaggle or terabyte data by applying log transformation
    # on dense features and converting everything to appropriate tensors.
    #
    # Inputs:
    #     X_cat (ndarray): array of integers corresponding to preprocessed
    #                      categorical features
    #     X_int (ndarray): array of integers corresponding to dense features
    #     y (ndarray):     array of bool corresponding to labels
    #     data_split(str): flag for splitting dataset into training/validation/test
    #                      sets
    #     randomize (str): determines randomization scheme
    #         "none": no randomization
    #         "day": randomizes each day"s data (only works if split = True)
    #         "total": randomizes total dataset
    #
    # Outputs:
    #     if split:
    #         X_cat_train (tensor): sparse features for training set
    #         X_int_train (tensor): dense features for training set
    #         y_train (tensor): labels for training set
    #         X_cat_val (tensor): sparse features for validation set
    #         X_int_val (tensor): dense features for validation set
    #         y_val (tensor): labels for validation set
    #         X_cat_test (tensor): sparse features for test set
    #         X_int_test (tensor): dense features for test set
    #         y_test (tensor): labels for test set
    #     else:
    #         X_cat (tensor): sparse features
    #         X_int (tensor): dense features
    #         y (tensor): label

    # define initial set of indices
    indices = np.arange(len(y))

    # create offset per file
    offset_per_file = np.array([0] + [x for x in total_per_file])
    for i in range(days):
        offset_per_file[i + 1] += offset_per_file[i]

    # split dataset
    if data_split == 'train':
        indices = np.array_split(indices, offset_per_file[1:-1])

        # randomize train data (per day)
        if randomize == "day":  # or randomize == "total":
            for i in range(len(indices) - 1):
                indices[i] = np.random.permutation(indices[i])
            print("Randomized indices per day ...")

        train_indices = np.concatenate(indices[:-1])
        test_indices = indices[-1]
        test_indices, val_indices = np.array_split(test_indices, 2)

        print("Defined training and testing indices...")

        # randomize train data (across days)
        if randomize == "total":
            train_indices = np.random.permutation(train_indices)
            print("Randomized indices across days ...")

        # indices = np.concatenate((train_indices, test_indices))

        # create training, validation, and test sets
        X_cat_train = X_cat[train_indices]
        X_int_train = X_int[train_indices]
        y_train = y[train_indices]

        X_cat_val = X_cat[val_indices]
        X_int_val = X_int[val_indices]
        y_val = y[val_indices]

        X_cat_test = X_cat[test_indices]
        X_int_test = X_int[test_indices]
        y_test = y[test_indices]

        print("Split data according to indices...")

        X_cat_train = X_cat_train.astype(np.long)
        X_int_train = np.log(X_int_train.astype(np.float32) + 1)
        y_train = y_train.astype(np.float32)

        X_cat_val = X_cat_val.astype(np.long)
        X_int_val = np.log(X_int_val.astype(np.float32) + 1)
        y_val = y_val.astype(np.float32)

        X_cat_test = X_cat_test.astype(np.long)
        X_int_test = np.log(X_int_test.astype(np.float32) + 1)
        y_test = y_test.astype(np.float32)

        print("Converted to tensors...done!")

        return (
            X_cat_train,
            X_int_train,
            y_train,
            X_cat_val,
            X_int_val,
            y_val,
            X_cat_test,
            X_int_test,
            y_test,
        )

    else:

        # randomize data
        if randomize == "total":
            indices = np.random.permutation(indices)
            print("Randomized indices...")

        X_cat = X_cat[indices].astype(np.long)
        X_int = np.log(X_int[indices].astype(np.float32) + 1)
        y = y[indices].astype(np.float32)

        print("Converted to tensors...done!")

        return (X_cat, X_int, y, [], [], [], [], [], [])


def getCriteoAdData(
        datafile,
        o_filename,
        max_ind_range=-1,
        sub_sample_rate=0.0,
        days=7,
        data_split='train',
        randomize='total',
        criteo_kaggle=True,
        memory_map=False
):
    # Passes through entire dataset and defines dictionaries for categorical
    # features and determines the number of total categories.
    #
    # Inputs:
    #    datafile : path to downloaded raw data file
    #    o_filename (str): saves results under o_filename if filename is not ""
    #
    # Output:
    #   o_file (str): output file path

    #split the datafile into path and filename
    lstr = datafile.split("/")
    d_path = "/".join(lstr[0:-1]) + "/"
    d_file = lstr[-1].split(".")[0] if criteo_kaggle else lstr[-1]
    npzfile = d_path + ((d_file + "_day") if criteo_kaggle else d_file)
    trafile = d_path + ((d_file + "_fea") if criteo_kaggle else "fea")

    # count number of datapoints in training set
    total_file = d_path + d_file + "_day_count.npz"
    logPerfMeasurement("getCriteoAdData initialisation")
    if path.exists(total_file):
        with np.load(total_file) as data:
            total_per_file = list(data["total_per_file"])
        total_count = np.sum(total_per_file)
        print("Skipping counts per file (already exist)")
    else:
        total_count = 0
        total_per_file = []
        if criteo_kaggle:
            # WARNING: The raw data consists of a single train.txt file
            # Each line in the file is a sample, consisting of 13 continuous and
            # 26 categorical features (an extra space indicates that feature is
            # missing and will be interpreted as 0).
            if path.exists(datafile):
                print("Reading data from path=%s" % (datafile))
                with open(str(datafile)) as f:
                    for _ in f:
                        total_count += 1
                total_per_file.append(total_count)
                # reset total per file due to split
                num_data_per_split, extras = divmod(total_count, days)
                total_per_file = [num_data_per_split] * days
                for j in range(extras):
                    total_per_file[j] += 1
                # split into days (simplifies code later on)
                file_id = 0
                boundary = total_per_file[file_id]
                nf = open(npzfile + "_" + str(file_id), "w")
                with open(str(datafile)) as f:
                    for j, line in enumerate(f):
                        if j == boundary:
                            nf.close()
                            file_id += 1
                            nf = open(npzfile + "_" + str(file_id), "w")
                            boundary += total_per_file[file_id]
                        nf.write(line)
                nf.close()
            else:
                sys.exit("ERROR: Criteo Kaggle Display Ad Challenge Dataset path is invalid; please download from https://labs.criteo.com/2014/02/kaggle-display-advertising-challenge-dataset")
        else:
            # WARNING: The raw data consist of day_0.gz,... ,day_23.gz text files
            # Each line in the file is a sample, consisting of 13 continuous and
            # 26 categorical features (an extra space indicates that feature is
            # missing and will be interpreted as 0).
            for i in range(days):
                datafile_i = datafile + "_" + str(i)  # + ".gz"
                if path.exists(str(datafile_i)):
                    print("Reading data from path=%s" % (str(datafile_i)))
                    # file day_<number>
                    total_per_file_count = 0
                    with open(str(datafile_i)) as f:
                        for _ in f:
                            total_per_file_count += 1
                    total_per_file.append(total_per_file_count)
                    total_count += total_per_file_count
                else:
                    sys.exit("ERROR: Criteo Terabyte Dataset path is invalid; please download from https://labs.criteo.com/2013/12/download-terabyte-click-logs")
    logPerfMeasurement("getCriteoAdData reading data finished")


    # process a file worth of data and reinitialize data
    # note that a file main contain a single or multiple splits
    def process_one_file(
            datfile,
            npzfile,
            split,
            num_data_in_split,
    ):

        def printTypesDataFrame(x, seriesName):
            print(f"####################Printing types of series {seriesName}###################", file = sys.stderr)
            for column in x:
                types = set()
                for val in x[column]:
                    if type(val) not in types:
                        types.add(type(val))
                print(f"column{column}: ", file = sys.stderr)
                print(types, file = sys.stderr)


        def printTypesSeries(x, seriesName):
            print(f"######################{seriesName}######################", file=sys.stderr)
            types = set()
            for val in x:
                types.add(type(val))
            print(types, file = sys.stderr)

        logPerfMeasurement("process_one_file starting")
        y = np.zeros(num_data_in_split, dtype="i4")  # 4 byte int
        X_int = np.zeros((num_data_in_split, 13), dtype="i4")  # 4 byte int
        X_cat = np.zeros((num_data_in_split, 26), dtype="i4")  # 4 byte int

        i = 0
        df = pandas.read_csv(datfile, sep="\t", header=None, dtype=np.str, engine='c')
        logPerfMeasurement("process_one_file read csv")

#        printTypesDataFrame(df, "df")

        targets = df[0].astype(dtype=np.int32, copy=False)
        rand_u = np.random.uniform(low=0.0, high=1.00, size=num_data_in_split)
        if sub_sample_rate != 0:
            rand_booleans = rand_u < sub_sample_rate
        else:
            rand_booleans = np.full(num_data_in_split, True, dtype=bool)
        keep_rows = ((targets > 0) | rand_booleans)
        df = df.loc[keep_rows]
        logPerfMeasurement("process_one_file drop random")

        y = df[0]
#        printTypesSeries(y, "y")
        # Assume there were no Nans in the original data, so only nans are
        # from missing values
        y.fillna("0", inplace=True)
        y = y.astype(dtype=np.int32, copy=False)
#        printTypesSeries(y, "y")
        X_int = df.loc[:, 1:13].fillna("0")
        X_int = X_int.astype(dtype=np.int32, copy=False)
        X_cat = df.loc[:, 14:39].fillna("0")
#        printTypesDataFrame(X_cat, "X_cat")

        if max_ind_range > 0:
            X_cat = X_cat.applymap(lambda x: int(x, 16) % max_ind_range if type(x) == type("") else x)
            X_cat = X_cat.astype(dtype=np.int32, copy=False)
        else:
            X_cat = X_cat.applymap(lambda x: int(x, 16))
            X_cat = X_cat.astype(dtype=np.int32, copy=False)
        d = {}
        logPerfMeasurement("process_one_file applymap")
        for j in range(26):
            d[j + 14] = j
        X_cat.rename(columns=d, inplace=True)
        for j in range(26):
            uniques = X_cat[j].unique()
            for elem in uniques:
                convertDicts[j][elem] = 1
            print(convertDicts[j])
        logPerfMeasurement("process_one_file convert-dicts stuff")


        filename_s = npzfile + "_{0}.npz".format(split)
        if path.exists(filename_s):
            print("\nSkip existing " + filename_s)
        else:
            np.savez_compressed(
                filename_s,
                X_int=X_int,
                X_cat=X_cat,
                y=y,
            )
            print("\nSaved " + npzfile + "_{0}.npz!".format(split))
        logPerfMeasurement("process_one_file save compressed")
        return i

    # create all splits (reuse existing files if possible)
    recreate_flag = False
    convertDicts = [{} for _ in range(26)]
    # WARNING: to get reproducable sub-sampling results you must reset the seed below
    # np.random.seed(123)
    # in this case there is a single split in each day
    for i in range(days):
        datfile_i = npzfile + "_{0}".format(i)  # + ".gz"
        npzfile_i = npzfile + "_{0}.npz".format(i)
        npzfile_p = npzfile + "_{0}_processed.npz".format(i)
        if path.exists(npzfile_i):
            print("Skip existing " + npzfile_i)
        elif path.exists(npzfile_p):
            print("Skip existing " + npzfile_p)
        else:
            recreate_flag = True
            total_per_file[i] = process_one_file(
                datfile_i,
                npzfile,
                i,
                total_per_file[i],
            )
    logPerfMeasurement(f"getCriteoAdData process_one_file on all the files finished")

    # report and save total into a file
    total_count = np.sum(total_per_file)
    if not path.exists(total_file):
        np.savez_compressed(total_file, total_per_file=total_per_file)
    print("Total number of samples:", total_count)
    print("Divided into days/splits:\n", total_per_file)

    # dictionary files
    counts = np.zeros(26, dtype=np.int32)
    if recreate_flag:
        # create dictionaries
        for j in range(26):
            for i, x in enumerate(convertDicts[j]):
                convertDicts[j][x] = i
            dict_file_j = d_path + d_file + "_fea_dict_{0}.npz".format(j)
            if not path.exists(dict_file_j):
                np.savez_compressed(
                    dict_file_j,
                    unique=np.array(list(convertDicts[j]), dtype=np.int32)
                )
            counts[j] = len(convertDicts[j])
        # store (uniques and) counts
        count_file = d_path + d_file + "_fea_count.npz"
        if not path.exists(count_file):
            np.savez_compressed(count_file, counts=counts)
    else:
        # create dictionaries (from existing files)
        for j in range(26):
            with np.load(d_path + d_file + "_fea_dict_{0}.npz".format(j)) as data:
                unique = data["unique"]
            for i, x in enumerate(unique):
                convertDicts[j][x] = i
        # load (uniques and) counts
        with np.load(d_path + d_file + "_fea_count.npz") as data:
            counts = data["counts"]
    logPerfMeasurement(f"getCriteoAdData reporting and saving total finished")

    # process all splits
    processCriteoAdData(d_path, d_file, npzfile, days, convertDicts, counts)
    logPerfMeasurement(f"getCriteoAdData calling processCriteoAdData")
    o_file = concatCriteoAdData(
        d_path,
        d_file,
        npzfile,
        trafile,
        days,
        data_split,
        randomize,
        total_per_file,
        total_count,
        memory_map,
        o_filename
    )
    logPerfMeasurement(f"getCriteoAdData calling concatCriteoAdData")

    return o_file


def loadDataset(
        dataset,
        max_ind_range,
        sub_sample_rate,
        randomize,
        data_split,
        raw_path="",
        pro_data="",
        memory_map=False
):
    # dataset
    if dataset == "kaggle":
        days = 7
        o_filename = "kaggleAdDisplayChallenge_processed"
    elif dataset == "terabyte":
        days = 24
        o_filename = "terabyte_processed"
    else:
        raise(ValueError("Data set option is not supported"))

    # split the datafile into path and filename
    lstr = raw_path.split("/")
    d_path = "/".join(lstr[0:-1]) + "/"
    d_file = lstr[-1].split(".")[0] if dataset == "kaggle" else lstr[-1]
    npzfile = d_path + ((d_file + "_day") if dataset == "kaggle" else d_file)
    # trafile = d_path + ((d_file + "_fea") if dataset == "kaggle" else "fea")

    # check if pre-processed data is available
    data_ready = True
    if memory_map:
        for i in range(days):
            reo_data = d_path + npzfile + "_{0}_reordered.npz".format(i)
            if not path.exists(str(reo_data)):
                data_ready = False
    else:
        if not path.exists(str(pro_data)):
            data_ready = False

    # pre-process data if needed
    # WARNNING: when memory mapping is used we get a collection of files
    if data_ready:
        print("Reading pre-processed data=%s" % (str(pro_data)))
        file = str(pro_data)
    else:
        print("Reading raw data=%s" % (str(raw_path)))
        file = getCriteoAdData(
            raw_path,
            o_filename,
            max_ind_range,
            sub_sample_rate,
            days,
            data_split,
            randomize,
            dataset == "kaggle",
            memory_map
        )

    return file, days


if __name__ == "__main__":
    ### import packages ###
    import argparse

    ### parse arguments ###
    parser = argparse.ArgumentParser(
        description="Preprocess Criteo dataset"
    )
    # model related parameters
    parser.add_argument("--max-ind-range", type=int, default=-1)
    parser.add_argument("--data-sub-sample-rate", type=float, default=0.0)  # in [0, 1]
    parser.add_argument("--data-randomize", type=str, default="total")  # or day or none
    parser.add_argument("--memory-map", action="store_true", default=False)
    parser.add_argument("--data-set", type=str, default="kaggle")  # or terabyte
    parser.add_argument("--raw-data-file", type=str, default="")
    parser.add_argument("--processed-data-file", type=str, default="")
    args = parser.parse_args()

    loadDataset(
        args.data_set,
        args.max_ind_range,
        args.data_sub_sample_rate,
        args.data_randomize,
        "train",
        args.raw_data_file,
        args.processed_data_file,
        args.memory_map
    )
