# CHAPTER NAME

## Summary
# Chapter 2.2— Create the Project Plan

- Reading / Citation: [Author, Title, Year, Pages]
- Date: YYYY-MM-DD
- Pages: [start–end]

## Summary
- The project plan defines the work to be done and who will do it. It typically contains a Statement of Work (SOW), a resource list, a Work Breakdown Structure (WBS) with effort estimates, a project schedule, and a risk plan. The plan is a living document used by project managers, team members, senior management, and stakeholders.

## Key Concepts
- Statement of Work (SOW): detailed list of features, intermediate deliverables, and the people responsible for producing them.
- Resource list: catalogue of all resources (people, hardware, facilities) with availability and costs.
- Work Breakdown Structure (WBS): decomposition of work into tasks that produce the work products.
- Estimates & Scheduling: effort estimation for WBS tasks, resource allocation, and calendar durations.
- Risk plan: identification, probability/impact assessment, prioritization, and mitigation actions.
- Plan inspection & revision history: periodic reviews and tracked changes to keep the plan current.

## Definitions / Important Terms
- Statement of Work (SOW) — an independent document listing features, deliverables (requirements, design docs, UML/class diagrams, code modules, test plans, acceptance plans), standards/templates, and estimated effort per work product.
- Resource list — a one-line entry per resource including name, short description, availability, and cost/constraints.
- Work Breakdown Structure (WBS) — task-level breakdown that produces all required work products.
- Risk plan — spreadsheet-like list with columns: Risk, Probability (1–5), Impact (1–5), Priority (P×I), Action.

## Important Details / Claims
- A project plan is used by multiple audiences: PMs (status & scheduling), team members (context & tasks), senior managers (cost/schedule assurance), and stakeholders (needs verification).
- Consensus is critical: review meetings should include team reps, senior managers, and stakeholders; deviations must be tracked in review sessions.
- The vision and scope document is a prerequisite — it informs the SOW and reduces duplicated planning work.
- The SOW must reference tasks in the project schedule so deliverables map to schedule items.

## Examples / Applications
- SOW entries: feature list (phase-based), software requirements specification (brief paragraph), design/architecture spec, class/UML diagrams, code packages/modules, test plans, user-acceptance plans, defect reports.
- Resource list example entry: "DB Server Cluster — 3 nodes; available from 2025-11-01 to 2026-03-31; cost estimate $X/month; note planned maintenance windows." 

## Estimates & Schedule Workflow
- Steps: (1) define WBS, (2) estimate effort per task (see Chapter 3 for Wideband Delphi), (3) assign resources and compute calendar durations, (4) record revision history for WBS/estimates/schedule.
- Maintain revision history: log who added/changed/removed tasks and when; include rationale from review meetings.

## Risk Plan / Process
- Run a ~2-hour risk planning meeting: brainstorm specific risks, estimate Probability (1–5) and Impact (1–5), compute Priority = Probability × Impact, and document mitigation Actions.
- Mitigation actions: alter schedule (move risky tasks earlier), add cross-training tasks, add contingency tasks, or document a recovery plan (steps to take if risk occurs).
- Output: a risk spreadsheet with columns Risk / Probability / Impact / Priority / Action.

## Important Quotes (copy exact phrasing)
- "The project plan defines the work that will be done on the project and who will do it." — captures the plan's purpose.

## Questions / Confusions
- What templates/standards will our org use for SOW and WBS? (projects should reference organization-specific templates where available)

## Connections / Thoughts
- Chapter 3 (estimation) and Chapter 4 (scheduling) are tightly coupled; implementers should follow the processes described there.
- Keep the plan short and actionable; store SOW separately so it can stand alone.

---

# Chapter 4 — Engineering for Equity

- Written by Demma Rodriguez
- Edited by Riona MacNamara
- Reading / Citation: [Author, Title, Year, Pages]
- Date: YYYY-MM-DD

## Summary
- Engineers must design products that respect and empower a broad, diverse user base; doing so requires organizational commitment to diversity, continuous learning, and design practices that prioritize marginalized or hard-to-reach users.
- Bias is the default — without explicit attention, products, data, tests, and processes will reproduce societal inequities.

## Key Concepts
- Bias Is the Default: unconscious bias leads teams to produce products that disadvantage underrepresented groups.
- Representation Matters: workforce and dataset diversity reduce blind spots in product design and testing.
- Build With Everyone: engage vulnerable communities early and center them in design and testing.
- Multicultural Capacity: engineers and organizations need multidisciplinary training (statistics, ethics, multicultural studies) to reduce harm.
- Measure Equity: instrument product features and processes to detect disparate impacts.

