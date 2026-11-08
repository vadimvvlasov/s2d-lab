# Independent Auditor — Complete Audit Checklist

This document contains the detailed 12-point audit checklist. Load this reference when performing comprehensive differential audits.

## Full 12-Point Checklist

### 1. Question Fidelity
Is each question explicitly asked, clearly implied, a concern, or added by research? Is attribution accurate?

**Check:**
- Explicit questions have direct quote/span from source
- Implied questions have clear supporting evidence
- Researcher-added questions labeled as such (not presented as participant questions)
- Attribution matches who actually raised the question
- No rhetorical questions or jokes treated as research requests

**Common defects:**
- Upgrading implied/researcher-added to explicit
- Misattributing questions to wrong participant
- Omitting explicit questions
- Treating rhetorical remarks as substantive questions

### 2. Question Decomposition
Are compound questions properly split into researchable components?

**Check:**
- Questions requiring different concepts/evidence/criteria split into separate IDs
- Each question has clear decision/information need
- No artificial merging of unrelated questions
- Split maintains original intent

**Common defects:**
- Merging distinct decisions into one question
- Not splitting compound "A and B and C?" into separate questions
- Forcing unrelated questions into single answer

### 3. Participant Criteria
Are participant-stated criteria captured accurately with provenance?

**Check:**
- Explicit criteria (stated by participant) marked with source
- Inferred criteria labeled as inferred
- Researcher-proposed criteria labeled as proposed
- Unknown/missing criteria acknowledged
- Personal rules attributed to owner (not generalized)

**Common defects:**
- Treating inferred criteria as participant-stated
- Generalizing one person's threshold to group
- Inventing criteria without labeling
- Not disclosing unknown constraints

### 4. Option Coverage
For decision questions, are feasible options identified and compared fairly?

**Check:**
- 2-4 distinct feasible options when they exist
- Options actually address the decision
- Comparison covers relevant dimensions (not exhaustive list)
- Trade-offs and benefits for each option
- "No clear winner" stated if criteria conflict or data missing

**Common defects:**
- Forcing comparison when only one option viable
- Omitting obvious feasible alternative
- Biased comparison (unequal detail/scrutiny)
- Inventing options participant never considered

### 5. Recommendation Logic
Do selection criteria support the chosen option? Are inferred criteria labeled? Are weights/thresholds invented?

**Check:**
- Recommendation criteria traceable to participant/conversation
- Inferred criteria explicitly labeled
- No invented weights, scores, or thresholds
- "Best-supported option under these criteria" phrasing
- Conditional recommendation if criteria unknown/conflicting
- When another option would be preferable stated

**Common defects:**
- Inventing scoring/weighting system
- Claiming "best" without criteria
- Not labeling inferred criteria
- Recommendation doesn't follow from comparison

### 6. Financial Safety
Did the report invent an entry, stop, target, position size, or actionable trading signal?

**Check:**
- No invented price levels (entry, stop, target) unless explicitly supplied by participant
- No position sizing unless requested
- Participant trading intention not upgraded to endorsement
- Recommendations focus on process/method, not executable prices
- Personal decision ownership preserved
- Illustrative hypothetical levels labeled "NOT A TRADE SIGNAL"

**Common defects:**
- Converting educational question into trade call
- Inventing entry/exit prices
- Generalizing personal rule to directive
- Producing timing signal without request

### 7. Conceptual Correctness
Are technical/financial concepts used accurately?

**Check:**
- Terms defined correctly on first use
- Concepts not conflated (e.g., duration vs. maturity, price return vs. total return)
- Market/instrument context appropriate
- No logical contradictions

**Common defects:**
- Conflating related but distinct concepts
- Applying concept outside valid scope (e.g., equity metric to bonds)
- Logical contradiction in recommendation
- Oversimplification that changes meaning

### 8. Evidence Access
Was each source actually opened/retrieved, or was only a snippet/metadata/inaccessible page available?

**Check:**
- Access status matches reality:
  - FULL_TEXT_OPENED: complete document/data retrieved
  - OFFICIAL_DATA_OR_API_RETRIEVED: structured data from authoritative API
  - SEARCH_SNIPPET_ONLY: preview/snippet from search
  - METADATA_ONLY: title, abstract, citation only
  - INACCESSIBLE: 401/403/404 or paywall
  - USER_SUPPLIED: from conversation/attachment
