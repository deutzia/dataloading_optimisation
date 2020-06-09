#include <sstream>
#include <thread>

#include "global.h"

#ifdef DEBUG

std::stringstream &sstream()
{
    static thread_local std::stringstream stream;
    return stream;
};

#endif