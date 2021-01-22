DROP VIEW vjson_songs_per_set;

CREATE VIEW vjson_songs_per_set 
AS
SELECT json_array(json_object('band_id', b.id, 'band_name', b.name, 'set_id', st.id, 'set_name', st.name, 'details', json_group_array(s.json)))
FROM sets st
LEFT JOIN songs2sets s2s
ON st.id = s2s.set_id
LEFT JOIN songs s
ON s.id = s2s.song_id
LEFT JOIN bands b
ON b.id = st.band_id
GROUP BY st.id, st.name, b.id, b.name;