- No false claims of full-text when only snippet available
- 401/403/404 pages not cited as verified source

**Common defects:**
- Claiming FULL_TEXT_OPENED when only snippet accessed
- Citing inaccessible page as if contents verified
- Treating search preview as full verification

### 9. Source Fit
Does the source support the exact claim, instrument, dates, market, and metric?

**Check:**
- Source covers the specific instrument/asset (not related one)
- Date/period matches (historical vs. current)
- Market/jurisdiction matches (US vs. global, equity vs. fixed income)
- Metric matches (headline number vs. adjusted figure)
- Claim precision matches evidence precision

**Common defects:**
- Citing source about related but different instrument
- Applying historical study to current question without caveat
- Mismatch in metric (using total return source for price return claim)
- Over-generalizing narrow source

### 10. Calculations
Inputs, units, formula, arithmetic, timestamp, rounding, and assumptions.

**Check:**
- All inputs shown with units
- Formula stated explicitly
- Intermediate steps shown for material calculations
- Arithmetic independently verified
- Result with units and appropriate rounding
- Timestamp/source date for data inputs
- Assumptions stated (compounding frequency, inflation adjustment, etc.)

**Common defects:**
- Arithmetic error (verify independently)
- Wrong formula (simple vs. compound, wrong rate convention)
- Missing units or wrong unit conversion
- Inputs without source/timestamp
- Assumptions not stated

### 11. Reader Quality
Is the final report clear, coherent, proportionate, and useful to participants?

**Check:**
- Questions accurately reflect conversation priorities
- Answers proportionate to importance (not inverted)
- Technical terms explained on first use
- No excessive jargon or generic education
- Recommendations actionable given participant context
- Length appropriate (target 700-1300 words)
- No repetition across sections

**Common defects:**
- Burying key answer in generic background
- Literature dump without decision focus
- Assuming expert knowledge without defining terms
- Over-length report with redundant sections

### 12. Audit Honesty
Did the auditor verify claims independently or endorse without checking?

**Check:**
- Source access actually attempted (not assumed)
- Calculations independently recalculated (not just re-stated)
- Participant attribution verified against source
- No "looks reasonable" without verification
- Limitations acknowledged if verification incomplete

**Common defects:**
- Claiming verification without independent check
- Passing claim because "it sounds right"
- Not admitting when source inaccessible
- Endorsing calculation without recomputing

## Audit Mode Application

### Baseline Audit (v1) — Artifact-Aware

**For Question Map / Research Packet:**
Apply checks **1, 2, 3, 5, 6, 7, 8, 9, 10, 12** (10 checks):
1. Question fidelity
2. Question decomposition
3. Participant criteria provenance
5. Recommendation logic
6. Financial safety
7. Conceptual correctness
8. Evidence access
9. Source fit
10. Calculations
12. Audit honesty

**For Final Report:**
Apply **all 12 checks** (add 4 and 11):
4. Option coverage
11. Reader quality

**Rationale:** Catch foundational defects that invalidate conclusions. Option coverage and reader quality are Final Report concerns, not Research Packet v1 concerns.

### Differential Audit (v2+)
Apply **all 12 checks** to affected scope:
- Sections explicitly changed to address CRs
- Claims that cite/depend on corrected content (via depends_on field)
- Adjacent context for coherence
- Regression check for new defects in edited areas

**Do not re-audit unchanged sections** unless they logically depend on corrected content.

## Severity Guidelines

Use severity definitions from main auditor prompt:
- **BLOCKER:** Invalidates conclusion, misrepresents source, unreliable output
- **MAJOR:** Materially weakens evidence/logic/attribution
- **MINOR:** Localized clarity issue
- **CLEAN:** No findings
- **BLOCKED:** Cannot complete review (missing inputs)

## Findings Template

See `templates/VERIFICATION-REPORT.md` for structured findings format.

---

**Document Purpose:** Reference for differential audits requiring comprehensive 12-point check.  
**Usage:** Load when performing differential audit (v2+ artifacts). Not required for baseline audit.  
**Created:** 2026-11-08 (Task B2 — auditor prompt refactor)
