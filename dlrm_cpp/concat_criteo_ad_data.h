#ifndef DATALOADING_OPTIMIZATIONS_CONCAT_CRITEO_AD_DATA_H
#define DATALOADING_OPTIMIZATIONS_CONCAT_CRITEO_AD_DATA_H

#include <cstdint>
#include <string>
#include <vector>

#include "global.h"

std::string concat_criteo_ad_data(
    std::string &d_path, std::string &d_file, std::string &npzfile,
    std::string &trafile, std::string &randomize, std::string &data_split,
    std::vector<unsigned> &total_per_file, unsigned total_count,
    bool memory_map, std::string &o_filename, std::vector<df_array_t> &x_int,
    std::vector<sf_array_t> &x_cat, std::vector<sf_t> &x_cat_t,
    std::vector<target_t> &y);

#endif // DATALOADING_OPTIMIZATIONS_CONCAT_CRITEO_AD_DATA_H
