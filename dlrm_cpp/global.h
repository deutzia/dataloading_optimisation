#ifndef DATALOADING_OPTIMIZATIONS_GLOBAL_H
#define DATALOADING_OPTIMIZATIONS_GLOBAL_H

#include <complex>
#include <unordered_map>

constexpr uint32_t NUM_INT = 13;
constexpr uint32_t NUM_CAT = 26;
constexpr uint32_t DAYS = 24;

typedef int32_t df_t;
typedef uint32_t sf_t;
typedef uint32_t target_t;

// typedef df_t df_array_t[NUM_INT];
// typedef sf_t sf_array_t[NUM_INT];

typedef struct df_array_t
{
    df_t x[NUM_INT];

    df_t &operator[](const int idx)
    {
        return x[idx];
    }
} df_array_t;

typedef struct sf_array_t
{
    sf_t x[NUM_CAT];

    sf_t &operator[](const int idx)
    {
        return x[idx];
    }
} sf_array_t;

typedef std::unordered_map<uint32_t, unsigned int> conv_dict_t;

#endif // DATALOADING_OPTIMIZATIONS_GLOBAL_H
