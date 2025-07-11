---
warning: DO NOT CHANGE THIS MANUALLY, THIS IS GENERATED BY https://github/duckdb/community-extensions repository, check README there
title: arrow
excerpt: |
  DuckDB Community Extensions
  This extension is an alias to the nanoarrow extension. Allows the consumption and production of the Apache Arrow interprocess communication (IPC) format, both from files and directly from stream buffers.

extension:
  name: arrow
  description: This extension is an alias to the nanoarrow extension. Allows the consumption and production of the Apache Arrow interprocess communication (IPC) format, both from files and directly from stream buffers.
  version: 1.2.1
  language: C++
  build: cmake
  license: MIT
  requires_toolchains: "python3" 
  maintainers:
    - pdet
repo:
  github: duckdb/duckdb-extension-alias
  ref: dce7fb0831e2b83d41746381c1a99979eecbe401
  canonical_name: nanoarrow

docs:
  hello_world: |
    -- Read from a file in Arrow IPC format
    FROM 'arrow_file.arrow';
    FROM 'arrow_file.arrows';
    FROM read_arrow('arrow_file.arrow');

    -- Write a file in Arrow IPC stream format
    CREATE TABLE arrow_libraries AS SELECT 'nanoarrow' as name, '0.6' as version;
    COPY arrow_libraries TO 'test.arrows' (FORMAT ARROWS, BATCH_SIZE 100);

    -- Write to buffers: This returns IPC message BLOBs and indicates which one is the header.
    FROM to_arrow_ipc((FROM arrow_libraries));


  extended_description: |
    The Arrow IPC library allows users to read and write data in the Arrow IPC stream format. 
    This can be done by either reading and producing `.arrow` files or by directly reading buffers using their pointers and sizes. 
    It is important to note that reading buffers is dangerous, as an incorrect pointer can crash the database system. 
    This process is temporary and will be deprecated in the future, as clients (e.g., the Python DuckDB client) will have a function that internally extracts these buffers from an Arrow stream.



extension_star_count: 1
extension_star_count_pretty: 1
extension_download_count: 152417
extension_download_count_pretty: 152.4k
image: '/images/community_extensions/social_preview/preview_community_extension_arrow.png'
layout: community_extension_doc
---

### Installing and Loading
```sql
INSTALL {{ page.extension.name }} FROM community;
LOAD {{ page.extension.name }};
```

{% if page.docs.hello_world %}
### Example
```sql
{{ page.docs.hello_world }}```
{% endif %}

{% if page.docs.extended_description %}
### About {{ page.extension.name }}
{{ page.docs.extended_description }}
{% endif %}

### Added Functions

<div class="extension_functions_table"></div>

|   function_name   | function_type | description | comment | examples |
|-------------------|---------------|-------------|---------|----------|
| nanoarrow_version | scalar        | NULL        | NULL    | []       |
| read_arrow        | table         | NULL        | NULL    | []       |
| scan_arrow_ipc    | table         | NULL        | NULL    | []       |
| to_arrow_ipc      | table         | NULL        | NULL    | []       |


