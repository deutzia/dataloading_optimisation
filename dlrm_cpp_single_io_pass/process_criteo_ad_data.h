#ifndef DATALOADING_OPTIMIZATIONS_PROCESS_CRITEO_AD_DATA_H
#define DATALOADING_OPTIMIZATIONS_PROCESS_CRITEO_AD_DATA_H

#include "global.h"
#include <string>

void process_criteo_ad_data(std::string &d_path, std::string &d_file,
                            std::string &npzfile, conv_dict_t convert_dicts[],
                            std::vector<df_array_t> &x_int,
                            std::vector<sf_array_t> &x_cat,
                            std::vector<sf_t> &x_cat_t,
                            std::vector<target_t> &y);

#endif // DATALOADING_OPTIMIZATIONS_PROCESS_CRITEO_AD_DATA_H
