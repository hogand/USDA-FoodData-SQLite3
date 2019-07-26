#!/bin/sh

set -e

# Import the USDA FoodData Central CSV files into SQLite using CLI.

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

# Import the CSVs using the default schema.
import_csv() {
    DIR="$1"

    cat <<EOF>extract/gen_import.sql
.echo on
.bail on

.mode csv

EOF

    for FILE in $(ls $DIR/*.csv | grep -v '/all_downloaded_table_record_counts.csv$'); do
        TABLE=$(basename "$FILE" | sed -e 's/\.csv$//')

        cat <<EOF>>extract/gen_import.sql
.import "$FILE" "$TABLE"
EOF
    done
}

# Update the file to replace "" with NULL
replace_empty_string() {
    OUTPUT="$1"

    cat <<EOF>extract/after_import.sql
.echo on
.bail on

EOF

    for FILE in $(ls $DIR/*.csv | grep -v '/all_downloaded_table_record_counts.csv$'); do
        TABLE=$(basename "$FILE" | sed -e 's/\.csv$//')

        COLUMNS=$(sqlite3 "$OUTPUT" <<EOF

SELECT GROUP_CONCAT(foo.name, " ")
FROM (
    -- Select all columns that allow NULL and are not part of the primary key.
    SELECT name
    FROM pragma_table_info('$TABLE')
    WHERE \`notnull\` = 0
    AND pk = 0
) AS foo
EOF
    )
        if [ ! "$COLUMNS" = "" ]; then
            for COL in $COLUMNS; do
                cat<<EOF>>extract/after_import.sql
UPDATE $TABLE
SET $COL = NULL
WHERE $COL = "";

EOF
            done
        fi
    done
}

# Add indices for things you may index on.
add_indices() {

    cat <<EOF>>extract/after_import.sql

CREATE INDEX idx_acquisition_sample_fdc_id_of_sample_food      ON acquisition_sample (fdc_id_of_sample_food);
CREATE INDEX idx_acquisition_sample_fdc_id_of_acquisition_food ON acquisition_sample (fdc_id_of_acquisition_food);

CREATE INDEX idx_agricultural_acquisition_fdc_id ON agricultural_acquisition (fdc_id);

CREATE INDEX idx_branded_food_fdc_id   ON branded_food (fdc_id);
CREATE INDEX idx_branded_food_gtin_upc ON branded_food (gtin_upc);

CREATE UNIQUE INDEX idx_food_fdc_id    ON food (fdc_id);
CREATE INDEX idx_food_food_category_id ON food (food_category_id);

CREATE INDEX idx_food_attribute_fdc_id                 ON food_attribute (fdc_id);
CREATE INDEX idx_food_attribute_food_attribute_type_id ON food_attribute (food_attribute_type_id);

CREATE UNIQUE INDEX idx_food_attribute_type_id ON food_attribute_type (id);

CREATE UNIQUE INDEX idx_food_category_id ON food_category (id);

CREATE INDEX idx_food_component_fdc_id ON food_component (fdc_id);

CREATE UNIQUE INDEX idx_food_nutrient_id     ON food_nutrient (id);
CREATE INDEX idx_food_nutrient_fdc_id        ON food_nutrient (fdc_id);
CREATE INDEX idx_food_nutrient_nutrient_id   ON food_nutrient (nutrient_id);

CREATE UNIQUE INDEX idx_food_nutrient_derivation_id ON food_nutrient_derivation (id);

CREATE UNIQUE INDEX idx_food_nutrient_source_id ON food_nutrient_source (id);

CREATE UNIQUE INDEX idx_food_portion_id  ON food_portion (id);
CREATE INDEX idx_food_portion_fdc_id     ON food_portion (fdc_id);

CREATE INDEX idx_foundation_food_fdc_id ON foundation_food (fdc_id);

CREATE UNIQUE INDEX idx_input_food_id            ON input_food (id);
CREATE INDEX idx_input_food_fdc_id               ON input_food (fdc_id);
CREATE INDEX idx_input_food_fdc_id_of_input_food ON input_food (fdc_id_of_input_food);

CREATE UNIQUE INDEX idx_lab_method_id ON lab_method (id);

CREATE UNIQUE INDEX idx_lab_method_code_id ON lab_method_code (id);
CREATE INDEX idx_lab_method_lab_method_id  ON lab_method_code (lab_method_id);

CREATE UNIQUE INDEX idx_lab_method_nutrient_id     ON lab_method_nutrient (id);
CREATE INDEX idx_lab_method_nutrient_lab_method_id ON lab_method_nutrient (lab_method_id);
CREATE INDEX idx_lab_method_nutrient_nutrient_id   ON lab_method_nutrient (nutrient_id);

CREATE INDEX idx_market_acquisition_fdc_id ON market_acquisition (fdc_id);

CREATE UNIQUE INDEX idx_measure_unit_id ON measure_unit (id);

CREATE UNIQUE INDEX idx_nutrient_id ON nutrient (id);
CREATE INDEX idx_nutrient_name ON nutrient (name);

CREATE UNIQUE INDEX idx_nutrient_incoming_name_id   ON nutrient_incoming_name (id);
CREATE INDEX idx_nutrient_incoming_name_nutrient_id ON nutrient_incoming_name (nutrient_id);

CREATE UNIQUE INDEX idx_retention_factor_id     ON retention_factor (id);
CREATE INDEX idx_retention_factor_food_group_id ON retention_factor (food_group_id);

CREATE INDEX idx_sr_legacy_food_fdc_id ON sr_legacy_food (fdc_id);

CREATE INDEX idx_sub_sample_food_fdc_id                ON sub_sample_food (fdc_id);
CREATE INDEX idx_sub_sample_food_fdc_id_of_sample_food ON sub_sample_food (fdc_id_of_sample_food);

CREATE INDEX idx_sub_sample_result_food_nutrient_id ON sub_sample_result (food_nutrient_id);
CREATE INDEX idx_sub_sample_result_lab_method_id    ON sub_sample_result (lab_method_id);

CREATE INDEX survey_fndds_food_fdc_id              ON survey_fndds_food (fdc_id);
CREATE INDEX survey_fndds_food_food_code           ON survey_fndds_food (food_code);
CREATE INDEX surveY_fndds_food_wweia_category_code ON survey_fndds_food (wweia_category_code);

CREATE UNIQUE INDEX wweia_food_category_wweia_food_category_code ON wweia_food_category (wweia_food_category_code);

PRAGMA integrity_check;

VACUUM;
ANALYZE;

EOF
}

# Make sure the number of records matches the CSV file.
query_counts() {
    DIR="$1"

    cat<<EOF>extract/query_counts.sql
.bail on

EOF

    IFS="
"
    for LINE in $(cat "$DIR/all_downloaded_table_record_counts.csv"); do
        TABLE=$(echo $LINE | sed -e 's/,.*$//' -e 's/"//g')
        COUNT=$(echo $LINE | sed -e 's/^.*,//' -e 's/"//g')

        # Skip the header
        if [ "$TABLE" = "Table" ]; then
            continue;
        fi

        cat<<EOF>>extract/query_counts.sql
SELECT count(*) AS ${TABLE}_count,
       $COUNT as CSV_${TABLE}_count
FROM $TABLE;

EOF
    done
}


# main
if [ ! "$#" = "2" ]; then
    echo "Usage: $0 <directory_csv> <output_file>"
    exit 1
fi

DIR="$1"
OUTPUT="$2"

rm -f extract/gen_import.sql extract/after_import.sql extract/query_counts.sql "$OUTPUT"

import_csv "$DIR"
sqlite3 "$OUTPUT" < extract/gen_import.sql

replace_empty_string "$OUTPUT"
add_indices
sqlite3 "$OUTPUT" < extract/after_import.sql

query_counts "$DIR"
sqlite3 "$OUTPUT" < extract/query_counts.sql

echo "Converted the CSV files to $OUTPUT"

