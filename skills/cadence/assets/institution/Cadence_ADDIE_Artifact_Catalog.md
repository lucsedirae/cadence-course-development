# Marine Corps ADDIE Artifact Catalog

A practical guide to all instructional documents produced during course development using the ADDIE framework.

## Quick Overview

The ADDIE framework has 5 phases. This catalog focuses on **Analysis, Design, and Development** — the phases where the actual course content is created.

| Phase | Purpose | Key Outputs | Time |
|-------|---------|------------|------|
| **Analysis** | Understand the training need and identify gaps | 1 comprehensive Analysis Summary Report | ~1-2 weeks |
| **Design** | Plan the learning outcomes and assessment | 1 comprehensive Course Design Document | ~1-2 weeks |
| **Development** | Create the actual course materials | 15+ documents (lessons, assessments, videos) | ~2-4 weeks |
| Implementation | Deliver the course and collect attendance | Attendance logs, delivery schedules | Ongoing |
| Evaluation | Measure whether training worked | Test scores, feedback surveys, performance data | After course |

---

## ANALYSIS PHASE: Understand the Need

The Analysis phase answers: *What is the problem, and what must people learn to solve it?*

All analysis work is consolidated into a single comprehensive document called the **Analysis Summary Report**.

### 1. **Analysis Summary Report**
*A unified document containing all analysis findings, recommendations, and source evaluation*

This single document integrates four core analysis functions into cohesive sections:

#### Section 1.1: Executive Summary & Training Needs Assessment
*Justifies why training is necessary and provides organizational context*

Contains:
- Executive summary of the performance problem
- Who is affected (target audience profile: rank, experience, specialty)
- Current performance level vs. desired level
- Why training is the right solution (vs. other interventions)
- Environmental constraints (facility, equipment, time available)
- Specific performance gaps that training must close
- Compliance or safety requirements
- Recommended training approach
- Time and resource requirements
- Expected impact/success measures

**Inputs:** Stakeholder interviews, performance data, operational requirements, input from instructors, facility managers, leadership

---

#### Section 1.2: Job Task Analysis (JTA)
*Defines exactly what trained people will do on the job*

Contains:
- Complete list of job duties and tasks (organized hierarchically)
- For each task: What conditions it's performed under (environment, equipment, time, stress)
- For each task: What "success" looks like (performance standards)
- Prerequisites: What skills/knowledge are needed before training
- Safety-critical steps and hazards
- Source citations (where these tasks come from in doctrine or operations)

**Example:** If training emergency shutdown, the JTA would specify:
- Task: "Perform electrical isolation"
- Conditions: "Without instructor, under high-stress simulation, within 30 seconds"
- Standard: "Zero safety violations, power verified at zero volts"
- Safety: "Electrical shock hazard—RED-level critical"

**Inputs:** Subject-matter experts, operational procedures, doctrine

---

#### Section 1.3: Doctrinal Synthesis & Source Material Evaluation
*Synthesizes relevant doctrine and evaluates source sufficiency*

**Part A: Doctrinal Summary & Procedures**
- Key paragraphs from MCDP/MCWP (Marine Corps doctrine) relevant to training
- How these principles apply to the training task
- Extracted procedures and standards aligned to JTA tasks
- All cited with source paragraph numbers and technical manual references

**Part B: Source Sufficiency Assessment**
- Inventory of available sources (doctrine, manuals, procedures, operational references)
- For each JTA task: How well the sources cover it
  - ✓ **COVERED** — Source fully explains procedure and standards
  - ⚠ **PARTIAL** — Source covers concept but lacks procedural detail
  - ✗ **GAP** — Information is entirely missing

**Examples of gaps:**
- Missing safety procedures
- Procedure steps not fully documented
- Performance standards unclear
- Equipment variations not addressed

**Critical:** We NEVER invent missing information. If a gap exists, we flag it and either get SME input or adjust the training scope.

**Inputs:** Supplied MCDP/MCWP extracts, technical manuals, available references, JTA tasks

---

#### Report Reviewers & Approvals

**Doctrinal SME:** Validates JTA tasks, doctrinal accuracy, source citations, gap severity  
**Training Sponsor:** Approves executive summary, needs assessment, resource plan  
**Learning Organization Leadership:** Confirms audience profile, environmental constraints, compliance  
**Approval Authority:** Signs off on entire Analysis Summary Report before Design Phase proceeds

---

### Analysis Phase Checkpoint
**Gate 1 Question:** Are we ready to start designing the course?
- ✓ Is the performance gap clear and well-documented?
- ✓ Are all job tasks well-defined with conditions and standards?
- ✓ Are critical information gaps identified and marked for resolution?
- ✓ Do we have adequate sources to teach this, or is a gap management plan in place?

If yes → Proceed to **Design Phase**. If no → Return to Analysis to resolve issues.

---

## DESIGN PHASE: Plan the Learning

The Design phase answers: *What should learners achieve, and how will we know they've achieved it?*

All design work is consolidated into a single comprehensive document called the **Course Design Document**.

### 1. **Course Design Document**
*A unified strategic blueprint for the entire course with integrated sections*

This single document integrates six core design functions into cohesive sections:

#### Section 2.1: Curriculum Map and Outline
*Shows how the course is organized and structured*

Contains:
- Module structure (how many modules, what each covers)
- Lesson-by-lesson breakdown (how each module breaks into lessons)
- Sequence and duration of each lesson
- How lessons connect and build on each other
- Prerequisites (what must learners know first)
- Visual flowchart showing the course flow

**Example:**
```
Module 1: Emergency Response Fundamentals (4 hours)
  ├─ Lesson 1.1: Recognizing Emergencies (1 hour)
  ├─ Lesson 1.2: Initial Response Procedures (1.5 hours)
  └─ Lesson 1.3: Communication Protocols (1.5 hours)

Module 2: Hands-On Response (3 hours)
  ├─ Lesson 2.1: Equipment Simulation (1.5 hours)
  └─ Lesson 2.2: Integrated Scenario Practice (1.5 hours)
```

**Inputs:** Analysis Summary Report, JTA tasks, time/resource constraints

---

#### Section 2.2: Learning Objectives Hierarchy
*Defines what learners will be able to do after training*

Contains:
- **Terminal Learning Objectives (TLOs):** The big goal learners must achieve
  - Format: *[Action Verb] [Condition] [Standard]*
  - Example: "**Perform** emergency shutdown **without assistance, under high-stress simulation** **within 30 seconds with zero safety violations**"

- **Enabling Learning Objectives (ELOs):** Smaller, prerequisite skills that build toward the TLO
  - Example for above TLO:
    - "**Identify** the 7-step shutdown sequence"
    - "**Understand** electrical isolation safety procedures"
    - "**Execute** electrical isolation without error"

- **Bloom's Taxonomy Alignment:** Each objective mapped to a cognitive level
  - Remember → Understand → Apply → Analyze → Evaluate → Create
  - Lower-level ELOs build up to higher-level TLOs

- **Source Traceability:** Every objective traces back to the Analysis Summary Report and doctrine
  - "This TLO comes from JTA Task 1.1; supported by TM 12.3.1"

**Inputs:** Analysis Summary Report, Performance standards, Bloom's Taxonomy

---

#### Section 2.3: Assessment Plan
*Defines how we'll measure whether learners learned*

Contains:
- **For each TLO:** What test or performance evaluation will measure it?
- **Summative Assessment** (the final test for mastery)
  - Hands-on Performance Evaluation Checklist (PEC) for skills
  - Written test or scenario for knowledge
- **Formative Assessment** (checkpoints during learning)
  - Quizzes, practice exercises, discussions
- **Objective-Assessment Matrix** showing what measures what
- **Grading and Scoring Criteria**

**Example Assessment Plan:**
| TLO | Type | How We'll Measure It | Success Criterion |
|-----|------|---------------------|-------------------|
| Perform shutdown within 30 sec | Summative | High-fidelity simulator PEC | All steps GO, zero safety violations |
| Identify 7-step sequence | Formative | Quiz on procedure steps | ≥80% correct |
| Understand electrical safety | Formative | Discussion + practice | Peer feedback + instructor observation |

**Inputs:** Learning Objectives Hierarchy, Performance standards

---

