#ifndef DATALOADING_OPTIMIZATIONS_GET_CRITEO_AD_DATA_H
#define DATALOADING_OPTIMIZATIONS_GET_CRITEO_AD_DATA_H

#include <string>

std::string
get_criteo_ad_data(std::string &datafile, std::string o_filename = "",
                   int max_ind_range = -1, float sub_sample_rate = 0.0,
                   std::string randomize = "total",
                   std::string data_split = "train", bool memory_map = false);

#endif // DATALOADING_OPTIMIZATIONS_GET_CRITEO_AD_DATA_H