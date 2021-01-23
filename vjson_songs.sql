DROP VIEW vjson_songs;
CREATE VIEW vjson_songs
AS
SELECT s.band_id, s.id as song_id, s.composer_id, json_object(
	'band_id', s.band_id,
	'band_name', b.name,
	'song_id', s.id,
	'song_name', s.name,
	'composer_id', s.composer_id,
	'composer_name', a.name,
	'version', s.version
) as details
FROM songs s
LEFT JOIN bands b
ON s.band_id = b.id
LEFT JOIN artists a
ON s.composer_id = a.id