# 04: Exchange, money, credit, markets, information and transport, from foragers to the present

Research folder 02zzj, part 4 of 9 (15 Nov 2026). The scope covers how people exchanged, paid, lent, met to trade, learned prices,
and moved goods, from forager exchange networks to 21st-century payments and logistics. It goes into most depth on the village to
the early modern period, because that is where the engine is. It is analysis to design from, not a proposal: nothing here is decided.
It builds on 02zzi (kinds of good, the sequence of societies), 02zzh §3.9 and §3.12 (travel and exchange rungs), 38.68 (the economy
that emerged in 197 runs) and `spec/economy/agreements.md`, `money_and_markets.md` and `transport.md` (what the engine does now).

## Summary

Every economy above the household combines a few forms of exchange: gifts that bind people over time, a centre that collects and
hands back, barter between strangers, and markets with prices. Which one dominates depends less on how advanced people are than on
how far apart the parties are, socially and in space, and on whether anyone can make a promise hold. Money began as **units of
account and credit** (Mesopotamian silver and barley, with fixed interest rates nearly four thousand years ago) well before coins.
Coins were added for paying strangers and soldiers. Even in coined economies, most village and town exchange ran on **credit**:
tallies, shop books and running debts between neighbours, settled now and then and enforced by witnesses and local courts. Coins
were too few and too large for small trades (the "big problem of small change"). Over the centuries the medium of exchange moved
from goods to coin, then to bank money, notes, fiat currency and digital entries. At each step it rested on whoever stood behind
the promise: kin, the village, a lord, a merchant coalition, a bank, the state.

Markets in space were shaped above all by **transport costs and information**. Before rail, moving bulk goods by road cost several
to many times more than by river, and much more again than by sea. A medieval English cart added roughly 3% to the price of wheat
every ten miles. Overland firewood paid only within about 20 km. So towns grew on water, markets sat about a day's round walk
apart, and long-distance trade carried what was valuable for its weight. Information moved only as fast as a person: a letter
took one to three weeks to reach Venice from the rest of Europe around 1500. European grain prices converged slowly from the late
15th century, then fast with the telegraph, rail and steam. Since 1800, transport cost has fallen in steps: canals (Erie: about 90%
off overland freight), rail, steamships (transatlantic freight down roughly 40 to 70% from 1850 to 1913), containers (loading cost
down from $5.83 to about 16 cents a ton in 1956) and air freight (down about tenfold since 1955). Each fall widened the market and
deepened specialisation. For a simulator, the mechanics that most change economic life are: prices that are known only where people
have been and that age; promises enforced by people, not the engine; a known market day at a central place; transport cost felt as
days times load, with water much cheaper than land; and credit with reckoning days. Central banks, stock markets and modern
logistics are context, not things to build.

## How to read the numbers

Each number carries a marker:
- **[c]**: checked by web search in this session (the source is named in Sources).
- **[s]**: a standard figure in the literature, not re-checked here. The search budget ran out before every figure could be checked.
- **[r]**: rough or approximate, an order of magnitude.
- **[x]**: contested; the sources disagree.

Money values are nominal for their time unless stated. A "quarter" of English wheat is 8 bushels, about 0.2 tonnes; English money
was 12 pence (d) to the shilling (s) and 20 shillings (240d) to the pound.

---

## 1. Forms of exchange

### 1.1 Polanyi's frame

Karl Polanyi (*The Great Transformation*, 1944; *Trade and Market in the Early Empires*, 1957) named three main "forms of
integration", plus householding:

| Form | How goods move | Needs | Typical setting |
|---|---|---|---|
| **reciprocity** | gifts and counter-gifts between kin, partners or neighbours, with the return delayed and unstated | lasting relations; memory of who gave what | bands, villages, kin networks, allies |
| **redistribution** | goods flow to a centre (chief, temple, palace, lord, state) and back out as rations, feasts, wages or works | a centre that can collect and store; records | chiefdoms, temple and palace economies, manors, taxation |
| **householding** | production for the household's own use | land and labour in one unit | the peasant household |
| **market exchange** | goods trade at prices set by supply and demand among many buyers and sellers | money or a unit of account, a place, information, enforcement of contracts | towns, fairs, merchant networks |

Polanyi argued that in pre-modern societies the economy was **embedded** in social relations: exchange followed kinship, status
and politics, and a self-regulating market society, in which land, labour and money themselves are traded as commodities, appeared
only in 19th-century Europe. His followers, the **substantivists** (George Dalton, Moses Finley on the ancient economy), held that
market reasoning did not apply to most past economies. The **formalists** answered that people everywhere weigh costs and gains.

### 1.2 Critiques

- **Markets are older and wider than Polanyi allowed.** Old Babylonian and Old Assyrian texts show prices that moved with supply,
  merchants who chased profit, and interest-bearing loans (§3). Peter Temin (*The Roman Market Economy*, 2013) argues that Roman
  wheat prices across the Mediterranean behaved like an integrated market. Medieval England had thousands of chartered markets by
  1350 (§6).
- **Redistribution and markets coexisted.** Mesopotamian palaces and temples ran rations and also traded through merchants. Manors
  took labour dues and also sold grain at market.
- **Barter was not the origin of money.** Anthropologists (Caroline Humphrey, 1985; David Graeber, *Debt*, 2011) found no society
  where barter was the everyday form of exchange between neighbours. Neighbours give and owe. Barter appears between strangers or
  enemies, or where money has failed (the late Roman west, post-Soviet Russia, prisons).

### 1.3 Reciprocity by social distance

Marshall Sahlins (*Stone Age Economics*, 1972) placed exchange on a scale that follows social distance:

| Kind | With whom | Terms |
|---|---|---|
| **generalised** | household and close kin | give without counting; return when able |
| **balanced** | village, allies, trade partners | return of equal value within a known time; failure ends the relation |
| **negative** | strangers, enemies | haggling, deceit, theft; get the most for the least |

This is the most useful single idea for a simulator. It predicts that gifts and running debts dominate inside a village, barter and
haggling with outsiders, and markets where many strangers meet under a peace that someone keeps.

### 1.4 Classic cases

- **The kula ring** (Bronisław Malinowski, *Argonauts of the Western Pacific*, 1922): shell necklaces and armbands circulated in
  opposite directions around a ring of Melanesian islands. They carried rank and partnership, and practical trade (gimwali, open
  barter) went on beside them. Ceremonial exchange made the peace that let ordinary trade happen.
- **The gift** (Marcel Mauss, 1925): the duties to give, to receive and to return; giving more than can be returned is dominance.
- **Hxaro** among the Ju/'hoansi of the Kalahari (Polly Wiessner): delayed gift partnerships, some with partners far away. In a bad
  year a household could move to a partner's water hole. The gifts were **insurance** against local failure [s].

### 1.5 When each form dominates

- **Small group, risk shared:** generalised reciprocity, sharing.
- **Households that store and meet repeatedly:** balanced reciprocity, running debts, help with work.
- **A centre that can collect and store** (a chief's granary, a temple, a lord's barn): redistribution beside reciprocity.
- **Strangers with no common authority:** barter, silent trade, raiding.
- **Many buyers and sellers, a known place and day, a unit of account, a keeper of the peace:** markets with prices.
- **Contracts enforceable across distance, money, information:** merchant networks and credit markets.

**What the runs show (38.68):** spot barter in 61% of formal agreements; gifts of food to the hungry; running work debts with
dunning, patience and release; private ledgers; almost no third-party reputation. That is balanced reciprocity in a village whose
engine enforces goods credit by itself.

