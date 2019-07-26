# Field Definitions

These are massaged out of the `Field Descriptions` tab in the
"Download & API Field Descriptions-2019-04-02-14-48.xlsx" file.

Reproducing them here so you don't need to read the public domain
Excel file.

## Global Column Definitions

These fields appear in multiple files, and their definition is typically the same unless noted below.

| Field  | Definition | Synonyms | API Location |
| ------ | ---------- | -------- | ------------ |
| fdc_id | Unique permanent identifier of a food in the food table | | |
| id     | Unique permanent identifier of other kinds of data (e.g. nutrients, lab methods, etc.) in their related table | | |


## agricultural_acquisition

Non-processed foods obtained directly from the location where they are produced.

API Location: food (is a type of food)

| Field            | Definition | Synonyms | API Location |
| ---------------- | ---------- | -------- | ------------ |
| fdc_id           | ID of the food in the food table | FDC Source ID | |
| acquisition_date | The date this food was obtained | | |
| market_class     | The name of the specific kind of this food (eg. `Pinto` for pinto beans) | | |
| treatment        | Any special condition relevant to the production of this food - typically `drought` or `control` | | |
| state            | The state in which this food was produced | | |


## acquisition_sample

Acquisitions may be blended with other acquisitions to create a sample food, and an acquisition can be used to created more than one sample food. This file stores which acquisitions and sample foods are related to each other.

API Location: N/A Download only

| Field                      | Definition | Synonyms | API Location |
| -------------------------- | ---------- | -------- | ------------ |
| fdc_id_of_sample_food      | ID of the sample food that uses the acquisitioned food | | |
| fdc_id_of_acquisition_food | ID of the acquisitioned food used in the sample food | | |


## branded_food

Foods whose nutrient values are typically obtained from food label data provided by food brand owners.

API Location: food (is a type of food)

| Field                      | Definition | Synonyms | API Location |
| -------------------------- | ---------- | -------- | ------------ |
| fdc_id                     | ID of the food in the food table | | |
| brand_owner                | Brand owner for the food | | |
| gtin_upc                   | GTIN or UPC code identifying the food | GTIN/UPC | gtinUpc |
| ingredients                | The list of ingredients (as it appears on the product label) | | |
| serving_size               | The amount of the serving size when expressed as gram or ml | | |
| serving_size_unit          | The unit used to express the serving size (gram or ml) | | |
| household_serving_fulltext | amount and unit of serving size when expressed in household units | | |
| branded_food_category      | The category of the branded food, assigned by GDSN or Label Insight | | |
| data_source                | The source of the data for this food. GDSN (for GS1) or LI (for Label Insight). | | |
| modified_date              | This date reflects when the product data was last modified by the data provider, i.e., the manufacturer | | |
| available_date             | This is the date when the product record was available for inclusion in the database. | | |


## food

Any substance consumed by humans for nutrition, taste and/or aroma.

| Field            | Definition | Synonyms | API Location |
| ---------------- | ---------- | -------- | ------------ |
| fdc_id           | Unique permanent identifier of the food | FDC Source ID (used for acquisition foods) | |
| foodClass        | For internal use only | | |
| data_type        | Type of food data (see Files tab for possible values). | | |
| description      | Description of the food | | |
| food_category_id | Id of the food category the food belongs to |  | foodGroup |
| publication_date | Date when the food was published to FoodData Central | Published, Published Date | |


## food_attribute

A constituent part of a food (e.g. bone is a component of meat).

API Location: food->foodAttributes (food_more_information)

| Field                  | Definition | Synonyms | API Location |
| ---------------------- | ---------- | -------- | ------------ |
| id                     | | | |
| fdc_id                 | ID of the food this food attribute pertains to |  | N/A |
| seq_num                | The order the attribute will be displayed on the released food. |  | sequenceNumber |
| food_attribute_type_id | ID of the type of food attribute to which this value is associated for a specific food |  | foodAttributeType |
| name                   | Name of food attribute | | |
| value                  | The actual value of the attribute | | |


