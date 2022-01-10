#!env python3

"""Convert the USDA's FoodData Central CSV files into a single sqlite3 file.

https://fdc.nal.usda.gov/download-datasets.html and select "All Foods" zip.
"""

# Copyright (c) 2019 Doug Hogan <github@acyclic.org>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import argparse
import csv
import os
import os.path
import sqlite3
import sys
from glob import glob
from typing import List, Optional


def import_csv(cursor: sqlite3.Cursor, csvfile: str, batch: int = 1000,
               verbose: bool = False) -> None:
    """Import a given USDA FoodData Central CSV file.
    Assumes that the schema has already been created."""

    table = os.path.basename(csvfile)[:-4]
    rows = []

    with open(csvfile, newline='') as desc:
        reader = csv.reader(desc, strict=True)
        next(reader)  # Skip the header
        for row in reader:
            # Replace "" with None so NULL values are handled properly.
            rows.append(list(map(lambda x: None if x == "" else x, row)))

            if len(rows) >= batch:
                rows = insert_many(cursor, table, rows, verbose)

        if rows:
            rows = insert_many(cursor, table, rows, verbose)


def insert_many(cursor: sqlite3.Cursor, table: str, rows: List[List[Optional[str]]],
                verbose: bool = False) -> List[List[Optional[str]]]:
    """Insert many rows into a table."""

    placeholders = ','.join(['?'] * len(rows[0]))
    sql = f"INSERT INTO {table} VALUES ({placeholders})"
    if verbose:
        print(f"Running {sql} with {rows}")
    cursor.executemany(sql, rows)
    return []


def query_counts(cursor: sqlite3.Cursor, csv_count_file: str, verbose: bool = False) -> None:
    """Double check the number of rows on disk matches the count file"""

    with open(csv_count_file, newline='') as desc:
        reader = csv.reader(desc, strict=True)
        next(reader)  # Skip the header
        for row in reader:
            row = [x.replace('"', '') for x in row]
            table, count = row[0], int(row[1])

            try:
              num_rows = cursor.execute(f'''
  SELECT COUNT(*) AS {table}_count
  FROM {table};
  ''').fetchone()[0]
            except sqlite3.OperationalError as err:
              print(f"Ignoring: {type(err)}: {err=}")
            if verbose:
                print(f"Inserted {num_rows} into {table}")
            if num_rows != count:
                print(f"==> Expected {count} but inserted {num_rows} in {table}")


