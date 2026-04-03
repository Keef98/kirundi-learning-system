# Kirundi Language Learning System — Project Brief

## What this is

An AI-assisted Kirundi language learning app for English/French speakers who want to speak Kirundi in real-life situations.

This is **not** a generic Kirundi chatbot or a from-scratch Kirundi LLM.

This is a **practical speaking tutor** that teaches what to say, translates, explains, corrects learner answers, and runs short dialogues — all grounded in curated, native-speaker-created content.

## Why this matters

Kirundi is a low-resource language. Frontier models (Claude, GPT-4) hallucinate when generating Kirundi — they produce plausible-looking but wrong sentences, mix in Kinyarwanda, and invent grammar. You cannot simply prompt an existing model and get reliable Kirundi output.

This means:

- A curated, native-reviewed dataset is the foundation of everything
- Model training is necessary but comes **after** content creation
- The system must constrain model outputs against trusted content

## Who is building this

The project lead is a native Kirundi speaker who has validated demand among the Kirundi-speaking diaspora. This means:

- Content creation, quality review, and Kinyarwanda boundary decisions are handled by the founder directly
- No dependency on external native speakers for the initial content phase
- The founder is the first and primary quality authority

---

## Core design principles

### 1. Content first, model second

The most valuable and irreplaceable work is producing high-quality Kirundi teaching content. Every other technical decision depends on this content existing. Model training, retrieval systems, and app development all consume this content — none of them create it.

**Priority order:**

1. Produce curated Kirundi content (only the founder can do this)
2. Structure it for retrieval and training (mechanical, can be automated)
3. Build a constrained prototype using retrieval + prompted model (no fine-tuning yet)
4. Fine-tune a model when content volume justifies it

### 2. Kirundi-first

- Collect natural Kirundi first, then add translations and explanations
- Never build teaching content by translating English/French into Kirundi
- English-first data creation produces literal, unnatural Kirundi

### 3. Situation-first, not grammar-first

The system is organized around real speaking situations, not grammar topics. Learners want to know "how do I greet an elder" not "what is the subjunctive."

### 4. Kinyarwanda is not the base

Kinyarwanda and Kirundi are close but distinct. Kinyarwanda may be used for inspiration or comparison, never as source material. The primary quality risk to watch for is Kinyarwanda leakage — in content, in model outputs, and in contributor habits.

### 5. Narrow and useful before broad

The first version covers a small number of situations done well. No attempt to build general-purpose Kirundi generation until the narrow system is validated.

---

## What the system does (target capabilities)

### Translation

- English → Kirundi
- French → Kirundi
- Kirundi → English
- Kirundi → French

### Explanation

- Explain a Kirundi sentence simply in English or French
- Provide short usage notes (register, context, cultural notes)

### Learner correction

- Judge learner output as: acceptable / awkward / wrong
- Propose a better version
- Explain why, simply

### Dialogue

- Generate short dialogues for a given situation
- Continue a dialogue naturally
- Role-play as different speakers (seller, relative, friend, elder)

### Controlled generation

- Produce 2–5 natural Kirundi options for a given situation
- Adjust by difficulty and register

---

## Version 1 scope

### Skill scope

- Translate simple phrases
- Explain simple Kirundi
- Correct beginner answers
- Generate short situation-based dialogues

### Content scope

- 3 pilot situations: **greetings**, **market**, **family visit**
- 50–100 records per situation
- All five content types per situation (see below)

### What "done" looks like for v1

- 150–300 curated, reviewed records across 3 situations
- A working prototype that retrieves this content and presents it to learners
- Model outputs constrained to approved content (no free Kirundi generation)
- 5–10 real learners have tested it and given feedback

---

## Content architecture

### The five content types

Every situation should have records of all five types. Each type maps directly to a model capability you'll train later.

#### 1. Translation pairs

A natural Kirundi sentence + its English and French equivalents. Not word-for-word glosses — how you'd actually say it.

**Later becomes:** translation fine-tuning data, retrieval base

#### 2. Explanation examples

A Kirundi sentence + a short, simple explanation in English and French. What a tutor would say, not a grammar lecture.

**Later becomes:** explanation fine-tuning data

#### 3. Correction pairs

