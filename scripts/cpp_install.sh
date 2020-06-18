#!/usr/bin/env bash

git submodule init
git submodule update

cd cnpy
cmake -DCMAKE_INSTALL_PREFIX=. .
make
