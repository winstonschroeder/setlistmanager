DROP VIEW vjson_shows;
CREATE VIEW vjson_shows
AS
SELECT s.id as 'show_id', json_object(
	'show_id', s.id,
	'show_name', s.name,
	'date', s.date
) as details
FROM shows s
LEFT JOIN shows2bands s2b
ON s2b.show_id = s.id
LEFT JOIN bands b
ON b.id = s2b.band_id