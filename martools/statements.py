PRAGMA = """
PRAGMA journal_mode = wal;
PRAGMA wal_autocheckpoint;
PRAGMA read_uncommitted = 1;
"""

CREATE_TABLE_PERMA = """CREATE TABLE IF NOT EXISTS
   guild_words_perma 
        (
        guild_id INTEGER NOT NULL,
        event TEXT NOT NULL,
        quantity INTEGER DEFAULT 1,
        PRIMARY KEY 
          (
            guild_id, 
            event
          )
        );
"""
CREATE_TABLE_TEMP = """CREATE TABLE IF NOT EXISTS
   guild_words_temp 
        (
        guild_id INTEGER NOT NULL,
        event TEXT NOT NULL,
        quantity INTEGER DEFAULT 1,
        PRIMARY KEY 
          (
            guild_id, 
            event
          )
        );
"""


UPSET_PERMA = """INSERT INTO 
guild_words_perma 
  (
    guild_id, 
    event
  ) 
VALUES 
  (
    ?, 
    ?
  )
ON CONFLICT
  (
    guild_id, 
    event
  ) 
DO UPDATE 
  SET quantity = quantity + 1;
"""

UPSET_TEMP = """INSERT INTO 
guild_words_temp 
  (
    guild_id, 
    event
  ) 
VALUES 
  (
    ?, 
    ?
  )
ON CONFLICT
  (
    guild_id, 
    event
  ) 
DO UPDATE 
  SET quantity = quantity + 1;
"""
DROP_TEMP = """
DROP TABLE IF EXISTS guild_words_temp;
"""

SELECT_TEMP = """
SELECT * 
FROM guild_words_temp
WHERE event 
LIKE :event;
"""

SELECT_PERMA = """
SELECT * 
FROM guild_words_perma
WHERE event 
LIKE :event;
"""

SELECT_PERMA_GLOBAL = """
SELECT sum(quantity) 
FROM guild_words_perma 
WHERE event = :event
GROUP BY event;
"""

SELECT_TEMP_GLOBAL = """
SELECT sum(quantity) 
FROM guild_words_temp 
WHERE event = :event
GROUP BY event;
"""

SELECT_PERMA_SINGLE = """
SELECT sum(quantity) 
FROM guild_words_perma 
WHERE event = :event AND guild_id = :guild_id
GROUP BY event;
"""

SELECT_TEMP_SINGLE = """
SELECT sum(quantity) 
FROM guild_words_temp 
WHERE event = :event AND guild_id = :guild_id
GROUP BY event;
"""
