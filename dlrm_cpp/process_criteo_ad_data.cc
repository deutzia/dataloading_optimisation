#include <cnpy.h>
#include <filesystem>
#include <iostream>

#include "process_criteo_ad_data.h"

void process_criteo_ad_data(std::string &d_path, std::string &d_file,
                            std::string &npzfile, conv_dict_t convert_dicts[],
                            std::vector<df_array_t> &x_int,
                            std::vector<sf_array_t> &x_cat,
                            std::vector<sf_t> &x_cat_t,
                            std::vector<target_t> &y)
{
    for (int i = 0; i < DAYS; i++)
    {
        auto filename_i = npzfile + "_" + std::to_string(i) + "_processed.npz";

        if (std::filesystem::exists(filename_i))
            std::cout << "Using existing " << filename_i << std::endl;
        else
        {
            auto data =
                cnpy::npz_load(npzfile + "_" + std::to_string(i) + ".npz");
            // categorical features
            // Approach 2a: using pre-computed dictionaries
            int num_data_in_split = data["X_cat_t"].shape[1];
            x_int.reserve(num_data_in_split);
            x_cat.reserve(num_data_in_split);
            y.reserve(num_data_in_split);
            auto x_cat_t_data = data["X_cat_t"].data<sf_t>();
            for (int j = 0; j < NUM_CAT; j++)
                for (int k = 0; k < num_data_in_split; k++)
                    x_cat[k][j] = convert_dicts[j][x_cat_t_data[j * num_data_in_split + k]];
            // continuous features
            auto x_int_data = data["X_int"].data<df_t>();
            for (int k = 0; k < num_data_in_split; k++)
                for (int j = 0; j < NUM_INT; j++)
                    x_int[k][j] =
                        std::max(0, x_int_data[k * NUM_INT + j]);
            // targets
            auto y_data = data["y"].data<target_t>();

            // save
            cnpy::npz_save(filename_i, "X_int", (df_t*) x_int.data(),
                           {(size_t)num_data_in_split, NUM_INT});
            cnpy::npz_save(filename_i, "X_cat", (sf_t*) x_cat.data(),
                           {(size_t)num_data_in_split, NUM_CAT}, "a");
            cnpy::npz_save(filename_i, "y", (target_t*) y_data, {(size_t)num_data_in_split},
                           "a");
            std::cout << "Processed " << filename_i << std::endl;
        }
        std::cout << std::endl;
    }
}