## Definitions / Important Terms
- Unconscious bias — implicit attitudes or stereotypes that affect decisions without conscious intent.
- Inclusive design — designing for the most-difficult or least-privileged users first to improve outcomes for all.
- Psychological safety — an environment where team members can raise concerns about equity without fear.

## Important Details / Claims
- Case study (Google Photos): classification errors (labeling Black people as "gorillas") caused by incomplete datasets, lack of representation in engineering teams, and insufficient testing across populations — resulted in harm and loss of trust.
- AI & datasets: biased or incomplete training data produces invalid outcomes; independent testing often lags behind deployment and must be strengthened.
- Organizational responsibility: hiring pipelines alone are insufficient — retention, progression, and workplace climate must be addressed.

## Case Studies / Examples
- Google Photos misclassification — example of biased data & inadequate testing.
- Hiring requisition system — surfacing performance ratings introduced equity risks; analysis showed ratings are not predictive of future success and required process change to avoid unfair internal mobility decisions.

## Recommendations / Actionable Steps
- Center vulnerable users in research and design; "build with" users rather than "for" them.
- Design for the user least like you; prioritize accessibility and inclusive UX.
- Measure equity: add metrics, track outcomes, and publish/discuss results within the organization.
- Slow development when data or tests are insufficient; invest in better datasets and independent audits.
- Invest in multidisciplinary professional development for engineers.
- Hold managers accountable for balanced candidate slates and equitable growth opportunities.

## Important Quotes
- "Bias is the default." — the chapter's central claim.
- "Don’t build for everyone. Build with everyone." — emphasizes collaboration with diverse users.

## Questions / Confusions
- What specific equity metrics should product teams instrument? Who owns them (product, PM, trust & safety, DEI)?

## Connections / Thoughts
- Links to chapters on estimation (Chapter 3), scheduling (Chapter 4), and project planning (Chapter 2): equity considerations must be baked into planning and reviews.


---

# Chapter 5 — How to Lead a Team

- Written by Brian Fitzpatrick
- Edited by Riona MacNamara
- Reading / Citation: [Author, Title, Year, Pages]
- Date: YYYY-MM-DD

## Summary
- Describes leadership roles (Manager, Tech Lead, Tech Lead Manager), servant leadership, and practical patterns and antipatterns for building and leading effective engineering teams.

## Key Concepts
- Manager vs Tech Lead: managers focus on people (performance, career, happiness); tech leads focus on technology (architecture, priorities, velocity).
- Servant leadership: protecting the team, removing roadblocks, and creating psychological safety.
- Positive patterns: lose the ego, be a catalyst, teach and mentor, set clear goals; Antipatterns: hire pushovers, ignore low performers, micromanage, compromise hiring bar.

## Definitions / Important Terms
- Tech Lead (TL) — leads technical efforts, architecture, and technical decisions.
- Tech Lead Manager (TLM) — combined people+tech role often used on small teams.
- Psychological safety — team members feel safe to take risks and surface issues.

## Important Details / Claims
- Leadership requires social skills distinct from engineering; humility, respect, and trust are core pillars.
- Managers should shield teams from organizational noise, provide air cover, and remove roadblocks quickly.
- Failing fast and learning via postmortems (no-blame) is central to engineering organizations like Google.

## Actionable Practices
- Delegate and grow others; seek to replace yourself by hiring and developing talent.
- Address low performers early with clear, measurable improvement plans.
- Track team happiness via regular one-on-ones and simple checks ("What do you need?", happiness rating).
- Set clear, concise goals and priorities; create mission statements to align the team.
- Give honest and direct feedback (be kind but clear); avoid ineffective compliment sandwiches.

## Antipatterns to Avoid
- Hiring cheap or substandard candidates, ignoring people problems, treating the team like children, and sacrificing long-term quality for short-term hires.

## Positive Patterns to Cultivate
- Maintain calm (be a Zen master), ask questions to help others find solutions, build consensus, and remove organizational blockers.

## Connections / Thoughts
- Reinforces the need for good planning and processes (Chapters 2–4) executed by well-led teams.

## TL;DR
- Serve your team: set clear goals, remove obstacles, develop people, and create a safe environment to experiment and learn.

---