---

## 2. Prehistoric exchange networks

Exchange over long distances is older than farming. Material that can be traced to its source shows how far goods went and how.

| Material | Where from, where to | When | What it shows |
|---|---|---|---|
| **obsidian** (volcanic glass for blades) | Anatolian and Armenian sources to the Levant and Mesopotamia | from about 12,000 BC; heavily in the Neolithic | Colin Renfrew, J. E. Dixon and J. R. Cann traced sources by trace elements (1964 to 1968). Within about **300 km** of a source, obsidian made up over 80% of chipped stone; beyond it the share fell off almost **exponentially with distance** [c]. Renfrew read this as **down-the-line exchange**: each community passed on part of what it got to the next. |
| **Spondylus shell** (ornaments) | Aegean to central Europe, up to about 1,500 km | about 5500 to 4500 BC | prestige goods moved through many hands; worn as status, buried with the dead [s, r] |
| **Baltic amber** | the Baltic to Mycenaean Greece and the Mediterranean | 2nd millennium BC | a long "amber road" of linked exchanges [s] |
| **Mesopotamian tin and lapis** | Afghanistan and Central Asia to Mesopotamia | 3rd millennium BC | the start of organised long-distance trade feeding bronze-making |

**Critiques of fall-off curves.** Later work shows that the curve's shape does not by itself say what kind of exchange made it.
Random movement can produce a curve that looks like down-the-line exchange. Agent-based models find that down-the-line exchange
alone cannot carry obsidian as far beyond 300 km as it actually went, so some long-distance carriers or visits to the source must
have existed [c].


---

## 3. Early money and Mesopotamian credit

### 3.1 Accounting before writing, money before coins

- **Tokens and writing.** Clay tokens (from about 8000 BC; Denise Schmandt-Besserat's reading, debated) recorded grain and beasts;
  writing at Uruk (about 3300 BC) began as accounts of goods owed and delivered [s].
- **Temple and palace economies.** In Sumer and Ur III (about 2100 to 2000 BC), large institutions owned land, herds and
  workshops, paid workers in rations of barley, oil and wool, and recorded flows in units of account.
- **Two standards.** **Barley** was the unit inside the village and the ration system. **Silver** was the unit of trade, debt and
  fines, weighed out (the shekel, about **8.3 to 8.4 g** [c, x]; 60 shekels to the mina). The Laws of Eshnunna set 1 shekel of
  silver equal to 1 gur (300 sila) of barley [s]. Most transactions were recorded in silver but paid in barley or goods. Silver was
  mainly a **money of account** and a store, not a coin in hand.

### 3.2 Interest and debt

- The Laws of Hammurabi (about 1750 BC) capped interest at **20% a year on silver** and **33⅓% on barley** loans; a creditor who
  charged more lost the loan [c]. Actual rates sometimes ran higher [c]. The barley rate may come from the one-third share of a
  sharecropping rent [c].
- Debt was the main path to dependence: debtors pledged land, then family members, then themselves.
- Kings periodically **cancelled debts** (Old Babylonian *mīšarum* edicts) to restore free farmers who owed military service
  (Michael Hudson's reading) [s].

### 3.3 The Old Assyrian trade (about 1950 to 1750 BC)

The best documented pre-modern trade network before the late Middle Ages:
- **Records:** over **22,000 tablets** of merchants' letters and accounts from the trading quarter (*kārum*) at Kanesh (Kültepe,
  central Anatolia) [c].
- **Goods:** tin (from further east) and fine textiles from Assur, carried to Anatolia and sold for silver and gold, which went back
  to Assur [c].
- **Transport:** black donkeys, each carrying about **65 kg of tin plus some 25 textiles**; caravans of about 15 donkeys; about
  **1,000 km** in six to seven weeks [c]. Tolls and taxes were paid to each kingdom on the way; donkeys were often sold at the end.
- **Margins:** tin sold in Anatolia for roughly twice its price in Assur, before transport, tolls and losses [s, r].
- **Organisation:** family firms with agents posted abroad; long-term joint investment funds (the *naruqqum*, "sack": a dozen or so
  investors pooled gold with a travelling merchant for about ten years, for a share of profit) [s]; consignment and credit; a court
  of the *kārum* and the city assembly at Assur to settle disputes; treaties with Anatolian rulers guaranteeing safety and fixing
  taxes.


---

## 4. Coinage

### 4.1 First coins

| Where | When | What |
|---|---|---|
| Lydia (western Anatolia) | about 630 to 600 BC | lumps of electrum (gold-silver alloy) stamped by the state [s] |
| Greek cities | 6th century BC on | silver coins (the Athenian drachm, the "owl") paid soldiers and builders; agoras with prices |
| China | Zhou period; unified under Qin, 221 BC | bronze spade and knife money, then the round *ban liang* with a square hole [s] |

Coins are pieces of metal whose weight and fineness are **guaranteed by a stamp**, so they need not be weighed or assayed at each
use. That made it cheap to pay large numbers of people who did not know each other: armies, crews and builders. David Graeber and
others tie early coinage to paying soldiers and collecting taxes [s].

### 4.2 Debasement

- **Roman denarius:** close to pure silver under Augustus, it was reduced step by step until by the 260s and 270s it held only a few
  per cent of silver [s, r]. Prices rose; Diocletian's **Edict on Maximum Prices** (301 AD) tried to fix them and failed. The Edict
  also lists freight rates (§7.1).
- **England's Great Debasement** (1544 to 1551): Henry VIII and Edward VI cut the silver standard from 92.5% to a low of about **25%
  in 1551** to pay for war [c]. Prices roughly doubled; the coinage was restored from 1551 to 1560.
- **Gresham's law:** where two coins must pass at the same face value, the one worth less as metal circulates and the better one is
  hoarded or melted.

### 4.3 Money of account and the medieval penny

- Charlemagne's reform (about 794) fixed a system that lasted a thousand years: **1 pound (livre, lira) = 20 shillings (sous,
  soldi) = 240 pence (deniers, denari)**. Only the penny was struck for centuries. The pound and shilling were **units of account**,
  used to reckon debts, rents and prices, not coins.
- **England's money supply grew sharply in the commercial boom.** Mayhew estimated about a 24-fold rise in the currency from 1086
  to 1300 [c]; Bolton's estimates run from 3 to 6 pence per head in 1042 to 1066 to about **65 to 101 pence per head by 1310** [c,
  r], while the population at least doubled.
- **A penny was a lot of money.** Around 1300 an English labourer earned about 1 to 2 pence a day [s, r]. A penny bought a few
  loaves. England struck round halfpennies and farthings only from 1279 [s].

### 4.4 The big problem of small change

Thomas Sargent and François Velde (*The Big Problem of Small Change*, 2002) showed that for centuries European states could not
supply enough small coin. Full-weight silver coins small enough for daily purchases were tiny and costly to mint; token coins of
base metal invited counterfeiting and over-issue. Consequences:
- **Small trades ran on credit,** in kind or by tally, and were settled when the sum reached a coin.
- **Private tokens filled the gap.** English tradesmen issued many thousands of kinds of copper and lead tokens from 1648 to 1672
  until the crown struck copper halfpennies (1672) [s]; again in the 1780s and 1790s until Matthew Boulton's steam-struck copper
  coins (1797) [s].
- **The modern fix** (19th century): token coins whose value comes from the state's promise to exchange them for full money, issued
  by a monopoly mint in limited quantities.

### 4.5 Paper money in China

