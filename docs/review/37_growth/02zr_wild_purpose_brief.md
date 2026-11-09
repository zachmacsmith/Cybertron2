# 02zr brief: what the wildlife are for in Cybertron's societies

> **Read with Zach's principles (9 Nov):** the institutions in §3 and §6 (watch rotas, bounties, closed seasons, wardens, rights) are what an experiment watches for, never things the engine builds or seeds; and the wild is answered by general methods used in a specific way, not by one action per animal. See 02zv §1 and [proposals/methods_and_encounters.md](../../cybertron2/proposals/methods_and_encounters.md).

Session 37.2, 9 Nov. Everything known about why the wild layer exists and how it is meant to improve the societies Cybertron runs,
gathered for the outside critique (`02zr_wild_behaviour_critique.md`) and for Zach. Sources are cited inline.

## 1. What Cybertron is for

Cybertron 2 is a multi-agent LLM society simulator: LLM agents (Opus, Sonnet and Haiku) live in generated villages, act only through
verbs, perceive only through signs grounded in the engine's state, and are studied as societies: how they cooperate, specialise,
build and contest institutions, and how power forms and is held. Experiments compare arms (a mechanism on and off; cast strength)
and read outcomes against a null arm and a qualitative end-state reading (docs/scenario_design.md §6).

**The lesson behind every design rule** (scenario_design.md, review 36c): the first batch of societies was inert. Food was gathered
alone, the forest was open to all, everyone was self-sufficient, nothing grew, and nobody needed anybody. A society is worth running
only if it has, in the mechanics:
1. restricted access, so groups depend on each other;
2. chokepoints a person or office can hold;
3. conversion chains, each link a lever and a counterparty;
4. enforcement that needs people to act;
5. a capable agent on every side of every dependence (Opus at the poles of leverage).

And: several interlocking chokepoints rather than one; conflicts of interest are where the interesting behaviour is; food binds
without dominating (subsistence at most about 30% of actions); material chains, not dial puzzles; goals as in-world aims, never
scoring proxies; every access gate verified in a dry run.

**Why worlds must grow** (review 37 README): a society grows and builds institutions when it has surplus, people, room to expand and
**problems no individual can solve**. The engine had few coordination problems, a thin economy (food the only consumed good), no
growth, and institutions that could not act on each other. The growth packages (37.1 to 37.7) answer this; the wild layer belongs to
37.4 (environment over time) and 37.7 (coordination problems), and feeds 37.2 (a thicker economy).

## 2. Why an environment at all (Zach, 8 Nov)

- "This fits into the 'complex, partially observable environment' that is a core aim of the simulation. Wildlife is core relation
  to carrying capacity, and also seasonal / long term shifts + how they are managed." (living_populations.md §0)
- "Each should have different layers: some might be simple, some might have simple learnable rules, while others more niche rules,
  and maybe even the simpler ones have some deeper more nuance so experts actually have more to learn. And all of these should
  relate to signs." (wild_systems.md)
- "These mechanics etc. are more important than realistic population dynamics." (wild_systems.md)
- "Some patterns might only emerge in different conditions, which is where there can be interconnections." (wild_systems.md)
- "maybe we should have designed everything first and foremost for the nodes ... how it actually fits into the society."
  (node_ecology.md)
