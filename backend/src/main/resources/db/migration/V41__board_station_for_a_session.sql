-- «Компьютер у доски» lives only while its browser tab is open (2026-11-03): the token moves from a cookie for a year to
-- the tab's sessionStorage, a silent station's row is deleted, nothing is revoked and kept. The stations of the old
-- cookies are removed; a test remembers its station's name by itself, since the station is gone soon after the test.
ALTER TABLE board_tests ADD COLUMN station_name TEXT;
UPDATE board_tests SET station_name = (SELECT name FROM board_stations s WHERE s.id = station_id) WHERE station_id IS NOT NULL;
UPDATE board_tests SET station_id = NULL;
DELETE FROM board_stations;
ALTER TABLE board_stations DROP COLUMN revoked_at;
