# Proposed Shape Input: Grounded Assistant and Job Context UX

**Flow ID:** `swe-product-designer`
**Parent:** parent orchestrator
**Run:** `job-intelligence-llm-planner-20261110`
**Status:** Proposed Shape input only. Not product, frame, legal, privacy, security, source, accessibility, technical, or release approval.
**Evidence cutoff:** 2026-11-10

## 1. Experience Position

The assistant is an evidence reader beside the existing roadmap, not a new
recommender. It helps a student understand an existing deterministic result,
then optionally compare that result with labelled role or posting context.

The experience must preserve these boundaries:

- The backend remains authoritative for prerequisites, readiness, filtering,
  ranking, recommendation source, exact-slot assignment, and open-slot reasons.
- Stage 1 and Stage 2 are read-only. No assistant action changes profile,
  preference, completion, recommendation, score, slot, or eligibility state.
- Generated text never appears as source evidence.
- Planning readiness is not registration eligibility.
- Reviewed course exposure is not student mastery.
- Taxonomy context is not employer evidence or current Singapore demand.
- A missing course link is an evidence unknown, not a student deficiency.
- Stage 2 shows item-level comparisons only. It has no aggregate gap, fit,
  coverage, employability, frequency, trend, demand, or missing-skills score.

## 2. Current-Product Fit

Preserve the current React shell and its conventions:

- Keep the centered `78rem` maximum content width, rounded panels, soft shadows,
  teal light-theme accent, cyan dark-theme accent, and dark roadmap canvas.
- Reuse the existing top navigation, section heading with accent rule, card,
  pill, empty-state, loading row, status row, and modal/panel patterns.
- Retain light/dark theme behavior and current roadmap, modules, and profile
  pages. Add no visual-system reset and introduce no new typeface in this Shape.
- Keep controls sentence case except existing compact uppercase utility labels.
- Prefer an in-page workspace on desktop and a full-screen sheet on mobile.
  Do not overlay a narrow floating chat bubble on roadmap content.

## 3. Information Architecture

### 3.1 Primary navigation

Proposed addition after `Modules`:

```text
Roadmap | Modules | Assistant | Profile | Log out
```

`Assistant` is a first-class view because evidence, limitations, expiry, and
posting review require more space than the existing module-detail dialog. It
contains three independently gated modes:

```text
Recommendation help | Role context | Posting context
```

- `Recommendation help`: Stage 1, available only when the required current
  roadmap, recommendation, slot, or course context exists.
- `Role context`: Stage 2A, only for supported Software Engineer or Data
  Engineer pilot targets.
- `Posting context`: Stage 2B, only in an approved controlled-user scope.
- Hide unreleased modes rather than showing aspirational disabled controls.
- A killed Stage 2 mode does not disable Stage 1 or the other Stage 2 mode.

### 3.2 Contextual entry points

| Current surface | Entry control | Preselected context | Supported route |
|---|---|---|---|
| Recommended course inside a choice slot | `Why this course?` | Result, slot, course | Explain recommendation |
| Locked roadmap course | `Why locked?` | Course and readiness snapshot | Readiness/prerequisite |
| Open recommendation slot | `Why was this left open?` | Open-slot ID and reason | Explain open slot |
| Two or more current recommendation cards | `Compare selected` | Current result IDs only | Compare recommendations |
| Module detail panel | `Explain course facts` | Course code | Show course fact |
| Roadmap or recommendation detail | `Compare reviewed skill exposure` | Current supported role and submitted course codes | Reviewed skill exposure |
| Profile career goal, when supported | `Explore role context` | Canonical pilot role | Role target |
| Assistant mode selector | `Analyze a posting` | None | Supplied posting |

Entry controls open the `Assistant` view with a visible context bar, for
example: `Using current result: SC4023 in Year 4 Semester 1`. The user can
return to the originating view. The assistant does not silently broaden or
replace the selected entities.

### 3.3 Session model

- No conversation history, history list, save, share, or export.
- Stage 1 may keep the current in-memory exchange while the view is open. A
  reload or logout clears it.
- Stage 2B has one active analysis, a visible expiry, and `Delete now`.
- Closing Stage 2B does not imply deletion. The active expiry and delete action
  remain visible when the user returns during the same active analysis window.
- Revisit after deletion or expiry requires a new declaration and submission.

## 4. Stage 1: Grounded Recommendation Help

### 4.1 Six intent patterns

