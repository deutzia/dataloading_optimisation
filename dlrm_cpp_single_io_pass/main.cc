#include <cstdlib>
#include <getopt.h>
#include <iostream>
#include <string>

#include "get_criteo_ad_data.h"

int main(int argc, char *argv[])
{
    int max_ind_range = -1;
    float data_sub_sample_rate = 0;
    int memory_map = 0;
    std::string data_randomize, data_split, data_set, raw_data_file,
        processed_data_file;

    while (true)
    {
        int c;
        static struct option long_options[] = {
            /* These options don’t set a flag.
                 We distinguish them by their indices. */
            {"max-ind-range", optional_argument, 0, 'a'},
            {"data-sub-sample-rate", optional_argument, 0, 'b'},
            {"data-randomize", optional_argument, 0, 'c'},
            {"data-split", optional_argument, 0, 'd'},
            {"memory-map", optional_argument, 0, 'e'},
            {"raw-data-file", optional_argument, 0, 'f'},
            {"processed-data-file", optional_argument, 0, 'g'},
            {0, 0, 0, 0}};
        /* getopt_long stores the option index here. */
        int option_index = 0;

        c = getopt_long(argc, argv, "", long_options, &option_index);

        /* Detect the end of the options. */
        if (c == -1)
            break;

        switch (c)
        {
        case 0:
            std::cout << "option " << long_options[option_index].name;
            if (optarg)
                std::cout << " with arg " << optarg;
            std::cout << std::endl;
            break;

        case 'a':
            max_ind_range = std::stoi(optarg);
            break;

        case 'b':
            data_sub_sample_rate = std::stof(optarg);
            break;

        case 'c':
            data_randomize = optarg;
            break;

        case 'd':
            data_split = optarg;
            break;

        case 'e':
            memory_map = true;
            break;

        case 'f':
            raw_data_file = optarg;
            break;

        case 'g':
            processed_data_file = optarg;
            break;

        case 'h':
            /* getopt_long already printed an error message. */
            break;

        default:
            abort();
        }
    }

    //    printf("max_ind_range=%d data_sub_sample_rate=%f memory_map=%d
    //    data_randomize=%s data_set=%s raw_data_file=%s
    //    processed_data_file=%s\n", max_ind_range, data_sub_sample_rate,
    //    memory_map, data_randomize.c_str(), data_set.c_str(),
    //    raw_data_file.c_str(), processed_data_file.c_str());

    /* Print any remaining command line arguments (not options). */
    if (optind < argc)
    {
        std::cout << "Non-option ARGV-elements found, exiting" << std::endl;
        exit(1);
    }

    get_criteo_ad_data(raw_data_file, "", max_ind_range, data_sub_sample_rate,
                       data_randomize, data_split, memory_map);
}
