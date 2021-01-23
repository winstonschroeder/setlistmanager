ALTER TABLE songs
ADD COLUMN json TEXT GENERATED ALWAYS AS (json_object(
	'id', id,
	'band_id', band_id,
	'name', name,
	'composer_id', composer_id,
	'version', version
	)) VIRTUAL
