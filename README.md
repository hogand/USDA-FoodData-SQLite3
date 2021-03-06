# USDA FoodData CSV Converter

USDA makes the FoodData Central database available in CSV and MS Access 2007.

The public domain source files are [here](https://fdc.nal.usda.gov/download-datasets.html).

The importers in this repo can convert USDA CSV to [SQLite3](https://www.sqlite.org).

There are two importers: shell script using Sqlite3 CLI and Python v3.

## Quick and Dirty Shell Importer

The fast importer uses the native sqlite3 command line interface to import the
files.  It uses the autogenerated schema and adds a few indices.

### Usage

```sh
$ sh ./import_fast.sh <dir_of_CSVs> <output_db>
```

## Python3 Importer

The python importer is about half as fast, but attempts to define a schema.
It uses foreign keys when possible and type hinting in Python 3.x.

I had to exclude some foreign keys because the source CSV files appear to
have data quality issues.

### Usage

```sh
$ python3 import_food_data.py [-d <dir_of_CSVs>] [-o <output_db] [-f] [-v]
```

## Source

Tested with CSVs from 2019-04-02.

### More Info

See [example queries](./QUERY.md) and [TODO](./TODO.md) for more info.

