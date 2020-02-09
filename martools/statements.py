PRAGMA_journal_mode = """
PRAGMA journal_mode = wal;
"""
PRAGMA_wal_autocheckpoint = """
PRAGMA wal_autocheckpoint;
"""
PRAGMA_read_uncommitted = """
PRAGMA read_uncommitted = 1;
"""
CREATE_TABLE_PERMA = """CREATE TABLE IF NOT EXISTS
   bot_stats_perma 
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
   bot_stats_temp 
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


UPSERT_PERMA = """INSERT INTO 
bot_stats_perma 
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

INSERT_PERMA_DO_NOTHING = """INSERT INTO 
bot_stats_perma 
  (
    guild_id, 
    event,
    quantity
  ) 
VALUES 
  (
    ?,
    ?,
    ?
  )
ON CONFLICT
  (
    guild_id, 
    event
  ) 
DO NOTHING;
"""

UPSERT_TEMP = """INSERT INTO 
bot_stats_temp 
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
DROP TABLE IF EXISTS bot_stats_temp;
"""

SELECT_TEMP = """
SELECT * 
FROM bot_stats_temp
WHERE event 
LIKE :event;
"""

SELECT_PERMA = """
SELECT * 
FROM bot_stats_perma
WHERE event 
LIKE :event;
"""

SELECT_PERMA_GLOBAL = """
SELECT sum(quantity) 
FROM bot_stats_perma 
WHERE event = :event
GROUP BY event;
"""

SELECT_TEMP_GLOBAL = """
SELECT sum(quantity) 
FROM bot_stats_temp 
WHERE event = :event
GROUP BY event;
"""

SELECT_PERMA_SINGLE = """
SELECT sum(quantity) 
FROM bot_stats_perma 
WHERE event = :event AND guild_id = :guild_id
GROUP BY event;
"""

SELECT_TEMP_SINGLE = """
SELECT sum(quantity) 
FROM bot_stats_temp 
WHERE event = :event AND guild_id = :guild_id
GROUP BY event;
"""
