-- «Жребий»: the weights the teacher set by hand before a run, {userId: weight} (null: none). Everybody else keeps the
-- computed weight. Rules: backend/README.md, «Жребий».
ALTER TABLE draw_runs ADD COLUMN weights_json TEXT;
