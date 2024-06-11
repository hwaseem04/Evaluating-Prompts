# Evaluating-Prompts

### To create table for each principle from json files
- Download all the json files. For testing you can start with just two files, i.e [w_principle_1.json](misc/json_files/w_principle_1.json) and [wo_principle_1.json](misc/json_files/wo_principle_1.json)
- Run this [jupyter file](misc/create_db.ipynb). You will have your table(`principle1`) generated for principle 1 in this [database](misc/DBs/principles.db)


### SCHEMA of the tables
```SQL
CREATE TABLE IF NOT EXISTS principle{i} (
    pid INT,
    qid INT,
    with_principle TEXT,
    without_principle TEXT,
    response_with_principle TEXT,
    response_without_principle TEXT,
    preference TEXT
)
```

### To check the stored data in database
- open terminal, run `sqlite3 misc/DBs/principles.db`
- run SQL commands. 
    - `SELECT COUNT(*) FROM principle1` - This will display total rows in table principle1.

### To run flask application
- Ensure you are in root directory of this repository.
- `python app.py`