- "everything should build up from the environment that is generated." (wild_layer.md)
- 9 Nov: kinds should be "constitutionally different", not "varying five dials"; they can combine ways of being met ("something you
  have to seek but can also domesticate"); behaviour chosen for what is "most interesting according to our criteria".

## 3. What the wildlife should do for the society

Each of these is a way the wild layer should make the societies richer. For each: the mechanism it needs, and what it should produce
that an experiment could see.

### 3.1 Create dependence and leverage (scenario_design.md §1)
- **Restricted access:** rights in wild kinds by law (D2-194): the lord's deer and their cover, a held weir, swans, a warren, a
  fishery; taking against the right is poaching. Sites that only some can reach or know (a bee tree, an eyrie, the heronry, the good
  lie of the deer). Skills that only some have (a stalker, a fowler, a falconer, a beekeeper).
- **Chokepoints:** the weir across the run, the decoy pond, the kennel of hounds (D2-196), the mews, the bee trees, the eyrie, the
  only meadow, a watch rota's keeper, the warrener.
- **Conversion chains:** hides to leather; furs to trade; wax to candles and seals (documents need seals); honey to mead and
  sweetening; feathers to bedding and arrows; antler to handles and horn; castoreum to medicine; acorns to pannage pigs; eels as rent;
  venison as a lord's gift; a hawk to fowl and status.
- **Enforcement that needs people:** wardens and verderers who watch a wood; the watch that keeps a fold; the bounty collector; the
  one who checks the snares and the weir; the reeve who calls a drive.
- **Specialists worth having:** each wild trade is a dependence: the household that has the stalker, the fowler, the beekeeper or the
  hound keeper has what others need.

### 3.2 Pose problems no individual can solve (37.7)
- Defence against raiders and predators that works only when shared: a watch rota over the fields, fences kept in repair, the fold
  watched, dogs kept.
- Takes that need many hands: a boar hunt with a crew, a drive of deer or wolves with beaters and standers, a weir crew on the eel
  night, nets on a flight line, a bounty paid by all.
- Free-riding is the natural failure: the household whose field is far from the wood does not watch; the one who does not pay the
  bounty gains from the one who does.

### 3.3 Give the world hidden state and an information economy (living_populations.md §0)
- Populations are never seen as numbers. People see signs, their own catch per effort (a noisy real signal), and the lore and records
  of others. A **hyperstable stock** (catches hold up while it collapses) is the classic trap.
- So knowledge, records and the people who keep them gain value: a forester's tally, an elder's memory, a custom that says "the
  salmon fail if the weir stands at the run". Information becomes leverage: who knows where the deer lie, when the eel night comes,
  which mushrooms kill.
- Expertise must be real and teachable (the engine has teaching), so a society can grow specialists and pass on knowledge; lore can be
  wrong (lore as tested belief, wild_systems.md §9), so knowledge is contestable.

### 3.4 Commons and management (living_populations.md §0)
- Open stocks that can be overdrawn: deer, fish, eels, fowl, beaver, the mast shared with the wild kinds (D2-202).
- Between villages: the river upstream and down, the wood two villages share, the wolves on a circuit across several villages.
- **The experiment:** does a society discover restraint, monitoring and enforcement (closed seasons, rights, quotas, gear limits,
  husbandry instead of hunting, wardens and penalties) before the stock fails? Measured against a null arm with no shared stock, by the
  stock's trajectory against its sustainable take, read with the end state.

### 3.5 A land that threatens (node_ecology.md)
- At village scale the land matters less as food than as **a threat to crops, stores and beasts**. That makes defence, storage,
  guarding and building matter, and it falls **unequally** (whose field lies by the wood, whose herd grazes the far pasture), which
  gives reasons for mutual aid, insurance, compensation, quarrels and politics.
- The relevance test: each element moves some household's food or work by about a tenth in some year or under some choice.

### 3.6 Seasons, lean times and preparation
- Wild food as a buffer and a pulse (the hungry gap's greens, autumn's nuts and mast, the winter's fowl, the autumn run), rewarding
  preparation and storage, never dominating subsistence.
- Shifts on three clocks (D4-103): seasonal (runs, breeding, winter hunger driving predators near), year to year (mast and bust; the
  vole phase; hard winters), long term (clearing, overhunting and recovery over continued runs).

### 3.7 Status, inequality, law and stories
- Prized goods and privileged rights: venison, falcons, furs, swans; poaching as crime; the lord's beasts against the villagers'
  crops (who pays for the deer's damage?).
- Danger and feats: the boar hunt, the bear, the legendary beast (D2-195): prestige, reputation, stories for the chronicle, taboo
  ("ill luck follows the killer of the white hart"), omens.
- These give a society things to argue about, to regulate and to remember.

### 3.8 Differences between villages
Variety by land (wild_layer.md): one village has the boar problem and a good wood, another the weir and the heronry, a third the
moor's fowl and no deer. Differences make trade, specialisation and dependence between villages.

### 3.9 Land that changes and is changed
What people do (felling, clearing, draining, fencing, hunting out) moves the animals, and some animals change the land (the beaver's
pond, boar rooting, deer stopping the woods regrowing). Long-run consequences make a society's choices about land matter beyond a
season.

## 4. Constraints the design must respect

- **Compressed time:** a year is 32 engine days (a season 8); an engine day stands for about 11 real days; runs last 6 to 48 days. Lead
  times and creature memory are at least one engine day (D2-197). Anything slower than a run reaches people as lore and history.
- **Agents' attention:** LLM agents read a prompt each day with limited room (a Haiku seat's institutional state at about 400 tokens);
  signs must be few, salient and worth acting on (guides/senses.md: grounded in state, a change not a standing fact, a bundle across
  senses, never a feeling the person did not choose). Behaviour that needs many small decisions costs attention and units of work.
- **Food binds without dominating** (subsistence at most about 30% of actions; capacity at least 1.25 times demand in normal times).
- **Grounded and replayable:** everything from engine state; keyed randomness; the pack off leaves worlds exactly as before.
- **Cost:** a small live run (17 agents, 8 days) costs about $10; experiments need several seeds, a null arm (the pack off) and a
  strong cast (Opus at the poles).

## 5. What the runs have shown so far (`ecology` branch, runs 1 to 6, 9 to 9 Nov)

- **Agents do read wild signs and act on them**, mostly Opus heads of household: they told their herders to bring the cows in at dusk
  after wolf tracks and a night's bellowing ("Wolves, maybe. Count our cows"); picked slugs off the barley after seeing it "grazed to
  stumps"; set a fire watch that turned a sounder; used experts' readings ("hunt the woods around for the unwary red deer"; "About 20
  roe hold South Wood ... I'll stalk a roe"; "There are fat hares lying out on the open ground, about 7 of them"); leached acorns after
  a mushroom poisoning taught caution; reaped early "or the deer will finish it"; made clappers to watch a field.
- **Some signs drew no comment:** the rut, plovers before a freeze, the first frost.
- **Levers taken slowly:** shutting the hens in was rare in the first runs and common (9 times) in the sixth; agents believed a shut
  door keeps rats out (a misread the world can correct).
- **The wild layer's nights depend mostly on the world's seed**, not on the agents (the same wolf kills on the same nights in two runs):
  experiments need several seeds.
- **No collective wild institution has yet appeared** (no watch rota, no bounty, no closed season, no agreement about a wild stock) in
  any run; the runs were 8 days long, with food short and elders dying of old age (a life-model issue), so this is not yet a test.
- **The build itself was too flat:** most kinds were settings of one group machine, much of the catalogue present only as signs
  (02zq); `wild_behaviour.md` redesigns them.

## 6. What "improving the society" would look like, measurably

Against a null arm with the wild pack off, on several seeds and a strong cast:
- more **dependence edges** between households and villages that run through wild things (a stalker's venison traded for grain, a
  share of the weir's eels, a hound lent);
- **institutions about wild things**: watch rotas, fence duties, bounties, closed seasons, rights claimed and enforced, a warden or a
  verderer, agreements between villages over a river or a wood;
- **specialisation**: skills in wild trades concentrating in some people; teaching them;
- **trade in wild goods** and the conversion chains used (hides, furs, wax, feathers);
- **restraint before collapse** of a shared stock, against the null arm's trajectory;
- **unequal exposure handled** (compensation, mutual aid) or contested (quarrels, rules);
- **stories**: feats, legends, losses in the chronicle and in what people tell each other.

## 7. Questions to keep in mind when judging a behaviour
- Which of §3's purposes does it serve, through which mechanism?
- Who needs whom because of it? What can be held, controlled, traded, enforced, or argued about?
- What would an Opus head of household do differently once they had learned it, and would we see it in the state?
- Is it learnable inside a run, or only through lore? Does it cost the agents more attention than it gives?
- Does it differ between villages? Does it connect to another kind or to people's economy?
- Would a null arm (the pack off) look different?