#### Section 2.4: Content Outline
*Lists what topics will be taught in each lesson*

Contains:
- Module-by-module organization
- For each lesson: Key concepts, supporting details, examples
- Topics organized in logical teaching sequence
- Links to learning objectives (which TLO/ELO does this content teach?)

**Example:**
```
Lesson 1.2: Shutdown Procedure Overview (1.5 hours)

Content Topics:
  ├─ The 7-step shutdown sequence (taught to address ELO 1.1)
  ├─ Electrical hazards and isolation (taught to address ELO 1.2)
  ├─ Performance standards and timing (taught to support TLO 1.0)
  └─ Real-world examples and scenarios

Related Learning Objectives:
  └─ TLO 1.0, ELO 1.1, ELO 1.2
```

**Inputs:** Curriculum Map, Learning Objectives Hierarchy, Source materials

---

#### Section 2.5: Instructional Strategy
*Explains HOW the course will be taught*

Contains:
- Overall teaching approach (lecture, hands-on, simulation, online, etc.)
- Rationale: Why this approach for this content?
- Delivery method for each lesson (classroom, distance, blended, simulator)
- Instructional techniques (discussion, demonstration, practice, role-play)
- Technology needed (projectors, simulators, video playback)
- Environment requirements (lab, classroom, outdoor range)
- Learner support (instructor feedback, peer learning, mentoring)

**Example:**
```
Lesson 1.2: Shutdown Procedure Overview

Instructional Approach: Blended
  ├─ Segment A (Conceptual): Classroom lecture + visual slides (10 min)
  ├─ Segment B (Safety Detail): Instructor demonstration + video + hands-on familiarization (15 min)
  └─ Segment C (Guided Practice): Learners practice on simulator with instructor feedback (10 min)

Rationale: Lecture introduces concepts, video shows procedure detail, simulator practice develops muscle memory
```

**Inputs:** Content Outline, Audience profile, Available resources

---

#### Section 2.6: Performance Standards & Success Criteria
*Specifies exactly what success looks like on the job*

Contains:
- For each JTA task: The measurable success criteria
- Accuracy standards (how correct must work be?)
- Speed standards (how fast must it be completed?)
- Safety thresholds (what hazards exist, what violations are unacceptable?)
- Environmental conditions (what the task looks like in real situations)
- Doctrinal source citations linking back to Analysis Summary Report

**Example:**
```
PERFORMANCE STANDARD: Emergency Shutdown Procedure

Task: Perform electrical isolation
Accuracy: All 7 steps executed correctly, in sequence, no errors on safety-critical steps
Speed: Completed within 30 seconds
Safety: Electrical power verified at zero volts before proceeding; any electrical violation = automatic failure
Conditions: Without assistance, under high-stress simulation
Source: TM 12.3.1 Section 3.2, MCDP 5 para 2.5.3
```

**Inputs:** Analysis Summary Report (JTA, Performance Standards), Doctrinal content, Operational requirements

---

#### Document Reviewers & Approvals

**Approval Authority:** Reviews entire Course Design Document for completeness and alignment  
**Doctrinal SME:** Validates objectives, assessment strategy, performance standards, doctrinal fidelity  
**Instructors:** Confirms curriculum map, instructional strategy, and practical feasibility  
**Assessment Specialist:** Validates assessment plan and objective-assessment alignment

**Synthesis Input:** This document synthesizes the Analysis Summary Report into actionable learning design, bridging analysis to development.

---

### Design Phase Checkpoint
**Gate 2 Question:** Is the learning design solid and ready for development?
- ✓ Are all learning objectives clear, measurable, and source-grounded?
- ✓ Does every TLO have a mapped assessment?
- ✓ Are assessments criterion-referenced (not just graded pass/fail)?
- ✓ Does content flow logically toward objectives?
- ✓ Is the instructional strategy appropriate for the audience and content?
- ✓ Are performance standards aligned to analysis findings?

If yes → Proceed to **Development Phase**. If no → Return to Design to refine.

---

## DEVELOPMENT PHASE: Build the Course

The Development phase answers: *What will learners actually see, read, do, and be tested on?*

This phase produces the most artifacts (15+), organized into four categories:

### Category 1: Instructional Materials

These are the documents and content learners encounter during training.

#### 1.1 **Lesson Plans**
*Day-by-day instruction scripts for instructors*

Each lesson plan contains:
- Learning objectives for that lesson
- Time allocation for each segment
- Instructional sequence: Introduction → Body → Closure
- Activities and learning experiences
- Resources needed (equipment, handouts, videos)
- Timing and pacing guidance
- Formative checks (how to know if learners are following)
- Remediation strategy (what to do if learners struggle)
- Transition to next lesson

**Example structure:**
```
Lesson 1.2: Shutdown Procedure Overview (1.5 hours)

INTRODUCTION (5 min)
  Attention grabber: Real-world emergency scenario
  State objective in learner-friendly language
  Explain relevance (why this matters for their job)

BODY
  Segment A – Conceptual Foundation (10 min): Lecture on 7-step sequence
  Segment B – Safety Deep Dive (15 min): Demonstration + video + hands-on familiarization  
  Segment C – Guided Practice (10 min): Learners practice on simulator with feedback

CLOSURE (5 min)
  Summarize key points
  Ask reflection question
  Preview next lesson

FORMATIVE ASSESSMENT
  Question check mid-lesson: "What is step 3?"
  Observation during practice: Instructor watches electrical isolation technique
  
REMEDIATION
  If learner struggles with electrical isolation → one-on-one demo + video replay
```

**Who uses it?** Instructors (primary) and Instructional Designers
**Key input?** Learning Objectives, Instructional Strategy, Assessment Plan

---

#### 1.2 **Instructor Guide & Lecture Notes**
*Comprehensive facilitation resource with detailed talking points and speaker notes*

Contains:

**Part A: Instructor Facilitation Guide**
- Module overview and learning context
- Detailed talking points for each segment
- Facilitation tips (how to handle discussions, manage time)
- Common student misconceptions and how to address them
- Answer keys for questions
- Troubleshooting guide
- Example responses to expect from learners
- Emphasis points (where to slow down and highlight critical content)
- References and appendices

**Part B: Detailed Lecture Notes & Speaker Notes**
- Detailed script for each lesson segment
- Key phrases and definitions to emphasize
- Transition cues between topics
- Emphasis markers (where to slow down, where to speed up)
- Pronunciation guides for technical terms
- Pause points (where to wait for learner response)

**Example:**
```
Segment B: Safety Deep Dive

TALKING POINTS & LECTURE SCRIPT
"Today, we're going to learn about electrical isolation. This is the #1 most important 
safety step in the shutdown procedure. You cannot skip it. Ever. Let me show you why..."

DEMONSTRATE
Show the electrical isolation procedure yourself first, narrating each action

COMMON MISCONCEPTIONS
Error: "I can skip step 3 if I'm in a hurry"
Fix: "Speed doesn't matter. Correct procedure is what keeps you safe. Electrical work 
done fast is electrical work done dangerous."

PRONUNCIATION GUIDE
- Electrical isolation: ih-LEK-tri-kul eye-so-LAY-shun

EMPHASIS MARKERS
- [EMPHASIS] "This is critical" - spoken with volume increase and deliberate pace
- [PAUSE 2 sec] - wait for learner processing time

EXPECTED LEARNER RESPONSE (to your question "Why is electrical isolation so important?")
"Because if we don't isolate the power, someone could get electrocuted"
(If they don't say this → provide mini-explanation and re-ask)
```

**Who uses it?** Instructors (primary), Subject-matter experts  
**Key input?** Lesson Plans, Assessment Plan, Content Outline

---

#### 1.3 **Student Course Book**
*Readable, reference-friendly course material for learners*

Contains:
- Clear narrative explanations of concepts
- Visual diagrams and illustrations
- Real-world examples and scenarios
- Key term glossary
- Self-check questions throughout
- Chapter summaries
- References and appendices
- Quick-reference cards or checklists

