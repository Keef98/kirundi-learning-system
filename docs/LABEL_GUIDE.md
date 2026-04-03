# Label Guide

Standard labels used across all CSV files in this project.

## difficulty

| Value | Meaning | Example learner |
|---|---|---|
| `beginner` | First week of learning. Single words, fixed phrases, basic greetings. | Knows zero Kirundi, just starting. |
| `elementary` | Can handle basic exchanges. Short sentences, common patterns. | Can greet someone and buy something at the market. |
| `intermediate` | Can navigate real conversations. Longer sentences, varied register. | Can visit family and have a simple conversation. |

## register

| Value | Meaning | When to use |
|---|---|---|
| `neutral` | Default, no special politeness markers. | Generic examples, context-free sentences. |
| `polite` | Standard everyday politeness. | Normal interactions with strangers or acquaintances. |
| `respectful` | Elevated respect, deference. | Speaking to elders, authority figures, in-laws. |
| `informal` | Casual, relaxed. | Friends, peers, siblings. |
| `child_friendly` | Speaking to or with children. | Simplified language, gentle tone. |
| `formal` | Official, ceremonial. | Speeches, official meetings, church. |

## review_status

| Value | Meaning | Rule |
|---|---|---|
| `draft` | Created but not yet reviewed. | Do not use in app or training. |
| `reviewed` | Reviewed at least once. May still have issues. | Do not use in app or training. |
| `approved` | Confirmed correct, natural, and ready. | OK for app content and training data. |

## source_type

| Value | Meaning |
|---|---|
| `original` | Created from scratch by a native speaker (you). |
| `collected` | Gathered from a native source (conversation, book, recording). |
| `adapted` | Modified from an existing source to fit the teaching context. |

## type (content type)

| Value | Meaning |
|---|---|
| `translation` | Kirundi sentence + English/French equivalents. |
| `explanation` | Kirundi sentence + simple tutor-style explanation. |
| `correction` | Learner mistake + corrected version + explanation. |
| `dialogue` | Multi-turn conversation for a situation. |
| `variants` | Multiple natural ways to express the same intent. |

## task_type (evaluation records)

| Value | Meaning |
|---|---|
| `translate_to_kirundi` | Given English/French, produce correct Kirundi. |
| `translate_from_kirundi` | Given Kirundi, produce correct English/French. |
| `explain` | Given Kirundi, produce a clear explanation. |
| `correct` | Given a learner error, produce a correction. |
| `dialogue_continue` | Given a partial dialogue, produce the next turn. |
| `generate_variants` | Given a situation + intent, produce natural options. |
