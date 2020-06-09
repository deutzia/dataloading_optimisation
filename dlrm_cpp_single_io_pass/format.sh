for f in *.c *.h *.cpp *.hpp *.cc; do
    if [ -f $f ] ; then
        clang-format -i $f
    fi
done
