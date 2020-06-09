#include <cnpy.h>
#include <cstdint>
#include <filesystem>
#include <iostream>
#include <map>
#include <random>
#include <string>

#include "global.h"
#include "parse.h"
#include "process_one_file.h"

int process_one_file(std::string &datfile, std::string &npzfile, int split,
                     int num_data_in_split, float sub_sample_rate,
                     int max_ind_range, std::vector<float> &rand_u,
                     conv_dict_t convert_dicts[], std::vector<sf_t> &counts,
                     std::vector<df_array_t> &x_int,
                     std::vector<sf_array_t> &x_cat, std::vector<target_t> &y)
{
    std::cout << "Opening: " << datfile << "\n";
    io::CSVReader<40, io::trim_chars<>, io::no_quote_escape<'\t'>> in(datfile);

    int type;
    char *x_int_str[NUM_INT];
    char *x_cat_str[NUM_CAT];

    if (sub_sample_rate == 0.0)
    {
        rand_u.reserve(1);
        rand_u[0] = 1.0;
    }
    else
    {
        std::random_device rd;
        std::mt19937 gen{rd()};
        std::uniform_real_distribution<> dis{0.0, 1.0};
        rand_u.reserve(num_data_in_split);
        for (int i = 0; i < num_data_in_split; i++)
            rand_u[i] = dis(gen);
    }

    x_int.reserve(num_data_in_split);
    x_cat.reserve(num_data_in_split);
    y.reserve(num_data_in_split);
    int sample_count = 0, line_count = 0;
    while (in.read_row(
        // type
        type,
        // 13 features taking integer values
        x_int_str[0], x_int_str[1], x_int_str[2], x_int_str[3], x_int_str[4],
        x_int_str[5], x_int_str[6], x_int_str[7], x_int_str[8], x_int_str[9],
        x_int_str[10], x_int_str[11], x_int_str[12],
        // 26 categorical features
        x_cat_str[0], x_cat_str[1], x_cat_str[2], x_cat_str[3], x_cat_str[4],
        x_cat_str[5], x_cat_str[6], x_cat_str[7], x_cat_str[8], x_cat_str[9],
        x_cat_str[10], x_cat_str[11], x_cat_str[12], x_cat_str[13],
        x_cat_str[14], x_cat_str[15], x_cat_str[16], x_cat_str[17],
        x_cat_str[18], x_cat_str[19], x_cat_str[20], x_cat_str[21],
        x_cat_str[22], x_cat_str[23], x_cat_str[24], x_cat_str[25]))
    {
        float ru;
        if (sub_sample_rate == 0.0)
            ru = rand_u[0];
        else
            ru = rand_u[line_count];
        line_count++;
        if (type == 0 && ru < sub_sample_rate)
            continue;

        y[sample_count] = type;

        for (int q = 0; q < NUM_INT; q++)
            x_int[sample_count][q] = std::max(0, parse_int(x_int_str[q]));
        for (int q = 0; q < NUM_CAT; q++)
        {
            auto key = parse_cat(x_cat_str[q]);

            auto it = convert_dicts[q].find(key);
            if (it != convert_dicts[q].end())
            {
                x_cat[sample_count][q] = it->second;
            }
            else
            {
                convert_dicts[q].insert(std::make_pair(key, counts[q]));
                x_cat[sample_count][q] = counts[q];
                counts[q]++;
            }
        }
        sample_count++;
    }

    std::string filename_s =
        npzfile + "_" + std::to_string(split) + "_processed.npz";
    if (std::filesystem::exists(filename_s))
        std::cout << "\nSkip existing " << filename_s << "\n";
    else
    {
        cnpy::npz_save(filename_s, "X_int", (df_t *)x_int.data(),
                       {(size_t)num_data_in_split, NUM_INT});
        cnpy::npz_save(filename_s, "X_cat", (sf_t *)x_cat.data(),
                       {(size_t)num_data_in_split, NUM_CAT}, "a");
        cnpy::npz_save(filename_s, "y", (target_t *)y.data(),
                       {(size_t)num_data_in_split}, "a");
        std::cout << "\nSaved " << filename_s << "!\n";
    }

    return sample_count;
}