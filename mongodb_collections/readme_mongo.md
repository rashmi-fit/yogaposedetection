If you want to import the data

- Open terminal
- Enter below command

### mongoimport --db yoga_db --collection slots --type csv --file "path/of/the/file/slots_data.xlsx" --headerline


export data from local

- open terminal
## mongoexport --db yoga_db --collection learn_and_grow --out learn_and_grow.json

## mongoexport --db yoga_db --collection slots --out slots.json

## mongoexport --db yoga_db --collection feedback --out feedback.json