| Intent | User patterns | Required UI context | Answer focus |
|---|---|---|---|
| `explain_recommendation` | "Why this course?", "Why here?", "What supported this?" | Current recommendation and slot IDs | Existing reason, source, readiness, prerequisites, qualitative evidence |
| `explain_readiness_or_prerequisite` | "Why is this locked?", "What must come first?", "Am I eligible?" | Course/roadmap ID and readiness snapshot | Implemented prerequisite/standing branch, plus registration limitation |
| `compare_current_recommendations` | "Compare these", "What are the tradeoffs?" | At least two IDs in current result | Evidence-backed differences without a universal best claim |
| `explain_open_slot` | "Why is this empty?", "Why no recommendation?" | Current open-slot ID | Exact `no-supported-match` or `limit-reached` explanation |
| `show_course_fact` | "How many AU?", "What are the prerequisites?", "What is this course about?" | Course code | Versioned catalog fields and seeded/non-live qualification |
| `show_reviewed_skill_exposure` | "What might these courses cover for my role?" | Supported role and submitted course codes | Reviewed likely exposure, depth, unmapped courses, and explicit unknowns |

Routing uses the entry context and allowlisted entities before synthesis. If
exactly two intents remain plausible, ask one clarification:

> Are you asking why this course was recommended, or why it is marked ready?

Buttons: `Why recommended` and `Why ready`. No free-text clarification loop.
If routing is still unclear, show `unsupported_intent`.

### 4.2 Stage 1 end-to-end flow

1. User enters from a contextual control or `Recommendation help`.
2. Context bar states the exact result, slot, course, or comparison set in use.
3. Composer offers intent-specific prompt chips and optional free text.
4. On submit, show `Checking current evidence...`; do not stream unsupported
   partial claims.
5. System builds the deterministic fallback before optional model synthesis.
6. Render the answer only after claim and citation validation.
7. If provider, timeout, budget, or validation fails, render the complete
   fallback in the same anatomy with a visible fallback status.
8. Keep bounded follow-ups tied to the same supported context. A new entity
   requires explicit selection from the roadmap or module UI.

### 4.3 Response anatomy

Every response uses this order:

1. **Answer:** one direct sentence or a short comparison.
2. **Status line:** `Deterministic explanation` or `Generated explanation`,
   freshness, and any fallback/stale state.
3. **Why:** two to five factual bullets. Each factual bullet ends with a
   keyboard-operable citation marker.
4. **Evidence:** collapsed by default after the first item; grouped by evidence
   class, with source, version, locator, and observed time.
5. **What this does not establish:** only material limitations for this answer.
6. **Next useful action:** zero to two bounded actions, such as `View course
   details`, `Check NTU registration information`, or `Compare selected
   courses`.

Do not expose raw recommendation score components. Translate them into
qualitative, source-backed reasons.

### 4.4 Unsupported intent

Use when the request asks for general career advice, salary or demand, an
unreturned course, a universal best course, registration eligibility, degree
audit, timetable/vacancy information, mastery, employability, mutation, or
another unsupported route.

Copy:

> I cannot answer that from the supported course and recommendation evidence.
> I can explain this recommendation, its readiness checks, the open slot, or
> compare courses already in your current result.

Show only actions valid for the current context. Do not send unsupported text
to the model.

## 5. Evidence Language and Components

### 5.1 Evidence classes

| Class | Visible label | Accent use | Required detail |
|---|---|---|---|
| `catalog_fact` | `Course catalog` | Teal | Field, catalog snapshot/version, seeded/non-live note |
| `deterministic_recommendation_fact` | `Current recommendation` | Cyan | Result/service version, slot or readiness locator |
| `job_evidence` | `Posting evidence` | Rose | Exact permitted excerpt, locator, observed-at-upload time, modality |
| `normalized_skill_inference` | `Mapped skill` | Violet | Raw mention, mapping state, mapper/taxonomy version, reason |
| `generated_advice` | `Generated explanation` | Neutral outlined | Citations for every factual premise; never a source badge |

Additional qualifiers appear beside, not instead of, the class:
`User supplied`, `Transcript derived`, `Reviewed course exposure`, `Taxonomy
context`, `Seeded snapshot`, `Stale`, `Conflicting`, `Ambiguous`, `Unmapped`,
`Unknown`, `Fallback`.

Color is redundant. Every state has text and, where useful, a simple icon with
an accessible name.

### 5.2 Evidence detail interaction

- Citation markers are buttons named, for example, `Evidence 2: current
  recommendation`.
- Activating a marker expands the matching evidence row and moves focus to its
  heading.
