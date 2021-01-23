SELECT s.band_id, json_group_array(s.json_song)
FROM (
	SELECT s.band_id, s.id, s.name, s.composer_id, s.version, json_object(
		'id', s.id,
		'name', s.name,
		'version', s.version) as json_song	
	FROM songs s
) s
GROUP BY s.band_id