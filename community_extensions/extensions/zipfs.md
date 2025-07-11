---
warning: DO NOT CHANGE THIS MANUALLY, THIS IS GENERATED BY https://github/duckdb/community-extensions repository, check README there
title: zipfs
excerpt: |
  DuckDB Community Extensions
  Read files within zip archives

extension:
  name: zipfs
  description: Read files within zip archives
  version: 1.2.2
  language: C++
  build: cmake
  license: MIT
  maintainers:
    - isaacbrodsky
  excluded_platforms: "windows_amd64_rtools;windows_amd64_mingw"

repo:
  github: isaacbrodsky/duckdb-zipfs
  ref: 6d4f61fb15cb1d6b258492631c885887bed4de14

docs:
  hello_world: |
    SELECT * FROM 'zip://my_zip.zip/my_file.csv';
  extended_description: |
    The zipfs extension adds support for reading files from within zip archives.

extension_star_count: 32
extension_star_count_pretty: 32
extension_download_count: 17221
extension_download_count_pretty: 17.2k
image: '/images/community_extensions/social_preview/preview_community_extension_zipfs.png'
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