- Evidence detail uses a non-modal disclosure in the assistant workspace.
- On mobile, evidence opens as an in-flow accordion, not a nested modal.
- Expired, withdrawn, or unavailable evidence retains metadata but never shows
  prohibited text. Copy: `This evidence is no longer available. Regenerate
  from currently permitted evidence before using this answer.`

## 6. Stage 2A: Role Context

### 6.1 Entry and scope

Role context is available only for:

- `Software Engineer`: software engineer, software developer, and explicit
  junior or graduate variants.
- `Data Engineer`: data engineer and explicit junior or graduate variants.
- English-language, Singapore, entry-level or graduate exploration.

The selector does not offer excluded titles. Typed unsupported titles are not
coerced:

> This pilot supports entry-level or graduate Software Engineer and Data
> Engineer roles in Singapore. The title you entered is outside that scope.

Actions: `Choose Software Engineer`, `Choose Data Engineer`, `Return to
recommendations`.

### 6.2 Role context flow

1. Select one canonical role.
2. Show pinned taxonomy match and release/version before skill content.
3. Display taxonomy concepts as `Role taxonomy context`, never `Employer
   requirements`.
4. Compare each concept with reviewed course-exposure evidence for submitted
   current courses.
5. Show mapping state and `No reviewed course link` where evidence ends.
6. End with the static limitation:

> This role context is from a pinned occupational taxonomy. It does not show
> current Singapore vacancies, employer demand, or what any employer requires.

No model or source outage may relabel taxonomy data as live market evidence.

## 7. Stage 2B: Supplied Posting Context

### 7.1 Input and origin declaration

The input screen has two steps in one page:

**1. Declare the source**

- Required checkbox: `I may provide this posting for private analysis.`
- Required origin radio:
  - `Direct employer`
  - `Approved provider`
  - `Other source I am authorized to provide`
- Required checkbox: `This content is not from LinkedIn or a LinkedIn export.`
- Supporting copy:

> Your declaration records the source you selected; it is not a legal
> determination. Do not submit LinkedIn-derived content. This service does not
> fetch URLs.

**2. Add one posting**

- Tabs: `Paste text` and `Upload file`.
- Paste control includes character count and accepted-limit hint.
- Upload accepts one approved text or text-bearing PDF file only.
- File row shows name, type, size, and `Remove`.
- Optional `Source reference` is provenance text only. Label it:
  `Reference only. No URL will be opened or fetched.`
- Primary action: `Review posting`.

Disable `Review posting` until declarations and one valid input are present.
Never preselect an origin or consent checkbox.

### 7.2 Input refusal copy

**Declared or detected LinkedIn origin**

> This pilot cannot analyze LinkedIn-derived content. It does not determine
> whether you have legal rights to the content. Use a posting from a direct
> employer or approved provider that you are authorized to provide.

**Unresolved origin after one clarification**

> I cannot confirm that this source fits the pilot input policy, so I cannot
> analyze it. You can submit a different posting with a supported origin.

**Unsupported file**

> This file cannot be analyzed. Use one text-bearing, unencrypted TXT or PDF
> file within the displayed size and page limits.

**Bulk or acquisition-workaround input**

> This pilot analyzes one posting at a time. Bulk collections and source
> acquisition workarounds are not supported.

### 7.3 Extraction review and one clarification

After parsing, show `Review extracted posting` before skill comparison:

```text
Posting identity
Title: Graduate Software Engineer
Location: Singapore
Source: Direct employer, declared by you
Observed: 10 Nov 2026, 14:30

Extracted requirements (7)
[Required] "Experience with Python..."        [View evidence]
[Preferred] "Familiarity with cloud..."       [View evidence]
[Unclear] "Strong communication..."           [View evidence]

Not treated as requirements (2)
"Our platform runs on..." [Company technology]

[Delete now]                         [Compare with courses]
```

The user reviews extraction but does not approve mappings as authoritative.
They may remove the posting and restart. They may not edit extracted evidence
into a new employer claim.

Permit one clarification total, only for provenance, document identity, or a
material fact the user can know. Present constrained choices plus `I do not
know`. Example:

> The document contains two job titles. Which one is this posting for?

After the answer or `I do not know`, continue with gaps or abstain. Do not ask a
second question and do not ask the user to infer employer intent, proficiency,
geography, work authorization, or degree equivalence.

### 7.4 Read-only skill comparison

The comparison is a list of evidence items, not a scorecard:

```text
Posting requirement
Python                                      Required
"Experience with Python..."                 Posting evidence [1]

Mapped skill
Programming foundations                    Alias match
Mapper v1.0 | Raw mention: Python

Reviewed course exposure
SC1003: introductory course-content exposure [2]

Boundary
Course exposure does not establish your mastery.
```

