import os
import json
import glob

base_dir = r"d:\dodge ai_assignment\sap-order-to-cash-dataset\sap-o2c-data"
schemas = {}

for root, dirs, files in os.walk(base_dir):
    for d in dirs:
        dir_path = os.path.join(root, d)
        jsonl_files = glob.glob(os.path.join(dir_path, '*.jsonl'))
        if jsonl_files:
            file_path = jsonl_files[0]
            with open(file_path, 'r', encoding='utf-8') as f:
                line = f.readline()
                if line:
                    try:
                        data = json.loads(line)
                        schemas[d] = list(data.keys())
                    except Exception as e:
                        pass

with open('schemas.json', 'w') as out_f:
    json.dump(schemas, out_f, indent=2)
print("Schemas saved to schemas.json")
