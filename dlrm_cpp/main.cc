#include<csv.h>
#include<cnpy.h>
#include<complex>
#include<cstdlib>
#include<iostream>
#include<map>
#include<string>
#include<getopt.h>

int parse_int(const char *data)
{
    //-1 case
    if (*data == '-')
    {
        return -1;
    }

    int result = 0;
    while (*data != '\0')
    {
        result = 10 * result + (*data - '0');
        ++data;
    }
    return result;
}

unsigned int parse_cat(const char *data)
{
    if (data[0] == '\0')
    {
        return 0;
    }
    unsigned int result = 0;
    for (int i = 0; i < 8; i++)
    {
        unsigned int data_value = (data[i] - ((data[i] >= '0' && data[i] <= '9') ? '0' : ('a' - 10)));
        result += data_value << (28 - 4 * i);
    }

    return result;
}

int main(int argc, char *argv[])
{
    int max_ind_range = -1;
    float data_sub_sample_rate = 0;
    int memory_map = 0;
    std::string data_randomize, data_set, raw_data_file, processed_data_file;

    while (1)
    {
        int c;
        static struct option long_options[] =
        {
            /* These options don’t set a flag.
                 We distinguish them by their indices. */
            {"max-ind-range",           optional_argument, 0, 'a'},
            {"data-sub-sample-rate",    optional_argument, 0, 'b'},
            {"data-randomize",          optional_argument, 0, 'c'},
            {"memory-map",              optional_argument, 0, 'd'},
            {"raw-data-file",           optional_argument, 0, 'e'},
            {"processed-data-file",     optional_argument, 0, 'f'},
            {0, 0, 0, 0}
        };
        /* getopt_long stores the option index here. */
        int option_index = 0;

        c = getopt_long (argc, argv, "", long_options, &option_index);

        /* Detect the end of the options. */
        if (c == -1)
            break;

        switch (c)
        {
            case 0:
                printf ("option %s", long_options[option_index].name);
                if (optarg)
                    printf (" with arg %s", optarg);
                printf ("\n");
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
                memory_map = true;
                break;

            case 'e':
                raw_data_file = optarg;
                break;

            case 'f':
                processed_data_file = optarg;
                break;

            case '?':
                /* getopt_long already printed an error message. */
                break;

            default:
                abort();
        }
    }

//    printf("max_ind_range=%d data_sub_sample_rate=%f memory_map=%d data_randomize=%s data_set=%s raw_data_file=%s processed_data_file=%s\n", max_ind_range, data_sub_sample_rate, memory_map, data_randomize.c_str(), data_set.c_str(), raw_data_file.c_str(), processed_data_file.c_str());

    /* Print any remaining command line arguments (not options). */
    if (optind < argc)
    {
        printf("Non-option ARGV-elements found, exiting");
        exit(1);
    }

    std::cout << "Opening: " << raw_data_file << "\n";
    io::CSVReader<40, io::trim_chars<>, io::no_quote_escape<'\t'>> in(raw_data_file);

    int type;
    char *x_int[13];
    char *x_cat[26];

    while (in.read_row(
            //type
            type,
            //13 features taking integer values
            x_int[0], x_int[1], x_int[2], x_int[3], x_int[4],
            x_int[5], x_int[6], x_int[7], x_int[8], x_int[9],
            x_int[10], x_int[11], x_int[12],
            //26 categorical features
            x_cat[0], x_cat[1], x_cat[2], x_cat[3], x_cat[4],
            x_cat[5], x_cat[6], x_cat[7], x_cat[8], x_cat[9],
            x_cat[10], x_cat[11], x_cat[12], x_cat[13], x_cat[14],
            x_cat[15], x_cat[16], x_cat[17], x_cat[18], x_cat[19],
            x_cat[20], x_cat[21], x_cat[22], x_cat[23], x_cat[24],
            x_cat[25]
    ))
    {
        for (int q = 0; q < 13; q++)
        {
            parse_int(x_int[q]);
            //TODO
        }
        for (int q = 0; q < 26; q++)
        {
            parse_cat(x_cat[q]);
            //TODO
        }
    }
}