For each item, show:

- Exact posting wording and `Required`, `Preferred`, `Optional`, `Unclear`,
  `Negated`, `Alternative`, or `Conflicting`.
- Raw mention and `Exact`, `Alias`, `Broader`, `Narrower`, `Ambiguous`, or
  `Unmapped` mapping state.
- Reviewed course-exposure links and depth, or `No reviewed course link`.
- Evidence and version details.

Never show:

- percentage fit, total matches, total gaps, coverage meter, readiness score;
- ranked missing skills or "top gaps";
- green/red pass-fail treatment of the student;
- current-demand, frequency, trend, or employability language;
- inferred requirements from responsibilities or company technology.

### 7.5 Expiry and deletion

Persistent bar within the active Stage 2B view:

> Private analysis. Deletes automatically at 15:30. No history is saved.
> [Delete now]

At 10 minutes remaining, change text, not color alone:

> Deletes in 10 minutes. Finish reviewing or submit again later.

`Delete now` opens a confirmation dialog:

> Delete this posting analysis?
>
> The posting, extracted evidence, course comparison, and result will be
> deleted together. This cannot be undone.

Buttons: `Keep analysis`, `Delete analysis`.

On success, focus the status heading:

> Posting analysis deleted
>
> The posting and its private derived result are no longer available.
> [Analyze another posting]

On expiry, show the same terminal state with `expired` wording. No answer,
evidence excerpt, or comparison remains visible.

## 8. State Table

| State | Trigger | UI behavior and copy | Recovery |
|---|---|---|---|
| Stage 1 no context | Direct assistant entry without required result | `Load a roadmap recommendation or select a course first.` | Links to Roadmap/Profile |
| Ready | Supported context resolved | Prompt chips and composer enabled | Submit |
| Loading | Context/answer request active | `Checking current evidence...`; disable duplicate submit | Cancel is optional; retain context |
| Generated success | Validated synthesis | Generated label plus citations and limitations | Bounded follow-up |
| Deterministic success | Model not used | Deterministic label; same response anatomy | Bounded follow-up |
| Provider outage | Timeout, auth, breaker, rate limit | `The enhanced explanation is unavailable. Here is the evidence-based fallback.` | No credential request; optional retry when operator state permits |
| Budget exhausted | Hard spend stop | `Enhanced explanations are paused for this pilot. The evidence-based explanation is still available.` | Deterministic use only |
| Validation failure | Generated claims fail checks | Do not show failed output; show fallback and `Generated wording was not used because it could not be validated.` | Continue deterministically |
| Unsupported intent | No allowlisted route | Scope copy plus nearest supported actions | Choose supported action |
| One route ambiguity | Exactly two plausible routes | One constrained clarification | Choose one; no second clarification |
| Stale recommendation | Current inputs changed | Warning before answer: `This result is stale because your roadmap inputs changed.` | Reload recommendations or explain stale result with label |
| Stale evidence | Source exceeded applicable freshness | `Stale evidence` label; no current wording | Regenerate or use static permitted context |
| Conflict | Two validated claims disagree | Present both side by side; `The available evidence conflicts.` | Source/advisor check; no synthesis |
| Unknown | Field absent or unsupported | `Unknown from the available evidence.` | Named source or human check |
| Ambiguous mapping | Multiple skill candidates | Show raw mention and candidates only if useful | No aggregate or accepted mapping |
| Unmapped | No accepted canonical skill | `No reviewed mapping` | Preserve raw requirement |
| No reviewed course link | Canonical skill has no reviewed link | State exactly that | No deficiency inference |
| Evidence unavailable | Purged/withdrawn/unresolvable citation | Hide excerpt; retain non-content state | Regenerate from permitted evidence |
| Unsupported role | Title outside allowlist | Exact pilot scope message | Choose supported role |
| Posting input invalid | Type, encryption, size, pages, binary, malware/content check | Specific reason without echoing hostile content | Remove and replace |
| Posting origin clarification | Origin ambiguous | One constrained question | Answer once or reject |
| Posting rejected | LinkedIn, unresolved origin, bulk/workaround, unsupported scope | Refusal copy; no extraction | Submit different posting |
| Extracting | Valid submission accepted | Step indicator: `Checking file`, `Finding requirements`, `Validating evidence` | Delete/cancel when technically safe |
| Completed with gaps | Some items ambiguous/unmapped | Show accepted items and explicit gaps | Continue to comparison |
| Abstained | No supported requirement evidence | `No supported requirement evidence could be extracted.` | Check source or use role context |
| Active private result | Posting analysis complete | Expiry bar and `Delete now` always visible | Review or delete |
| Delete pending | User confirms deletion | Disable comparison and announce progress | Retry on failure |
| Deleted | Joint deletion succeeds | Terminal deletion state, no content | Analyze another |
| Expired | One-hour limit reached | Clear content and show terminal expiry state | Submit again |
| Deletion failed | Operation not confirmed | `Deletion could not be confirmed. The result is locked while we retry.` | Automatic/operator recovery; no content interaction |
| Offline/network loss | Request cannot reach service | Preserve local input only until user chooses retry; do not claim server deletion/completion | Retry or remove local input |