The first government paper money was issued in Sichuan in the 1020s (the *jiaozi*, taken over by the Song state in 1023 to 1024
from private deposit-receipt houses), where iron coins were too heavy for trade [s]. The Yuan made paper the main currency; over-issue
caused inflation, and the Ming abandoned paper by the mid-15th century and moved to silver by weight [s]. The lesson that recurs
through §9: **paper works while issuers limit it, and fails when they print to pay their own debts.**


---

## 5. Credit and trust

### 5.1 Village credit

In medieval and early modern Europe, **credit, not coin, was the main medium of everyday exchange.**
- **Medieval England:** Chris Briggs (*Credit and Village Society in Fourteenth-Century England*, 2009) found debt the commonest
  civil plea in manor courts. Loans were made in grain, malt and cash between neighbours, often with personal pledges (sureties)
  standing behind the debtor [s].
- **Early modern England:** Craig Muldrew (*The Economy of Obligation*, 1998) argued that almost all buying and selling ran on
  credit, and that **a household's "credit" meant its reputation** for paying, its honesty and its standing. Debt litigation in
  English courts rose to a peak around 1600, at a scale he estimated at roughly one suit for every household in some years [s, r].
  Most suits were a way to record or enforce, not true disputes, and settled before judgement. Litigation fell after about 1690 as
  paper money spread and credit networks changed; small debts of the poor went to new local Courts of Requests [c].
- **The rhythm:** neighbours kept running accounts, in memory, chalk, notches or books, and met to **reckon** at intervals (often at
  the quarter days or after harvest). They then cancelled what they owed each other and settled the balance in coin, goods or a new
  bond. Clearing between neighbours saved coin.

### 5.2 Instruments

| Instrument | What it is | Where and when |
|---|---|---|
| **the tally** | a hazel stick notched for the sum and split lengthwise; each party keeps half, and the halves must match | medieval Europe, villages to the English Exchequer, which used them until 1826; burning the old tallies set fire to Parliament in 1834 [s] |
| **book credit** | a shopkeeper's or craftsman's ledger of what each customer owes | town and village shops from the Middle Ages; the main form in early modern retail |
| **the bond (obligation)** | a sealed written promise to pay, often with a penalty for default (a bond for double the sum) | medieval and early modern England; enforceable at common law |
| **the pledge (pawn)** | a good handed over as security | everywhere; Lombard and Jewish pawnbrokers in medieval Europe; Franciscan *monti di pietà*, charitable pawn banks, from Perugia 1462 [s] |
| **sureties** | neighbours who promise to pay if the debtor does not | manor courts, early modern bonds |
| **the statute merchant and staple** | debts registered before a town official, with fast seizure of goods or the debtor's body on default | England from 1283 and 1285 [s] |

### 5.3 What made promises hold

- **Repetition and reputation:** a person who defaulted lost future credit with everyone who heard, which only works if others hear.
- **Witnesses:** agreements were made before others ("in the presence of") so that they could be proved in court.
- **Local courts:** manor, borough and church courts heard small debts cheaply and fast.
- **Collective liability:** under the **community responsibility system** (Avner Greif), a whole town's merchants were liable for
  one member's debts abroad, and a creditor's town could seize the goods of any of them. This gave towns a reason to police their own
  [s].
- **Merchant coalitions:** Greif argued that the 11th-century **Maghribi traders** of the Cairo Geniza enforced honesty among
  agents by collective boycott of cheats [s]. Jeremy Edwards and Sheilagh Ogilvie, and Jessica Goldberg, answered that the same
  letters show heavy use of public courts and formal contracts [s, x].
- **The state:** in the long run, public courts that enforced contracts between strangers impartially (Douglass North's argument)
  mattered most for trade that reached beyond the village.

### 5.4 Default and its spread

- Chains of credit carried failure from one party to the next. A merchant whose debtors failed could not pay his own creditors.
- **The Florentine houses of the Bardi and Peruzzi** failed in the 1340s after lending heavily to Edward III, who stopped paying
  [s, x: how much the English default alone caused is debated].
- **Philip II of Spain** suspended payments on his debts four times (1557, 1560, 1575, 1596). Mauricio Drelichman and Hans-Joachim
  Voth argue that the Genoese bankers' contracts expected and priced these suspensions [s].
- **Interest rates fell as enforcement improved:** from rates of 10 to 20% or more on medieval commercial loans to about 4% on Dutch
  public debt in the 17th century and 3 to 4% on British government debt in the 18th [s, r].


---

## 6. Markets and fairs

### 6.1 Market charters

- In England from about 1200, a market or fair was a **royal franchise**: a lord, abbey or town bought a charter for a weekly market
  on a set day and a yearly fair on a saint's day [c]. Grants were often conditional on not harming an existing market nearby [c].
- **The proliferation of markets 1200 to 1349** (Richard Britnell): grants peaked in the late 13th century. The *Gazetteer of
  Markets and Fairs in England and Wales to 1516* (Samantha Letters) counts grants for well over a thousand places [c for the
  source; r for the count]. Many new markets were speculative and did not last, and political patronage, not only demand, drove
  grants [c].
- **The lord's profits:** tolls, stall rents, fines in the market court (the fairs' quick "piepowder" court), and dearer land nearby.

### 6.2 Spacing and central places

- **Bracton's rule** (13th-century English law): a new market harmed an old one if it lay within **6⅔ miles**. A reasonable day's
  journey was 20 miles, split into thirds: going to market, doing business, coming home [s].
- **In practice** most English villagers around 1300 lived within a few hours' walk, under about 7 to 10 miles, of a market [s, r]
  (Christopher Dyer, James Masschaele).
- **Central-place theory** (Walter Christaller, 1933; August Lösch, 1940): if buyers walk to the nearest place offering a good,
  places form a hierarchy. Many small centres sell everyday goods (bread, ale, shoes) within short ranges, and fewer large centres
  sell rarer goods (fine cloth, lawyers, spices) to wider hinterlands. On flat, even ground they form hexagons.
- **G. William Skinner's** studies of rural China (1964 to 1965) are the strongest fit: a **standard market town** served about 18
  villages, some 1,500 households, within a few hours' walk. Markets met on a periodic schedule (every few days), staggered so that
  itinerant traders could visit each in turn, and markets nested upward into intermediate and central towns [s].
- **How well it fits medieval Europe:** partly. Market spacing was roughly regular in old-settled lowlands, and the hierarchy of
  village markets, market towns and regional cities is clear. Rivers, coasts, lords' politics and old Roman roads distort the
  pattern, so **a theory of evenly spaced hexagons fits a plain; real places fit rivers**.

### 6.3 What was sold where

| Place | When | What | Who |
|---|---|---|---|
| **weekly market** in a village or small town | one day a week | grain, ale, bread, eggs, poultry, butter, cheese, beasts, wool, small hardware, cheap cloth | peasants selling surplus; hucksters and regrators reselling; local craftsmen |
| **shops** in towns | daily | bread, meat, shoes, ironware, cloth, spices | resident craftsmen and retailers, increasingly on book credit |
| **regional fair** | one to a few weeks a year | horses and cattle (droves), wool clips, cloth in bulk, wine, salt, fish | merchants, dealers, gentry and religious houses buying stores for the year |
| **international fair** (Champagne, later Geneva, Lyon, Frankfurt, Antwerp) | several a year in rotation | fine cloth, spices, silk, furs, leather; above all **settlement of credit** | international merchants and their agents, moneychangers |

### 6.4 The Champagne fairs

- **Six fairs a year in four towns** (Lagny, Bar-sur-Aube, Provins twice, Troyes twice), so that a fair was nearly always running,
  at their height about 1180 to 1300 [c]. None of the four was a major merchant centre in its own right [c].
