USE placement_db;

-- KPI 1: Branch-wise placement rate
SELECT s.branch,
       COUNT(DISTINCT s.student_id) AS total_students,
       COUNT(DISTINCT o.student_id) AS placed_students,
       ROUND(100 * COUNT(DISTINCT o.student_id) / COUNT(DISTINCT s.student_id), 1) AS placement_pct
FROM students s
LEFT JOIN offers o ON s.student_id = o.student_id
GROUP BY s.branch
ORDER BY placement_pct DESC;

-- KPI 2: Placement funnel (Applied -> OA -> Interview -> Offer)
SELECT COUNT(*) AS applied,
       SUM(stage_reached IN ('OA', 'Interview', 'Offer')) AS reached_oa,
       SUM(stage_reached IN ('Interview', 'Offer')) AS reached_interview,
       SUM(stage_reached = 'Offer') AS offers
FROM applications;

-- KPI 3: Company-wise offers and ranking (window function)
SELECT c.company_name,
       COUNT(*) AS offers,
       ROUND(AVG(o.ctc_lpa), 2) AS avg_ctc_lpa,
       RANK() OVER (ORDER BY COUNT(*) DESC) AS offer_rank
FROM offers o
JOIN companies c ON o.company_id = c.company_id
GROUP BY c.company_name
ORDER BY offer_rank;