## food_attribute_type

The list of supported attributes associated with a food.

API Location: food->foodAttributes->foodAttributeType

| Field       | Definition | Synonyms | API Location |
| ----------- | ---------- | -------- | ------------ |
| id          | | | |
| name        | Name of the attribute associated with the food - should be displayable to users | | |
| description | Description of the attribute | | |


## food_calorie_conversion_factor

The multiplication factors to be used when calculating energy from macronutrients for a specific food.

API Location: food->nutrientConversionFactors

| Field                              | Definition | Synonyms | API Location |
| ---------------------------------- | ---------- | -------- | ------------ |
| food_nutrient_conversion_factor_id | ID of the related row in the nutrient_conversion_factor table |  | id |
| protein_value                      | The multiplication factor for protein | | |
| fat_value                          | The multiplication factor for fat | | |
| carbohydrate_value                 | The multiplication factor for carbohydrates | | |


## food_category

Foods of defined similarity.

API Location: food->foodCategory

| Field       | Definition | Synonyms | API Location |
| ----------- | ---------- | -------- | ------------ |
| id          | | | |
| code        | Food group code | | |
| description | Description of the food group | | |


## food_component

A constituent part of a food (e.g. bone is a component of meat).

API Location: food->foodComponents

| Field             | Definition | Synonyms | API Location |
| ----------------- | ---------- | -------- | ------------ |
| id                | | | |
| fdc_id            | ID of the food this food component pertains to |  | N/A |
| name              | The kind  of component, e.g. bone | | |
| pct_weight        | The weight of the component as a percentage of the total weight of the food  | Weight (%) | percentWeight |
| is_refuse         | Whether the component is refuse, i.e. not edible | Refuse | |
| gram_weight       | The weight of the component in grams | Weight (g) | |
| data_points       | The number of observations on which the measure is based | n | |
| min_year_acquired | Minimum purchase year of all acquisitions used to derive the component value | Year Acquired | |


## food_fat_conversion_factor

Factor to calculate total lipid fat (204).

API Location: food->nutrientConversionFactors

| Field                              | Definition | Synonyms | API Location |
| ---------------------------------- | ---------- | -------- | ------------ |
| food_nutrient_conversion_factor_id | Id of the related row in the nutrient_conversion_factor table |  | id |
| fat_nlea_value                     | The multiplication factor to convert from fat NLEA (298) to total fat (204) | | |


## food_nutrient

A nutrient value for a food.

API Location: Add nutrientAnalysisDetails

| Field             | Definition | Synonyms | API Location |
| ----------------- | ---------- | -------- | ------------ |
| id                | | | |
| fdc_id            | ID of the food this food nutrient pertains to |  | N/A |
| nutrient_id       | ID of the nutrient to which the food nutrient pertains |  | nutrient |
| amount            | Amount of the nutrient per 100g of food. Specified in unit defined in the nutrient table. | | |
| data_points       | Number of observations on which the value is based | n | |
| derivation_id     | ID of the food nutrient derivation technique used to derive the value |  | foodNutrientDerivation |
| standard_error    | Standard error | | |
| min               | The minimum amount | | |
| max               | The maximum amount | | |
| median            | The median amount | | |
| footnote          | Comments on any unusual aspects of the food nutrient. Examples might include why a nutrient value is different than typically expected. | | |
| min_year_acquired | Minimum purchase year of all acquisitions used to derive the nutrient value | Year Acquired | |


## food_nutrient_conversion_factor

Top level type for all types of nutrient conversion factors. A separate row is stored for each of these 3 types of conversion factor.

API Location: N/A - abstract class

| Field  | Definition | Synonyms | API Location |
| ------ | ---------- | -------- | ------------ |
| id     | | | |
| fdc_id | ID of the food that this food nutrient conversion factor pertains to |  | N/A |


## food_nutrient_derivation

Procedure indicating how a food nutrient value was obtained.

API Location: food->foodNutrients->foodNutrientDerivation

