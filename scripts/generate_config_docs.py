import os
import sys
import re
import subprocess
import csv
import io

if len(sys.argv) < 2:
    print(
        "Expected usage: python3 scripts/generate_config_docs.py /path/to/duckdb/binary"
    )
    exit(1)

db_path = sys.argv[1]

keywords = [
    'STANDARD',
    'DETAILED',
    'ALL',
    'OPTIMIZED_ONLY',
    'PHYSICAL_ONLY',
    'JSON',
    'QUERY_TREE',
    'ASC',
    'DESC',
    'NULLS_FIRST',
    'NULLS_LAST',
    'AUTOMATIC',
    'READ_ONLY',
    'READ_WRITE',
]

description_replacement = "description.replace('e.g. ', 'e.g., ')"
for keyword in keywords:
    description_replacement += f".replace('{keyword}', '**{keyword}**')"

cmd = f'''
.mode markdown
INSTALL httpfs;
LOAD httpfs;
CREATE MACRO surround_with_backticks(str) AS '`' || str || '`';
SELECT
    substr(name, 2, (LEN(name) - 2)::int) AS Name,
    {description_replacement} AS Description,
    surround_with_backticks(input_type) AS "Input type",
    default_value AS "Default value"
FROM (
SELECT ARRAY_AGG(surround_with_backticks(name))::VARCHAR AS name, description, input_type,
	FIRST(CASE
    WHEN value = ''
    THEN ''
    WHEN name='memory_limit' OR name='max_memory'
	THEN '80% of RAM'
    WHEN name='secret_directory'
    THEN '`' || regexp_replace(value, '/(home|Users)/[a-z][-a-z0-9_]*/', '~/') || '`'
	WHEN name='threads' OR name='worker_threads'
	THEN '# Cores'
	WHEN name='TimeZone'
	THEN 'System (locale) timezone'
	WHEN name='Calendar'
	THEN 'System (locale) calendar'
	WHEN lower(value) IN ('null', 'nulls_last', 'asc', 'desc')
	THEN surround_with_backticks(upper(value))
    ELSE surround_with_backticks(value) END) AS default_value
FROM duckdb_settings()
WHERE name NOT LIKE '%debug%' AND description NOT ILIKE '%debug%'
GROUP BY description, input_type
) tbl
ORDER BY 1
;
'''


res = subprocess.run(
    db_path,
    input=bytearray(cmd, 'utf8'),
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)
stdout = res.stdout.decode('utf8').strip()
stderr = res.stderr.decode('utf8').strip()

if len(stderr) != 0:
    print("Failed to run command " + cmd)
    print(stdout)
    print(stderr)
    exit(1)

option_split = '## Configuration Reference'
doc_file = 'docs/configuration/overview.md'

with open(doc_file, 'r') as f:
    text = f.read()

if option_split not in text:
    print("Could not find " + option_split)
    exit(1)

text = text.split(option_split)[0]

text += (
    option_split
    + "\n\nNote that configuration options come with different default [scopes](statements/set#scopes). These will be documented in the future. For now, please consult the [source code](https://github.com/duckdb/duckdb/blob/v0.10.0/src/main/config.cpp#L56)."
    + "\n\n<!-- This section is generated by scripts/generate_config_docs.py -->\n\n"
    + "Below is a list of all available settings."
)

text += '\n\n' + stdout + '\n'
text = re.sub(
    r'^\|---*\|---*\|---*\|---*\|$', '|----|--------|--|---|', text, flags=re.MULTILINE
)
text = text.replace('**QUERY_TREE**_OPTIMIZER', '**QUERY_TREE_OPTIMIZER**')

with open(doc_file, 'w+') as f:
    f.write(text)
