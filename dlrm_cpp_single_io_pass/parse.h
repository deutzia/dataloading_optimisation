#ifndef DATALOADING_OPTIMIZATIONS_PARSE_H
#define DATALOADING_OPTIMIZATIONS_PARSE_H

#include <csv.h>

df_t parse_int(const char *data)
{
    //-1 case
    if (*data == '-')
    {
        return -1;
    }

    df_t result = 0;
    while (*data != '\0')
    {
        result = 10 * result + (*data - '0');
        ++data;
    }
    return result;
}

sf_t parse_cat(const char *data)
{
    if (data[0] == '\0')
    {
        return 0;
    }

    long long result = 0;

    for (int i = 0; i < 8; i++)
    {
        long long data_value =
            (data[i] - ((data[i] >= '0' && data[i] <= '9') ? '0' : ('a' - 10)));
        result += data_value << (28 - 4 * i);
    }

    return result;
}

#endif // DATALOADING_OPTIMIZATIONS_PARSE_H