## 9. Wireframe-Level Layouts

### 9.1 Desktop: Stage 1 workspace

```text
+--------------------------------------------------------------------------+
| NTU Course Recommender                         Roadmap Modules Assistant...|
+--------------------------------------------------------------------------+
| Assistant                                                                |
| Explain current recommendations with their supporting evidence.          |
| [Recommendation help] [Role context] [Posting context]                   |
+--------------------------+-----------------------------------------------+
| Current context          | Conversation                                  |
| SC4023                   | You: Why was this recommended here?           |
| Year 4 Semester 1        |                                               |
| Career recommendation    | Answer                                        |
| [Back to roadmap]        | SC4023 was assigned to this open slot... [1]  |
|                          | [Deterministic recommendation] [Current]       |
| Suggested questions      |                                               |
| [Why this course?]       | Why                                           |
| [What prerequisites?]    | - It matched... [1]                           |
| [Compare selected]       | - Its prerequisite path... [2]                |
|                          |                                               |
|                          | Evidence (2) [Expand all]                      |
|                          | > [1] Current recommendation                   |
|                          | > [2] Course catalog                           |
|                          |                                               |
|                          | What this does not establish                   |
|                          | This does not confirm registration eligibility.|
|                          |                                               |
|                          | [Ask about this result________________] [Send]  |
+--------------------------+-----------------------------------------------+
```

Desktop uses a `17rem-21rem` context rail and flexible response column inside
the existing maximum width. The response column owns page scrolling; no
independent nested scroll until viewport height requires a sticky composer.

### 9.2 Desktop: posting declaration and review

```text
+--------------------------------------------------------------------------+
| Assistant > Posting context                                              |
| Private, one-posting analysis. No history is saved.                      |
+----------------------------------+---------------------------------------+
| 1. Declare the source            | 2. Add one posting                    |
| [ ] I may provide this posting   | [Paste text] [Upload file]            |
| ( ) Direct employer              |                                       |
| ( ) Approved provider            | [Posting text........................] |
| ( ) Other authorized source      | [....................................] |
| [ ] Not LinkedIn-derived         | 8,420 / configured limit              |
|                                  | Source reference (not fetched)         |
| Declaration is not a legal       | [....................................] |
| determination.                   |                                       |
|                                  |                       [Review posting] |
+----------------------------------+---------------------------------------+
```

After extraction, replace the input area with review. Keep the source
declaration summary, observed time, expiry, and delete action visible.

### 9.3 Desktop: item-level comparison

```text
+--------------------------------------------------------------------------+
| Graduate Software Engineer | Direct employer | Deletes at 15:30          |
| [Back to extraction review]                              [Delete now]      |
+--------------------------------------------------------------------------+
| Posting requirements (7)                                                |
|                                                                          |
| Python                                                     Required      |
| "Experience with Python..." [Posting evidence 1]                         |
| Mapped: Programming foundations | Alias | Mapper v1.0                    |
| Reviewed exposure: SC1003, introductory [Course evidence 2]              |
| Note: Course exposure does not establish mastery.                        |
|--------------------------------------------------------------------------|
| Kubernetes                                                  Preferred     |
| "Familiarity with Kubernetes..." [Posting evidence 3]                    |
| Unmapped                                                                 |
| No reviewed course link                                                  |
+--------------------------------------------------------------------------+
| No fit score or aggregate skills-gap summary is calculated.              |
+--------------------------------------------------------------------------+
```

### 9.4 Mobile

```text
+--------------------------------+
| < Roadmap        Assistant     |
| Recommendation help            |
| Context: SC4023, Y4 S1 [Change] |
+--------------------------------+
| Answer                         |
| SC4023 was assigned... [1]     |
| [Deterministic] [Current]      |
|                                |
| Why                            |
| - ... [1]                      |
|                                |
| > Evidence (2)                 |
| > Limitations                  |
|                                |
| [Ask about this result......]  |
| [Send]                         |
+--------------------------------+
```

