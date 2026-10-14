-- Hard mode uses only the curated hard bank: the teacher does not trust generated algorithmic tasks.
-- Submissions and credit of these tasks stay; they are no longer assigned.
UPDATE tasks SET active = 0 WHERE mode = 'HARD' AND source = 'LLM';
