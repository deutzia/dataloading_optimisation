#ifndef DATALOADING_OPTIMIZATIONS_PROCESS_ONE_FILE_H
#define DATALOADING_OPTIMIZATIONS_PROCESS_ONE_FILE_H

#include <cstdint>
#include <string>

#include "global.h"

/**
 * Process a file worth of data and reinitialize data.
 * Note that a file main contain a single or multiple splits.
 */
int process_one_file(std::string &datfile, std::string &npzfile, int split,
                     int num_data_in_split, float sub_sample_rate,
                     int max_ind_range, std::vector<float> &rand_u,
                     conv_dict_t convert_dicts[],
                     std::vector<df_array_t> &x_int,
                     std::vector<sf_array_t> &x_cat, std::vector<sf_t> &x_cat_t,
                     std::vector<target_t> &y);

#endif // DATALOADING_OPTIMIZATIONS_PROCESS_ONE_FILE_H
