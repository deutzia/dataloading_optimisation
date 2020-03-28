#include <algorithm>
#include <cnpy.h>
#include <cstdint>
#include <filesystem>
#include <iostream>
#include <random>
#include <string>
#include <vector>

#include "concat_criteo_ad_data.h"
#include "global.h"

std::string concat_criteo_ad_data(
    std::string &d_path, std::string &d_file, std::string &npzfile,
    std::string &trafile, std::string &randomize, std::string &data_split,
    std::vector<unsigned> &total_per_file, unsigned total_count,
    bool memory_map, std::string &o_filename, std::vector<df_array_t> &x_int,
    std::vector<sf_array_t> &x_cat, std::vector<sf_t> &x_cat_t,
    std::vector<target_t> &y)
{
    if (memory_map)
    {
        // create offset per file
        std::vector<int> offset_per_file(DAYS + 1);
        offset_per_file[0] = 0;
        for (int i = 0; i < DAYS; i++)
            offset_per_file[i + 1] = total_per_file[i] + offset_per_file[i];

        // Approach 4: Fisher-Yates-Rao (FYR) shuffle algorithm
        // 1st pass of FYR shuffle
        // check if data already exists
        bool recreate_flag = false;
        for (int j = 0; j < DAYS; j++)
        {
            auto filename_j_y =
                npzfile + "_" + std::to_string(j) + "_intermediate_y.npy";
            auto filename_j_d =
                npzfile + "_" + std::to_string(j) + "_intermediate_d.npy";
            auto filename_j_s =
                npzfile + "_" + std::to_string(j) + "_intermediate_s.npy";
            if (std::filesystem::exists(filename_j_y) &&
                std::filesystem::exists(filename_j_d) &&
                std::filesystem::exists(filename_j_s))
                std::cout << "Using existing\n"
                          << filename_j_y << "\n"
                          << filename_j_d << "\n"
                          << filename_j_s << std::endl;
            else
                recreate_flag = true;
        }

        int max_size =
            *std::max_element(total_per_file.begin(), total_per_file.end());
        x_int.reserve(max_size);
        x_cat.reserve(max_size);
        y.reserve(max_size);

        // reorder across buckets using sampling
        if (recreate_flag)
        {
            // init intermediate files (.npy appended automatically)
            std::fill(y.begin(), y.begin() + max_size, 0);
            for (int i = 0; i < max_size; i++)
                for (int j = 0; j < NUM_INT; j++)
                    x_int[i][j] = 0;
            for (int i = 0; i < max_size; i++)
                for (int j = 0; j < NUM_CAT; j++)
                    x_cat[i][j] = 0;
            for (int j = 0; j < DAYS; j++)
            {
                auto filename_j_y =
                    npzfile + "_" + std::to_string(j) + "_intermediate_y.npy";
                auto filename_j_d =
                    npzfile + "_" + std::to_string(j) + "_intermediate_d.npy";
                auto filename_j_s =
                    npzfile + "_" + std::to_string(j) + "_intermediate_s.npy";
                cnpy::npy_save(filename_j_y, y.data(),
                               {(size_t)total_per_file[j]});
                cnpy::npy_save(filename_j_d, x_int.data(),
                               {(size_t)total_per_file[j], NUM_INT});
                cnpy::npy_save(filename_j_s, x_cat.data(),
                               {(size_t)total_per_file[j], NUM_CAT});
            }
            // start processing files
            std::vector<int> total_counter(DAYS, 0);
            for (int i = 0; i < DAYS; i++)
            {
                auto filename_i =
                    npzfile + "_" + std::to_string(i) + "_processed.npz";
                auto data = cnpy::npz_load(filename_i);
                auto x_cat_data = data["X_cat"].data<sf_array_t>();
                auto x_int_data = data["X_int"].data<df_array_t>();
                auto y_data = data["y"].data<target_t>();
                unsigned size = data["y"].shape[0];
                // sanity check
                assert(("ERROR: sanity check on number of samples failed",
                        total_per_file[i] == size));

                std::cout << "Reordering (1st pass) " << filename_i
                          << std::endl;

                // create buckets using sampling of random ints
                // from (discrete) uniform distribution
                std::vector<std::vector<int>> buckets(DAYS);
                std::vector<int> counter(DAYS, 0);
                int days_to_sample = DAYS - 1;
                if (data_split != "none")
                    days_to_sample--;
                int p;
                if (randomize == "total")
                {
                    std::random_device rd;
                    std::mt19937 gen{rd()};
                    std::uniform_int_distribution<> dis{0, days_to_sample};
                    std::vector<int> rand_u(size);
                    for (int k = 0; k < size; k++)
                        rand_u[k] = dis(gen);
                    for (int k = 0; k < size; k++)
                    {
                        // sample and make sure elements per buckets do not
                        // overflow
                        if (data_split == "none" || i < DAYS - 1)
                        {
                            // choose bucket
                            p = rand_u[k];
                            // retry of the bucket is full
                            while (total_counter[p] + counter[p] >=
                                   total_per_file[p])
                                p = dis(gen);
                        }
                        else // preserve the last day/bucket if needed
                            p = i;
                        buckets[p].push_back(k);
                        counter[p]++;
                    }
                }
                else // randomize is day or none
                    for (int k = 0; k < size; k++)
                    {
                        // do not sample, preserve the data in this bucket
                        p = i;
                        buckets[p].push_back(k);
                        counter[p]++;
                    }

                // sanity check
                assert(("ERROR: sanity check on number of samples failed",
                        std::accumulate(counter.begin(), counter.end(), 0) ==
                            size));

                // partially feel the buckets
                for (int j = 0; j < DAYS; j++)
                {
                    auto filename_j_y = npzfile + "_" + std::to_string(j) +
                                        "_intermediate_y.npy";
                    auto filename_j_d = npzfile + "_" + std::to_string(j) +
                                        "_intermediate_d.npy";
                    auto filename_j_s = npzfile + "_" + std::to_string(j) +
                                        "_intermediate_s.npy";
                    int start = total_counter[j];

                    // target buckets
                    auto fj_y_npy = cnpy::npy_load(filename_j_y);
                    auto fj_y = fj_y_npy.data<target_t>();
                    for (int k = 0; k < counter[j]; k++)
                        fj_y[start + k] = y_data[buckets[j][k]];
                    cnpy::npy_save(filename_j_y, fj_y,
                                   {(size_t)total_per_file[j]});

                    // dense buckets
                    auto fj_d_npy = cnpy::npy_load(filename_j_d);
                    auto fj_d = fj_d_npy.data<df_array_t>();
                    for (int k = 0; k < counter[j]; k++)
                        for (int q = 0; q < NUM_INT; q++)
                            fj_d[start + k][q] = x_int_data[buckets[j][k]][q];
                    cnpy::npy_save(filename_j_d, fj_d,
                                   {(size_t)total_per_file[j], NUM_INT});

                    // sparse buckets
                    auto fj_s_npy = cnpy::npy_load(filename_j_s);
                    auto fj_s = fj_s_npy.data<sf_array_t>();
                    for (int k = 0; k < counter[j]; k++)
                        for (int q = 0; q < NUM_CAT; q++)
                            fj_s[start + k][q] = x_cat_data[buckets[j][k]][q];
                    cnpy::npy_save(filename_j_s, fj_s,
                                   {(size_t)total_per_file[j], NUM_CAT});

                    // update counters for next step
                    total_counter[j] += counter[j];
                }
            }
        }

        // 2nd pass of FYR shuffle
        // check if data already exists
        for (int j = 0; j < DAYS; j++)
        {
            auto filename_j =
                npzfile + "_" + std::to_string(j) + "_reordered.npz";
            if (std::filesystem::exists(filename_j))
                std::cout << "Using existing " << filename_j << std::endl;
            else
                recreate_flag = true;
        }
        // reorder within buckets
        if (recreate_flag)
            for (int j = 0; j < DAYS; j++)
            {
                auto filename_j_y =
                    npzfile + "_" + std::to_string(j) + "_intermediate_y.npy";
                auto filename_j_d =
                    npzfile + "_" + std::to_string(j) + "_intermediate_d.npy";
                auto filename_j_s =
                    npzfile + "_" + std::to_string(j) + "_intermediate_s.npy";
                auto fj_y_npy = cnpy::npy_load(filename_j_y);
                auto fj_d_npy = cnpy::npy_load(filename_j_d);
                auto fj_s_npy = cnpy::npy_load(filename_j_s);
                auto fj_y = fj_y_npy.data<unsigned>();
                std::array<int32_t, NUM_INT> *fj_d =
                    reinterpret_cast<std::array<int32_t, NUM_INT> *>(
                        fj_d_npy.data<int32_t>());
                std::array<uint32_t, NUM_CAT> *fj_s =
                    reinterpret_cast<std::array<uint32_t, NUM_CAT> *>(
                        fj_s_npy.data<uint32_t>());

                std::vector<int> indices(total_per_file[j]);
                for (int i = 0; i < total_per_file[j]; i++)
                    indices[i] = i;
                if ((randomize == "day" || randomize == "total") &&
                    (data_split == "none" || j < DAYS - 1))
                    random_shuffle(indices.begin(), indices.end());

                auto filename_r =
                    npzfile + "_" + std::to_string(j) + "_reordered.npz";
                std::cout << "Reordering (2nd pass) " << filename_r
                          << std::endl;

                for (int i = 0; i < total_per_file[j]; i++)
                {
                    int idx = indices[i];
                    for (int q = 0; q < NUM_CAT; q++)
                        x_cat[i][q] = fj_s[idx][q];
                }
                for (int i = 0; i < total_per_file[j]; i++)
                {
                    int idx = indices[i];
                    for (int q = 0; q < NUM_INT; q++)
                        x_int[i][q] = fj_d[idx][q];
                }
                for (int i = 0; i < total_per_file[j]; i++)
                    y[i] = fj_y[indices[i]];

                cnpy::npz_save(filename_r, "X_cat", x_cat.data(),
                               {(size_t)total_per_file[j], NUM_CAT});
                cnpy::npz_save(filename_r, "X_int", x_int.data(),
                               {(size_t)total_per_file[j], NUM_INT}, "a");
                cnpy::npz_save(filename_r, "y", y.data(),
                               {(size_t)total_per_file[j]}, "a");
            }
    }
    else
    {
        // TODO if memory_map == false
    }

    return o_filename;
}