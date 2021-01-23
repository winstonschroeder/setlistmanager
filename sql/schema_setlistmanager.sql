BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "songs" (
	"id"	INTEGER,
	"band_id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	"composer_id"	INTEGER,
	"version"	TEXT,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "songs2sets" (
	"id"	INTEGER,
	"song_id"	INTEGER NOT NULL,
	"set_id"	INTEGER NOT NULL,
	"successor_id"	INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY("song_id") REFERENCES "songs"("id"),
	FOREIGN KEY("set_id") REFERENCES "sets"("id"),
	FOREIGN KEY("successor_id") REFERENCES "songs2sets"("id")
);
CREATE TABLE IF NOT EXISTS "setlists2shows" (
	"setlist_id"	INTEGER NOT NULL,
	"show_id"	INTEGER NOT NULL,
	FOREIGN KEY("setlist_id") REFERENCES "setlists"("id")
);
CREATE TABLE IF NOT EXISTS "setlists" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL,
	"band_id"	INTEGER DEFAULT 0,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "sets2setlists" (
	"setlist_id"	INTEGER NOT NULL,
	"set_id"	INTEGER NOT NULL,
	FOREIGN KEY("setlist_id") REFERENCES "setlists"("id"),
	FOREIGN KEY("set_id") REFERENCES "sets"("id")
);
CREATE TABLE IF NOT EXISTS "sets" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL,
	"band_id"	INTEGER NOT NULL,
	FOREIGN KEY("band_id") REFERENCES "bands"("id"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "shows" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL,
	"date"	TEXT,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "songparts" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL,
	"song_id"	INTEGER NOT NULL,
	"successor_id"	INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY("song_id") REFERENCES "songs"("id"),
	FOREIGN KEY("successor_id") REFERENCES "songparts"("id")
);
CREATE TABLE IF NOT EXISTS "artists" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "shows2bands" (
	"show_id"	INTEGER,
	"band_id"	INTEGER,
	"running_order"	INTEGER,
	FOREIGN KEY("band_id") REFERENCES "bands"("id"),
	FOREIGN KEY("show_id") REFERENCES "shows"("id")
);
CREATE TABLE IF NOT EXISTS "mididevices" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "bands" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "user" (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  "username" TEXT UNIQUE NOT NULL,
  "password" TEXT NOT NULL
);
CREATE VIEW v_songs_per_band AS 
SELECT b.name AS band_name, s.name AS song_name, s.version, a.name as composer
FROM bands b
JOIN songs s
ON s.band_id = b.id
JOIN artists a
ON a.id = s.composer_id;
COMMIT;
