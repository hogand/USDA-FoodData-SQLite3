all: slow fast

# SHA256 (FoodData_Central_csv_2019-04-02.zip) = 1e635ef8257ad32b58fbbca5f05d06b9b85c16824102091d2eab7bb357817428
.PHONY: download
download:
	@if [ ! -d extract ]; then \
		mkdir extract; \
	fi
	@if [ ! -f extract/FoodData_Central_csv_2019-04-02.zip ]; then \
		cd extract; \
		curl -O https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_csv_2019-04-02.zip; \
		cd ..; \
	fi
	unzip -n -d extract/FoodData_Central_csv_2019-04-02 extract/FoodData_Central_csv_2019-04-02.zip

.PHONY: clean
clean:
	@rm -f extract/*.db extract/after_import.sql extract/gen_import.sql extract/query_counts.sql

.PHONY: dist-clean
dist-clean:
	@rm -rf extract

.PHONY: fast
fast: download
	time sh ./import_fast.sh extract/FoodData_Central_csv_2019-04-02 extract/food_data_quick_2019-04-02.db

.PHONY: check
check:
	mypy 	--python-version 3.7 \
		--strict \
		--strict-equality \
		--show-error-context \
		--show-column-numbers \
		import_food_data.py
	flake8 \
		--count \
		--ignore=E501 \
		import_food_data.py
	pylint import_food_data.py

.PHONY: slow
slow: download
	time python3 import_food_data.py -f -d extract/FoodData_Central_csv_2019-04-02 -o extract/food_data_sqlite_2019-04-02.db