At widths below `700px`:

- Stack the context rail above content as a collapsible `Current context`
  summary.
- Use a full-width mode selector with horizontal overflow and visible labels.
- Stack declaration and posting input; keep source declaration first.
- Use one item per row; never create a horizontally scrolling evidence table.
- Make the composer part of document flow unless sticky placement leaves at
  least 44px clear of browser and screen-reader controls.
- Keep `Delete now` visible near the expiry text, not in an overflow menu.
- All touch targets are at least `44px` by `44px`.
- Long titles, excerpts, IDs, and URLs wrap without clipping. Evidence excerpts
  use a maximum collapsed length with `Show full excerpt`.

## 10. Content Tokens and Component Inventory

### 10.1 Visual tokens

Reuse current CSS variables and derive new semantic aliases:

| Token | Proposed source | Use |
|---|---|---|
| `surface-page` | Existing app gradient/dark background | Page |
| `surface-panel` | `--header-bg` | Assistant cards and disclosures |
| `border-subtle` | `--panel-border` | Panels and dividers |
| `text-primary` | `--page-text` | Body |
| `text-heading` | `--heading-text` | Headings |
| `text-muted` | `--muted-text` | Metadata and limitations |
| `evidence-catalog` | `#0f7c8a` / dark cyan equivalent | Catalog label |
| `evidence-deterministic` | Existing `#38bdf8` family | Backend result label |
| `evidence-posting` | Existing rose family | Posting excerpt label |
| `evidence-mapped` | Existing violet family | Normalized inference |
| `state-warning` | Existing amber family | Stale, unclear, expiring |
| `state-danger` | Existing rose/red family | Rejection, delete, unavailable |

Do not rely on new colors until contrast is verified in both themes. Keep
border radii aligned with current `0.7rem`, `1rem`, `1.25rem`, and pill values.
Use existing `150-160ms` transitions and honor reduced motion.

### 10.2 Components

- `AssistantModeTabs`
- `AssistantContextBar`
- `IntentPromptChips`
- `AssistantComposer`
- `ResponseCard`
- `ResponseStatusLine`
- `ClaimClassBadge`
- `QualifierBadge`
- `CitationButton`
- `EvidenceDisclosure`
- `LimitationBlock`
- `FallbackNotice`
- `UnsupportedIntentPanel`
- `ConflictPair`
- `RoleScopeSelector`
- `PostingOriginDeclaration`
- `PostingTextInput`
- `PostingFileInput`
- `ExtractionProgress`
- `ExtractionReviewList`
- `RequirementEvidenceCard`
- `SkillMappingRow`
- `CourseExposureRow`
- `PrivateAnalysisExpiryBar`
- `DeleteAnalysisDialog`
- `TerminalDeletionState`

### 10.3 Controlled vocabulary

Use:

- `Current recommendation`, not `AI recommendation`.
- `Generated explanation`, not `AI fact`.
- `Planning readiness`, not `eligible`.
- `Reviewed course exposure`, not `skill gained` or `mastery`.
- `Posting evidence`, not `market truth`.
- `Role taxonomy context`, not `market demand`.
- `No reviewed course link`, not `skill gap`.
- `Unknown`, not `not required`.
- `Deterministic explanation`, not `basic mode`.
- `Enhanced explanation unavailable`, not `AI failed`.

## 11. Over-Trust Prevention

- Put evidence class labels adjacent to the claim, not only in a legend.
- Keep generated advice visually quieter than source evidence.
- Repeat the readiness/registration limitation on every applicable answer.
- Repeat exposure/mastery language on each course-exposure comparison, not only
  at page bottom.
- Show taxonomy version before taxonomy concepts and keep taxonomy cards
  separate from posting requirements.
- Never use celebratory success styling for posting/course matches.
- Never use red failure styling for unknown, unmapped, or no reviewed link.
- Avoid avatars, typing theatrics, confidence percentages, and human-like
  statements that imply authority.
- Do not auto-open generated links, images, or remote resources.
- Preserve conflicts side by side and prevent generated text from resolving
  them without evidence.

## 12. Keyboard and Screen-Reader Requirements

- Use semantic navigation, headings, forms, lists, buttons, radio groups,
  checkboxes, status regions, and dialogs. Do not use clickable `div` elements.
- Page title and `h1` identify the active assistant mode. Maintain sequential
  heading levels within responses and evidence details.
- Focus order follows mode selector, context, suggestions, response, evidence,
  composer. On contextual entry, focus the assistant heading, not the composer.
