---
title: "Fix the sale timesheet estimate report"
state: completed
model: moonshotai/Kimi-K2.6
input_tokens:
---

# Run 01

Note: @Clanker refers to the "ai agent" (you) who is working on this task.

@Clanker when working on this task, make sure to:

- Read context and task section first
- Prepare a list of todos
- Update the todo list while working on the task

## Context

@Clanker Read the `AGENTS.md` and `README.md` to get an understanding of the project.

## Task

I ant you to fix
`addons/sale_workflow/sale_timesheet_estimate_report/report/hr_timesheet_templates.xml`

If `effective_hours_validated​` is more than `planned_hours` then the
`remaining_hours_validated` goes into minus. For each estimate line the max
`progress_validated` is 100%. The total percentage is calculated based
`progress_validated`. I have this case where this logic fails:

Phase | Geplant | Effektiv | Verbleibend | Progress Projektleitung | 16:00 | 22:15 |
-06:15 | 100% Projektadministration | 00:00 | 11:30 | -11:30 | 100% Server |
Bereitstellung | 02:00 | 02:00 | 00:00 | 100% Odoo | Installation | 04:00 | 01:15 |
02:45 | 31% Kontakte | 02:00 | 09:45 | -07:45 | 100% CRM | 04:00 | 18:30 | -14:30 | 100%
Verkauf | 04:00 | 06:00 | -02:00 | 100% Projekt | 08:00 | 05:30 | 02:30 | 68%
Zeiterfassung | 04:00 | 00:00 | 04:00 | 0% Rechnungsstellung | 08:00 | 00:45 | 07:15 |
9% E-Mail-Marketing | 04:00 | 00:45 | 03:15 | 18% Gesamt | 56:00 | 78:15 | -22:15 | 66%

The total progress must be calculated based on the total values.

## Worklog

- Fixed `remaining_hours_validated` in
  `addons/project/project_phase_estimate/models/project_estimate.py` by capping the
  value at `0.0` so it no longer goes negative when effective hours exceed planned
  hours.
- Fixed total progress calculation in
  `addons/sale_workflow/sale_timesheet_estimate_report/report/hr_timesheet_templates.xml`
  to use `env['project.estimate']._calculate_progress()` with the summed `planned_hours`
  and `effective_hours_validated` values, ensuring the total progress reflects the
  overall project status rather than an average of individual line percentages.
