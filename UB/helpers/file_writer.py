

def load_lines(filepath):
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()