- New response completion moves no focus. Announce `Explanation ready` through
  a polite live region; the user then navigates to the response heading.
- Validation and refusal summaries use `role="alert"` only when immediate
  action is required. Loading and deletion progress use polite status updates.
- Citation buttons expose class and sequence. Expanded evidence returns focus
  to the citation button when collapsed.
- The one-clarification choice group has a `fieldset` and `legend`.
- Upload includes an accessible native file input, selected-file text, and
  explicit remove button.
- Modal delete confirmation traps focus, supports `Escape`, names the dialog,
  and returns focus to `Delete now` when cancelled.
- On confirmed deletion or expiry, focus the terminal state heading because the
  prior trigger and evidence have been removed.
- Tabs implement the ARIA tabs pattern only if panels switch in place;
  otherwise use ordinary navigation buttons. Arrow-key behavior must match the
  chosen semantic pattern.
- All actions work by keyboard alone. Visible focus uses the existing 3px
  accent outline in both themes.
- Status, modality, mapping, and freshness never depend on color alone.
- Test at 200% zoom and with text spacing overrides. No loss of content or
  function at 320 CSS px.
- Respect `prefers-reduced-motion`; no animated streaming or auto-scrolling.

## 13. Analytics Without Content

No event may contain prompts, answers, excerpts, posting text, filenames,
source references, student identifiers, course titles, URLs, credentials, or
raw payloads. Use opaque session/analysis IDs only within approved retention.

| Event | Allowed properties |
|---|---|
| `assistant_opened` | entry surface, released mode |
| `assistant_intent_submitted` | routed intent, entry type, entity count |
| `assistant_clarification_shown` | candidate intent codes |
| `assistant_response_completed` | intent, generated boolean, fallback reason, latency bucket, claim count, citation count |
| `assistant_unsupported_intent` | nearest supported action codes only |
| `evidence_detail_opened` | evidence class, state, ordinal |
| `role_context_opened` | canonical pilot role code, taxonomy version |
| `posting_declaration_completed` | origin enum, policy result |
| `posting_input_validated` | input type enum, size/page bucket, outcome code |
| `posting_extraction_completed` | terminal state, item counts by modality/mapping state, latency bucket |
| `posting_clarification_shown` | clarification category |
| `posting_comparison_opened` | accepted/ambiguous/unmapped/no-link counts |
| `private_analysis_deleted` | user/expiry/system reason, deletion outcome, duration bucket |
| `provider_fallback_served` | outage/budget/timeout/validation/circuit reason |
| `capability_unavailable` | capability code, kill-switch state |

Analytics must not reconstruct a posting or conversation from event sequences.
General logs follow the same content-free rule.

## 14. Usability Test Protocol

This is a proposed protocol, not measured evidence.

### 14.1 Participants and design

- At least 20 target NTU computing students in a moderated crossover.
- Evaluate unchanged recommendations alone versus recommendations plus the
  tested read-only mode.
- Evaluate `role_target` and `supplied_posting` independently; do not average.
- Include keyboard-only and screen-reader sessions. Include mobile sessions at
  320-390 CSS px and desktop sessions.
- Use synthetic or legally retained fixtures and predeclared task/rubric sets.

### 14.2 Core tasks

1. Explain why a course was assigned to a slot and identify its source.
2. Determine whether `ready` means registration eligibility.
3. Compare two current recommendations without choosing a universal best.
4. Explain why a slot was left open.
5. Identify a seeded catalog fact and its freshness limitation.
6. Distinguish reviewed course exposure from mastery.
7. Distinguish role taxonomy context from employer posting evidence.
8. Submit a permitted posting, complete origin declaration, and interpret one
   ambiguous or unmapped item.
9. Find exact evidence for a posting requirement.
10. Explain why no aggregate fit or gap score is shown.
11. Recognize provider fallback and state whether evidence authority changed.
12. Delete a private posting analysis and verify that no history remains.

### 14.3 Scored comprehension probes

- Which sentence is supported by a citation?
- Which content is generated rather than a source fact?
- Is stale/unknown evidence equivalent to absent/not required?
- Does course exposure establish mastery?
- Does planning readiness establish registration permission?
- Does taxonomy context describe this employer?
- Did fallback change the underlying recommendation?
- Can the deleted posting result be reopened?

### 14.4 Proposed continuation gates

Per mode:

- Task success improves by at least 10 percentage points.
- At least 80% distinguish employer evidence from taxonomy context.
- At least 80% answer each critical distinction correctly.
- Unsupported takeaways occur in no more than 5% of scored answers.
- Median task time worsens by no more than 20%.
- At least 70% rate the context useful for the decision.
- Any critical misconception repeated by two participants blocks progression
  until correction and retest.

