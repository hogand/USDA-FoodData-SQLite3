# Examples Queries

After you have generated the sqlite file, here are a few sample queries.

```sh
$ sqlite3 -readonly ./extract/food_data_sqlite_2019-04-02.db
SQLite version 3.24.0 2018-06-04 14:10:15
Enter ".help" for usage hints.

sqlite> .tables
acquisition_sample               input_food
agricultural_acquisition         lab_method
branded_food                     lab_method_code
food                             lab_method_nutrient
food_attribute                   market_acquisition
food_attribute_type              measure_unit
food_calorie_conversion_factor   nutrient
food_category                    nutrient_incoming_name
food_component                   retention_factor
food_nutrient                    sample_food
food_nutrient_conversion_factor  sr_legacy_food
food_nutrient_derivation         sub_sample_food
food_nutrient_source             sub_sample_result
food_portion                     survey_fndds_food
food_protein_conversion_factor   wweia_food_category
foundation_food

sqlite> .mode column
sqlite> .headers on

sqlite> SELECT f.fdc_id
   ...>       ,f.description
   ...>       ,m.sales_type
   ...>       ,m.store_name
   ...>       ,m.store_state
   ...>       ,m.upc_code
   ...> FROM food f
   ...> INNER JOIN market_acquisition m
   ...>    ON f.fdc_id = m.fdc_id
   ...> WHERE f.data_type = 'market_acquisition'
   ...>   AND m.upc_code IS NOT NULL
   ...> LIMIT 3;
fdc_id      description                               sales_type    store_name           store_state  upc_code
----------  ----------------------------------------  ------------  -------------------  -----------  ----------
327702      Lettuce, Romaine, 2 Ct (FL1) - NFY0905F9  Retail store  Publix Super Market  FL           3338365101
329719      Dry white cheese, Queso seco, CACIQUE CO  Retail store  El Super             CA           7456200110
329720      Dry white cheese, Queso seco, CACIQUE CO  Retail store  El Super             CA           7456200110

sqlite> SELECT data_type
   ...> FROM food
   ...> GROUP BY 1
   ...> ORDER BY 1;
data_type
------------------------
agricultural_acquisition
branded_food
foundation_food
market_acquisition
sample_food
sr_legacy_food
sub_sample_food
survey_fndds_food

sqlite> .quit
```

# TODO

Note: See [TODO](./TODO.md) about missing Microsoft Access queries.

