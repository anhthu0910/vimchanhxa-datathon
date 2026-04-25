import json
nb = json.load(open('notebooks/03_EDA_.ipynb', encoding='utf-8'))
for i, c in enumerate(nb['cells']):
    if c['cell_type'] == 'code':
        if c.get('execution_count') == 9 or any(o.get('output_type') == 'error' for o in c.get('outputs', [])):
            print(f'--- Cell Index {i}, Exec Count {c.get("execution_count")} ---')
            for o in c.get('outputs', []):
                if o.get('output_type') == 'error':
                    print('Error:', o.get('ename'), o.get('evalue'))
