DROP VIEW vjson_sets_per_setlist;
CREATE VIEW vjson_sets_per_setlist
AS
SELECT s.id as setlist_id, json_object(
	'setlist_id', s.id,
	'setlist_name', s.name,
	'band_id', s.band_id,
	'details', json_group_array(vsps.details)
	) as details
FROM setlists s
LEFT JOIN sets2setlists s2s
ON s.id = s2s.setlist_id
LEFT JOIN vjson_songs_per_set vsps
ON vsps.set_id = s2s.set_id
LEFT JOIN bands b
ON b.id = s.band_id
GROUP BY s.id