- Each fair ran several weeks in phases: arrival, a cloth fair, leather and furs, goods sold by weight, then a **settlement** period
  when debts contracted during the fair, and contracts written payable "at the next fair", were cleared. The fairs worked as a
  **clearing house** between Italian and Flemish merchants.
- **What made them work:** Paul Milgrom, Douglass North and Barry Weingast (1990) credited private merchant judges and a "law
  merchant". Edwards and Ogilvie (2012) found **no evidence of a private merchant code**. The counts of Champagne supplied public
  order: a dedicated fair court sitting through each fair, safe-conducts on the roads, guarded halls, fair-keepers who enforced
  judgements, and reprisals pursued through public courts [c].
- **Why they declined (from the 1280s):** the county passed to the French crown in 1285, French kings taxed and fought with
  Flanders, and Genoese galleys opened a sea route to Bruges (1277) [s]. **A market's success depended on the policies of the
  authority that kept it.**

### 6.5 Prices and how fast they converged

Price gaps between two places can stay up to the cost of moving goods between them, plus tolls, risk and the cost of knowing the
price. So convergence measures transport, information and institutions together.
- **Medieval England:** overland transport of wheat around 1300 cost about **0.2s a quarter per 10 miles**, against a wheat price
  of about 6s, so about **3% of value per 10 miles** (Gregory Clark) [c]. James Masschaele put grain carriage at about **0.25% of
  price per km** [c]. Clark and others find that English grain prices moved together across regions by 1300, more so than the
  older view of isolated local markets supposed [s].
- **Europe, 1350 to 1913:** Giovanni Federico, Max-Stephan Schulze and Oliver Volckart (2021), using prices from almost 600 markets,
  found that **convergence was mostly pre-modern**. It began in the late 15th century, advanced fast until the early 17th, stalled
  in the Thirty Years' War, resumed after it, and accelerated after the Napoleonic wars. They tie the differences to institutions
  and to how fast information systems spread [c].