**Example chapter:**
```
CHAPTER 1: EMERGENCY SHUTDOWN PROCEDURES

1.1 Introduction
Why is shutdown important? When an emergency occurs, our first job is to safely secure 
the equipment. An improperly shut down system can injure the next person who works on it.

1.2 The Seven-Step Procedure
Step 1: Acknowledge alarm and announce shutdown decision
Step 2: Secure the surrounding area
Step 3: Perform electrical isolation ← MOST CRITICAL FOR SAFETY
...

1.3 Electrical Safety: What You Need to Know
Electrical hazards specific to this equipment include...
If you're unsure at any point, STOP and ask for help.

Self-Check Questions:
1. Name the 7 steps in order
2. Which step is most critical for safety?
Answers: [at end of chapter]
```

**Who uses it?** Learners (primary), Instructors (reference)
**Key input?** Content Outline, Lesson Plans, Learning Objectives

---

#### 1.4 **PowerPoint / Presentation Slides**
*Visual aids for classroom or distance delivery*

Contains:
- Title slides, module overview slides
- Content slides (text, graphics, animations)
- Real-world scenarios and examples
- Transition slides between topics
- Discussion prompts
- Visual diagrams and flowcharts
- Consistent branding and design

**Who uses it?** Instructors (primary) and Learners (visual reference)
**Key input?** Content Outline, Learning Objectives, Multimedia/UX standards

---

#### 1.5 **Curated Reading Package**
*Curated source materials for learners*

Contains:
- Extracted doctrine (MCDP/MCWP sections with citations)
- Technical procedure excerpts from manuals
- Case studies and historical examples
- Supplemental articles
- Annotated bibliography

**Purpose:** Gives learners direct access to authoritative sources without requiring them to hunt through entire manuals.

**Who uses it?** Learners (reference), Subject-matter experts (verification)
**Key input?** Source materials, Analysis Phase Doctrinal Summary

---

### Category 2: Assessment Instruments

These measure whether learners achieved the learning objectives.

#### 2.1 **Performance Evaluation Checklist (PEC)**
*Step-by-step scoring tool for hands-on skills*

A PEC is used when learners must **perform a procedure** (like emergency shutdown).

Contains:
- **Each critical step as a GO/NO-GO criterion**
  - GO = Performed correctly
  - NO-GO = Error or omission
  
- **Safety-critical items marked RED**
  - Any RED-level NO-GO = Automatic test failure
  
- **Important items marked YELLOW**
  - Multiple YELLOW NO-GOs = Test failure
  
- **Standard procedural items marked GREEN**

- **Scoring instructions for raters**

- **Rater guidance** (what to look for, common errors)

**Example PEC:**
```
PERFORMANCE EVALUATION CHECKLIST
Task: Emergency Shutdown Procedure
Learner: ____________ | Evaluator: ____________ | Date: _____

[RED-LEVEL SAFETY-CRITICAL — Any NO-GO = Automatic Failure]

Step 1: Acknowledge alarm and announce shutdown decision
  ☐ GO: Clear verbal announcement within 3 seconds
  ☐ NO-GO: No announcement or delays >3 seconds

Step 3: Perform electrical isolation [CRITICAL SAFETY]
  ☐ GO: Correct isolation procedure per TM 12.3.1 (breaker switch, power-down verification, lockout hasp, caution tag)
  ☐ NO-GO: Omits any sub-step or performs out of sequence

[YELLOW-LEVEL IMPORTANT]

Step 2: Secure surrounding area
  ☐ GO: Equipment and personnel moved to safe distance
  ☐ NO-GO: Area not secured before proceeding

[GREEN-LEVEL PROCEDURAL]

Procedure Sequencing
  ☐ GO: All steps performed in correct order (1→2→3→4→5→6→7)
  ☐ NO-GO: Any step performed out of sequence

Time Compliance
  ☐ GO: All steps completed within 30-second limit
  ☐ NO-GO: Exceeds 30-second limit

OVERALL RESULT
☐ GO (PASS) — Qualified to perform independently
☐ NO-GO (FAIL) — Requires additional training

Evaluator Notes: ________________________
```

**Who uses it?** Evaluators/Raters (primary), Instructors (training)
**Key input?** Learning Objectives, Performance Standards, JTA

---

#### 2.2 **Multiple-Choice Assessment Questions**
*Written knowledge tests*

Used when learners must **know or understand** something (not physically perform it).

Each question contains:
- **Stem (the question/scenario):** Clear, unambiguous problem
- **Correct answer:** The right response
- **Three distractors:** Wrong answers that are plausible (based on real misconceptions)
  - **Rationale for each wrong answer:** Explains WHY it's wrong and what misconception it addresses

**Example question:**
```
QUESTION: Emergency Isolation Verification

STEM:
"You are at step 3 (electrical isolation). You've switched the main breaker to OFF. 
The equipment's power indicator light goes dark. You now have a multi-meter ready. 
What should you do?"

A) Assume the power is off (the light went dark) and proceed to step 4
   RATIONALE: Wrong — the indicator light only shows that LIGHT has power, not the whole 
   system. Power could still be present. This tests whether learner confuses light status 
   with full de-energization.

B) **CORRECT:** Use the multi-meter to verify zero voltage before proceeding
   RATIONALE: Right — TM 12.3.1 mandates verification with a multi-meter. This is the 
   only reliable method.

C) Call a supervisor and ask permission to skip the multi-meter check
   RATIONALE: Wrong — safety procedures are never negotiable, even with authority approval. 
   Tests whether learner believes rank/authority can override safety.

D) Use a piece of wet paper to test if there's electricity
   RATIONALE: Wrong — this is dangerous and unreliable. Tests whether learner uses proper 
   testing methods (multi-meter, not improvised).

Bloom's Level: Apply (decision-making, not rote recall)
Linked Objective: ELO 1.3 (Execute electrical isolation correctly)
Source: TM 12.3.1 Section 4.1
```

**Who uses it?** Learners (answer), Instructors (grade), Assessment specialists (validate)
**Key input?** Learning Objectives, Assessment Plan, Bloom's Taxonomy

---

#### 2.3 **Scenario-Based Essay Assessment Items**
*Real-world decision-making scenarios*

Used when learners must **make judgments** or **decide on actions** in complex situations.

Contains:
- **Realistic scenario/context setup**
- **Decision point or problem statement**
- **Multiple response options** with analysis:
  - Correct responses (with reasoning)
  - Incorrect responses (with analysis of misconception)
- **Optional branching scenarios** (if you choose X, what happens next?)
- **Scoring rubric** (how to grade)

**Example scenario:**
```
SCENARIO: "You're halfway through emergency shutdown (at step 4). A facility-wide alarm 
sounds—actual emergency elsewhere in the building. Your supervisor appears and says, 
'Leave it. We need you over there now.' What do you do?"

CORRECT RESPONSE:
"I pause the shutdown, complete steps 5–7 (electrical verification, documentation, hand-off) 
to secure the equipment. This takes ~3 more minutes. Then I report to the emergency."

Reasoning: Leaving partially de-energized equipment unsecured is a safety and legal liability. 
The 3-minute investment to complete isolation is worth the risk mitigation.
Source: TM 12.3.1 Sections 1, 6, 7

INCORRECT RESPONSE A:
"I leave the equipment as-is and run to the emergency."

Misconception Being Tested: Learner believes operational urgency overrides safety procedure
Feedback: "I understand the urgency, but leaving a partially de-energized system is a hazard 
for the next person. Safety doesn't take a back seat to emergencies."

[Additional scenarios, follow-up branching, scoring rubric...]
```

**Who uses it?** Learners (work through), Instructors (grade and discuss), Assessment specialists (validate)
**Key input?** Learning Objectives, Performance Standards, Real-world duty scenarios

---

#### 2.4 **Answer Key**
*Correct answers with explanations*

Contains:
- Question-by-question answers
- For MC questions: Distractor explanation (why each wrong answer is wrong)
- For PECs: What correct performance looks like
- Scoring guide (how many right = passing score)
- Passing threshold and failure remediation paths

**Who uses it?** Instructors (grading), Subject-matter experts (validation)
**Key input?** Assessment instruments above

---

#### 2.5 **Assessment Rubric**
*Detailed scoring guide for complex assignments*

Contains:
- **Performance levels:** Unsatisfactory, Developing, Proficient, Advanced
- **Criteria for each level:** What does unsatisfactory look like vs. proficient?
- **Point scale:** How many points for each level
- **Alignment to objectives:** Which TLO/ELO does each criterion measure