A plausible learner mistake + the corrected version + a short explanation of why it's wrong.

**Later becomes:** correction fine-tuning data

#### 4. Short dialogues

2–6 turns, tagged with situation and speaker roles. Natural and short.

**Later becomes:** dialogue fine-tuning data, app content

#### 5. Variant sets

For a given situation and intent, 2–4 natural ways to say it, tagged by register.

**Later becomes:** controlled generation training data, evaluation reference

### Content metadata (keep it light)

For each record, capture:

- **situation** — which situation this belongs to (greetings, market, family_visit)
- **type** — translation / explanation / correction / dialogue / variants
- **difficulty** — beginner / elementary / intermediate
- **register** — neutral / polite / respectful / informal / child_friendly / formal
- **review_status** — draft / reviewed / approved

That's it for now. You can add fields later. Don't let schema design slow down content production.

### The training-readiness test

Every record you create should pass this test: **can you see how it becomes an instruction / input / output triple?**

Examples:

- Translation pair → instruction: "Translate to Kirundi" / input: "Good morning, sir" / output: "Mwaramutse, mushingantahe"
- Correction → instruction: "Correct this Kirundi and explain" / input: learner's bad sentence / output: corrected version + explanation
- Dialogue → instruction: "Continue this greeting dialogue at the market" / input: first two turns / output: next turn

You don't need to format them as triples now. Just make sure the conversion is obvious and mechanical later.

---

## Situation taxonomy

### Pilot situations (v1)

1. Greetings
2. Market / shopping
3. Family visit

### Expansion candidates (v2+)

4. Self-introduction
5. Asking for help
6. Transport
7. Meals / food
8. Daily routine
9. Phone / WhatsApp
10. Directions
11. Emotions
12. Misunderstandings
13. Speaking respectfully to elders
14. Speaking to children

### What each situation defines

- **Learner goal** — what should the learner be able to do after this?
- **Core communicative functions** — greeting, requesting, thanking, apologizing, etc.
- **Core vocabulary** — 10–30 key words
- **Register notes** — what politeness distinctions matter here?
- **Cultural notes** — what would a foreigner get wrong?

---

## Technical strategy

### Phase 1: Content + constrained prototype (NOW)

**You do:**

