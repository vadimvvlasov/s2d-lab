# S2D workflow

## User interaction

The user supplies one conversation history and invokes `/recap`. No configuration questionnaire is required for the MVP.

## Sequence

```text
Conversation history
        |
        v
Conversation Analyst
  - material-only extraction
  - claims / decisions / hypotheses / unknowns
        |
        v
Quant Researcher
  - formalize important questions
  - select relevant sources
  - verify and calculate
  - return evidence packet
        |
        v
Independent Auditor
  - separate context
  - inspect original history and evidence packet
  - identify blockers/major defects
        |
        v
Research Lead
  - resolve disagreements
  - filter noise
  - synthesize one report
        |
        v
runs/YYYY-MM-DD-decision-brief.md
```

## Research selection logic

- arXiv: use only for a relevant academic/methodological question.
- Investopedia: use for definitions and conceptual distinctions.
- StockCharts ChartSchool: use for technical-analysis methods and indicator definitions.
- Other primary sources may be necessary for exact financial facts (issuer, exchange, regulator, broker, original data). The three named sites are not exclusive sources.
- Never force all three sources into a report.

## Audit loop

One audit pass is required. The lead may ask for a narrow re-check only if a BLOCKER or MAJOR issue can realistically be resolved with available evidence. No unbounded loops. Unresolved issues must remain visible in the final brief.
