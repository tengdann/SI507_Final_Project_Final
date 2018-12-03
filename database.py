import sqlite3 as sqlite

DBNAME = 'final_project.sqlite3'

# REQUIRES: a valid DBNAME
# MODIFIES: DBNAME file
# EFFECTS: drops existing DB tables and creates new ones
# DEPENDENCIES: nothing
def create_tables():
    conn.connect(DBNAME)
    cur = conn.cursor()
    
    # Drop tables :(
    statement = '''
        DROP TABLE IF EXISTS Cache
    '''
    cur.execute(statement)
    
    statement = '''
        DROP TABLE IF EXISTS Articles
    '''
    cur.execute(statement)
    
    statement = '''
        DROP TABLE IF EXISTS Tags
    '''
    cur.execute(statement)
    
    statement = '''
        DROP TABLE IF EXISTS Regions
    '''
    cur.execute(statement)
    
    conn.commit()
    
    # Create tables
    statement = '''
        CREATE TABLE Cache (
            id INTEGER PRIMARY KEY,
            url TEXT UNIQUE,
            html BLOB
        )
    '''
    cur.execute(statement)
    
    statement = '''
        CREAT TABLE Articles (
            id INTEGER PRIMARY KEY,
            author TEXT,
            title TEXT UNIQUE,
        )
    '''
    

if __name__ == '__main__':
    create_tables()
    print('Tables created successfully!')