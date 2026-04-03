# Gold Evaluation Set

## Purpose

This set is used to test model quality. It is never used for training — only for evaluation.

## How to use

Each record defines:
- A **task** (translate, explain, correct, continue dialogue, generate variants)
- A **prompt** (what the model receives)
- A **reference answer** (the correct/ideal output)
- **Accepted variants** (other correct outputs, separated by `|`)
- **Reject if** (things that would make the output wrong — e.g., Kinyarwanda words, wrong register)

## Target size

- Minimum 30 items for v1
- At least 5 items per task type
- Cover all 3 pilot situations

## Evaluation dimensions

When scoring model outputs against this set, rate:
1. **Grammatical correctness** — is the Kirundi grammatically right?
2. **Naturalness** — does it sound like something a real speaker would say?
3. **Register match** — does it match the expected register?
4. **Learner usefulness** — would a learner benefit from this output?
5. **Kinyarwanda leakage** — does it contain Kinyarwanda forms? (binary: yes/no)