**Example (for a practical exercise):**
```
ASSESSMENT RUBRIC: Shutdown Procedure

| Level | Procedure Accuracy | Safety Awareness | Time Compliance | Overall Score |
|-------|--------------------|------------------|-----------------|---|
| Advanced (4 pts) | All 7 steps correct, performed smoothly | Exceeds safety requirements, proactive hazard identification | Completes in <25 sec | 4/4 |
| Proficient (3 pts) | All 7 steps correct, minor hesitation | Meets all safety requirements | Completes in 25–30 sec | 3/4 |
| Developing (2 pts) | 6 of 7 steps correct, significant hesitation | Meets most safety requirements, one oversight | Completes in 30–35 sec | 2/4 |
| Unsatisfactory (1 pt) | <6 steps correct or major sequence error | Misses critical safety requirement | >35 sec or incomplete | 1/4 |

Passing Score: 3/4 (Proficient or Advanced)
```

**Who uses it?** Instructors (grading), Learners (self-assessment), Assessment specialists (validation)
**Key input?** Learning Objectives, Performance Standards

---

### Category 3: Multimedia Assets

These are scripts and specifications for video, animation, and graphics.

#### 3.1 **Two-Column AV Script (Video Script)**
*Synchronizes audio narration with visual content*

Contains:
- **Timing (in seconds)** for each segment
- **Video/Visual Column:** Shot descriptions, graphics, on-screen text, transitions, camera movements
- **Audio/Narration Column:** Dialogue, narration script, sound effects cues, music cues
- **Learning objective(s) addressed**
- **Source citations**

**Example script segment:**
```
| TIME | VISUAL COLUMN | AUDIO COLUMN |
|------|---------------|--------------|
| 0–5 sec | Wide shot: Equipment with red alarm flashing | NARRATOR: "When an emergency occurs, your task is to safely shut down the equipment. We'll walk through this step-by-step. First—electrical isolation." |
| 5–15 sec | Close-up: Main breaker panel with label "STEP 3: ELECTRICAL ISOLATION" | NARRATOR: "Step 3 is electrical isolation. This is NOT optional. Move to the main breaker and before you flip it, verify that no one is touching the equipment." |
| 25–35 sec | Animation: Breaker flipping to OFF position. Power light dims. SOUND: Click (breaker mechanism) | NARRATOR: "You'll hear a click. The power light goes dark. BUT—a dark light does NOT mean the power is isolated. There could still be residual energy. Never assume. Always verify." |
| 50–65 sec | Close-up of multi-meter probes placed on equipment test points. Display shows "0.0V" | NARRATOR: "The multi-meter reads zero volts. That means the power is isolated. You are now safe to proceed." |
```

**Who uses it?** Video producers (primary), Instructors (review)
**Key input?** Learning Objectives, Storyboard, Instructional Strategy

---

#### 3.2 **Storyboard (Panel-by-Panel Visual Breakdown)**
*Visual plan for video/animation production*

Contains:
- **Panel-by-panel breakdown** (like a comic strip)
- **Each panel shows:** Frame description, what's happening visually, narration/dialogue for that moment
- **Visual style guide:** Fonts, colors, graphics standards
- **Animation/transition notes**
- **Timing for each panel**

**Example:**
```
PANEL 1 (0–5 sec): Scene Setup
[VISUAL]: Wide shot of emergency equipment with red alarm flashing. Facility background.
VISUAL NOTES: Equipment labeled clearly; alarm light prominent in upper right
NARRATION: "When an emergency occurs, your task is to safely shut down the equipment..."

PANEL 2 (5–15 sec): Main Breaker Close-up
[VISUAL]: Close-up of breaker panel. Rater's hand approaching the breaker.
VISUAL NOTES: Breaker labeled clearly; well-lit and in focus
TEXT OVERLAY: "STEP 3: ELECTRICAL ISOLATION"
NARRATION: "Step 3 is electrical isolation. Before you flip the breaker, verify that no one is touching the equipment."

[... additional panels ...]
```

**Who uses it?** Video/graphic designers (primary), Subject-matter experts (review)
**Key input?** AV Script, Visual style guide

---

#### 3.3 **Audio Script**
*Full narration with detailed performance notes*

Contains:
- Full narration text (word-for-word what narrator will read)
- **Pronunciation guide** for technical terms
- **Pacing notes** (where to slow down, where to speed up)
- **Emphasis markers** (stress important words)
- **Pause points** (where to wait for listener response)
- **Background music and sound effect cues**

**Example:**
```
AUDIO SCRIPT: Electrical Isolation Procedure (2 minutes)

[0–5 sec]
NARRATOR (calm, authoritative tone):
"When an emergency occurs, your immediate task is to safely shut down the equipment. 
We'll walk through this procedure step-by-step. [PAUSE 2 sec] First—electrical isolation, 
the single most critical safety step."

[5–15 sec]
NARRATOR:
"Step 3 is electrical isolation. [PAUSE 1 sec] Before you do anything else, you must 
de-energize the equipment. [PAUSE 1 sec] Move to the main breaker. [PAUSE 1 sec] 
Before you flip the breaker, look around. Is anyone touching the equipment? 
[PAUSE 2 sec — allow audience to check] Good."

[50–65 sec]
NARRATOR:
"The multi-meter reads zero volts. [EMPHASIS] Zero. Volts. [PAUSE 1 sec] 
That means the power is isolated."

PRONUNCIATION GUIDE:
- Multi-meter: MUL-tee-MEE-tur
- Residual: reh-ZID-oo-uhl
- De-energize: dee-EN-ur-jyz

PACING NOTES:
- Overall: 120 words per minute (allows for natural pauses)
- Emphasis words: Spoken with slight volume increase
- Pauses: 1–2 seconds at key decision points
```

**Who uses it?** Voice actors/narrators (primary), Audio engineers (production)
**Key input?** AV Script, Learning Objectives

---

#### 3.4 **Graphics and Illustrations Specifications**
*Detailed requirements for diagrams, charts, and images*

Contains:
- **Diagram specifications:** Technical drawings, labels, dimensions
- **Chart specifications:** Data visualizations, colors, scales
- **Icon library reference**
- **Visual style guide:** Fonts, color palette, layout standards
- **Accessibility requirements:** Alt text, contrast ratios, captioning

**Example:**
```
DIAGRAM 1: Main Breaker Panel Anatomy

Specification:
  ├─ Size: 8" × 10" (for course book)
  ├─ Medium: Vector graphics (scalable, not raster)
  ├─ Perspective: Front view, slightly angled (isometric)
  ├─ Labels: Identify breaker handle, power indicator light, isolation test points
  ├─ Color: Use facility standard colors (red for hazard, green for safe)
  └─ Accessibility: High-contrast labels, alt text: "Main breaker panel with three labeled components: breaker handle (top left), power indicator light (top right), isolation test points (bottom center)"

CHART 1: Seven-Step Shutdown Flowchart

Specification:
  ├─ Size: Full-page or half-page (depending on course book layout)
  ├─ Style: Box-and-arrow flowchart
  ├─ Sequence: Seven boxes in order (Step 1 → 2 → 3 ... → 7)
  ├─ Color coding: RED for safety-critical steps, YELLOW for important, GREEN for standard
  ├─ Font: Arial 12pt, bold for step numbers
  └─ Accessibility: Alt text provided for entire flowchart
```

**Who uses it?** Graphic designers (primary), Subject-matter experts (review)
**Key input?** Content Outline, Visual style guide, Doctrinal content

---

#### 3.5 **Multimedia Asset Inventory**
*Tracking sheet for all video, audio, graphics, and animations*

Contains:
- Asset ID (unique identifier)
- Type (Video, Audio, Graphic, Animation)
- File name and location
- Format and technical specifications
- Learning objective(s) it addresses
- Current status (Draft, Final, Approved)
- Production completion date