- Produce 150–300 curated records for 3 pilot situations
- Use CSV files in this repo
- Review and approve your own content (you're the native authority)

**The system does:**

- Retrieval over your approved content by situation, type, difficulty, register
- A prompted frontier model (Claude/GPT-4) handles ONLY:
  - Presenting your content to learners
  - Explaining your content in English/French (verified against your explanations)
  - Scaffolding dialogue from your approved dialogue scripts
- The model NEVER generates free Kirundi — it retrieves and presents

**Why this works despite hallucination:**
The model doesn't need to know Kirundi. It needs to know how to teach. Your content provides the Kirundi; the model provides the pedagogical interaction layer.

### Phase 2: Model fine-tuning (LATER)

**When to start:** when you have 500+ approved records and have identified specific gaps that retrieval alone can't fill.

**Approach:**

- Take a pretrained multilingual base model
- Continued pretraining on raw Kirundi corpus (if available) for language familiarity
- Instruction fine-tuning (LoRA/PEFT) on your curated content, formatted as instruction/input/output triples
- Evaluate with your gold evaluation set

**What fine-tuning buys you:**

- The model can generalize beyond your exact curated examples
- Better Kirundi fluency in generated outputs
- More natural dialogue continuation
- Correction of novel learner errors not in your dataset

### Phase 3: Evaluation

**Evaluate on:**

- Grammatical correctness
- Naturalness (does it sound like real Kirundi?)
- Register appropriateness
- Learner usefulness (is the explanation helpful?)
- Kinyarwanda leakage (critical)

**Who evaluates:** you, initially. Later, additional native speakers.

### Phase 4: Production deployment

**Architecture:**

- Layer 1: Trusted pedagogical content (your reviewed CSV data)
- Layer 2: Retrieval layer (selects content by situation, level, function, register)
- Layer 3: Adapted model (explains, personalizes, generates constrained output)
- Layer 4: Guardrails (accepted variants, difficulty limits, register control, rejection of unsupported outputs)

---

## Quality risks to watch

| Risk                                       | Mitigation                                            |
| ------------------------------------------ | ----------------------------------------------------- |
| Kinyarwanda leakage in content             | You're the native reviewer — flag consciously         |
| Kinyarwanda leakage in model output        | Evaluate explicitly, include in eval set              |
| Unnatural Kirundi from literal translation | Kirundi-first principle: never translate from English |
| Poor register control                      | Tag every record, include register in eval            |
| Overcomplicated schema                     | Start with 5 fields, add only when needed             |
| Training before content is ready           | Don't fine-tune until 500+ approved records           |
| Building too broad too early               | 3 situations first, expand only after v1 works        |

---

## Review labels

### Difficulty

- `beginner` — first week of learning
- `elementary` — can handle basic exchanges
- `intermediate` — can navigate real conversations

### Register

- `neutral` — default, no special politeness
- `polite` — standard politeness
- `respectful` — for elders, authority figures
- `informal` — friends, peers
- `child_friendly` — speaking to/with children
- `formal` — official or ceremonial contexts

### Review status

- `draft` — created, not yet reviewed
- `reviewed` — reviewed once
- `approved` — ready for production use

### Source type

- `original` — created by the founder/native speaker
- `collected` — gathered from a native source
- `adapted` — modified from an existing source

**Rule: only `approved` content is used in the app or as trusted training data.**

---

## Milestones

### Milestone 1: First situation pack (target: 1–2 weeks)

- Complete greetings situation: 50+ records across all 5 types
- CSV files filled and reviewed
- Situation README complete

### Milestone 2: Three situation packs (target: 4–6 weeks)

- Greetings + market + family visit complete
- 150–300 total approved records
- Gold evaluation set: 30+ items

### Milestone 3: Working prototype (target: 8–10 weeks)

- Retrieval system over approved content
- Prompted model presenting content to learners
- 5–10 real learners tested
- Feedback collected, gaps identified

### Milestone 4: Fine-tuning readiness (target: 12+ weeks)

- 500+ approved records
- Training export script working
- Evaluation pipeline defined
- Base model selected
- Ready to start LoRA/PEFT experiments

---

## Repo structure

```
kirundi-learning-system/
├── README.md                          # Repo overview and quickstart
├── docs/
│   ├── PROJECT_BRIEF.md               # This document
│   ├── REVIEW_GUIDELINES.md           # How to review and approve content
│   ├── LABEL_GUIDE.md                 # Definitions for all labels
│   └── TRAINING_EXPORT_FORMAT.md      # How content becomes training data
├── data/
│   ├── raw/                           # Raw Kirundi text (for future pretraining)
│   │   └── README.md
│   ├── pedagogical/                   # Teaching content (your main work)
│   │   ├── greetings/
│   │   │   ├── README.md              # Situation definition
│   │   │   ├── translations.csv
│   │   │   ├── explanations.csv
│   │   │   ├── corrections.csv
│   │   │   ├── dialogues.csv
│   │   │   └── variants.csv
│   │   ├── market/
│   │   │   └── (same structure)
│   │   └── family-visit/
│   │       └── (same structure)
│   ├── evaluation/
│   │   ├── README.md
│   │   └── gold_eval.csv              # Gold evaluation set
│   └── exports/
│       ├── README.md
│       └── (generated training files go here)
├── scripts/
│   ├── README.md
│   ├── validate_csv.py                # Validate CSV files against schema
│   ├── export_training_data.py        # Convert CSVs to training triples
│   └── stats.py                       # Content statistics and coverage
├── prompts/
│   ├── README.md
│   └── (system prompts for the retrieval prototype)
└── config/
    ├── README.md
    └── schema_version.json            # Schema version tracking
```

---

## How to use this brief

**Give this document to Claude (or any AI assistant) along with your repo, and ask it to help you with specific tasks:**

- "Help me fill in translations.csv for the greetings situation"
- "Review my corrections.csv and check for gaps"
- "Generate the training export from my approved content"
- "Write the retrieval prototype"
- "Analyze my content coverage across situations"

**The brief gives the assistant enough context to understand:**

- What the project is
- What the content structure looks like
- What the quality standards are
- What the technical direction is
- What NOT to do (generate free Kirundi, skip review, overcomplicate)
