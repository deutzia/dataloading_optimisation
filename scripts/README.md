Contents:
- [Extracting representative samples from file day_0](https://github.com/deutzia/dataloading_optimisation/new/master/scripts#extracting-representative-samples-from-file-day_0)

# Extracting representative samples from file day_0

## Spliting `day_0`

Spliting `day_0` into 23 files `day_0_big_0`, ..., `day_0_big_22`
```bash
for i in {0..22}; do split -d -n l/${i+1}/23 day_0 > day_0_big_$i; done
```

## Creating files with representative samples

Extracting samples from the files `day_0_big_0`, ..., `day_0_big_22` into files:
- `day_0_repr_sample_big` (~2GiB)
- `day_0_repr_sample_medium` (~0.5GiB)
- `day_0_repr_sample_small` (~2MiB)
- `day_0_repr_sample_1000r` (~250KiB - 1000 records)

Records from the above files meet the following condition:

`day_0_repr_sample_1000r` ⊆ `day_0_repr_sample_small` ⊆ `day_0_repr_sample_medium` ⊆ `day_0_repr_sample_big`

```
python3 extract_smaples.py <path>
```
where `<path>` link to a directory containing files `day_0_big_0`, ..., `day_0_big_22`