Interview every participant who forms an unsupported takeaway. Report
confidence intervals, observed causes, assistive-technology defects, and mode
results separately.

## 15. Acceptance Criteria

### Information architecture and flow

- [ ] The current roadmap, recommendation, open-slot, module-detail, and
  supported-profile entry points lead to the correct bounded context.
- [ ] All six Stage 1 intents have explicit prompt, loading, success,
  clarification, fallback, limitation, and unsupported behavior.
- [ ] No UI route permits preference, completion, recommendation, ranking,
  readiness, prerequisite, or slot mutation.
- [ ] Stage 2 role and posting modes can release, fail, hide, and roll back
  independently.

### Evidence and trust

- [ ] Every factual span exposes a resolvable citation and visible evidence
  class, source/version, locator, and freshness state.
- [ ] Generated advice is never styled or labelled as evidence.
- [ ] Stale, conflicting, unknown, ambiguous, unmapped, unavailable, and no
  reviewed course-link states are distinct in text and behavior.
- [ ] Readiness answers always state that planning readiness is not
  registration eligibility.
- [ ] Course-skill answers always use exposure language and never mastery.
- [ ] Role context always states that taxonomy is not an employer requirement,
  live vacancy, current-demand, frequency, or trend source.
- [ ] Stage 2 contains no aggregate gap, fit, coverage, employability,
  missing-skills ranking, frequency, trend, or demand claim.

### Fallback and refusal

- [ ] Provider outage, timeout, validation failure, circuit open, missing
  configuration, and budget exhaustion preserve a complete deterministic
  answer for every supported Stage 1 intent.
- [ ] The UI never asks a user for an API key.
- [ ] Unsupported intents and titles provide exact scope and valid next
  actions without model-generated widening.
- [ ] LinkedIn-derived, ambiguous-origin, unsupported-file, bulk, and
  acquisition-workaround inputs fail closed with the specified neutral copy.

### Posting privacy and lifecycle

- [ ] Source declaration requires an allowed origin, right-to-provide
  confirmation, and non-LinkedIn confirmation with no preselection.
- [ ] Text and approved text-bearing PDF are the only input modes; no URL is
  fetched.
- [ ] Extraction review preserves exact evidence and modality and allows no
  user edit that would become employer evidence.
- [ ] At most one constrained clarification appears per posting.
- [ ] Active result, raw input, claims, citations, and rendered comparison
  share one visible expiry and delete together.
- [ ] Delete success and expiry remove all private content from the UI and
  provide no history, save, share, or export path.

### Responsive and accessibility

- [ ] Desktop, mobile, 200% zoom, long-content, light-theme, and dark-theme
  layouts preserve all labels, evidence, expiry, and actions.
- [ ] All pointer interactions have keyboard equivalents and visible focus.
- [ ] Screen readers receive mode, context, loading, completion, refusal,
  fallback, expiry, deletion, and error changes in a controlled order.
- [ ] Dialog focus, citation disclosure focus, and terminal deletion focus
  match Section 12.
- [ ] Color contrast, target size, reduced motion, and 320px reflow pass
  accessibility review.

### Analytics and evaluation

- [ ] Analytics capture only allowlisted enums, counts, booleans, versions,
  buckets, and opaque IDs; no user or source content is emitted.
- [ ] `role_target` and `supplied_posting` have separate usability results,
  defects, kill decisions, and continuation records.
- [ ] Over-trust comprehension tasks pass the predeclared gates before release.

## 16. Dependencies and Open Shape Decisions

Dependencies before implementation:

- Final typed assistant, claim, citation, extraction, expiry, and deletion
  contracts.
- Approved component-level contrast tokens for both themes.
- Reviewed canonical skill labels and course-exposure copy.
- Exact configured file size, page, character, and token limits.
- Controlled-user identity and tenant scope for Stage 2B.
- Deletion transaction and operator recovery behavior.
- Capability state endpoint for independent mode availability.

Open Shape decisions that do not broaden product scope:

1. Whether desktop evidence defaults to one expanded item or all collapsed.
2. Whether Stage 1 comparison selection happens entirely on the roadmap or in
   the assistant context rail.
3. Exact mobile placement of the non-sticky versus sticky composer after
   assistive-technology testing.
4. Exact timeout copy when extraction can still be deleted but has no result.

These decisions require prototype and accessibility testing. They do not confer
approval to implement, release, persist history, add source access, or alter
recommendation behavior.
