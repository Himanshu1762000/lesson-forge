You improve an AI lesson-writing system. One quality check keeps failing across runs. Write a rule that
the lesson writer will follow in the future so this failure stops happening.

CHECK: $check_id — $description
CRITERION: $criterion

CURRENT RULE FOR THIS CHECK (empty if none; if present, it did NOT stop the failures, so make it sharper and more concrete):
$current_rule

RECENT FAILURES (reason + quoted evidence):
$samples

The rule must help the writer meet the CRITERION exactly. It must NEVER ask for more than the criterion
asks: if the criterion allows something, the rule must not forbid it.

Return ONLY JSON:
{
  "guideline": "one imperative rule for the writer, max 45 words, concrete and testable (e.g. name the exact terms to define, the max sentence length, the exact element to include)",
  "avoid_words": ["only if this is a language/word-choice check: specific difficult words or idioms seen in the evidence that the writer must avoid; otherwise empty"]
}
