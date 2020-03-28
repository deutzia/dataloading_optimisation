import sys

# Ensures that the project root path belongs to the paths variable of the launched script
suffix = "dataloading_optimisation/"
path = None
for p in sys.path:
    pos = p.find(suffix)
    if (pos != -1):
        path = p[:pos + len(suffix)]

if (path == None):
    raise Exception("No path containing 'dataloading_optimisation/'")
elif (not path in sys.path):
    sys.path.append(path)