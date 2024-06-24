# Evaluating-Prompts

### Clone the repo locally
- `git clone https://github.com/hwaseem04/Evaluating-Prompts`

### To create table for each principle from json files
- Run this [jupyter file](misc/create_db.ipynb). You will have your table(`principle1`) generated for principle 1 in this [database](misc/DBs/principles.db) (currently not available in the repo due to its large size. Will be uploaded to drive and the link will be attached soon)


### SCHEMA of the tables
```SQL
CREATE TABLE IF NOT EXISTS principle{i} (
    pid INT,
    qid INT,
    with_principle TEXT,
    without_principle TEXT,
    response_with_principle TEXT,
    response_without_principle TEXT,
    human_preference INT,
    machine_preference INT,
    correctness_gpt3_5turbo INT,
    correctness_gpt4 INT,
    correctness_gpt4o INT
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
