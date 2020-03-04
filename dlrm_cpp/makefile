COMPILER = clang++
HOMEDIR = ..
CNPY = $(HOMEDIR)/cnpy
CSV_PARSER = $(HOMEDIR)/fast-cpp-csv-parser
CPPFLAGS = -Wall -Wextra -std=c++17 -O2
INCFLAGS = -I$(CNPY) -I$(CSV_PARSER)
LINKFLAGS = -L$(CNPY) -lcnpy -lz

DEPDIR := .d
DEPFLAGS = -MT $@ -MMD -MP -MF $(DEPDIR)/$*.d
$(shell mkdir -p $(DEPDIR) >/dev/null)

SRCS = main.cc
OBJS = $(SRCS:.cc=.o)

main: $(OBJS)
	$(COMPILER) $(CPPFLAGS) $(LINKFLAGS) $(OBJS) -o main

%.o: %.cc $(DEPDIR)/%.d
	$(COMPILER) $(CPPFLAGS) $(INCFLAGS) $(DEPFLAGS) $< -o $@ -c

clean:
	@rm -f $(OBJS) main
	@rm -rf .d/

$(DEPDIR)/%.d: ;
.PRECIOUS: $(DEPDIR)/%.d

include $(wildcard $(patsubst %,$(DEPDIR)/%.d,$(basename $(SRCS))))
