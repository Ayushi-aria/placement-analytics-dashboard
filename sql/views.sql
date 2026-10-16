USE placement_db;

CREATE VIEW v_branch_placement AS
SELECT s.branch,
       COUNT(DISTINCT s.student_id) AS total_students,
       COUNT(DISTINCT o.student_id) AS placed_students,
       ROUND(100 * COUNT(DISTINCT o.student_id) / COUNT(DISTINCT s.student_id), 1) AS placement_pct
FROM students s
LEFT JOIN offers o ON s.student_id = o.student_id
GROUP BY s.branch;

CREATE VIEW v_funnel AS
SELECT '1. Applied' AS stage, COUNT(*) AS students FROM applications
UNION ALL
SELECT '2. OA', COUNT(*) FROM applications WHERE stage_reached IN ('OA','Interview','Offer')
UNION ALL
SELECT '3. Interview', COUNT(*) FROM applications WHERE stage_reached IN ('Interview','Offer')
UNION ALL
SELECT '4. Offer', COUNT(*) FROM applications WHERE stage_reached = 'Offer';

CREATE VIEW v_company_performance AS
SELECT c.company_name, c.sector,
       COUNT(*) AS offers,
       ROUND(AVG(o.ctc_lpa), 2) AS avg_ctc_lpa,
       RANK() OVER (ORDER BY COUNT(*) DESC) AS offer_rank
FROM offers o
JOIN companies c ON o.company_id = c.company_id
GROUP BY c.company_name, c.sector;

CREATE VIEW v_offer_details AS
SELECT o.offer_id, s.branch, s.cgpa, c.company_name, c.sector, o.ctc_lpa
FROM offers o
JOIN students s ON o.student_id = s.student_id
JOIN companies c ON o.company_id = c.company_id;