**Example:**
```
MULTIMEDIA ASSET INVENTORY

| Asset ID | Type | File Name | Format | Objectives | Status | Date |
|----------|------|-----------|--------|------------|--------|------|
| VID-001 | Video | Electrical_Isolation_Procedure.mp4 | MP4, 1080p, 2 min | ELO 1.2, ELO 1.3 | Final | 9/15 |
| AUD-001 | Audio | Electrical_Isolation_Narration.wav | WAV, 48kHz stereo | ELO 1.2, ELO 1.3 | Final | 9/14 |
| GRA-001 | Graphic | Breaker_Panel_Diagram.ai | Vector (Adobe Illustrator) | ELO 1.1 | Draft | 9/10 |
| GRA-002 | Graphic | Shutdown_Flowchart.pdf | PDF | ELO 1.1 | Approved | 9/13 |
| ANI-001 | Animation | Power_Light_Dimming.mp4 | MP4, 1080p, 5 sec | ELO 1.2 | Final | 9/15 |

[... more assets ...]
```

**Who uses it?** Project manager (primary), Production team (tracking), Subject-matter experts (verification)
**Key input?** AV Scripts, Storyboards, Graphics Specifications

---

### Category 4: Live Instruction Components

Supporting materials for classroom or virtual instruction.

#### 4.1 **Discussion Guide**
*Facilitation guide for group discussions*

Contains:
- Discussion topic/prompt
- Facilitator notes (what to look for, how to guide conversation)
- Expected student responses (what should they say?)
- Follow-up questions (how to deepen thinking)
- Common misconceptions to address
- Time allocation

**Example:**
```
DISCUSSION TOPIC: "What could go wrong if we skip electrical isolation?"

FACILITATOR NOTES:
This discussion tests whether learners understand WHY electrical isolation is critical, 
not just HOW to do it.

EXPECTED STUDENT RESPONSES:
- "Someone could get electrocuted"
- "The next person working on the equipment could be shocked"
- "Residual energy could cause injury"

FOLLOW-UP QUESTIONS:
- "Why do you think residual energy is dangerous?"
- "How would you verify that power is really isolated?"

COMMON MISCONCEPTIONS:
Misconception: "If the power light is off, the power is definitely off"
Fix: "The power light only shows that LIGHT has power, not the entire system. 
We must use a multi-meter to be sure."

TIME ALLOCATION: 10 minutes
```

**Who uses it?** Instructors (primary), Subject-matter experts (review)
**Key input?** Learning Objectives, Lesson Plans

---

#### 4.2 **Practical Exercise Workbook**
*Hands-on activities for learners to practice skills*

Contains (for each exercise):
- Learning objective(s) addressed
- Scenario or context
- Step-by-step procedures
- Expected output/result
- Student worksheet (space to write, draw, record results)
- Solution key (for instructors)

**Example exercise:**
```
EXERCISE 1: Identify Electrical Isolation Steps

Learning Objective: ELO 1.1 (Identify the 7-step shutdown sequence)

SCENARIO:
You're responding to an equipment emergency. Your supervisor tells you to shut down 
the system safely. Walk through the shutdown procedure.

TASK:
Write the 7 steps in order. For each step, note what you're checking or doing.

STUDENT WORKSHEET:
Step 1: ____________________________
Step 2: ____________________________
Step 3: ____________________________ ← Most critical for safety
Step 4: ____________________________
Step 5: ____________________________
Step 6: ____________________________
Step 7: ____________________________

EXPECTED OUTPUT:
(See answer key below)

SOLUTION KEY (for instructor):
Step 1: Acknowledge alarm, announce shutdown
Step 2: Secure surrounding area (equipment, personnel to safe distance)
Step 3: Perform electrical isolation (breaker OFF, verify light off)
Step 4: Drain residual energy
Step 5: Verify isolation with multi-meter (read 0.0V)
Step 6: Apply lock-out hasp
Step 7: Document shutdown and hand-off
```

**Who uses it?** Learners (primary), Instructors (guide and grade)
**Key input?** Learning Objectives, Performance Standards, Lesson Plans

---

#### 4.3 **Case Study Materials**
*Real-world problems for small-group analysis*

