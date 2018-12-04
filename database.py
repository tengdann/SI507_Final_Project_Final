import sqlite3 as sqlite

DBNAME = 'final_project.sqlite3'

# REQUIRES: a valid DBNAME
# MODIFIES: DBNAME file
# EFFECTS: drops existing DB tables and creates new ones
# DEPENDENCIES: nothing
def create_tables():
    conn = sqlite.connect(DBNAME)
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
    
    statement = '''
        DROP TABLE IF EXISTS Authors
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
        CREATE TABLE Articles (
            id INTEGER PRIMARY KEY,
            author_id INTEGER,
            title TEXT UNIQUE,
            date TEXT,
            region_id INTEGER,
            tag_id INTEGER,
            url TEXT
        )
    '''
    cur.execute(statement)
    
    statement = '''
        CREATE TABLE Tags (
            id INTEGER PRIMARY KEY,
            tag TEXT UNIQUE
        )
    '''
    cur.execute(statement)
    
    statement = '''
        CREATE TABLE Regions (
            id INTEGER PRIMARY KEY,
            region TEXT UNIQUE
        )
    '''
    cur.execute(statement)
    
    statement = '''
        CREATE TABLE Authors (
            id INTEGER PRIMARY KEY,
            author TEXT UNIQUE
        )
    '''
    cur.execute(statement)
    
    conn.commit()
    conn.close()

def pop_tables():
    conn = sqlite.connect(DBNAME)
    cur = conn.cursor()
    
    statement = '''
        INSERT INTO Tags (tag) VALUES (?)
    '''
    cur.execute(statement, ('Unknown',))
    
    statement = '''
        INSERT INTO Regions (region) VALUES (?)
    '''
    cur.execute(statement, ('Unknown',))
    
    statement = '''
        INSERT INTO Authors (author) VALUES (?)
    '''
    cur. execute(statement, ('Unknown',))
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_tables()
    print('Tables re-created successfully!')
    pop_tables()
    print('Null values established!')