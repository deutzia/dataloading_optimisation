#include<csv.h>
#include<cnpy.h>
#include<complex>
#include<cstdlib>
#include<iostream>
#include<map>
#include<string>

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
    //TODO program arguments
    int max_ind_range = 9999 * 9999;

    std::cout << "Opening: " << argv[1] << "\n";
    io::CSVReader<40, io::trim_chars<>, io::no_quote_escape<'\t'>> in(argv[1]);

    int type;
    char *x_int[13];
    char *x_cat[26];

    while (in.read_row(
            //type
            type,
            //13 features taking integer values
            x_int[0], x_int[1], x_int[2], x_int[3], x_int[4],
            x_int[5], x_int[6], x_int[7], x_int[8], x_int[9],
            x_int[10], x_int[11], x_int[13],
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