- **The 19th century:** the gap between wheat prices in Chicago and Liverpool fell from about 58% of the Liverpool price in 1870 to
  about 16% by 1913 (Kevin O'Rourke and Jeffrey Williamson) [s]. Transatlantic telegraph news (from 1866) removed most of the gap
  between New York and London cotton prices that came from slow information [s].

### 6.6 Information: how prices and news travelled

| Means | Speed | When | What it carried |
|---|---|---|---|
| word of mouth, travellers, carriers | the speed of walking or riding | always | rumour, prices "last heard" |
| merchants' letters | to Venice about 1500: **one week from Genoa or Munich, two from Marseille or Paris, three from Barcelona or Antwerp** [c] | from the 12th century | prices, exchange rates, ship arrivals, politics; recipients noted days in transit, so speeds are measurable [c] |
| merchant archives | Francesco Datini of Prato (d. 1410) left about 150,000 letters [s] | 14th and 15th centuries | what a firm with a dozen branches knew |
| relay posts | Taxis family posts across the Habsburg lands from 1490; Brussels to Innsbruck in five days (six in winter) [c] | 16th century | letters for anyone who paid |
| printed price currents | weekly lists of commodity prices and exchange rates, Antwerp and Amsterdam from the late 16th century [s] | 1580s on | public prices; anyone could compare places |
| newsletters, newspapers | weekly, then daily | 17th century on | ship news, prices, politics |
| electric telegraph | minutes | 1840s; transatlantic 1866 | prices, orders, transfers |
| internet, electronic exchanges | milliseconds | 1990s on | prices for everyone; algorithmic trading |

**Information as a good:** before printed price lists, whoever knew prices elsewhere made the margin. Public price lists made it
cheap and moved profit from knowing to carrying and financing.


---

## 7. Transport and space

### 7.1 Costs by mode before railways

The single most important fact about pre-industrial space: **bulk moved cheaply only on water.**

| Era and source | Road | River | Sea | Notes |
|---|---|---|---|---|
| **Roman Empire, Diocletian's Edict (301 AD)** | wheat carried 100 Roman miles by land cost about **55%** of its value | river freight about **5 times** sea freight [c] | wheat carried 100 miles by sea, about **1.3%** of its value [c] (Richard Duncan-Jones) | the often-quoted ratio sea : river : land = 1 : 4.9 : 28 to 56 is not confirmed here [x]; the Edict gave maximum, not market, rates |
| **England about 1300** | about 3% of wheat value per 10 miles (Clark) [c]; about 1 to 1.5 pence per ton-mile [r: converted from Clark, a quarter ≈ 0.2 t] | Thames grain from Wargrave to London (about 70 river miles) at about 3.3d a quarter [c], about 0.25d per ton-mile [r] | coastal wheat at about 10 to 10.5d a quarter, excluding tolls (distance varies) [c] | Masschaele argued medieval road haulage was relatively cheap, not prohibitive [c] |
| **rough medieval ratio** | 1 | about 1/4 to 1/2 | about 1/5 to 1/10 | [r, x] varies with route, season, goods and loading costs |

**Load and speed by mode, pre-industrial** [s, r unless marked]:

| Mode | Load | Speed per day | Notes |
|---|---|---|---|
| a person on foot | 20 to 40 kg | 20 to 30 km | porters in Africa and the Andes carried about this for long distances |
| a donkey | 50 to 70 kg | 20 to 30 km | Old Assyrian donkeys about 65 kg of tin plus textiles [c] |
| a pack horse or mule | 100 to 150 kg | 25 to 35 km | strings of 20 to 40 in upland England until the 18th century |
| a camel | 150 to 250 kg | 30 to 40 km | displaced wheeled transport in the Middle East and North Africa from late antiquity (Richard Bulliet) |
| a two-wheeled cart, one horse | 0.3 to 0.5 t | 25 to 35 km | horses replaced oxen in English haulage from the 12th century (John Langdon) |
| an ox cart or ox wagon | 0.5 to 1 t | 15 to 20 km | cheaper beasts, slower; oxen eat grass, horses oats |
| an 18th-century stage wagon | 3 to 4 t, 6 to 8 horses | 30 km | turnpike roads |
| a river barge | 10 to 50 t | 20 to 40 km downstream; slow and towed upstream | often by horse or men on a towpath |
| a medieval cog (Hanse) | about 100 to 200 t | 100 to 150 km in fair wind | seasonal; winter sailing stopped in the Baltic |
| a 17th-century Dutch fluyt | 200 to 500 t, small crew | similar | cheap bulk carrier; part of why Amsterdam won the Baltic grain trade |
| a courier relay | a letter | 100 to 200 km | the Mongol *yam*, the Roman *cursus publicus*, the Taxis post |

### 7.2 Roads, bridges, fords, tolls and inns

- **Roads** were mostly rights of way, not built surfaces, after the Roman roads decayed. A road was where people had the right to
  pass. Parishes had to repair their roads (England from 1555), and did it badly. **Turnpike trusts** (England from 1663, mostly
  1700 to 1830) charged tolls to pay for surfaced roads. Journey times fell sharply: London to Manchester or Edinburgh by coach fell
  by about three quarters between the 1750s and the 1830s [s, r].
- **Bridges and fords** decided routes. England saw a wave of bridge building in the 12th and 13th centuries, paid by lords, towns,
  religious guilds and pontage tolls [s]. Towns grew at the **lowest bridging point** of rivers (London, Rouen, Cologne), at fords
  and at the **head of navigation**.
- **Tolls** were the lord's or town's rent on movement: pontage (bridges), murage (walls), pavage, market tolls, and river tolls.
  The Rhine had dozens of toll stations by the late Middle Ages, enough to make river transport much dearer than it needed to be
  [s, r]. Freedom from tolls was one of the most valued privileges a town or merchant guild could win.
- **Inns** were the infrastructure of trade: lodging for people, stabling for beasts, storage for goods, and a place to hear news
  and meet buyers. The English 1686 War Office survey counted inns able to lodge tens of thousands of travellers and stable many
  more horses [s, r].
- **Security:** brigands, war and seizures cost as much as feed; safe-conducts, convoys and the king's peace were paid-for public goods.

### 7.3 How transport costs set the size of markets

- **Value per weight decides distance.** At about 3% per 10 miles, grain could go 30 miles by road before adding about 10% to its
  price, and much further by water. **Overland firewood paid only up to about 18 to 20 km** around London in the early 14th century,
  and less after the Black Death as carriage costs rose (James Galloway, Derek Keene and Margaret Murphy, 1996) [c]. Silver,
  spices, silk and fine cloth could pay for thousands of miles; wool, wine, salt and salt fish for hundreds by water; grain for tens
  by land or hundreds by water; hay, stone, firewood and manure only locally.
- **London's grain hinterland about 1300** (Bruce Campbell, Galloway, Keene and Murphy, 1993) reached much further along the Thames
  and the coast than over land [c for the study].
- **Adam Smith's point** (1776): the division of labour is limited by the extent of the market, and water carriage opens far wider
  markets than land carriage, which is why the first civilisations grew along rivers and coasts.

### 7.4 Von Thünen's rings

Johann Heinrich von Thünen (*The Isolated State*, 1826) asked what a farmer should produce at each distance from a single town on a
featureless plain. The answer is rings, ordered by how costly each product is to carry relative to its value per acre:
1. **market gardening and dairy** nearest (perishable, heavy, high value per acre);
2. **forestry** next (wood is heavy and the town burns a great deal of it, so it must be close; the surprising ring);
3. **crop farming**, with more intensive rotations nearer and longer fallows further;
4. **livestock grazing** furthest (animals walk to market);
5. wilderness beyond.

A navigable river stretches the rings along its course. London's hinterland around 1300 fits the pattern well: intensive mixed
farming and wood near the city and the river, grain from further along the Thames, and cattle driven in from far off [c, r].

### 7.5 The industrial and modern transport revolutions

| Step | When | What changed | Numbers |
|---|---|---|---|
| **canals** | Bridgewater 1761; English canal mania 1790s; Erie Canal 1825 | water where there was none | Bridgewater roughly halved Manchester's coal price [s]; Erie Canal (363 miles, Albany to Buffalo) cut freight from Buffalo to New York from about **$100 to about $10 a ton** [c, x: estimates run $90 to $125 before, $4 to $10 after], and the journey from about three weeks to one week or less [c, x] |
| **railways** | Liverpool and Manchester 1830; US network from the 1830s | cheap land transport, all year, fast | US average rail freight **2.58 cents a ton-mile in 1859** (Albert Fishlow) [c], against roughly 15 to 25 cents for wagons [s, r]; Robert Fogel's counterfactual put the "social saving" of rails in 1890 at only a few per cent of GNP, because canals and rivers were the alternative [s, x] |
| **steamships, iron and steel hulls** | from the 1850s; Suez Canal 1869 | ocean freight fell; schedules became regular | transatlantic transport costs fell about **41 to 70%** from the mid-19th century to 1913 (pooled North, Isserlis and Harley data) [c]; tramp shipping rates roughly halved from the early 1870s to the early 1910s [c]; Knick Harley credits iron hulls and steam [c] |
| **trucks and highways** | 1920s on; US Interstate system 1956 | door to door; factories leave railheads | [s] |
| **the container** | Ideal-X, Newark to Houston, April 1956, 58 containers [c]; ISO standard sizes from the late 1960s | handling costs collapsed; ships, trains and trucks share one box | loading loose cargo **$5.83 a ton** against **about 16 cents** by container (Marc Levinson, *The Box*) [c] |
| **air freight** | jet freighters from the 1960s | speed for high-value goods | the cost of air freight fell about **an order of magnitude** from 1955 to 2004 (David Hummels) [c]; air carries a large share of world trade by value but under 1% by weight [s] |
| **modern logistics and supply chains** | 1970s on: just-in-time, barcode, global value chains, e-commerce | parts cross borders many times; inventory becomes flow | the 2021 container squeeze and the Suez blockage (*Ever Given*, March 2021) showed how tightly coupled the system had become [s] |

**Modern costs per tonne-km, order of magnitude** (US-centred, 2020s): ocean vessels about **0.4 cents** (container about 0.5),
barge about **1 cent**, rail about **4 cents**, long-haul truck about **12 cents**, air about **84 cents** [c, r] (Krammer et al.
2025 for air and ocean; ICCT for barge, rail and truck). The ordering **sea < river < rail < road < air** is the same as in the Roman
Edict. What changed is the level: ocean freight is now so cheap that distance barely matters for most manufactured goods, while
**time, handling, borders and reliability** became the costs that shape trade.


---

## 8. Merchants and the organisation of trade

### 8.1 Who moved goods

| Kind | What they did | Era |
|---|---|---|
| **pedlars and chapmen** | walked village to village with a pack of small wares (pins, ribbons, needles, cheap print) | all periods; a mass trade in 17th to 18th century England |
| **carriers** | ran regular wagon or pack services on fixed days between a town and London or the county town; carried goods and letters for anyone who paid | England from the 16th century; listed in printed carrier guides from 1637 [s] |
| **drovers** | walked cattle and sheep hundreds of miles from Wales, Scotland and the uplands to fattening grounds and London | medieval to 19th century |
| **merchants** | bought in bulk in one place to sell in another; financed the trade; kept agents and correspondents | from Assur to Amsterdam |

### 8.2 Partnerships and firms

- **The commenda** (Italian, from the 11th century; Islamic *qirāḍ* and Jewish *ʿisqa* came before it): a sedentary investor
  provided capital, a travelling merchant took the goods on a voyage. If the investor put up all the capital, the traveller usually
  took about **a quarter of the profit**; in the **societas maris** (Genoa) or *colleganza* (Venice) the investor put up two thirds,
  the traveller one third and his labour, and they **split profit equally** [s]. Losses fell on capital; the traveller lost only his
  work. The Genoese notary Giovanni Scriba's register (1154 to 1164) holds hundreds of these contracts [s]. One merchant could hold
  shares in many voyages at once, which **spread risk**.
- **The compagnia** (Florence, 13th to 15th century): partners with unlimited liability running branches across Europe (the Bardi,
  Peruzzi, later the Medici, whose bank had branches from London to Rome). It used **double-entry bookkeeping** (Genoa's city
  accounts by 1340; Luca Pacioli's printed description 1494) [s].
- **The joint-stock company:** the English East India Company (1600) and the Dutch **VOC (1602)**, whose permanent capital and
  transferable shares were traded on the Amsterdam exchange [s]. Limited liability by general law came much later (Britain 1855 to
  1862) [s].

### 8.3 Merchant guilds and the Hanse

- **Merchant guilds** (gilds merchant) held town charters, controlled who could trade retail in the town, set terms for outsiders,
  and negotiated privileges abroad. Sheilagh Ogilvie (*Institutions and European Trade: Merchant Guilds, 1000 to 1800*, 2011)
  argues that their main effect was to capture rents for members through monopolies and exclusion, not to solve problems of trust
  [s, x].
- **The Hanseatic League** was a loose association of North German and Baltic towns and their merchants, from the 13th to the 17th
  century. At its height in the 14th century it had **over 100, by some counts about 200, participating towns**; no official member
  list was ever kept [c, x].
  - **Kontore** (privileged trading stations): the Steelyard in London, Bruges, Bergen and Novgorod.
  - **Goods:** Baltic grain, timber, furs, wax and pitch west; Flemish and English cloth, salt (Lüneburg, then the Bay of Bourgneuf),
    herring and Norwegian stockfish, and wine in other directions.
  - **Tools:** the cog, then the hulk; Lübeck law shared across member towns; **trade embargoes** against rulers who broke their
    privileges (Flanders, 1358); war when embargoes failed (against Denmark, ending in the Peace of Stralsund, 1370) [s].
  
### 8.4 Comparative advantage and specialisation in practice

David Ricardo (1817) showed that two countries gain from trade when each makes what it is **relatively** best at, even if one is
better at everything; his example was English cloth for Portuguese wine. In medieval and early modern Europe specialisation followed
land, water and skill:

| Region | Specialised in | Traded to | For |
|---|---|---|---|
| England | raw wool (tens of thousands of sacks a year around 1300 [s, r]), later woollen cloth | Flanders, Italy | cloth, wine, luxuries, cash for the crown's taxes |
| Flanders and Brabant | fine woollen cloth from English wool | all Europe | wool, food, money |
| Gascony | wine | England, the Low Countries | grain, cloth, fish |
| Baltic lands (Poland, Prussia) | grain, timber, flax, potash | Amsterdam (the "mother trade") | cloth, salt, herring, colonial goods |
| Norway | stockfish | Hanse (Bergen) | grain |
| northern Italy | silk, banking, shipping, re-export of eastern goods | Europe | wool, metal, cash |
| Bay of Bourgneuf, Lüneburg, Cheshire | salt | the North Sea and the Baltic | food, cash |

Each case needed cheap water transport (or high value per weight), steady demand, credit to carry stock to sale, and a guarantor
of merchants' rights abroad. It also made regions fragile: a war that closed the Sound cost a region its market and its food.

---

## 9. Banking and finance: from moneychangers to digital money

### 9.1 Early banks and bills of exchange

- **Moneychangers** at fairs and in Italian towns exchanged coins of many mints and began to hold deposits. Deposit bankers in
  Genoa and Venice by the 12th to 13th century made **transfers between accounts on spoken order** (giro), so merchants could pay
  each other without moving coin [s].
- **The bill of exchange** (from the 13th century): a merchant in Florence pays florins to a banker, who writes to his
  correspondent in Bruges to pay the equivalent in local money to the merchant's agent at a set date (the usance, often one to
  three months depending on the distance) [s]. It combined **transfer of funds across distance, exchange of currencies, and credit**.
  Because the rate built in the time, it also let bankers earn interest without breaking the church's ban on usury.
- **Exchange fairs** (the Genoese "Besançon" fairs, held at Piacenza from 1579) existed only to clear bills, four times a year [s].
- **Endorsement and discounting** of bills (Antwerp, 16th century) made them transferable and close to money [s].

### 9.2 Public banks and central banks

| Bank | Year | What it did |
|---|---|---|
| **Bank of Amsterdam** (Wisselbank) | 1609 | took coin of uncertain quality and credited accounts in a stable **bank money** that traded at a premium (the agio); large bills had to be paid through it [s] |
| Riksbank | 1668 | the oldest surviving central bank [s] |
| **Bank of England** | 1694 | founded on a £1.2 million loan to the government; banknotes; later lender of last resort [s] |
| Federal Reserve | 1913 | after the panic of 1907 [s] |

- **Goldsmith-bankers** (17th-century London) lent more than they held: fractional-reserve banking, and runs.
- **The lender of last resort:** Walter Bagehot's rule (*Lombard Street*, 1873): in a panic, lend freely to solvent banks, against
  good collateral, at a high rate.
- **Public debt:** the Dutch Republic and, after 1688, Britain borrowed long-term at low rates against taxes voted by a parliament.
  That **financial revolution** let them outspend larger rivals in war (North and Weingast, 1989; John Brewer's "fiscal-military
  state").

### 9.3 Standards: gold, Bretton Woods, fiat

- **Britain** moved onto gold de facto in 1717 (Isaac Newton set the gold guinea's value high, so silver left the country) and by law
  in 1816 to 1821 [s].
- **The classical gold standard** (about 1870s to 1914): most trading nations fixed their currency to gold. Exchange rates were
  stable and capital flowed freely, but money supply depended on gold mining, and deflation and bank crises recurred.
- **Bretton Woods** (1944): currencies pegged to the dollar, the dollar convertible to gold for central banks; the IMF and World
  Bank. **The US closed the gold window on 15 August 1971**; floating rates followed from 1973.
- **Fiat money** since: currency backed by nothing but the state's acceptance of it for taxes and the central bank's management.
  Inflation targeting by independent central banks spread from New Zealand (1990) [s].

### 9.4 Stock markets and modern finance

- **Amsterdam's bourse** traded VOC shares from 1602, with forwards and options within decades. London's stock brokers met in
  coffee houses (Jonathan's) before forming the Stock Exchange (1801); New York's brokers signed the Buttonwood Agreement in 1792 [s].
- **Bubbles** came with them: the Mississippi and South Sea schemes (1720), railway mania (1840s), 1929, 2000, 2008.
- They added **capital pooled from many savers for long-lived works**, and **liquidity**: a share can be sold without the firm repaying.

### 9.5 Payment systems and digital money

| Step | When | What it changed |
|---|---|---|
| cheques and bank clearing houses | London clearing house from the 1770s [s] | banks net their claims daily instead of moving coin |
| telegraphic money transfer | Western Union from 1871 [s] | money across a continent in hours |
| credit and charge cards | Diners Club 1950, BankAmericard 1958 [s] | consumer credit at the point of sale |
| SWIFT messaging between banks | founded 1973 [s] | standard cross-border payment messages; in 2025 about **15.1 billion messages**, an average of **59.8 million per business day** [c] |
| cards and wallets | 2024: contactless card spending about **$10.4 trillion over 456.6 billion transactions** [c] | most retail payments in rich countries become electronic |
| mobile money | M-Pesa, Kenya, 2007 [s] | payments by phone for people without bank accounts |
| instant account-to-account payments | India's UPI from 2016: **about 25.5 billion transactions in October 2026** [c] | free, instant retail payments at national scale |
| cryptocurrency | Bitcoin, 2009 | a ledger kept by no single party; mostly a speculative asset |
| central bank digital currencies | e-CNY pilots from 2020 [s] | state money as a digital account |

The long arc runs from **settling in goods** to **settling in metal** to **settling in claims on a trusted ledger**: the temple's
accounts, the banker's book, the central bank's reserves, the payment network's database. Each step lowered the cost of paying across
distance and between strangers, and moved the trust from the person paying to whoever kept the ledger.

---

## 10. What each step needed and what it enabled

| Step | Needed (goods, institutions, information, security) | Enabled next |
|---|---|---|
| gift and reciprocity | lasting relations; memory | alliances; insurance; safe meetings for barter |
| down-the-line exchange (obsidian, shell) | valued, durable materials; contact between neighbouring groups | prestige hierarchies; knowledge of distant sources |
| redistribution (chief, temple, palace) | storage; a centre; tallies and records | units of account; rations as wages; big works; writing |
| silver as money of account; interest | a metal valued everywhere; scales; laws; scribes | long-distance partnerships; debt bondage; debt cancellation as politics |
| coinage | mines, mints, a trusted stamp; taxes paid in coin | paid armies; money rents; retail markets; comparable prices |
| village credit (tallies, books, bonds) | witnesses; local courts; reputation that others hear | trade without coin; smoothing over seasons; clearing between neighbours |
| chartered markets and fairs | a lord or town to grant and police them; weights and measures; roads | specialisation by village and craft; towns; visible prices |
| merchant partnerships (commenda, compagnia) | written contracts; notaries; courts that enforce them | pooled capital and spread risk; branch networks; double entry |
| bills of exchange and deposit banks | correspondents in many towns; letters; trust between bankers | moving funds without coin; credit across borders; clearing fairs |
| public banks, public debt | taxes voted by assemblies; stable bank money | cheap state borrowing; banknotes; central banks |
| canals and turnpikes | capital from investors and tolls; acts of parliament | cheap bulk transport inland; coal for industry |
| railways and steamships | coal, iron, engineering, large companies | national and world markets; price convergence |
| the gold standard | gold reserves; convertibility; capital mobility | stable exchange rates; the first globalisation |
| the telegraph | wire, batteries, cables | prices known everywhere in minutes; futures markets |
| fiat money and central banking | trusted institutions; statistics | active monetary policy; inflation risk |
| containers, trucks and air freight | standards; ports; highways; airports | global supply chains |
| digital payments | networks; phones; regulation | instant payment between anyone, at near zero cost |

---

## 11. What a simulator could take from this

The engine now has: offers and agreements made of legs (goods, coin, work, repeated payments), settled automatically when both
parties are at one node; prices known only as witnessed or told (D2-29); copper coin struck by smiths (D2-28); markets as seeded
custom with no mechanism (D2-30); carriers on roads measured in days, with capacities of 10 on foot, 20 with a pack, 60 with a pack
ox, 40 with a handcart and 300 to 400 with an ox cart (D2-135). The runs show balanced reciprocity, spot barter and work debts, and
almost no third-party reputation (38.68).

### 11.1 What would most change agents' economic life, in order

1. **Promises enforced by people, not the engine (OPEN L-106).** History's main point about credit is that it rests on witnesses,
   reputation and courts. Today the engine pays a goods debt automatically when the debtor holds the goods, so credit needs no
   trust, and the runs show trust-like behaviour only where the engine leaves a gap (work debts). Two pieces would turn on the
   history of §5:
   - **defaults seen by witnesses** as a sign (a debt "due and unpaid", by the senses guide), so reputation can spread;
   - **goods credit paid by choice**, with remedies by a person: sureties named in the agreement, a court or arbiter institution,
     the pledge (collateral) leg the presets already name.
   This is the experiment 38.68 proposed; it is the gate to everything from §5 on.
2. **Prices that travel and age.** D2-29 already has prices as dated beliefs. What history adds:
   - **carriers bring price news** from where they have been, so the trader with the freshest news makes the margin;
   - **a posted price at a market day** (a board, a crier, a price current kept by an institution), so information becomes a good
     someone can supply, and price gaps between nodes can be measured against transport cost (§6.5).
   The measure: do price gaps between villages fall to roughly the cost of carrying between them?
3. **A market day at a central node,** as a coordination device rather than a building. The value of a market is that everyone
   knows **when** and **where**: a weekly day, a yearly fair, a charter granted by whoever holds the place, with a stall rent or toll
   (D2-30 allows it) and a court for the day. Test whether agents converge on it unprompted, and whether a second market close to the
   first fails (Bracton's 6⅔ miles).
4. **Transport cost felt as days times load, with water far cheaper than land.** The engine has the ladder on land. The single
   biggest historical lever missing is the **boat** (02zzh §3.9: later). A river edge that carries ten times a cart's load for a
   fraction of the days would create the town-on-the-river pattern, von Thünen's rings stretched along water, and a reason to fight
   over the ford, the bridge and the toll. Value-to-weight thresholds will then decide what is worth carrying, as in §7.3.
   - Check: a pack beast carried 3 to 4 times a person and a cart 15 to 30 times; the engine's 6 and 30 to 40 are plausible [r].
5. **Book credit with reckoning days.** Running accounts between households, cleared at set days (quarter days, after harvest)
   with the balance paid in goods or coin, are what village economies actually ran on. The engine's ledgers (D2-33) and release
   (D4-37) are most of it; a "reckon" act that nets two households' open agreements against each other would complete it.
6. **The small-change problem as a design choice.** If one coin is worth a day's food or more, agents will keep using credit and
   kind for small trades, as medieval villagers did; if it is worth a loaf, coin will take over. Coin's value relative to daily
   needs (a calibrate parameter in money_and_markets.md) should be set on purpose, and the null arm should be read with it in mind.
7. **The commenda as a preset.** "Capital from one, travel by another, profit shared by a rule" fits the existing carrier and
   consignment presets with one more leg (a share of proceeds). It lets a household with goods and no time trade far through a
   carrier with time and no goods, which is how merchant capital first formed.
8. **Tolls at chokepoints and safety on roads.** A toll at a bridge or ford is the oldest rent on movement and a ready source of
   lordship (02zzi §3.3); danger per edge (OPEN C-6) is what made convoys, safe-conducts and the "king's peace" worth paying for.

### 11.2 What to leave out

- **Engine-set prices, market clearing and auctions by rule.** History's markets formed prices through haggling between people with
  partial information; the engine's rule that it never states a price (D2-29) is right.
- **Central banks, fiat regimes, stock markets, derivatives and modern payments.** They need populations, institutions and records
  far beyond a region of villages. They belong in the frame, not the build.
- **Railways, steamships, containers and air freight.** Past the organic economy's edge (02zzi §3.8).
- **Imposed central-place hexagons or von Thünen rings.** Both should emerge from transport cost and demand, or not at all; they
  are measures to read a run against, not layouts to seed.
- **Polanyi's categories as mechanics.** Reciprocity, redistribution and markets are what agents already do with give, store and
  offer; give them the conditions (distance, a centre, a market day, enforcement) and read which form wins.
- **Bills of exchange and paper money, for now.** They need correspondents at several distant nodes and ledgers that trust each
  other ("letters of credit between ledgers: later", agreements.md). They are the right next step only once merchants already work
  between towns.

### 11.3 Measures to read against the null arm

- the share of exchange in gifts, spot barter, credit and coin, by the social distance of the parties (Sahlins's scale);
- price gaps between nodes against the cost of carrying between them, over time;
- whether a market day forms, and how many households come to it from how far;
- how many defaults are known to third parties, and whether lenders refuse known defaulters;
- the longest distance goods travel, by value per weight;
- whether a carrier or merchant household forms and lives by margin.

---

## Sources

Checked in this session [c] (by web search; full texts were not reachable from the session, so figures are as reported by these
sources or their abstracts):
- Renfrew, C., Dixon, J. E. and Cann, J. R. (1964 to 1968), obsidian sourcing; summarised in EBSCO Research Starters, "Renfrew,
  Dixon, and Cann Reconstruct Ancient Near Eastern Trade Routes"; mapaspects.org, "Quantitative approaches to regional exchange"
  (300 km supply zone, over 80%, exponential fall-off); critiques in *Journal of Archaeological Method and Theory* (2014,
  agent-based model) and later papers.
- Laws of Hammurabi on interest (20% silver, 33⅓% barley): Biblical Archaeology Society, "Ancient interest rates"; Michael Hudson,
  "How interest rates were set, 2500 BC to 1000 AD" (2000).
- Kültepe/Kanesh: Livius.org, "Kaneš (Kültepe)"; Metropolitan Museum of Art, caravan account tablets; donkey loads and journey
  times from secondary summaries.
- Great Debasement fineness: Royal Mint, "Debasement and Tudor coinage"; Wikipedia, "The Great Debasement".
- Bolton, J. L., *Money in the Medieval English Economy 973 to 1489* (2012), reviewed by John Munro on EH.Net; Allen, M. (2015) in
  the Mayhew festschrift *Money, Prices and Wages*, on Mayhew's 24-fold estimate.
- Muldrew, C., "Credit and the courts" (*Economic History Review* 46, 1993) and a 2025 Cambridge chapter on the decline of
  litigation after 1690.
- Centre for Metropolitan History, *Gazetteer of Markets and Fairs in England and Wales to 1516* (Letters), introduction; Kent
  Archaeological Society, "Factors in market establishment in medieval England: the evidence from Kent 1086 to 1350"; Britnell,
  R. H., "The proliferation of markets in England, 1200 to 1349", *Economic History Review*.
- Edwards, J. and Ogilvie, S., "What lessons for economic development can we draw from the Champagne fairs?", *Explorations in
  Economic History* 49 (2012); CEPR VoxEU column.
- Clark, G., "Markets and economic growth: the grain market of medieval England" (working paper, UC Davis, 2001): 0.2s per quarter
  per 10 miles against 6s wheat.
- Masschaele, J., "Transport costs in medieval England", *Economic History Review* 46 (1993): about 0.25% per km; road haulage
  relatively cheap (as summarised by Ballaux and Blondé).
- Galloway, J., "London and the grain trade of England" (SAS-Space): Thames costs per quarter; Campbell, B. M. S., Galloway, J. A.,
  Keene, D. and Murphy, M., *A Medieval Capital and its Grain Supply* (1993); Galloway, Keene and Murphy (1996) on firewood, cited in
  *LAMAS* 50, "Metropolitan market networks".
- Federico, G., Schulze, M.-S. and Volckart, O., "European goods market integration in the very long run: from the Black Death to
  the First World War", *Journal of Economic History* 81 (2021).
- Courier times to Venice about 1500 and Brussels to Innsbruck: Tim Parks, "Couriers before the Net"; Congdon, E., on transit
  notations in merchant letters (Manuscript Evidence, 2024).
- Diocletian's Edict: Thayer Watkins (San José State) citing Duncan-Jones (55% by land against 1.3% by sea per 100 miles); MIT
  working paper on river at about five times sea; Scheidel, W., "ORBIS prices" (2013).
- Erie Canal: Britannica; American Heritage, "Moving freight"; Transport Geography; EBSCO; Baruch College NYC data.
- Fishlow's 1859 rail rate and Fogel's social saving: *Journal of Economic History* debate ("Notes on the social saving
  controversy"; "United States transport advance and externalities").
- Harley, C. K., "Ocean freight rates and productivity, 1740 to 1913", *Journal of Economic History* 48 (1988); University of
  Copenhagen working paper 02-02 (41 to 70% fall); Hatton, IZA discussion paper (tramp rates halved).
- Levinson, M., *The Box* (2006), as reported in reviews ($5.83 against 15.8 cents a ton; Ideal-X, 58 containers).
- Hummels, D., "Transportation costs and international trade in the second era of globalization", *Journal of Economic
  Perspectives* 21 (2007); ITF/OECD forum paper (2009).
- Krammer et al. (2025), *npj Sustainable Mobility and Transport* (air and ocean cost per tonne-km); ICCT (barge, rail, truck).
- Hanseatic League membership: Britannica, "The league in its final form"; hanse.org.
- SWIFT Annual Review 2025 (15.1 billion messages, 59.8 million per business day); Global Payments Report 2026 (contactless 2024);
  NPCI data via Entrepreneur India (UPI, October 2026).

Standard works, not re-checked here [s]:
- Polanyi, K., *The Great Transformation* (1944); Polanyi, Arensberg and Pearson (eds.), *Trade and Market in the Early Empires*
  (1957); Sahlins, M., *Stone Age Economics* (1972); Malinowski, B., *Argonauts of the Western Pacific* (1922); Mauss, M., *The
  Gift* (1925); Humphrey, C., "Barter and economic disintegration", *Man* (1985); Graeber, D., *Debt: The First 5,000 Years*
  (2011); Granovetter, M., "Economic action and social structure" (1985); Temin, P., *The Roman Market Economy* (2013); Wiessner,
  P., on hxaro.
- Schmandt-Besserat, D., *Before Writing* (1992); Veenhof, K. R. and Larsen, M. T. on Old Assyrian trade.
- Sargent, T. and Velde, F., *The Big Problem of Small Change* (2002); Spufford, P., *Money and its Use in Medieval Europe* (1988);
  von Glahn, R., *Fountain of Fortune* (1996) on Chinese paper money.
- Briggs, C., *Credit and Village Society in Fourteenth-Century England* (2009); Muldrew, C., *The Economy of Obligation* (1998);
  Greif, A., *Institutions and the Path to the Modern Economy* (2006); Goldberg, J., *Trade and Institutions in the Medieval
  Mediterranean* (2012); Drelichman, M. and Voth, H.-J., *Lending to the Borrower from Hell* (2014); Homer, S. and Sylla, R., *A
  History of Interest Rates*.
- Christaller, W., *Die zentralen Orte in Süddeutschland* (1933); Lösch, A. (1940); Skinner, G. W., "Marketing and social
  structure in rural China", *Journal of Asian Studies* (1964 to 1965); Dyer, C., *Making a Living in the Middle Ages* (2002);
  Masschaele, J., *Peasants, Merchants, and Markets* (1997).
- Milgrom, P., North, D. and Weingast, B., "The role of institutions in the revival of trade", *Economics and Politics* (1990);
  North, D. and Weingast, B., "Constitutions and commitment" (1989); Brewer, J., *The Sinews of Power* (1989).
- von Thünen, J. H., *Der isolierte Staat* (1826); Smith, A., *The Wealth of Nations* (1776); Ricardo, D., *Principles of
  Political Economy and Taxation* (1817).
- Langdon, J., *Horses, Oxen and Technological Innovation* (1986); Bulliet, R., *The Camel and the Wheel* (1975); Bogart, D. on
  turnpikes; O'Rourke, K. and Williamson, J., *Globalization and History* (1999); Garbade, K. and Silber, W. on the telegraph and
  price convergence (1978).
- Lopez, R. S. and Raymond, I., *Medieval Trade in the Mediterranean World* (1955), on the commenda; de Roover, R., *The Rise and
  Decline of the Medici Bank* (1963); Ogilvie, S., *Institutions and European Trade: Merchant Guilds, 1000 to 1800* (2011);
  Dollinger, P., *The German Hansa* (1970).
- Bagehot, W., *Lombard Street* (1873); Eichengreen, B., *Globalizing Capital* (1996); Quinn, S. and Roberds, W. on the Bank of
  Amsterdam.

In the project: 02zzi, 02zzh §3.9 and §3.12, 38.68, `docs/cybertron2/spec/economy/agreements.md`, `money_and_markets.md`,
`transport.md`; OPEN L-106 (enforcement), C-1 (capacities), C-6 (danger per edge); D2-1, D2-25 to D2-30, D2-33, D2-135, D4-37.

*Current as of 15 Nov 2026.*
