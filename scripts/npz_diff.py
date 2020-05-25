import sys
import numpy as np

def npz_equal(
        npz_file_path1,
        npz_file_path2
):
    are_equal = True

    with np.load(npz_file_path1) as f1, np.load(npz_file_path2) as f2:

        paths = (npz_file_path1, npz_file_path2)
        files = (f1, f2)

        # check types of objects returned by np.load
        for f, path in zip(files, paths):
            if type(f) != np.lib.npyio.NpzFile:
                are_equal = False
                print(f"The type of a loaded object for the file '{path}' is not np.lib.npyio.NpzFile", file=sys.stderr)

        # check objects' keys
        objs_keys = tuple(set(f.keys()) for f in files)
        common_keys = objs_keys[0].intersection(objs_keys[1])
        # check if keys sets are equal
        if len(common_keys) < max(len(objs_keys[0]), len(objs_keys[1])):
            are_equal = False
            print(f"Keys in the loaded objects are not the same:", file=sys.stderr)
            for path, keys in zip(paths, objs_keys):
                addit_keys = keys - common_keys
                if len(addit_keys) > 0:
                    print(f"  - additonal keys in the object from file '{path}': {', '.join(addit_keys)}",
                          file=sys.stderr)

        # iterate over common keys and check equality of their values
        for key in common_keys:
            if not np.array_equal(files[0][key], files[1][key]):
                are_equal = False
                print(f"Arrays for the key '{key}' are not equal in the objects loaded from files {' and '.join(paths)}", file=sys.stderr)

    return are_equal

# a1 = np.random.rand(3, 2)
#
# b1 = np.random.rand(4)
# b2 = np.random.rand(4)
#
# np.savez_compressed('tmp1', a=a1, b=b1, d=b1)
# np.savez_compressed('tmp2', c=b1, a=a1, b=b2, d=a1)
# np.savez_compressed('tmp3', a=a1, b=b1, d=b1)
#
#
# print(npz_equal('tmp1.npz', 'tmp2.npz'), file=sys.stderr)
#
# print(npz_equal('tmp1.npz', 'tmp3.npz'), file=sys.stderr)