def sqlite3_schema(cursor: sqlite3.Cursor) -> None:
    """SQLite3 Schema for USDA's FoodData Central database"""

    cursor.executescript('''
CREATE TABLE acquisition_sample (
  "fdc_id_of_sample_food"      INT REFERENCES food(fdc_id),
  "fdc_id_of_acquisition_food" INT REFERENCES food(fdc_id),

  PRIMARY KEY(fdc_id_of_sample_food, fdc_id_of_acquisition_food)
);

CREATE TABLE agricultural_acquisition (
  "fdc_id"           INT NOT NULL PRIMARY KEY,
  "acquisition_date" TEXT
      CHECK(acquisition_date IS NULL OR
            acquisition_date GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]' IS 1),
  "market_class"     TEXT,
  "treatment"        TEXT,
  "state"            TEXT
);

CREATE TABLE branded_food (
  "fdc_id"                     INT NOT NULL PRIMARY KEY REFERENCES food(fdc_id),
  "brand_owner"                TEXT,  -- XXX Inconsistent names
  "brand_name"                 TEXT,
  "subbrand_name"              TEXT,
  "gtin_upc"                   TEXT,
  "ingredients"                TEXT,
  "not_a_significant_source_of" TEXT,
  "serving_size"               REAL,
--  "serving_size_unit"          TEXT
--      CHECK(serving_size_unit IS NULL OR
--            serving_size_unit IN ('g', 'ml')),
  "serving_size_unit"          TEXT,
  "household_serving_fulltext" TEXT,
  "branded_food_category"      TEXT,
--  "data_source"                TEXT
--      CHECK(data_source IS NULL OR data_source IN ('GDSN', 'LI')),
  "data_source"                TEXT,
  "package_weight"             TEXT,
--  "modified_date"              TEXT
--      CHECK(modified_date IS NULL OR
--            modified_date GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]' IS 1),
--  "available_date"             TEXT
--      CHECK(available_date IS NULL OR
--            available_date GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]' IS 1),
  "modified_date"              TEXT,
  "available_date"             TEXT,
  "market_country"             TEXT,
--  "discontinued_date"              TEXT
--      CHECK(discontinued_date IS NULL OR
--            discontinued_date GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]' IS 1)
  "discontinued_date"              TEXT
);

CREATE INDEX idx_branded_food_gtin_upc              ON branded_food (gtin_upc);
CREATE INDEX idx_branded_food_branded_food_category ON branded_food (branded_food_category);

CREATE TABLE food (
  "fdc_id"           INT NOT NULL PRIMARY KEY,
  "data_type"        TEXT,
  "description"      TEXT,
--  "food_category_id" INT REFERENCES food_category(id),
  "food_category_id" INT,
  "publication_date" TEXT
      CHECK(publication_date IS NULL OR
            publication_date GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]' IS 1)
--  "scientific_name"  TEXT
--  "food_key"         TEXT
);

CREATE INDEX idx_food_data_type        ON food (data_type);
CREATE INDEX idx_food_food_category_id ON food (food_category_id);

CREATE TABLE food_attribute (
  "id"                     INT NOT NULL PRIMARY KEY,
  "fdc_id"                 INT REFERENCES food(fdc_id),
  "seq_num"                INT,
  "food_attribute_type_id" INT REFERENCES food_attribute_type(id),
  "name"                   TEXT,
  "value"                  TEXT
);

CREATE INDEX idx_food_attribute_fdc_id                 ON food_attribute (fdc_id);
CREATE INDEX idx_food_attribute_food_attribute_type_id ON food_attribute (food_attribute_type_id);

CREATE TABLE food_attribute_type (
  "id"          INT NOT NULL PRIMARY KEY,
  "name"        TEXT,
  "description" TEXT
);

CREATE TABLE food_calorie_conversion_factor (
--  "food_nutrient_conversion_factor_id" INT NOT NULL PRIMARY KEY REFERENCES food_nutrient_conversion_factor(id),
  "food_nutrient_conversion_factor_id" INT NOT NULL PRIMARY KEY,
  "protein_value"      REAL,
  "fat_value"          REAL,
  "carbohydrate_value" REAL
);

CREATE TABLE food_category (
  "id"          INT NOT NULL PRIMARY KEY,
  "code"        TEXT,
  "description" TEXT
);

CREATE TABLE food_component (
  "id"                INT NOT NULL PRIMARY KEY,
  "fdc_id"            INT REFERENCES food(fdc_id),
  "name"              TEXT,
  "pct_weight"        REAL,
  "is_refuse"         TEXT
      CHECK(is_refuse IN ('Y', 'N')),
  "gram_weight"       REAL,
  "data_points"       INT,
  "min_year_acquired" TEXT
      CHECK(min_year_acquired IS NULL OR
            min_year_acquired GLOB '[0-9][0-9][0-9][0-9]' IS 1)
);

CREATE INDEX idx_food_component_fdc_id ON food_component (fdc_id);

-- XXX Field Descriptions describes "food_fat_conversion_factor" but there is no table for it.
-- XXX File is missing?

CREATE TABLE food_nutrient (
  "id"                INT NOT NULL PRIMARY KEY,
--  "fdc_id"            INT REFERENCES food(fdc_id),
  "fdc_id"            INT,
--  "nutrient_id"       INT REFERENCES nutrient(id),
  "nutrient_id"       INT,
  "amount"            REAL,
  "data_points"       INT,
--  "derivation_id"     INT REFERENCES food_nutrient_derivation(id),
  "derivation_id"     INT,
  -- XXX Missing standard_error from Field Descriptions
  "min"               REAL,
  "max"               REAL,
  "median"            REAL,
  "loq"               REAL,
  "footnote"          TEXT,
  "min_year_acquired" TEXT
      CHECK(min_year_acquired IS NULL OR
            min_year_acquired GLOB '[0-9][0-9][0-9][0-9]' IS 1)
);

CREATE INDEX idx_food_nutrient_fdc_id         ON food_nutrient (fdc_id);
CREATE INDEX idx_food_nutrient_nutrient_id    ON food_nutrient (nutrient_id);
CREATE INDEX idx_food_nutrient_derivation_id  ON food_nutrient (derivation_id);

CREATE TABLE food_nutrient_conversion_factor (
  "id"     INT NOT NULL PRIMARY KEY,
  "fdc_id" INT REFERENCES food(fdc_id)
);

CREATE INDEX idx_food_nutrient_conversion_factor_fdc_id ON food_nutrient_conversion_factor (fdc_id);

CREATE TABLE food_nutrient_derivation (
  "id"          INT NOT NULL PRIMARY KEY,
  "code"        TEXT,
  "description" TEXT,
  "source_id"   INT REFERENCES food_nutrient_source(id)
);

CREATE INDEX idx_food_nutrient_derivation_source_id ON food_nutrient_derivation (source_id);

CREATE TABLE food_nutrient_source (
  "id"          INT NOT NULL PRIMARY KEY,
  "code"        INT UNIQUE,  -- Code for source (4=calculated).  XXX FK to ?
  "description" TEXT
);

CREATE TABLE food_portion (
  "id"                  INT NOT NULL PRIMARY KEY,
  "fdc_id"              INT REFERENCES food(fdc_id),
  "seq_num"             INT,
  "amount"              REAL,
  "measure_unit_id"     INT REFERENCES measure_unit(id),
  "portion_description" TEXT,
  "modifier"            TEXT,
  "gram_weight"         REAL,
  "data_points"         INT,
  "footnote"            TEXT,
  "min_year_acquired"   TEXT
      CHECK(min_year_acquired IS NULL OR
            min_year_acquired GLOB '[0-9][0-9][0-9][0-9]' IS 1)
);

CREATE INDEX idx_food_portion_fdc_id           ON food_portion (fdc_id);
CREATE INDEX idx_food_portion_measure_unit_id  ON food_portion (measure_unit_id);

CREATE TABLE food_protein_conversion_factor (
  "food_nutrient_conversion_factor_id" INT NOT NULL PRIMARY KEY REFERENCES food_nutrient_conversion_factor(id),
  "value"                              REAL
);

-- CREATE TABLE food_update_log_entry (
--   "fdc_id"               INT REFERENCES food(fdc_id),
--   "description"          TEXT,
--   "publication_date"   TEXT
--       CHECK(publication_date IS NULL OR
--             publication_date GLOB '[0-9][0-9][0-9][0-9]' IS 1)
-- );

CREATE TABLE foundation_food (
  "fdc_id"     INT NOT NULL PRIMARY KEY REFERENCES food(fdc_id),
  "NDB_number" INT UNIQUE,
  "footnote"   TEXT
);

CREATE TABLE input_food (
  "id"                   INT NOT NULL PRIMARY KEY,
  "fdc_id"               INT REFERENCES food(fdc_id),
  "fdc_id_of_input_food" INT REFERENCES food(fdc_id),
  "seq_num"              INT,
  "amount"               REAL,
  "sr_code"              INT,  -- NDB code of SR food XXX but not a FK
  "sr_description"       TEXT,
  "unit"                 TEXT, -- Unit of measure (but inconsistent)
  "portion_code"         INT,  -- Code for portion description XXX FK?
  "portion_description"  TEXT,
  "gram_weight"          REAL,
  "retention_code"       INT,
  "survey_flag"          INT
);

CREATE INDEX idx_input_food_fdc_id               ON input_food (fdc_id);
CREATE INDEX idx_input_food_fdc_id_of_input_food ON input_food (fdc_id_of_input_food);

CREATE TABLE lab_method (
  "id"          INT NOT NULL PRIMARY KEY,
  "description" TEXT,
  "technique"   TEXT
);

CREATE TABLE lab_method_code (
  "id"            INT NOT NULL PRIMARY KEY,
  "lab_method_id" INT REFERENCES lab_method(id),
  "code"          TEXT
);

CREATE INDEX idx_lab_method_code_lab_method_id ON lab_method_code (lab_method_id);

CREATE TABLE lab_method_nutrient (
  "id"            INT NOT NULL PRIMARY KEY,
  "lab_method_id" INT REFERENCES lab_method(id),
  "nutrient_id"   INT -- XXX this constraint fails: REFERENCES nutrient(id)
);

CREATE INDEX idx_lab_method_nutrient_lab_method_id ON lab_method_nutrient (lab_method_id);

CREATE TABLE market_acquisition (
  "fdc_id"            INT NOT NULL PRIMARY KEY REFERENCES food(fdc_id),
  "brand_description" TEXT,
  "expiration_date"   TEXT
      CHECK(expiration_date IS NULL OR
            expiration_date GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]' IS 1),
  "label_weight"      REAL,
  "location"          TEXT,
  "acquisition_date"  TEXT
      CHECK(acquisition_date IS NULL OR
            acquisition_date GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]' IS 1),
  "sales_type"        TEXT,
  "sample_lot_nbr"    INT,
  "sell_by_date"      TEXT
      CHECK(sell_by_date IS NULL OR
            sell_by_date GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]' IS 1),
  "store_city"        TEXT,
  "store_name"        TEXT,
  "store_state"       TEXT,
  "upc_code"          TEXT
);

CREATE TABLE measure_unit (
  "id"   INT NOT NULL PRIMARY KEY,
  "name" TEXT UNIQUE
--  "abbreviation" TEXT
);

CREATE TABLE nutrient (
  "id"           INT NOT NULL PRIMARY KEY,
  "name"         TEXT,
  "unit_name"    TEXT,
  "nutrient_nbr" INT UNIQUE,
  "rank"         INT    -- XXX Not documented
);

-- XXX Missing table nutrient_analysis_details per Field Descriptions

CREATE TABLE nutrient_incoming_name (
  "id"          INT NOT NULL PRIMARY KEY,
  "name"        TEXT,
  "nutrient_id" INT REFERENCES nutrient(id)
);

CREATE INDEX idx_nutrient_incoming_name_nutrient_id ON nutrient_incoming_name (nutrient_id);

CREATE TABLE retention_factor (
  "id"            INT NOT NULL PRIMARY KEY,
  "code"          TEXT,
  "food_group_id" INT REFERENCES food_category(id),
  "description"   TEXT
);

CREATE INDEX idx_retention_factor_food_group_id ON retention_factor (food_group_id);

CREATE TABLE sample_food (
  "fdc_id" INT NOT NULL PRIMARY KEY REFERENCES food(fdc_id)
);

CREATE TABLE sr_legacy_food (
  "fdc_id"     INT NOT NULL PRIMARY KEY REFERENCES food(fdc_id),
  "NDB_number" INT UNIQUE  -- XXX doc says starts at 100k but not in practice
);

CREATE TABLE sub_sample_food (
--  "fdc_id"                INT NOT NULL PRIMARY KEY REFERENCES food(fdc_id),
  "fdc_id"                INT NOT NULL PRIMARY KEY,
--  "fdc_id_of_sample_food" INT REFERENCES food(fdc_id)
  "fdc_id_of_sample_food" INT
);

CREATE INDEX idx_sub_sample_food_fdc_id_of_sample_food ON sub_sample_food (fdc_id_of_sample_food);

CREATE TABLE sub_sample_result (
  "food_nutrient_id" INT NOT NULL PRIMARY KEY REFERENCES food_nutrient(id),
  "adjusted_amount"  REAL,
  "lab_method_id"    INT REFERENCES lab_method(id), -- XXX cannot use this because of broken refs: REFERENCES lab_method(id),
  "nutrient_name"    TEXT
);

CREATE INDEX idx_sub_sample_result_lab_method_id ON sub_sample_result (lab_method_id);

CREATE TABLE survey_fndds_food (
  "fdc_id"              INT NOT NULL PRIMARY KEY REFERENCES food(fdc_id),
  "food_code"           INT UNIQUE,
  "wweia_category_code" INT REFERENCES wweia_food_category(wweia_food_category_code),
  "start_date"          TEXT
      CHECK(start_date IS NULL OR
            start_date GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]' IS 1),
  "end_date"            TEXT
      CHECK(end_date IS NULL OR
            end_date GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]' IS 1)
);

CREATE INDEX idx_survey_fndds_food_wweia_category_code ON survey_fndds_food (wweia_category_code);

CREATE TABLE wweia_food_category (
  "wweia_food_category_code"        INT NOT NULL PRIMARY KEY,
  "wweia_food_category_description" TEXT
);
''')


