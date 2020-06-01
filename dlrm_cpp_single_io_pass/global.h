#ifndef DATALOADING_OPTIMIZATIONS_GLOBAL_H
#define DATALOADING_OPTIMIZATIONS_GLOBAL_H

#include <complex>
#include <unordered_map>
#include <sstream>

#ifdef DEBUG

const bool DB = true;

std::stringstream& sstream();

#define FLUSH(cond) {if (cond) {std::clog << sstream().str(); sstream().str("");}}
#define PRINT(cond, val) {if (cond) {sstream() << val;}}
#define PRINTLN(cond, val) {if (cond) {sstream() << val << "\n";}}
#define PRINTLNF(cond, val) {PRINTLN(cond, val) FLUSH(cond)}
#define DEB(cond, instr) instr;

#else

const bool DB = false;

#define FLUSH(cond) ;
#define PRINT(cond, val) ;
#define PRINTLN(cond, val) ;
#define PRINTLNF(cond, val) ;
#define DEB(cond, instr) ;

#endif

constexpr uint32_t NUM_INT = 13;
constexpr uint32_t NUM_CAT = 26;
constexpr uint32_t DAYS = 24;

typedef int32_t df_t;
typedef int32_t sf_t;
typedef int32_t target_t;

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

typedef std::unordered_map<sf_t, unsigned int> conv_dict_t;

#endif // DATALOADING_OPTIMIZATIONS_GLOBAL_H