Contains (for each case):
- Situation description (background, context)
- Problem statement (what's the issue?)
- Analysis questions (what should they think about?)
- Decision points (what would you do?)
- Facilitator debrief notes (what's the lesson?)
- Learning objectives addressed

**Example:**
```
CASE STUDY 1: The Rushed Shutdown

SITUATION:
Marine A is conducting emergency shutdown of the power system. They've completed steps 1–2. 
They're now at step 3 (electrical isolation). Their supervisor appears and says, 
"We don't have time for this. Just hurry up and shut it down. We need you at the briefing."

PROBLEM STATEMENT:
Operational pressure is pushing Marine A to skip or rush critical safety procedures. 
What should they do?

ANALYSIS QUESTIONS:
1. Why is electrical isolation step 3 (not step 1)?
2. What safety risks does rushing this step create?
3. What should Marine A say to their supervisor?

EXPECTED DECISION:
Marine A should: Calmly but firmly continue the proper procedure. Safety procedures 
are non-negotiable, even under time pressure.

FACILITATOR DEBRIEF:
This case highlights a common real-world scenario: operational urgency vs. safety. 
The learning point: Safety is always the priority. Taking 3 extra minutes to do 
electrical isolation correctly is worth it—it prevents injuries and liability.

LEARNING OBJECTIVES ADDRESSED:
ELO X.X (Evaluate competing priorities; Evaluate level)
ELO Y.Y (Defend safety-critical procedures)
```

**Who uses it?** Instructors (facilitate discussion), Learners (analyze)
**Key input?** Real-world duty scenarios, Learning Objectives

---

#### 4.4 **Simulation Event Script**
*Guidance for hands-on scenario simulations*

Contains:
- Event title and duration
- Learning objectives
- Scenario setup and conditions
- Role-player instructions (if using role-play)
- Facilitation/observation points (what to watch for)
- Expected learner actions
- Grading/assessment method
- Debrief talking points

**Example:**
```
SIMULATION EVENT: High-Fidelity Emergency Shutdown

Duration: 30 minutes (20 min simulation + 10 min debrief)

Learning Objectives:
  ├─ TLO 1.0: Perform emergency shutdown within 30 sec with zero safety violations
  └─ ELO 1.3: Execute electrical isolation correctly under pressure

Scenario Setup:
  ├─ Equipment: Full high-fidelity simulator
  ├─ Condition: Facility-wide alarm (audio and visual stressors)
  ├─ Time Limit: 30 seconds to complete shutdown
  └─ Observer: Instructor with PEC checklist

Expected Learner Actions:
  1. Responds to alarm calmly (doesn't panic)
  2. Announces "Shutdown initiated"
  3. Moves systematically through 7 steps
  4. Pauses slightly longer at electrical isolation (shows deliberate technique)
  5. Completes documentation
  6. Reports "Shutdown complete" within time limit

Grading:
  ├─ Criterion-Referenced: All steps GO on PEC = PASS
  ├─ RED-level failures = automatic FAIL
  └─ YELLOW-level failures = <2 acceptable

Debrief Talking Points:
  ├─ "I noticed you stayed calm under the alarm. That's crucial."
  ├─ "Your electrical isolation was careful and deliberate. Perfect."
  ├─ "Here's where you hesitated—that's normal. With practice, it becomes automatic."
  └─ "You're ready for real-world deployment. Any questions?"
```

**Who uses it?** Instructors (facilitate), Subject-matter experts (design and review)
**Key input?** Learning Objectives, PEC, Performance Standards

---

### Category 5: Compilation and Audit

Documentation proving the course was built correctly.

#### 5.1 **Development Audit Trail**
*Complete history of how the course was created and reviewed*

Contains:
- **Artifact Version History:** Every version of every document, with dates
- **Revision Change Log:** What changed and why in each version
- **Reviewer Dispositions:** Who reviewed it, what they approved/asked for
- **Source Citation Verification:** Checklist confirming every fact is sourced
- **Quality Assurance Sign-Off:** Approval from Doctrinal SME, Multimedia/UX, Editorial

**Example:**
```
DEVELOPMENT AUDIT TRAIL

Artifact: Lesson Plan 1.2 (Shutdown Procedure Overview)
  ├─ Version 1.0: Submitted Sept 15 (first draft)
  ├─ Version 1.1: Submitted Sept 17 (revisions from Doctrinal SME review)
  │    ├─ Change: Generalized voltage range in Segment A
  │    ├─ Change: Added video reference to TM 12.3.1 supplement
  │    └─ Reviewer: Dr. Jane Smith (Doctrinal SME) — Approved Sept 17
  ├─ Version 1.2: Submitted Sept 18 (revisions from Multimedia/UX review)
  │    ├─ Change: Reformatted segment timing for clarity
  │    └─ Reviewer: Tom Garcia (Multimedia/UX) — Approved Sept 18
  └─ Final Version: 1.2 (Approved Sept 19)

SOURCE VERIFICATION CHECKLIST
  ✓ Procedure matches TM 12.3.1 Section 3.2
  ✓ Safety points match Safety Manual Section 2.3
  ✓ Performance standards match MCDP 5 para 2.5.3
  ✓ Video reference matches TM 12.3.1 supplement catalog
  → All critical facts sourced. No invented content.
```

**Who uses it?** Quality assurance, Compliance verification, Subject-matter experts
**Key input?** All Development artifacts, Review feedback

---

#### 5.2 **Objective-Content-Assessment Alignment Matrix**
*Proof that every learning objective is measured and taught*

Contains (one row per objective):
- TLO/ELO ID and description
- Bloom's Level
- Assessment items that measure it (which PEC steps? which questions?)
- Content elements that teach it (which lessons? which materials?)
- Source citation

**Example:**
```
ALIGNMENT MATRIX: TLO/ELO → Assessment → Content

| TLO/ELO ID | Description | Bloom's | Assessment Items | Content Elements | Source |
|---|---|---|---|---|---|
| TLO 1.0 | Perform emergency shutdown within 30 sec with zero safety violations | Apply | Summative PEC "Emergency Shutdown" (high-fidelity sim) | Lesson 1.2 (proc. overview), Lesson 1.3 (safety deep dive), Lesson 2.2 (high-fidelity practice) | TM 12.3.1, MCDP 5 |
| ELO 1.1 | Identify the 7-step shutdown sequence | Remember | Formative Quiz Q1–Q3 | Lesson 1.1 (intro), Lesson 1.2 Segment A (lecture), Course Book Ch 1.2 | TM 12.3.1 Sec 3.2 |
| ELO 1.2 | Understand electrical safety & isolation | Understand | Formative Scenario Q4–Q5, Summative PEC Steps 3, 5 | Lesson 1.3 (safety deep dive), AV Script (safety video), Reading Package | Safety Manual 2.3, TM 12.3.1 Sec 4.1 |
| ELO 1.3 | Execute electrical isolation correctly | Apply | Summative PEC Step 3 (GO/NO-GO) | Lesson 1.2 Segment B (demo), Lesson 1.4 (guided sim), Lesson 2.2 (high-fidelity) | TM 12.3.1 Sec 3.3 |

Verification: ✓ Every TLO has ≥1 summative assessment
           ✓ Every ELO has ≥1 formative assessment
           ✓ Every assessment maps to ≥1 objective
           ✓ Every objective has content that teaches it
```

**Who uses it?** Quality assurance, Course reviewers, Subject-matter experts
**Key input?** All Development artifacts

---

#### 5.3 **Content Development Checklist**
*Final verification before the course is ready*

Contains (with sign-off boxes):
- ✓ Analysis Phase artifacts completed
- ✓ Design Phase artifacts completed
- ✓ Development artifacts completed (all 15+)
- ✓ Quality reviews completed (three pillars)
- ✓ Gaps documented (if any)
- ✓ Authorizations obtained
- ✓ Ready for Implementation

**Who uses it?** Project manager, Approval Authority
**Key input?** All artifacts, Audit trail, Reviews

---

### Development Phase Checkpoint
**Gate 3 Question:** Is the course ready to teach?
- ✓ All instructional materials are complete and reviewed
- ✓ All assessments are valid and criterion-referenced
- ✓ All multimedia scripts/storyboards are approved
- ✓ Multi-pillar critique is complete (three pillars approved)
- ✓ Audit trail is complete (all sources verified, gaps documented)
- ✓ Human authorization obtained

If yes → Course is **APPROVED FOR IMPLEMENTATION**. If no → Return to Development to complete work.

---

## Quick Reference: Document Summary Table

| Phase | Document | Primary Purpose | Sections | Length | Audience |
|-------|----------|-----------------|----------|--------|----------|
| **ANALYSIS** | Analysis Summary Report | Unified analysis of training need, tasks, sources, doctrine | Executive Summary & Needs Assessment, JTA, Doctrinal Synthesis & Source Evaluation | 20–40 pg | Leadership, Instructional designers, SMEs |
| **DESIGN** | Course Design Document | Strategic blueprint for course architecture and outcomes | Curriculum Map, Learning Objectives, Assessment Plan, Content Outline, Instructional Strategy, Performance Standards | 30–50 pg | Instructional designers, Subject-matter experts, Instructors |
| **DEVELOPMENT** | Lesson Plans | Script daily instruction | 3–5 pg/lesson | Instructors |
| | Instructor Guide & Lecture Notes | Facilitation + detailed talking points | 30–50 pg | Instructors |
| | Course Book | Student reference | 50–100 pg | Learners |
| | PowerPoint | Classroom visuals | 30–60 slides | Instructors, Learners |
| | Reading Package | Curated sources | 20–40 pg | Learners |
| | Lecture Notes | Speaker notes | 10–20 pg | Instructors |
| | PEC | Hands-on assessment | 2–5 pg | Evaluators |
| | MC Questions | Knowledge test | 20–50 questions | Learners |
| | Scenario Assessment | Decision-making test | 5–10 scenarios | Learners |
| | Answer Key | Correct answers | 5–10 pg | Instructors |
| | Assessment Rubric | Scoring guide | 2–3 pg | Instructors, Learners |
| | AV Script | Video production guide | 5–10 pg | Video producers |
| | Storyboard | Visual breakdown | 10–20 panels | Graphic designers |
| | Audio Script | Narration guide | 2–3 pg | Voice actors |
| | Graphics Specs | Design requirements | 5–10 pg | Graphic designers |
| | MM Inventory | Asset tracking | 2–3 pg | Project manager |
| | Discussion Guide | Facilitate group learning | 2–3 pg/discussion | Instructors |
| | Practical Exercises | Hands-on practice | 3–5 pg/exercise | Learners |
| | Case Studies | Problem analysis | 3–5 pg/case | Instructors, Learners |
| | Simulation Script | Scenario facilitation | 2–5 pg | Instructors |
| | Audit Trail | Documentation record | 5–10 pg | Quality assurance |
| | Traceability Matrix | Objective mapping | 2–3 pg | Quality assurance |
| | Development Checklist | Final verification | 1 pg | Project manager |

---

## Key Principles for Hackathon Implementation

1. **Traceability First**: Every artifact links to the analysis (where does this come from?) and to assessment (how will we know learners learned it?).

2. **Source Control**: Every fact, procedure, and safety control must cite its source doctrine or manual. No invented content.

3. **Gap Flagging**: Missing information is documented, severity-rated, and escalated. The system should halt on critical gaps.

4. **Multi-Pillar Review**: Doctrinal SME, Multimedia/UX, and Editorial/Standards each validate independently. Their critiques create an audit trail.

5. **Criterion-Referenced Assessments**: Every assessment measures specific, observable learning objectives. Not "Did they learn?" but "Can they perform this specific task to this specific standard?"

6. **Production-Ready Artifacts**: AV scripts, storyboards, and graphics specs are detailed enough for contractors/vendors to execute without constant designer involvement.

---

**This catalog is your blueprint for building a course development system that is auditable, traceable, and grounded in doctrine. Use it to guide your hackathon prototype.**

│   ├── Training_Needs_Analysis_Report.md
│   │   ├── Executive Summary
│   │   ├── Training Gap Assessment
│   │   ├── Stakeholder Input Summary
│   │   └── Recommendation
│   │
│   ├── Job_Task_Analysis.md
│   │   ├── Job Description
│   │   ├── Tasks Inventory
│   │   ├── Task Conditions and Standards
│   │   ├── Knowledge/Skills/Abilities Required
│   │   └── Environmental/Safety Factors
│   │
│   ├── Source_Material_Evaluation.md
│   │   ├── Doctrine References Identified
│   │   ├── Technical Manual Excerpts
│   │   ├── Sufficiency Assessment
│   │   ├── Information Gaps Flagged
│   │   └── Critical Safety/Procedural Gaps
│   │
│   ├── Doctrinal_Summary_Report.md
│   │   ├── Relevant MCDP/MCWP Paragraphs
│   │   ├── Key Doctrinal Principles
│   │   ├── Application to Training Context
│   │   └── Source Citations
│   │
│   └── Stakeholder_Requirements_Document.md
│       ├── Learning Organization Needs
│       ├── Target Audience Profile
│       ├── Environmental Constraints
│       └── Performance Gap Description
│
├── DESIGN_PHASE/
│   ├── Curriculum_Map_and_Outline.md
│   │   ├── Course Structure Overview
│   │   ├── Module-Level Organization
│   │   ├── Lesson Sequence and Duration
│   │   ├── Content Flowchart
│   │   └── Prerequisite Dependencies
│   │
│   ├── Learning_Objectives_Hierarchy.md
│   │   ├── Terminal Learning Objectives (TLOs)
│   │   │   └── Objective: [Action Verb + Condition + Standard]
│   │   ├── Enabling Learning Objectives (ELOs)
│   │   │   └── Objective: [Action Verb + Condition + Standard]
│   │   ├── Bloom's Taxonomy Alignment
│   │   │   ├── Remember Level
│   │   │   ├── Understand Level
│   │   │   ├── Apply Level
│   │   │   ├── Analyze Level
│   │   │   ├── Evaluate Level
│   │   │   └── Create Level
│   │   └── Source Traceability (TLO/ELO to Doctrine/JTA)
│   │
│   ├── Assessment_Plan.md
│   │   ├── Assessment Strategy Overview
│   │   ├── Formative Assessment Methods
│   │   ├── Summative Assessment Methods
│   │   ├── Performance Standards
│   │   ├── Grading/Scoring Scheme
│   │   └── Objective-Assessment Matrix (Traceability)
│   │
│   ├── Content_Outline.md
│   │   ├── Module 1: [Title]
│   │   │   ├── Lesson 1.1: [Title]
│   │   │   │   ├── Key Concepts
│   │   │   │   ├── Supporting Details
│   │   │   │   ├── Examples/Scenarios
│   │   │   │   └── Linked Objectives (TLOs/ELOs)
│   │   │   └── Lesson 1.2: [Title]
│   │   └── Module 2: [Title]
│   │
│   ├── Instructional_Strategy_Document.md
│   │   ├── Overall Pedagogical Approach
│   │   ├── Delivery Method Selection (Classroom/Distance/Blended)
│   │   ├── Instructional Events Mapping
│   │   ├── Learning Environment Requirements
│   │   ├── Technology/Resource Needs
│   │   └── Learner Support Strategy
│   │
│   └── Performance_Standards_Document.md
│       ├── Duty/Task-Specific Standards
│       ├── Safety Thresholds
│       ├── Accuracy/Speed Requirements
│       ├── Environmental Task Conditions
│       └── Doctrinal Source Citations
│
├── DEVELOPMENT_PHASE/
│   │
│   ├── INSTRUCTIONAL_MATERIALS/
│   │   ├── Lesson_Plan_Template.md
│   │   │   ├── Terminal and Enabling Learning Objectives
│   │   │   ├── Time Allocation
│   │   │   ├── Required Resources and Materials
│   │   │   ├── Instructional Sequence (Introduction → Body → Closure)
│   │   │   ├── Learning Activities
│   │   │   ├── Assessment Methods
│   │   │   └── Remediation Strategy
│   │   │
│   │   ├── Instructor_Guide.docx
│   │   │   ├── Course Overview
│   │   │   ├── Module Facilitator Notes
│   │   │   ├── Talking Points for Each Lesson
│   │   │   ├── Timing and Pacing Guidelines
│   │   │   ├── Discussion Facilitation Tips
│   │   │   ├── Troubleshooting/Common Student Misconceptions
│   │   │   ├── Answer Keys
│   │   │   └── References/Appendices
│   │   │
│   │   ├── Student_Course_Book.pdf
│   │   │   ├── Table of Contents
│   │   │   ├── Module Overview Pages
│   │   │   ├── Lesson Content (narrative, diagrams, examples)
│   │   │   ├── Key Term Glossary
│   │   │   ├── Self-Assessment Questions
│   │   │   ├── References
│   │   │   └── Appendices (checklists, quick-reference cards)
│   │   │
│   │   ├── PowerPoint_Presentation_Slides.pptx
│   │   │   ├── Title Slide
│   │   │   ├── Module 1 Slides
│   │   │   │   ├── Overview Slide
│   │   │   │   ├── Content Slides (text, graphics, animations)
│   │   │   │   ├── Example Scenarios
│   │   │   │   └── Transition/Review Slide
│   │   │   └── Module N...
│   │   │
│   │   ├── Reading_Package.pdf
│   │   │   ├── Doctrine Excerpts (MCDP/MCWP sections with citations)
│   │   │   ├── Technical Procedure Extracts
│   │   │   ├── Case Studies/Historical Examples
│   │   │   ├── Supplemental Articles
│   │   │   └── Annotated Bibliography
│   │   │
│   │   └── Lecture_Notes_and_Talking_Points.md
│   │       ├── By-Lesson Speaker Notes
│   │       ├── Key Phrases and Definitions
│   │       ├── Transition Cues
│   │       └── Emphasis Points for Critical Concepts
│   │
│   ├── ASSESSMENTS/
│   │   ├── Performance_Evaluation_Checklist_PEC.xlsx
│   │   │   ├── Task/Duty Identifier
│   │   │   ├── Step-by-Step Performance Criteria
│   │   │   ├── GO/NO-GO Scoring
│   │   │   ├── Conditions and Standards
│   │   │   ├── Safety Critical Items
│   │   │   ├── Scoring Instructions
│   │   │   └── Rater Guidance
│   │   │
│   │   ├── Multiple_Choice_Assessment_Questions.docx
│   │   │   ├── Stem (Clear Question/Scenario)
│   │   │   ├── Correct Answer
│   │   │   ├── Distractor A (Plausible Wrong Answer + Rationale)
│   │   │   ├── Distractor B (Plausible Wrong Answer + Rationale)
│   │   │   ├── Distractor C (Plausible Wrong Answer + Rationale)
│   │   │   ├── Bloom's Level
│   │   │   ├── Objective Alignment (TLO/ELO)
│   │   │   └── Source Citation
│   │   │
│   │   ├── Scenario_Based_Assessment_Items.docx
│   │   │   ├── Scenario Context and Setup
│   │   │   ├── Decision Point/Problem Statement
│   │   │   ├── Correct Response Options (with Rationale)
│   │   │   ├── Incorrect Response Options (Distractor Analysis)
│   │   │   ├── Follow-up Branching Scenarios
│   │   │   ├── Cognitive Level
│   │   │   ├── Objective Alignment
│   │   │   └── Source/Doctrinal Basis
│   │   │
│   │   ├── Answer_Key.pdf
│   │   │   ├── Question-by-Question Answers
│   │   │   ├── Distractor Explanation (Why Each is Wrong)
│   │   │   ├── Scoring Guide
│   │   │   ├── Passing Threshold
│   │   │   └── Remediation Recommendations by Objective
│   │   │
│   │   └── Assessment_Rubric.xlsx
│   │       ├── Performance Levels (Unsatisfactory, Developing, Proficient, Advanced)
│   │       ├── Criteria for Each Level
│   │       ├── Point Scale
│   │       └── Alignment to Learning Objectives
│   │
│   ├── MULTIMEDIA_ASSETS/
│   │   ├── Video_AV_Script_Two_Column.docx
│   │   │   ├── Scene/Segment Identifier
│   │   │   ├── Timing (seconds)
│   │   │   ├── Video/Visual Column
│   │   │   │   ├── Shot Descriptions
│   │   │   │   ├── Graphics/Overlays
│   │   │   │   ├── Camera Movements
│   │   │   │   └── Transitions
│   │   │   ├── Audio/Narration Column
│   │   │   │   ├── Dialogue/Voiceover Script
│   │   │   │   ├── Sound Effects
│   │   │   │   ├── Background Music
│   │   │   │   └── Pause Points
│   │   │   ├── Learning Objective(s) Addressed
│   │   │   └── Source/Reference Citations
│   │   │
│   │   ├── Storyboard_Panels.pdf
│   │   │   ├── Panel 1: [Frame Description + Narration]
│   │   │   ├── Panel 2: [Frame Description + Narration]
│   │   │   ├── Panel N...
│   │   │   ├── Visual Style Guide
│   │   │   └── Animation/Transition Notes
│   │   │
│   │   ├── Audio_Script.txt
│   │   │   ├── Speaker Identification
│   │   │   ├── Dialogue
│   │   │   ├── Pronunciation Guide (Technical Terms)
│   │   │   ├── Pacing Notes
│   │   │   └── Emphasis Markers
│   │   │
│   │   ├── Graphics_and_Illustrations_Specifications.docx
│   │   │   ├── Diagram 1: [Technical Drawing Specifications]
│   │   │   ├── Chart 1: [Data Visualization Requirements]
│   │   │   ├── Icon Library [Reference]
│   │   │   ├── Style Guide (colors, fonts, formatting)
│   │   │   └── Accessibility Requirements (alt text, captions)
│   │   │
│   │   └── Multimedia_Asset_Inventory.xlsx
│   │       ├── Asset ID
│   │       ├── Type (Video, Audio, Graphic, Animation)
│   │       ├── File Name/Location
│   │       ├── Format and Specifications
│   │       ├── Objective(s) Addressed
│   │       ├── Status (Draft/Final)
│   │       └── Completion Date
│   │
│   ├── LIVE_INSTRUCTION_COMPONENTS/
│   │   ├── Discussion_Guide.md
│   │   │   ├── Discussion Topic/Prompt
│   │   │   ├── Facilitator Notes
│   │   │   ├── Expected Student Responses
│   │   │   ├── Follow-up Questions
│   │   │   ├── Common Misconceptions to Address
│   │   │   └── Time Allocation
│   │   │
│   │   ├── Practical_Exercise_Workbook.pdf
│   │   │   ├── Exercise 1: [Hands-on Task Description]
│   │   │   │   ├── Learning Objective(s)
│   │   │   │   ├── Scenario/Context
│   │   │   │   ├── Step-by-Step Procedures
│   │   │   │   ├── Expected Output/Result
│   │   │   │   ├── Student Worksheet
│   │   │   │   └── Solution Key
│   │   │   └── Exercise N...
│   │   │
│   │   ├── Case_Study_Materials.docx
│   │   │   ├── Case Study 1: [Situation Description]
│   │   │   │   ├── Background/Context
│   │   │   │   ├── Problem Statement
│   │   │   │   ├── Analysis Questions
│   │   │   │   ├── Decision Points
│   │   │   │   ├── Facilitator Debrief Notes
│   │   │   │   └── Learning Objectives Addressed
│   │   │   └── Case Study N...
│   │   │
│   │   └── Simulation_Event_Script.md
│   │       ├── Event Title and Duration
│   │       ├── Learning Objectives
│   │       ├── Scenario Setup and Conditions
│   │       ├── Role-Player Instructions
│   │       ├── Facilitation/Observation Points
│   │       ├── Expected Learner Actions
│   │       ├── Grading/Assessment Method
│   │       └── Debrief Talking Points
│   │
│   └── COMPILATION_AND_AUDIT/
│       ├── Development_Audit_Trail.md
│       │   ├── Artifact Version History
│       │   ├── Revision Change Log
│       │   ├── Reviewer Dispositions and Comments
│       │   ├── Source Citation Verification Checklist
│       │   └── Quality Assurance Sign-Off
│       │
│       ├── Objective_Assessment_Traceability_Matrix.xlsx
│       │   ├── TLO | ELO | Content | Assessment Item | MM Asset | Source
│       │   └── [All objectives traced to assessment and content]
│       │
│       └── Content_Development_Checklist.xlsx
│           ├── Analysis Phase Completion ✓
│           ├── Design Phase Completion ✓
│           ├── Development Artifact Deliverables ✓
│           ├── Quality Review Sign-Offs ✓
│           ├── Gaps/Unresolved Issues
│           └── Authorization for Implementation

```

## Document Purpose Summary

| Phase | Document | Purpose | Key Inputs | Key Outputs |
|-------|----------|---------|-----------|------------|
| **ANALYSIS** | TNA Report | Identify and justify training need | Stakeholder interviews, performance data | Gap statement, training recommendation |
| | JTA | Define target duties and conditions | SME input, doctrine, operational context | Task list, task standards, prerequisites |
| | Source Evaluation | Assess doctrine/manual sufficiency | Available references, JTA | Information gaps flagged, gaps list |
| | Doctrinal Summary | Synthesize relevant doctrine | MCDP/MCWP, TM extracts | Cited principles, application guidance |
| | Stakeholder Reqs | Capture learning organization needs | Student population, constraints | Requirements matrix, audience profile |
| **DESIGN** | Curriculum Map | Structure course organization | Analysis artifacts, time budget | Module sequence, lesson flow |
| | Objectives Hierarchy | Define measurable learning outcomes | Bloom's taxonomy, JTA, doctrine | TLOs/ELOs with condition/standard |
| | Assessment Plan | Define how to evaluate learning | Objectives, performance standards | Assessment-to-objective matrix |
| | Content Outline | Identify content organization | Curriculum map, objectives | Topic hierarchy, lesson content list |
| | Instructional Strategy | Select delivery and pedagogy methods | Audience, environment, resources | Teaching approach, technology decisions |
| | Performance Standards | Specify duty-task success criteria | JTA, safety/doctrinal requirements | Pass/fail thresholds, safety rules |
| **DEVELOPMENT** | Lesson Plans | Script daily instruction | Curriculum map, objectives, assessment | Time-phased activities and content |
| | Instructor Guide | Support instructor delivery | Lesson plans, source materials | Talking points, facilitation guidance |
| | Course Book | Provide student reference | Lesson plans, illustrations, case studies | Readable narrative with examples |
| | PowerPoint | Present visual lesson content | Lesson topics, graphics, animations | Slide decks aligned to lessons |
| | Reading Package | Aggregate source doctrine/references | MCDP/MCWP, technical manuals, articles | Curated citations with annotations |
| | PEC/Rubrics | Evaluate hands-on performance | Objectives, task standards, safety | Step-by-step scoring criteria |
| | MC Questions | Test knowledge retention | Objectives, Bloom's levels | Question bank with distractor rationales |
| | Scenario Assessment | Evaluate decision-making | Real-world duty contexts | Branching scenarios with feedback |
| | AV Script | Direct video production | Objectives, storyboard, resources | Two-column script with timing |
| | Storyboard | Visualize video/animation sequence | Script, learning objectives | Panel-by-panel visual breakdown |
| | Discussion Guides | Facilitate group learning | Objectives, case studies | Prompts, expected answers, follow-ups |
| | Practical Exercises | Enable skill practice | Objectives, task procedures | Hands-on activity with solution key |
| | Audit Trail | Verify quality and traceability | All artifacts, reviews, changes | Version history, sign-offs, gaps log |

## Notes for Hackathon Implementation

1. **Traceability**: Every document must link Analysis → Design → Development artifacts. Use the Objective-Assessment-Content Matrix to verify complete tracing.

2. **Source Control**: Maintain visible citations to MCDP/MCWP paragraphs, technical manuals, or JTA. Mark inferences and unresolved gaps explicitly.

3. **Gatekeeping**: Require human authorization before moving from Analysis to Design and from Design to Development. Each gate should verify:
   - Analysis: Source sufficiency, gap flagging
   - Design: Objective-assessment alignment, doctrinal correctness
   - Development: Content accuracy, assessment validity, audit trail completeness

4. **Multimedia Scripting**: Use two-column AV scripts (visual + audio) to ensure both audio narration and visual elements are choreographed together.

5. **Assessment Quality**: Every multiple-choice question must include distractor rationales (why each wrong answer is plausible) to aid instructors in diagnosing misconceptions.

6. **Audit Log**: Keep a running log of reviewer comments, revision decisions, and source verification. This becomes the non-negotiable evidence trail for the training program.

---

**Reference**: MCDP 5, *Planning* (supplied extraction); Marine Corps Handbook for Training and Education; ISD Best Practices (Bloom's Taxonomy, criterion-referenced assessment, performance evaluation checklists).