def process(directory: str, database: str, force: bool = False, batch: int = 1000,
            verbose: bool = False) -> None:
    """Process a directory of USDA FoodData CSVs into a SQLite file"""

    # Import in this order so it will not cause problems with foreign key
    # constraints.
    # Note that in the October 2021 dataset, you need to rename the following files:
    #    acquisition_samples.csv -> acquisition_sample.csv
    #    agricultural_samples.csv -> agricultural_acquisition.csv
    ordered = [
        'food_category.csv',
        'food.csv',
        'food_nutrient_conversion_factor.csv',
        'nutrient.csv',
        'food_nutrient_source.csv',
        'measure_unit.csv',
        'lab_method.csv',
        'wweia_food_category.csv',
        'acquisition_sample.csv',
        'agricultural_acquisition.csv',
        'branded_food.csv',
        'food_attribute_type.csv',
        'food_attribute.csv',
        'food_calorie_conversion_factor.csv',
        'food_component.csv',
        'food_nutrient_derivation.csv',
        'food_portion.csv',
        'food_protein_conversion_factor.csv',
        'foundation_food.csv',
        'sr_legacy_food.csv',
        'survey_fndds_food.csv',
        'input_food.csv',
        'lab_method_code.csv',
        'lab_method_nutrient.csv',
        'market_acquisition.csv',
        'nutrient_incoming_name.csv',
        'retention_factor.csv',
        'sample_food.csv',
        'sub_sample_food.csv',
        'food_nutrient.csv',
        'sub_sample_result.csv',
        'all_downloaded_table_record_counts.csv',
        'fndds_derivation.csv',
        'fndds_ingredient_nutrient_value.csv',
        'food_update_log_entry.csv',
    ]

    ignore = [
        'all_downloaded_table_record_counts.csv',
        'fndds_derivation.csv',
        'fndds_ingredient_nutrient_value.csv',
        'food_update_log_entry.csv',
    ]

    # Make sure we accounted for everything
    csvs = [os.path.basename(x) for x in glob(os.path.join(directory, "*.csv"))]
    diff = set(ordered) ^ set(csvs)
    if diff != set():
        raise Exception(f"Unhandled input: {diff}")

    if os.path.isfile(database):
        if force:
            os.remove(database)
        else:
            print("Output already exists.  Use --force or delete it first")
            sys.exit(1)

    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()

        # This must be enabled at runtime every time you want to check FK.
        cursor.executescript('''
PRAGMA foreign_keys = ON;

''')
        sqlite3_schema(cursor)

        for fname in ordered:
            if fname in ignore:
                print(f"Skipping {fname}")
            else:
                print(f"Importing {fname}")
                import_csv(cursor, os.path.join(directory, fname), batch, verbose)

        # Due to lots of inserts, force a vacuum to reduce fragmentation
        print("Running integrity check, vacuum and analyze on database")
        cursor.executescript('''
PRAGMA foreign_key_check;
PRAGMA integrity_check;

VACUUM;
ANALYZE;
''')

    conn.close()


def check(directory: str, database: str, verbose: bool = False) -> None:
    """Re-open the database from disk to verify it matches the record count"""

    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()

        check_file = os.path.join(directory, 'all_downloaded_table_record_counts.csv')
        print(f"Checking counts against {check_file}")
        query_counts(cursor, check_file, verbose)

    conn.close()


def main() -> None:
    """Main func"""
    parser = argparse.ArgumentParser(description='Convert USDA FoodData CSV files to SQLite3')
    parser.add_argument('-d', '--directory', default='.',
                        help='Base directory with the *.csv files')
    parser.add_argument('-b', '--batch', default=1000, type=int,
                        help='Batch inserts into sets of this length')
    parser.add_argument('-o', '--output', default='usda_food_data.db',
                        help='Output SQLite3 file')
    parser.add_argument('-f', '--force', action='store_true', default=False,
                        help='Whether to clobber output file')
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='Verbose output')
    parser.add_argument('-c', '--check', action='store_true', default=False,
                        help="Only check the database, don't create it")
    args = parser.parse_args()

    if not args.check:
      process(args.directory, args.output, args.force, args.batch, args.verbose)
    check(args.directory, args.output, args.verbose)


if __name__ == '__main__':
    main()
