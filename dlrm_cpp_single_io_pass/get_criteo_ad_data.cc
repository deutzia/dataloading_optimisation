#include <cnpy.h>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <map>
#include <regex>
#include <string>
#include <vector>

#include "concat_criteo_ad_data.h"
#include "get_criteo_ad_data.h"
#include "global.h"
#include "process_one_file.h"

std::string get_criteo_ad_data(std::string &datafile, std::string o_filename,
                               int max_ind_range, float sub_sample_rate,
                               std::string randomize, std::string data_split,
                               bool memory_map)
{
    // split the datafile into path and filename
    auto found = datafile.find_last_of("/");
    auto d_path = datafile.substr(0, found) + "/";
    auto d_file = datafile.substr(found + 1);
    auto &npzfile = datafile;
    auto trafile = d_path + "fea";

    // count number of datapoints in training set
    unsigned total_count = 0;
    std::vector<unsigned> total_per_file;
    total_per_file.resize(DAYS);
    auto total_file = d_path + d_file + "_day_count.npz";

    if (std::filesystem::exists(total_file))
    {
        auto npy = cnpy::npz_load(total_file, "total_per_file");
        unsigned *total_per_file_loaded = npy.data<unsigned>();
        for (int i = 0; i < DAYS; i++)
        {
            total_per_file[i] = total_per_file_loaded[i];
            total_count += total_per_file[i];
        }
        std::cout << "Skipping counts per file (already exist)" << std::endl;
    }
    else
    {
        for (int i = 0; i < DAYS; i++)
        {
            auto datfile_i = npzfile + "_" + std::to_string(i);
            std::ifstream datafile_ifstream{datfile_i};

            // new lines will be skipped unless we stop it from happening:
            datafile_ifstream.unsetf(std::ios_base::skipws);

            // count the newlines with an algorithm specialized for counting:
            total_per_file[i] =
                std::count(std::istream_iterator<char>(datafile_ifstream),
                           std::istream_iterator<char>(), '\n');
            total_count += total_per_file[i];
        }
    }

    // create all splits (reuse existing files if possible)
    bool recreate_flag = false;
    conv_dict_t convert_dicts[NUM_CAT];
    std::vector<sf_t> counts(NUM_CAT);
    std::vector<float> rand_u;

    std::vector<df_array_t> x_int;
    std::vector<sf_array_t> x_cat;
    std::vector<target_t> y;

    for (int i = 0; i < DAYS; i++)
    {
        auto datfile_i = npzfile + "_" + std::to_string(i);
        auto npzfile_p = npzfile + "_" + std::to_string(i) + "_processed.npz";
        if (std::filesystem::exists(npzfile_p))
            std::cout << "Skip existing " << npzfile_p << std::endl;
        else
        {
            recreate_flag = true;
            total_per_file[i] = process_one_file(
                datfile_i, npzfile, i, total_per_file[i], sub_sample_rate,
                max_ind_range, rand_u, convert_dicts, counts, x_int, x_cat, y);
        }
    }

    // report and save total into a file
    total_count = 0;
    for (auto t : total_per_file)
        total_count += t;

    if (!std::filesystem::exists(total_file))
        cnpy::npz_save(total_file, "total_per_file", total_per_file);
    std::cout << "Total number of samples: " << total_count
              << "\nDivided into days/splits:\n[";
    std::string separator;
    for (auto t : total_per_file)
    {
        std::cout << separator << t;
        separator = ", ";
    }
    std::cout << "]" << std::endl;

    // dictionary files
    if (recreate_flag)
    {
        // create dictionaries
        for (int j = 0; j < NUM_CAT; j++)
        {
            auto dict_file_j =
                d_path + d_file + "_fea_dict_" + std::to_string(j) + ".npz";
            if (!std::filesystem::exists(dict_file_j))
            {
                std::vector<sf_t> unique(convert_dicts[j].size());
                for (auto it = convert_dicts[j].begin();
                     it != convert_dicts[j].end(); it++)
                    unique[it->second] = it->first;
                cnpy::npz_save(dict_file_j, "unique", unique);
            }
        }
        // store (uniques and) counts
        auto count_file = d_path + d_file + "_fea_count.npz";
        if (!std::filesystem::exists(count_file))
            cnpy::npz_save(count_file, "counts", counts);
    }
    else
    {
        // create dictionaries (from existing files)
        // load uniques and counts
        for (int j = 0; j < NUM_CAT; j++)
        {
            auto dict_file_j =
                d_path + d_file + "_fea_dict_" + std::to_string(j) + ".npz";
            auto unique_npy = cnpy::npz_load(dict_file_j, "unique");
            auto unique = unique_npy.data<sf_t>();
            for (int i = 0; i < unique_npy.shape[0]; i++)
                convert_dicts[j][unique[i]] = i;
        }

        auto count_file = d_path + d_file + "_fea_count.npz";
        auto counts_npy = cnpy::npz_load(count_file, "counts");
        auto counts_data = counts_npy.data<unsigned>();
        for (int j = 0; j < NUM_CAT; j++)
            counts[j] = counts_data[j];
    }

    auto o_file = concat_criteo_ad_data(
        d_path, d_file, npzfile, trafile, randomize, data_split, total_per_file,
        total_count, memory_map, o_filename, x_int, x_cat, y);

    return o_file;
}