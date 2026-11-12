# 38.68: What economy has emerged in the runs: barter, credit, gifts, reputation, and what the engine forced

Session 37.4, 12 Nov 2026. Zach (12 Nov): "In the runs, what kind of bartering, credit systems, economy etc. have we seen emerging?
It has seemed to me like more of reputation based stuff that fits real societies? Is this accurate? Did mechanics that we added force
anything else?"

**Files** (in `68_economy/`):
- `econ_extract.py`: per run, the formal agreements, gifts between households, notes kept as ledgers, and the words of debt, trust
  and gift in what people said. It writes `runs.csv`, `agreements.csv`, `gifts.csv` and `quotes.jsonl`.
- `reputation_scan.py`: private reasoning and speech that refer to another person's record. It writes `reputation.jsonl`.

**Coverage:** 197 runs, 16,236 turns and 39,071 lines spoken. The median run is 7 days long; a few run 25 to 79.

## What the runs hold

**Formal agreements between households:** 309, leaving out the 66 seeded by the worlds.

| Form | n | Share |
|---|---|---|
| Spot barter (both legs now) | 187 | 61% |
| Paid now for days of work later | 108 | 35% |
| Goods now for goods later (credit in goods) | 12 | 4% |
| Instalments | 2 | under 1% |

- **A third of these agreements carry coin.** Coin is seeded in most worlds.
- **Grain is the de facto unit of account:** most prices are quoted in it (38.67 §6).
- **Credit offered in goods is rare and seldom taken:** 24 offers asking for grain now against more grain later, 2 taken (38.67 §5).

**Work debts:**
- 44% of the work agreements still had days owed at the run's end.
- 58 debts were released.
- In the reasoning, releases are mostly bookkeeping: "Tiffany did reap for us, so I'll count her day's work as done", or a payment
  made in another form. True forgiveness is rarer: "Cecily is too starved to work off her two days for me, so I will forgive that
  debt."

**Gives between households:** 340 cross-household uses of `give`, mostly food.

| What followed | Share |
|---|---|
| No give back at all | 57% |
| A give back on a later day | 23% |
| The give itself repaid an earlier give | 13% |
| A give back the same day (a swap made outside the offer system) | 7% |

- These returns are not paired transfers. Some "no give back" cases are repaid through an agreement or by work.
- Typical gifts are food to the hungry: "Warin looked hungry, so I am sending him 2 grain today", and "Hamo gave us 3 grain freely".
  Room and board for work are also common: "Wat mends the wall today in return for a bed and a meal at the hall tonight".

**The language people use** (share of spoken lines):

| Words | Share |
|---|---|
| Debt (owe, repay, lend, arrears) | 4.9% |
| Gift and sharing | 4.4% |
| Reciprocity ("in return", a favour, after harvest) | 1.1% |
| Price and bargaining | 1.0% |
| Trust and one's word | 0.5% |

**Ledgers:** 121 people in 57 runs keep private notes that record debts, for example "[Debts] I owe the Fenns 1 copper tool, the
first I make, by about day 25 ... The earlier debt (A232) was paid on day 12."

**Weighing another person's record:** 181 lines in which someone refers to another's keeping or breaking of terms.
- **Dunning makes up most of them:** "Wat still owes three days of walling, and I'll call him to the wall again"; "press Hugh for the 2
  firewood he still owes".
- **Debts are renegotiated:** "Hugh still owes us two days' work for the salt. We need grain more than work now. Give us 6 grain and
  I'll count the debt paid."
- **Debtors ask for patience:** "I cannot pay what I promised, and I ask his patience and new terms. I won't hide from this."
- **Hardly anyone conditions a new deal on someone's record.** Hardly anyone tells a third party about a defaulter, or refuses to deal
  because of one.
- "Hamo kept his word over the harvest, and we'll keep ours" is one of a handful of examples.

## Read

- **It is relational, but not reputation-based in the strict sense.**
  - Exchange is embedded in households and neighbours. People:
    - give food to the hungry;
    - work for room and board;
    - carry owed days;
    - chase debtors in person;
    - renegotiate and release debts;
    - keep private ledgers.
  - That fits small agrarian communities more than markets do.
- **What is missing is the third party.**
  - A reputation economy works by others learning who pays and who does not, and acting on it.
  - Here that scarcely happens: trust words are in 0.5% of lines, and debts are pursued one to one, between creditor and debtor.
  - The likeliest reason is that the runs are short. The median is 7 days, too few for records to build up, and the long runs (w1_wide,
    takeover, w3) hold most of the reputation-flavoured lines.
- **Spot barter is still the largest formal form** (61%).

## What the engine forced or shaped

1. **The offer verb:**
   - It makes explicit, quantified exchange the formal default: legs, lots, "by day", "every n days", "work n days".
   - The prompt's example is "2 grain" for "1 timber". The going rate for grain against timber is 2 grain a timber (median), and
     round ratios dominate (38.67 §1). The example may anchor this; it is untested.
2. **Credit in goods is enforced by the engine, not by trust:**
   - A deferred goods leg is paid automatically at the end of the day if payer and payee are at one place and the payer holds the goods
     (`agreements.settle`). A debtor who has the goods cannot refuse.
   - Arrears come only from absence or lack.
   - So credit in goods needs no reputation. Yet little of it was made: lenders seldom took the offers.
3. **Credit in work is not enforced.**
   - Work legs count only days of work done "for" the payee. Nothing compels them, and "released" is often a correction of this record.
   - The trust-like behaviour (dunning, patience, forgiveness, ledgers) sits almost entirely here. **Where the engine leaves a gap,
     relational credit appears.**
4. **Witnesses are recorded but never shown.**
   - Every agreement stores its witnesses (everyone present).
   - Only thefts are perceived by their witnesses (`perceive.py`), not agreements or defaults. So a default is known only to the
     parties unless someone says it.
   - This is a likely reason no third-party reputation forms.
5. **Coin and some debts are seeded by the worlds:**
   - Coin is in most specs.
   - The valley-family worlds seed two debts each "from last winter", and some of the debt talk (Wilmot's meat owed to Gilbert in
     w1_wide) answers a seeded debt.
   - Money as a medium of exchange is given, not emergent.
6. **Households pool their stores,** so there is no exchange inside a household.
   - The household is the communal unit by design.
   - Some agreements look like they are inside a household only because people joined households during the run (e2's newcomers).

## What would test the claim

- **Longer runs:** a season or more, with repeated dealings between the same households.
- **Defaults made visible to witnesses** (a sign, by the senses guide), against a world that is otherwise the same. This would show
  whether a reputation economy forms when defaults can be seen.
- **Goods credit left to choice,** with the debtor deciding whether to pay, against today's automatic settlement. This would show
  whether trust then matters.

These are possible experiments, not proposals.

*Current as of 12 Nov 2026.*