| Field       | Definition | Synonyms | API Location |
| ----------- | ---------- | -------- | ------------ |
| id          | | | |
| code        | Code used for the derivation (e.g. A means analytical) | | |
| description | Description of the derivation | Deriv. By | |
| source_id   | ID of the nutrient source associated with the derivation |  | foodNutrientSource |


## food_nutrient_source

An information source from which we can obtain food nutrient values.

API Location: food->foodNutrients->foodNutrientDerviation->foodNutrientSource

| Field       | Definition | Synonyms | API Location |
| ----------- | ---------- | -------- | ------------ |
| id          | | | |
| code        | Code used for the source (e.g. 4 means calculated or imputed) | | |
| description | Description of the source | | |


## food_portion

Discrete amount of food.

API Location: food->foodPortions

| Field               | Definition | Measures/Portions | API Location |
| ------------------- | ---------- | -------- | ------------ |
| id                  | | | |
| fdc_id              | ID of the food this food portion pertains to |  | N/A |
| seq_num             | The order the measure will be displayed on the released food. |  | sequenceNumber |
| amount              | The number of measure units that comprise the measure (e.g. if measure is 3 tsp, the amount is 3). Not defined for survey (FNDDS) foods (amount is instead embedded in portion description). | | |
| measure_unit_id     | The unit used for the measure (e.g. if measure is 3 tsp, the unit is tsp). For food types that do not use measure SR legacy foods and survey (FNDDS) foods), a value of '9999' is assigned to this field. | Unit | measureUnit |
| portion_description | Foundation foods: Comments that provide more specificity on the measure. For example, for a pizza measure the dissemination text might be 1 slice is 1/8th of a 14 inch pizza.   Survey (FNDDS) foods: The household description of the portion. | Measure Description | |
| modifier            | Foundation foods: Qualifier of the measure (e.g. related to food shape or form)  (e.g. melted, crushed, diced). Survey (FNDDS) foods: The portion code. SR legacy foods: description of measures, including the unit of measure and the measure modifier (e.g. waffle round (4" dia)).  | | |
| gram_weight         | The weight of the measure in grams | Weight (g) | |
| data_points         | The number of observations on which the measure is based | n | |
| footnote            | Comments on any unusual aspects of the measure. These are released to the public. Examples might include caveats on the usage of a measure, or reasons why a measure gram weight is an unexpected value. | | |
| min_year_acquired   | Minimum purchase year of all acquisitions used to derive the measure value | Year Acquired | |


## food_protein_conversion_factor

API Location: food->nutrientConversionFactors

| Field                              | Definition | Synonyms | API Location |
| ---------------------------------- | ---------- | -------- | ------------ |
| food_nutrient_conversion_factor_id | Id of the related row in the nutrient_conversion_factor table |  | id |
| value                              | The multiplication factor used to calculate protein from nitrogen | | |


## foundation_food

Foods whose nutrient and food component values are derived primarily by chemical analysis. Foundation data also include extensive underlying metadata, such as the number of samples, the location and dates on which samples were obtained, analytical approaches used, and if appropriate, cultivar, genotype, and production practices.

API Location: food (is a type of food)

| Field      | Definition | Synonyms | API Location |
| ---------- | ---------- | -------- | ------------ |
| fdc_id     | ID of the food in the food table | | |
| NDB_number | Unique number assigned for the food, different from fdc_id, assigned in SR |  | ndbNumber |
| footnote   | Comments on any unusual aspects. These are released to the public. Examples might include unusual aspects of the food overall. | | |


## input_food

A food that is an ingredient (for survey (FNDDS) foods) or a source food (for foundation foods or their source foods) to another food.

API Location: food->inputFoods

| Field                | Definition | Sources/Ingredients | API Location |
| -------------------- | ---------- | ------------------- | ------------ |
| id                   | | | |
| fdc_id               | fdc_id of the food that contains the input food |  | N/A |
| fdc_id_of_input_food | fdc_id of the food that is the input food |  | inputFood |
| seq_num              | The order in which to display the input food |  | sequenceNumber |
| amount               | The amount of the input food included within this food given in terms of unit | | |
| sr_code              | The SR (aka NDB) code of the SR food that is the ingredient food (used for Survey (FNDDS) foods only) | | |
| sr_description       | The description of the SR food that is the ingredient food (used for Survey (FNDDS) foods only) | | |
| unit                 | The unit of measure for the amount of the input food that is included within this food (used for Survey (FNDDS) foods only) | Measure | |
| portion_code         | Code that identifies the portion description used to measure the amount of the ingredient (used for Survey (FNDDS) foods only) | | |
| portion_description  | The description of the portion  used to measure the amount of the ingredient (used for Survey (FNDDS) foods only) | Portion | |
| gram_weight          | The weight in grams of the input food | Weight (g) | |
| retention_code       | A numeric code identifying processing on the input food that may have impacted food nutrient content (used for Survey (FNDDS) foods only) |  | retentionFactor |
| survey_flag          | 2 = SR description does not match SR code, other values = internal processing codes for FSRG use only  | Flag | |


## lab_method

A chemical procedure used to measure the amount of one or more nutrients in a food.

API Location: For reference only

| Field       | Definition | Synonyms | API Location |
| ----------- | ---------- | -------- | ------------ |
| id          | | | |
| description | Description of the lab method | | |
| technique   | General chemical analysis approach used by the lab method | | |


## lab_method_code

A short, sometimes lab-specific, sequence of characters used to identify a lab method.

API Location: For reference only

| Field         | Definition | Synonyms | API Location |
| ------------- | ---------- | -------- | ------------ |
| id            | | | |
| lab_method_id | ID of the lab method the code refers to | | |
| code          | Value of the method code | | |


## lab_method_nutrient

A nutrient whose amount can be measured by a lab method.

API Location: For reference only

| Field         | Definition | Synonyms | API Location |
| ------------- | ---------- | -------- | ------------ |
| id            | | | |
| lab_method_id | ID of the lab method the nutrient is measured by | | |
| nutrient_id   | ID of the nutrient that can be measured by the lab method | | |


## market_acquisition

A food obtained for chemical analysis.

API Location: food (is a type of food)

| Field             | Definition | Synonyms | API Location |
| ----------------- | ---------- | -------- | ------------ |
| fdc_id            | ID of the food in the food table | FDC Source ID | |
| brand_description | Brand name description of the food | | |
| expiration_date   | Date the food will expire | | |
| label_weight      | The weight of the  food per the product label | | |
| location          | The region in which the food was purchased, e.g. CA1 | | |
| acquisition_date  | Date the food was purchased | | |
| sales_type        | The type of establishment in which the food was acquired (e.g. Retail Store, restaurant, farm, etc.) | | |
| sample_lot_nbr    | The lot number of the food | Sample Lot Number | sampleLotNumber |
| sell_by_date      | Date the food should be sold by | | |
| store_city        | The city where the food was acquired | | |
| store_name        | The name of the store the food is purchased from | | |
| store_state       | The state where the food was acquired | | |
| upc_code          | UPC code for the food. Only applicable for retail products. | | |


## measure_unit

units for measuring quantities of foods.

API Location: food->foodMeasures->measureUnit

| Field        | Definition | Synonyms | API Location |
| ------------ | ---------- | -------- | ------------ |
| id           | | | |
| name         | name of the unit | | |
| abbreviation | abbreviated name of the unit | | |


## nutrient

The chemical constituent of a food (e.g. calcium, vitamin E) officially recognized as essential to human health.

API Location: food->foodNutrients->nutrient

| Field        | Definition | Synonyms | API Location |
| ------------ | ---------- | -------- | ------------ |
| id           | | | |
| name         | Name of the nutrient | | |
| unit_name    | The standard unit of measure for the nutrient (per 100g of food) | Unit | |
| nutrient_nbr | A unique code identifying a nutrient or food constituent |  | number |


## nutrient_analysis_details

Info for the nutrient source info shown on the nutrient source popdown window.

API Location: food->nutrientAnalysisDetails

| Field            | Definition | Synonyms | API Location |
| ---------------- | ---------- | -------- | ------------ |
| amount           | Amount of the nutrient | | |
| unit             | Unit used to express nutrient amount | | |
| method           | Lab method used to analyze the nutrient | | |
| city             | City where the food was acquired | | |
| state            | State  where the food was acquired | | |
| acquisition_date | Date when the food was acquired | | |
| details          | Acquisition food FDC ID | | |


## nutrient_incoming_name

A nutrient name used to identify a nutrient in incoming nutrient data.

| Field       | Definition | Synonyms | API Location |
| ----------- | ---------- | -------- | ------------ |
| id          | | | |
| name        | The name used for the incoming nutrient (e.g. if nutrient is Protein, name might be Prot) | | |
| nutrient_id | The id of the nutrient (in the nutrient file) related to the incoming name. Optional (see is_ignored for more info). | | |


## retention_factor

Definitions are available [from](http://www.ars.usda.gov/SP2UserFiles/Place/12354500/Data/retn/retn06.pdf).

API Location: food->inputFoods->retentionFactor

| Field | Definition | Synonyms | API Location |
| ----- | ---------- | -------- | ------------ |


## sample_food

A food that is acquired as a representative sample of the food supply. It may be created from a single acquired food, or from a composite of multiple acquired foods.

API Location: food (is a type of food)

| Field  | Definition | Synonyms | API Location |
| ------ | ---------- | -------- | ------------ |
| fdc_id | ID of the food in the food table |  | N/A |


## sr_legacy_food

Foods from the April 2018 release of the USDA National Nutrient Database for Standard Reference. Nutrient and food component values are derived from chemical analysis and calculation. 

API Location: food (is a type of food)

| Field      | Definition | Synonyms | API Location |
| ---------- | ---------- | -------- | ------------ |
| fdc_id     | ID of the food in the food table | | |
| NDB_number | Unique number assigned for final food, starts from the minimum number of 100,000 |  | ndbNumber |


## sub_sample_food

A portion of a sample food used for the purpose of specific chemical analysis.

API Location: N/A - download only

| Field                 | Definition | Synonyms | API Location |
| --------------------- | ---------- | -------- | ------------ |
| fdc_id                | ID of the food in the food table | | |
| fdc_id_of_sample_food | ID of the sample food from which the sub sample originated | | |


## sub_sample_result

The result of chemical analysis of a lab on a particular sub sample for a particular nutrient.

API Location: food->foodNutrients (is a type of food nutrient)

| Field            | Definition | Synonyms | API Location |
| ---------------- | ---------- | -------- | ------------ |
| food_nutrient_id | Unique ID for row, same as the food_nutrient ID |  | id |
| adjusted_amount  | Amount after adjusting for unit | | |
| lab_method_id    | ID of the lab method used to measure the nutrient | | |
| nutrient_name    | The name of the nutrient as supplied by the lab | | |


## survey_fndds_food

Foods whose consumption is measured by the What We Eat In America dietary survey component of the National Health and Nutrition Examination Survey (NHANES). Survey nutrient values are usually calculated from Branded and SR Legacy data.

API Location: food (is a type of food)

| Field               | Definition | Synonyms | API Location |
| ------------------- | ---------- | -------- | ------------ |
| fdc_id              | ID of the food in the food table | | |
| food_code           | A unique ID identifying the food within FNDDS | | |
| wweia_category_code | Unique Identification code for WWEIA food category to which this food is assigned | Food Category | wweiaFoodCategory |
| start_date          | Start date indicates time period corresponding to WWEIA data  | | |
| end_date            | End date indicates time period corresponding to WWEIA data  | | |


## wweia_food_category

Food categories for fndds.

API Location: food->wweiaFoodCategory

| Field                           | Definition | Synonyms | API Location |
| ------------------------------- | ---------- | -------- | ------------ |
| wweia_food_category_code        | Unique identification code | | |
| wweia_food_category_description | Description for a WWEIA Category | | |

