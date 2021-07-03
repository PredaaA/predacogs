PRAGMA_journal_mode = """
PRAGMA journal_mode = wal;
"""
PRAGMA_wal_autocheckpoint = """
PRAGMA wal_autocheckpoint;
"""
PRAGMA_read_uncommitted = """
PRAGMA read_uncommitted = 1;
"""
CREATE_TABLE = """CREATE TABLE IF NOT EXISTS
  bot_stats 
  (
    event TEXT NOT NULL,
    quantity INTEGER DEFAULT 1,
    PRIMARY KEY (event)
  );
"""
CREATE_VERSION_TABLE = """CREATE TABLE IF NOT EXISTS
  version 
  (
    version_num INTEGER DEFAULT 1,
    PRIMARY KEY (version_num)
  );
"""
GET_VERSION = """
SELECT version_num
FROM version
"""

UPSERT = """INSERT or REPLACE INTO 
bot_stats 
  (event, quantity) 
VALUES 
  (:event, :quantity)
"""

INSERT_OR_IGNORE = """INSERT or IGNORE INTO 
bot_stats 
  (event, quantity) 
VALUES 
  (:event, :quantity)
"""

GET_EVENT_VALUE = """
SELECT quantity
FROM bot_stats
WHERE event 
LIKE :event;
"""

# Only used for old data migrate.
SELECT_OLD = """
SELECT sum(quantity) 
FROM bot_stats_perma 
WHERE event = :event
GROUP BY event;
"""
DROP_OLD_TEMP = """
DROP TABLE IF EXISTS bot_stats_temp
"""
DROP_OLD_PERMA = """
DROP TABLE IF EXISTS bot_stats_perma
"""
