# Evaluating-Prompts

### Clone the repo locally
- `git clone https://github.com/hwaseem04/Evaluating-Prompts`

### To create table for each principle from json files
- Download all the json files from [here](https://github.com/VILA-Lab/ATLAS/tree/main/data/principles/boosting). For quick testing you can start with just two files which is already downloaded, i.e [w_principle_1.json](misc/json_files/w_principle_1.json) and [wo_principle_1.json](misc/json_files/wo_principle_1.json). But I would suggest downloading all files and test it once you are comfortable doing it with the two files.
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
- Now open the local host link, usually - ` http://127.0.0.1:5000`

### Bug tracking
- You can either text me in teams or (Most preferred)you can raise an issue in this repository along with steps to reproduce the bug. 