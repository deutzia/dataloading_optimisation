COMPILER = clang++
HOMEDIR = ..
CNPY = $(HOMEDIR)/cnpy
CSV_PARSER = $(HOMEDIR)/fast-cpp-csv-parser
CPPFLAGS = -Wall -Wextra -std=c++17 -O2 -pthread
INCFLAGS = -I$(CNPY) -I$(CSV_PARSER)
LINKFLAGS = -L$(CNPY) -lcnpy -lz

-include $(OBJS:.o=.d)

SRCS = main.cc get_criteo_ad_data.cc process_one_file.cc process_criteo_ad_data.cc concat_criteo_ad_data.cc
OBJS = $(SRCS:.cc=.o)

main: $(OBJS)
	$(COMPILER) $(CPPFLAGS) $(LINKFLAGS) $(OBJS) -o main

# This is some dark magic and I don't want to understand
# http://www.scottmcpeak.com/autodepend/autodepend.html
%.o: %.cc
	$(COMPILER) -c $(CPPFLAGS) $(INCFLAGS) $(DEPFLAGS) $< -o $@
	$(COMPILER) -MM $(CPPFLAGS) $(INCFLAGS) $(DEPFLAGS) $< -o $*.d
	@mv -f $*.d $*.d.tmp
	@sed -e 's|.*:|$*.o:|' < $*.d.tmp > $*.d
	@sed -e 's/.*://' -e 's/\\$$//' < $*.d.tmp | fmt -1 | \
	  sed -e 's/^ *//' -e 's/$$/:/' >> $*.d
	@rm -f $*.d.tmp

clean:
	@rm -f $(OBJS) main
	@rm -rf *.d

