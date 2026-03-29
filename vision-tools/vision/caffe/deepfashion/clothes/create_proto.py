# script creates prototxt file with available clothing categories

import re

INPUT_FILE = "/tytan/raid/fashion/data/deepfashion/CategoryAndAttributePrediction/Anno/list_category_cloth.txt"
OUTPUT_FILE = "/tytan/raid/fashion/detection/lmdb/deepfashion/category_label.prototxt"
DEMO_LABELS_FILE = "/tytan/raid/fashion/detection/lmdb/deepfashion/demo_label.txt"

TEMPLATE = """item {{
  name: "{0}"
  label: {1}
  display_name: "{2}"
}}"""

with open(INPUT_FILE, 'r') as input_file, open(OUTPUT_FILE, 'w') as output_file, open(DEMO_LABELS_FILE, 'w') as demo_file:
    r = []
    d = []
    lines = input_file.read().splitlines()
    n = int(lines[0])
    r.append(TEMPLATE.format("none_of_the_above", 0, "background"))
    for i in range(n):
        line = lines[i + 2]
        line = re.sub(' +', ' ', line)
        cat, _ = line.split(' ')
        r.append(TEMPLATE.format(cat, i + 1, cat))
        d.append("{0} {1}".format(i + 1, cat))

    output_file.write("\n".join(r))
    demo_file.write("\n".join(d))

