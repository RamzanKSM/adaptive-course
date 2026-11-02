-- «Эстафета»: the board station projects a relay only when the teacher put it on the board.
ALTER TABLE relays ADD COLUMN on_board INTEGER NOT NULL DEFAULT 0;
