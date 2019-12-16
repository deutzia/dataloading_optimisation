import sys
import os
import numpy as np

if len(sys.argv) == 2:
    path_to_dir = sys.argv[1]
else:
    print('usage: python3 extract_smaples.py path_to_dir_with_original_files')
    sys.exit(2)

rec_cnt_for_2GiB = 8523973 # number of records
rec_cnt = [rec_cnt_for_2GiB, rec_cnt_for_2GiB // 4, rec_cnt_for_2GiB // 1024, 1000]
out_name_suff = ["big", "medium", "small", "1000r"]

outs = list(map(
    lambda suff: open(os.path.join(path_to_dir, "day_0_repr_sample_" + suff), "w"),
    out_name_suff
))

all_idxs = np.arange(0, rec_cnt_for_2GiB, 1)

np.random.seed(1412191834)

rec_added = [0] * 4

files_cnt = 23

for fno in range(0, files_cnt):
    with open(os.path.join(path_to_dir, "day_0_big_{}".format(fno))) as orig_file:
        np.random.shuffle(all_idxs)
        sorted_idxs_arr = [[]] * len(rec_cnt)
        for i, cnt in enumerate(rec_cnt):
            size = (cnt - rec_added[i]) // (files_cnt - fno);
            sorted_idxs_arr[i] = np.sort(all_idxs[: size])
            rec_added[i] += size
        inds = np.zeros(len(rec_cnt), dtype=int)
        for lno, line in enumerate(orig_file):
            for i, (idxs, out) in enumerate(zip(sorted_idxs_arr, outs)):
                if (inds[i] < idxs.size and lno == idxs[inds[i]]):
                    out.write(line)
                    inds[i] += 1
                else:
                    break # we assume that sorted_idxs[k + 1] \subseteq sorted_idxs[k]
        for out in outs:
            out.flush()

for out in outs:
    out.close()