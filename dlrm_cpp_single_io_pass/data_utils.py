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

import os
from os import path


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
        raise(ValueError("Kaggle data set is not supported in this version"))
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
        file = d_path + o_filename + ".npz"
        os.system("cd dlrm_cpp_single_io_pass; ./build.sh; cd ..")
        os.system("dlrm_cpp_single_io_pass/build/main "
                  f"--max-ind-range={max_ind_range} "
                  f"--data-sub-sample-rate={sub_sample_rate} "
                  f"--data-split={data_split} "
                  f"--data-randomize={randomize} "
                  f"--raw-data-file={raw_path} "
                  f"--memory-map={memory_map}")

    return file, days