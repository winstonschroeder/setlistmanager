SELECT json_object(
	'band_id', s.band_id,
	'song_id', s.id,
	'song_name', s.name,
	'composer_id', s.composer_id
)
FROM songs s