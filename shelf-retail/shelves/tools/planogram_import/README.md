1. Fill planogram.ods with planogram data and export to csv. 
Csv export options:

* delimiter=,
* string_quote="
* save_cell_contents_as_shown=yes
* quote_all_text=yes 

2. Check postgres connection string in main.py (prod database) and test.py (test database)

3. Run

```
# !reset local db!
sudo -u postgres psql < planogram.sql
 
# run test
python3 test.py

# run import from csv
python3 main.py test prod_data/planogram.csv
```
