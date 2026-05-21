# Awesome LLMs for Political Strategy, Geopolitics, and Decision-Making

A curated guide to large language models for political strategy, geopolitics, policymaking, strategic studies, and high-stakes decision-making.

The README is intentionally a curated route through the literature. The full bibliography remains available in [`docs/full-bibliography.md`](docs/full-bibliography.md) and `data/processed/thematic_papers.csv`.

Current coverage: **378 papers** in the full bibliography; **159 Core/Important papers** highlighted on this page.

Citation counts are from the Semantic Scholar Graph API, collected on 2026-05-21.

## Contents

- [What Belongs Here](#what-belongs-here)
- [Reader Guide](#reader-guide)
- [Start Here](#start-here)
- [Papers by Theme](#papers-by-theme)
- [Data and Collection](#data-and-collection)
- [Contributing](#contributing)

## What Belongs Here

A paper belongs in this repository if it satisfies at least one of these tests:

- It directly studies LLMs or LLM agents in politics, geopolitics, policymaking, strategic studies, diplomacy, forecasting, wargaming, public opinion, or high-stakes decision-making.
- It provides a benchmark, dataset, evaluation method, or empirical application for political or strategic LLM behavior.
- It is a foundational political-science, IR, strategic-studies, intelligence-analysis, or forecasting work needed to interpret LLM-for-strategy research.
- It is a classical political NLP, text-as-data, or event-data paper that current LLM methods build on.

Out of scope: finance-only LLMs, trading systems, stock prediction, portfolio management, generic financial benchmarks, generic foundation-model papers, and generic safety papers without a direct political, policy, geopolitical, or strategic-decision link.

Importance labels:

- `Core`: field-shaping work or necessary background.
- `Important`: strong empirical, methodological, benchmark, dataset, or research value.
- `Curated`: relevant but not essential for the public README route.
- `Watchlist`: recent, low-citation, unresolved, or borderline work kept for review in the full bibliography.

## Reader Guide

- New to the area: start with Foundations and Theory, then Forecasting and Foresight, then Geopolitics, Diplomacy, and Wargaming.
- Building benchmarks or agents: use Forecasting, Strategic Reasoning, Diplomacy, Wargaming, and Social Simulation.
- Studying democratic effects: use Public Opinion, Elections, Persuasion, and Policy and Governance Support.
- Looking for data sources: use Political Text and Measurement plus `data/processed/thematic_papers.csv`.
- Checking long-tail coverage: use [`docs/full-bibliography.md`](docs/full-bibliography.md).

## Start Here

- [Perception and Misperception in International Politics](https://www.semanticscholar.org/paper/4339c93c91e296e34ce08cb3555e48d6244ac0f8) (1976) - Core; citations: 2913. Classic baseline for interpreting misperception, signaling, and crisis reasoning.
- [Arms and Influence](https://www.semanticscholar.org/paper/c4a1ff7f04858b2869298b99de53b906361b538f) (1966) - Core; citations: 2033. The core coercion and bargaining frame behind much of the escalation literature.
- [Rationalist Explanations for War](https://www.semanticscholar.org/paper/505ed8c92f0b1ca9afdccdf4890f4e79415ee788) (1995) - Core; citations: 3515. Canonical account of war through information problems, incentives, and commitment problems.
- [Essence of Decision: Explaining the Cuban Missile Crisis](https://www.semanticscholar.org/paper/fac3a8649c09224e1167a6ea403886f99899133d) (1971) - Core; citations: 3145. Foundational decision-making models for crisis behavior and bureaucratic politics.
- [Text as Data: The Promise and Pitfalls of Automatic Content Analysis Methods for Political Texts](https://www.semanticscholar.org/paper/b9921fb4d1448058642897797e77bdaf8f444404) (2013) - Core; citations: 2987. Methodological bridge from political text measurement to current LLM annotation and scaling work.
- [Conflict and Mediation Event Observations (CAMEO): A New Event Data Framework for the Analysis of Foreign Policy Interactions](https://www.semanticscholar.org/paper/775d7f7262ffb42972e5b87a245bc4b63c20396d) (2002) - Core; citations: 189. Core event-data ontology for conflict, diplomacy, and foreign-policy interactions.
- [Can Large Language Models Transform Computational Social Science?](https://aclanthology.org/2024.cl-1.8/) (2024) - Core; citations: 508. Broad orientation to what LLMs change, and do not change, in computational social science.
- [Whose Opinions Do Language Models Reflect?](https://www.semanticscholar.org/paper/e38a29f6463f38f43797b128673b9e44d18a991e) (2023) - Important; citations: 782. High-impact entry point for political representation and bias in language models.
- [AI can help humans find common ground in democratic deliberation](https://www.semanticscholar.org/paper/5456e833710dba2bb3ae92621fa89c27733b1db0) (2024) - Important; citations: 208. A flagship empirical case for LLMs in democratic deliberation and policy communication.
- [Escalation Risks from Language Models in Military and Diplomatic Decision-Making](https://arxiv.org/abs/2401.03408) (2024) - Core; citations: 85. Core LLM crisis-simulation paper for military and diplomatic escalation behavior.
- [Human-level play in the game of Diplomacy by combining language models with strategic reasoning](https://www.semanticscholar.org/paper/e89ed6bb1864558e3889f5f2fb8931643c633479) (2022) - Important; citations: 548. Major demonstration of language-mediated strategic action in a diplomatic game.
- [ForecastBench: A Dynamic Benchmark of AI Forecasting Capabilities](https://arxiv.org/abs/2409.19839) (2024) - Core; citations: 57. Central benchmark for evaluating AI forecasting across changing real-world questions.
- [MIRAI: Evaluating LLM Agents for Event Forecasting](https://arxiv.org/abs/2407.01231) (2024) - Core; citations: 33. Agent-oriented benchmark for event forecasting and temporal reasoning.
- [Approaching Human-Level Forecasting with Language Models](https://arxiv.org/abs/2402.18563) (2024) - Core; citations: 77. Key reference for comparing LLM forecasting systems with human forecasting performance.
- [Playing repeated games with large language models](https://www.semanticscholar.org/paper/3f98cf521222c65522200037c0eb95a17081b2dd) (2023) - Important; citations: 243. Useful baseline for strategic behavior in repeated interaction.
- [Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442) (2023) - Important; citations: 4046. Canonical generative-agent paper behind many social and political simulation systems.
- [Out of One, Many: Using Language Models to Simulate Human Samples](https://www.cambridge.org/core/journals/political-analysis/article/out-of-one-many-using-language-models-to-simulate-human-samples/035D7C8A55B237942FB6DBAD7CAA4E49) (2023) - Important; citations: 1023. High-impact foundation for synthetic samples and population-level opinion simulation.
- [Generative Agent Simulations of 1,000 People](https://arxiv.org/abs/2411.10109) (2024) - Core; citations: 304. Recent large-scale person-specific simulation reference with direct social-science relevance.
- [Generative Language Models and Automated Influence Operations: Emerging Threats and Potential Mitigations](https://www.semanticscholar.org/paper/c9ad9d69d7568110dd5527598a92c7f8b335eef4) (2023) - Important; citations: 317. Core risk framing for automated influence operations and strategic information environments.

## Papers by Theme

This section highlights Core and Important papers only. See [`docs/full-bibliography.md`](docs/full-bibliography.md) for all Curated and Watchlist entries.

### Foundations and Theory

Canonical IR, strategic-studies, intelligence-analysis, and forecasting foundations for interpreting LLM behavior in strategic settings.

30 highlighted papers; 33 total in the full bibliography.

#### Deterrence, coercion, and nuclear strategy

- [Arms and Influence](https://www.semanticscholar.org/paper/c4a1ff7f04858b2869298b99de53b906361b538f) (1966) - Core; citations: 2033. The core coercion and bargaining frame behind much of the escalation literature.
- [The Spread of Nuclear Weapons: More May Be Better](https://www.semanticscholar.org/paper/05af40c56355e30332c4e8f131d4f7ebc824df97) (1981) - Important; citations: 395.
- [The Delicate Balance of Terror](https://www.semanticscholar.org/paper/d7975b7956a2ca1cd73e75c836db7fb0c433ff3d) (1958) - Core; citations: 360.
- [The Nuclear Taboo: The United States and the Non-Use of Nuclear Weapons Since 1945](https://www.semanticscholar.org/paper/e448d18989ff9c23f8203e4d6077efd656eb5469) (2007) - Core; citations: 351.
- [Nuclear Weapons and Coercive Diplomacy](https://www.semanticscholar.org/paper/5c640b359f5f003fd1cfedd3b970730574a35f13) (2017) - Important; citations: 67.
- [The Meaning of the Nuclear Revolution: Statecraft and the Prospect of Armageddon](https://www.semanticscholar.org/paper/6c4f043a33dc0fe5e2610b44a40b024eb8c04258) (1989) - Core; citations: 24.
- [The Evolution of Nuclear Strategy](https://www.semanticscholar.org/paper/9c6d7b47d877c7552ab98da841ca933fd049afdb) (1981) - Core; citations: 20.
- [The Strategy of Conflict](https://www.semanticscholar.org/paper/3f20d642bc455bc34df41fbf24e297d16f930359) (1960) - Core; citations: n/a.

#### Bargaining, signaling, and war

- [Rationalist Explanations for War](https://www.semanticscholar.org/paper/505ed8c92f0b1ca9afdccdf4890f4e79415ee788) (1995) - Core; venue: International Organization; citations: 3515. Canonical account of war through information problems, incentives, and commitment problems.
- [Domestic Political Audiences and the Escalation of International Disputes](https://www.semanticscholar.org/paper/f1de5d9f3a4f0282aff7363f30b652797f2f5d95) (1994) - Important; venue: American Political Science Review; citations: 2205.
- [War as a Commitment Problem](https://www.semanticscholar.org/paper/c1326170cf6201586f0281177bcd4259a70cdae5) (2006) - Core; venue: International Organization; citations: 858.
- [Democracy and Coercive Diplomacy](https://www.semanticscholar.org/paper/ae16fef14ee8088ee77a9e3008dfae6d1c496d9a) (2001) - Important; citations: 579.
- [Exploring the Bargaining Model of War](https://www.semanticscholar.org/paper/f6f4f629792c070f050d28e30e84d5770e1735f1) (2003) - Important; venue: Perspectives on Politics; citations: 342.
- [Bargaining and Learning While Fighting](https://www.semanticscholar.org/paper/36bd10840fd5ed90ef02b6c7cd285b40fade92dc) (2003) - Core; citations: 341.
- [A Bargaining Model of War and Peace: Anticipating the Onset, Duration, and Outcome of War](https://www.semanticscholar.org/paper/ddf87b9f14dd4ab89190b3a48d3ab163fb9dc091) (2002) - Important; citations: 340.
- [The Inefficient Use of Power: Costly Conflict with Complete Information](https://www.semanticscholar.org/paper/9a1d08d579ac683b73fde4ed8e75bb9316f8c254) (2004) - Core; venue: American Political Science Review; citations: 258.

#### International politics, intelligence, and crisis judgment

- [Perception and Misperception in International Politics](https://www.semanticscholar.org/paper/4339c93c91e296e34ce08cb3555e48d6244ac0f8) (1976) - Core; citations: 2913. Classic baseline for interpreting misperception, signaling, and crisis reasoning.
- [Analysis, War, and Decision: Why Intelligence Failures Are Inevitable](https://www.semanticscholar.org/paper/0d5f8a5303dc849f3a3c0080fbf0ca683066024d) (1978) - Core; venue: World Politics; citations: 326.
- [Advisers and Aggregation in Foreign Policy Decision Making](https://www.semanticscholar.org/paper/63ebe0f54b97741fce6d056a5475ed6a855358b2) (2024) - Important; venue: International Organization; citations: 16.

#### Intelligence analysis and structured analytic techniques

- [Essence of Decision: Explaining the Cuban Missile Crisis](https://www.semanticscholar.org/paper/fac3a8649c09224e1167a6ea403886f99899133d) (1971) - Core; citations: 3145. Foundational decision-making models for crisis behavior and bureaucratic politics.
- [Victims of Groupthink](https://www.semanticscholar.org/paper/1d804dc3800de03a6b9a6cd8e89318f6fb4b57bd) (1972) - Important; citations: 1862.
- [Psychology of Intelligence Analysis](https://www.semanticscholar.org/paper/11a4401589217f85bbb8136ebbe482dac69732ad) (1999) - Core; citations: 918.
- [Analogies at War: Korea Munich Dien Bien Phu and the Vietnam Decisions of 1965](https://www.semanticscholar.org/paper/c9d362b44ba6397a9ba5b9fcff75d563dcf0de9f) (1992) - Important; citations: 701.
- [Thinking in Time: The Uses of History for Decision-Makers](https://www.semanticscholar.org/paper/6df5b7e3cdf23535b53fd170526ef2dbb2d8e426) (1986) - Important; citations: 369.
- [Intelligence Analysis: A Target-Centric Approach](https://www.semanticscholar.org/paper/35b5e2a9320f75122aa00612934f2ed1fc6560cd) (2003) - Important; citations: 232.
- [Structured Analytic Techniques for Intelligence Analysis](https://www.semanticscholar.org/paper/8adafdfdd58e8dcbf31d9cd21e2a6afaec61bfc4) (2010) - Core; citations: 158.
- [Pearl Harbor: Warning and Decision](https://www.semanticscholar.org/paper/0cdc0746b4c5678c9bd455f74f30c75ee3477381) (1962) - Core; citations: 129.

#### Forecasting, hindsight bias, and expert judgment

- [Superforecasting: The Art and Science of Prediction](https://www.semanticscholar.org/paper/7fd0b7c04157ca1459ca16607de9ec139fd9ad51) (2015) - Core; citations: 660.
- [Hindsight (Not Equal To) Foresight: The Effect of Outcome Knowledge on Judgment Under Uncertainty.](https://www.semanticscholar.org/paper/e1f8236ec4aadff6caa0f55b91c87b02f2e9b6f9) (1975) - Core; citations: 444.
- [Expert Political Judgment: How Good Is It? How Can We Know?](https://www.semanticscholar.org/paper/adb3753db12988a3269c4b0e7ec42db87ff61e5e) (2007) - Core; venue: Perspectives on Politics; citations: 382.

### LLM Surveys and Method Overviews

LLM-era surveys and methodological overviews that orient political science, social simulation, and game-theoretic agent work.

7 highlighted papers; 19 total in the full bibliography.

#### Political science and computational social science overviews

- [Can Large Language Models Transform Computational Social Science?](https://aclanthology.org/2024.cl-1.8/) (2024) - Core; venue: International Conference on Computational Logic; citations: 508. Broad orientation to what LLMs change, and do not change, in computational social science.
- [Large language models and political science](https://www.frontiersin.org/journals/political-science/articles/10.3389/fpos.2023.1257092/full) (2023) - Important; venue: Frontiers in Political Science; citations: 36.
- [Political-LLM: Large Language Models in Political Science](https://arxiv.org/abs/2412.06864) (2024) - Core; venue: arXiv.org; citations: 32.
- [Intelligent Computing Social Modeling and Methodological Innovations in Political Science in the Era of Large Language Models](https://www.semanticscholar.org/paper/be8c344ed7728367a25b074bf98c9a7569d15f74) (2024) - Important; venue: Journal of Chinese Political Science; citations: 19.
- [Large Language Models in Politics and Democracy: A Comprehensive Survey](https://arxiv.org/abs/2412.04498) (2024) - Core; venue: arXiv.org; citations: 5.

#### Social simulation and agent-based modeling reviews

- [Validation is the central challenge for generative social simulation: a critical review of LLMs in agent-based modeling](https://www.semanticscholar.org/paper/5cd29f769cced349fb7c5affb5c6d27fb387a69c) (2025) - Important; venue: Artificial Intelligence Review; citations: 12.

#### Evaluation, validity, and contamination

- [LLM-Based Social Simulations Require a Boundary](https://www.semanticscholar.org/paper/345a35ad4020dee737cb905239af9234584fbd33) (2025) - Important; venue: arXiv.org; citations: 11.

### Political Text and Measurement

Pre-LLM and bridge methods for political text measurement, legislative text classification, and event-data extraction.

31 highlighted papers; 43 total in the full bibliography.

#### Political text as data and policy-position extraction

- [Text as Data: The Promise and Pitfalls of Automatic Content Analysis Methods for Political Texts](https://www.semanticscholar.org/paper/b9921fb4d1448058642897797e77bdaf8f444404) (2013) - Core; venue: Political Analysis; citations: 2987. Methodological bridge from political text measurement to current LLM annotation and scaling work.
- [Extracting Policy Positions from Political Texts Using Words as Data](https://www.semanticscholar.org/paper/7d9cc63dfbd34acf271e3a2c922ea1c07fb2f482) (2003) - Core; venue: American Political Science Review; citations: 1353.
- [A Method of Automated Nonparametric Content Analysis for Social Science](https://www.semanticscholar.org/paper/f057500971a5466f9580002e495044fd3e64429d) (2010) - Core; citations: 815.
- [A Scaling Model for Estimating Time-Series Party Positions from Texts](https://www.semanticscholar.org/paper/5109c519cd4442041a5d3915ca305eba6d68ee10) (2007) - Core; citations: 741.
- [How to Analyze Political Attention with Minimal Assumptions and Costs](https://www.semanticscholar.org/paper/43233894df92aba0267d182d1f0b27651d0935ee) (2010) - Core; citations: 703.
- [Fightin' Words: Lexical Feature Selection and Evaluation for Identifying the Content of Political Conflict](https://www.semanticscholar.org/paper/ebc37575aa4e4afeb1dc94a18022cc0ebeb2fe09) (2008) - Core; venue: Political Analysis; citations: 646.
- [A Bayesian Hierarchical Topic Model for Political Texts: Measuring Expressed Agendas in Senate Press Releases](https://www.semanticscholar.org/paper/b06056c20f4ed118e7db9f4e35e674570b2cf8f6) (2010) - Core; venue: Political Analysis; citations: 584.
- [Computer-Assisted Text Analysis for Comparative Politics](https://www.semanticscholar.org/paper/ca1469279ace2e341fd385c884129367e1b7dda7) (2015) - Core; venue: Political Analysis; citations: 464.
- [Using Imperfect Surrogates for Downstream Inference: Design-based Supervised Learning for Social Science Applications of Large Language Models](https://www.semanticscholar.org/paper/04071b5817d84eacc5d56816c0158c1fbee0d286) (2023) - Important; venue: Neural Information Processing Systems; citations: 49.

#### Legislative speech and policy text classification

- [Get out the vote: Determining support or opposition from Congressional floor-debate transcripts](https://www.semanticscholar.org/paper/dc832b298290e316d1218266f6f33de97c9b5679) (2006) - Core; venue: Conference on Empirical Methods in Natural Language Processing; citations: 648.
- [The Media Frames Corpus: Annotations of Frames Across Issues](https://www.semanticscholar.org/paper/92408cc19033cc4af29accef3793014ab79355c2) (2015) - Important; venue: Annual Meeting of the Association for Computational Linguistics; citations: 271.
- [Predicting Legislative Roll Calls from Text](https://www.semanticscholar.org/paper/62e14dec73970514a5e3f81b059d63b34e9ad37c) (2011) - Core; venue: International Conference on Machine Learning; citations: 209.
- [Measuring Political Positions from Legislative Speech](https://www.semanticscholar.org/paper/78073f687117e15ca4786def603d1509d09c99bf) (2016) - Core; venue: Political Analysis; citations: 155.
- [Textual Predictors of Bill Survival in Congressional Committees](https://www.semanticscholar.org/paper/36da409e56a1a47691bd880fa73954a4aeae41b3) (2012) - Core; venue: North American Chapter of the Association for Computational Linguistics; citations: 70.

#### Political event data and conflict information extraction

- [An Automated Information Extraction Tool for International Conflict Data with Performance as Good as Human Coders: A Rare Events Evaluation Design](https://www.semanticscholar.org/paper/195ba4e60c5840de438aa5b22bd99aca33339ffd) (2003) - Core; venue: International Organization; citations: 432.
- [Integrated Data for Events Analysis (IDEA): An Event Typology for Automated Events Data Development](https://www.semanticscholar.org/paper/e2ea7868124efba5283ee98f3d0db5ebb296cc86) (2003) - Core; citations: 257.
- [Conflict and Mediation Event Observations (CAMEO): A New Event Data Framework for the Analysis of Foreign Policy Interactions](https://www.semanticscholar.org/paper/775d7f7262ffb42972e5b87a245bc4b63c20396d) (2002) - Core; citations: 189. Core event-data ontology for conflict, diplomacy, and foreign-policy interactions.
- [Political Science: KEDS-A Program for the Machine Coding of Event Data](https://www.semanticscholar.org/paper/f2a0ce8d7316814628853ec135d465e25dd89279) (1994) - Core; citations: 165.
- [Precedents, Progress, and Prospects in Political Event Data](https://www.semanticscholar.org/paper/86b1d0c06965266939a167ebe135bfda62234d0d) (2012) - Important; citations: 126.
- [Learning to Extract International Relations from Political Context](https://www.semanticscholar.org/paper/de0c0563ee36f3485b5547482cf2b9296107d716) (2013) - Core; venue: Annual Meeting of the Association for Computational Linguistics; citations: 76.
- [Automated Coding of International Event Data Using Sparse Parsing Techniques](https://www.semanticscholar.org/paper/f9dc1de1dea55eef0bfdea0231e95045dd7e64b3) (2000) - Core; citations: 67.
- [The CAMEO (Conflict and Mediation Event Observations) Actor Coding Framework](https://www.semanticscholar.org/paper/dd9b3253977b889490c5baf33502230b6939fa6b) (2008) - Important; citations: 67.
- [Automated Coding of Political Event Data](https://www.semanticscholar.org/paper/f572d3ae9579b94dd7576ea16ff879ee357c54d9) (2013) - Important; citations: 52.
- [Automatic Extraction of Events from Open Source Text for Predictive Forecasting](https://www.semanticscholar.org/paper/323d03d202b9fea2696cbfa86ef86a29bea10b50) (2013) - Important; citations: 52.
- [Three's a Charm?: Open Event Data Coding with EL:DIABLO, PETRARCH, and the Open Event Data Alliance.](https://www.semanticscholar.org/paper/ebec268b3097a364f04c9630521ca2c16a3bdfb2) (2014) - Important; citations: 49.
- [Automated Production of High-Volume, Near-Real-Time Political Event Data](https://www.semanticscholar.org/paper/22317c1fb2e0339771cb6f263e58c31ea421054c) (2011) - Important; citations: 35.
- [Improving the selection of news reports for event coding using ensemble classification](https://www.semanticscholar.org/paper/b1dc323fcad19c28240906b989afc02f7d2849d4) (2015) - Important; citations: 34.
- [Creating Custom Event Data Without Dictionaries: A Bag-of-Tricks](https://www.semanticscholar.org/paper/3a8d5ee46951eda62e38ca4d9b364de5387d8be4) (2023) - Important; venue: arXiv.org; citations: 9.
- [Creating a Real-Time, Reproducible Event Dataset](https://www.semanticscholar.org/paper/680ef0b7b3e0a415a29ca28e4bb40dad220ad69e) (2016) - Important; venue: arXiv.org; citations: 5.
- [Political Event Coding as Text-to-Text Sequence Generation](https://www.semanticscholar.org/paper/f4666ec25c7af298ed359c0eca05295b908bab59) (2022) - Important; venue: CASE; citations: 3.
- [GDELT: Global Data on Events, Location and Tone, 1979-2012](https://data.gdeltproject.org/documentation/ISA.2013.GDELT.pdf) (2013) - Core; citations: n/a.

### Public Opinion, Elections, and Persuasion

LLM work on ideology, voter behavior, opinion simulation, political annotation, deliberation, and persuasion.

23 highlighted papers; 52 total in the full bibliography.

#### Political ideology, representation, and bias

- [Whose Opinions Do Language Models Reflect?](https://www.semanticscholar.org/paper/e38a29f6463f38f43797b128673b9e44d18a991e) (2023) - Important; venue: International Conference on Machine Learning; citations: 782. High-impact entry point for political representation and bias in language models.
- [More human than human: measuring ChatGPT political bias](https://www.semanticscholar.org/paper/3d8a3517231643c1df79bc32c8c2664a4cba3a41) (2023) - Important; venue: Public Choice; citations: 407.
- [Should ChatGPT be Biased? Challenges and Risks of Bias in Large Language Models](https://www.semanticscholar.org/paper/16d83e930a4dab2d49f5d276838ddce79df3f787) (2023) - Important; venue: First Monday; citations: 369.
- [Cultural bias and cultural alignment of large language models](https://www.semanticscholar.org/paper/5f8bf881c80125452e4a73ad51fdb2c72c65c551) (2023) - Important; venue: PNAS Nexus; citations: 307.
- [Political Compass or Spinning Arrow? Towards More Meaningful Evaluations for Values and Opinions in Large Language Models](https://www.semanticscholar.org/paper/5bd44a34457d3f323eea4d961dd762003be3961d) (2024) - Important; venue: Annual Meeting of the Association for Computational Linguistics; citations: 155.
- [Large language models reflect the ideology of their creators](https://www.nature.com/articles/s44387-025-00048-0) (2025) - Important; venue: npj Artificial Intelligence; citations: 58.
- [Beyond Prompt Brittleness: Evaluating the Reliability and Consistency of Political Worldviews in LLMs](https://www.semanticscholar.org/paper/292d5013b1642eb7245f3d653695c4d31f4f3aa5) (2024) - Important; venue: Transactions of the Association for Computational Linguistics; citations: 52.
- [Large Means Left: Political Bias in Large Language Models Increases with Their Number of Parameters](https://www.semanticscholar.org/paper/2d635fa1b8af339e7029105fc5e0a64681d9b5e5) (2025) - Important; venue: arXiv.org; citations: 10.
- [What Is The Political Content in LLMs' Pre- and Post-Training Data?](https://www.semanticscholar.org/paper/6ea5c7a8dcd2e516177cd1cc49c14babc0b2962c) (2025) - Important; venue: arXiv.org; citations: 3.

#### Multilingual and geopolitical bias

- [This Land is Your, My Land: Evaluating Geopolitical Bias in Language Models through Territorial Disputes](https://www.semanticscholar.org/paper/1f5c666f2462190f76749be65764f43c393b0c0c) (2023) - Important; venue: North American Chapter of the Association for Computational Linguistics; citations: 34.
- [Democratic or Authoritarian? Probing a New Dimension of Political Biases in Large Language Models](https://www.semanticscholar.org/paper/e97107eede375d1eb0dfc540e3c0753a5b35b18d) (2025) - Important; venue: arXiv.org; citations: 5.
- [Framing Political Bias in Multilingual LLMs Across Pakistani Languages](https://www.semanticscholar.org/paper/a643e78f431e94749c681a8009f6e7a3003e707a) (2025) - Important; venue: arXiv; citations: 4.
- [Mapping Geopolitical Bias in 11 Large Language Models: A Bilingual, Dual-Framing Analysis of U.S.-China Tensions](https://www.semanticscholar.org/paper/e1bd56bf0964cdb979cc6ba65c8b93a79eb8b8e5) (2025) - Important; venue: arXiv.org; citations: 4.
- [Bias Beyond Borders: Political Ideology Evaluation and Steering in Multilingual LLMs](https://www.semanticscholar.org/paper/81024568c22b38af2e40df9964ddc91dbd825248) (2026) - Important; venue: arXiv.org; citations: 1.

#### Elections, voters, and campaign discourse

- [Hidden Persuaders: LLMs’ Political Leaning and Their Influence on Voters](https://www.semanticscholar.org/paper/af47fadf6adaa81c949c82c8479734d4ea727795) (2024) - Important; venue: Conference on Empirical Methods in Natural Language Processing; citations: 74.

#### Public opinion, polling, and political annotation

- [ChatGPT-4 Outperforms Experts and Crowd Workers in Annotating Political Twitter Messages with Zero-Shot Learning](https://www.semanticscholar.org/paper/6354f2639d07bf8d5b08a4dcaef4c5db5fe19fdb) (2023) - Important; venue: arXiv.org; citations: 206.
- [Performance and biases of Large Language Models in public opinion simulation](https://www.semanticscholar.org/paper/e6d14d140c4faaf8f3d9f47e61cc5c6091bccf1e) (2024) - Important; venue: Humanities and Social Sciences Communications; citations: 97.
- [Large language models as a substitute for human experts in annotating political text](https://www.semanticscholar.org/paper/f8b64c2dad165c92cfb43081c7e0ed70b077ae85) (2024) - Important; venue: Research &amp; Politics; citations: 94.

#### Deliberation, persuasion, and information environments

- [Generative Echo Chamber? Effect of LLM-Powered Search Systems on Diverse Information Seeking](https://www.semanticscholar.org/paper/0b26abcbb54394c79234eeefe9cb1da5f183d47b) (2024) - Important; venue: International Conference on Human Factors in Computing Systems; citations: 171.
- [Systematic Biases in LLM Simulations of Debates](https://www.semanticscholar.org/paper/f503b95c0a64f6a84eb1d90e5ea1e094b1e1892b) (2024) - Important; venue: Conference on Empirical Methods in Natural Language Processing; citations: 119.
- [Looking Under the Hood: How LLMs Attempt Political Persuasion and Microtargeting](https://www.semanticscholar.org/paper/0f0f6e16b4f9cb45cda4f38f377c676725eac2aa) (2026) - Important; venue: Chinese Political Science Review; citations: 1.

#### Legislative and political-agent simulation

- [Political Actor Agent: Simulating Legislative Politics with LLM Agents](https://arxiv.org/abs/2412.07144) (2024) - Important; venue: arXiv.org; citations: 6.
- [Persona-driven Simulation of Voting Behavior in the European Parliament with Large Language Models](https://www.semanticscholar.org/paper/f4e98cd3a09593e02240f97dab0e75ea556bec75) (2025) - Important; venue: Conference of the European Chapter of the Association for Computational Linguistics; citations: 0.

### Policy and Governance Support

Papers on public decision support, policy communication, democratic deliberation, and institutional uses of LLMs.

16 highlighted papers; 44 total in the full bibliography.

#### Democratic governance and augmentation

- [Surfacing citizens’ policy perspectives at scale in the age of large language models](https://www.semanticscholar.org/paper/44ffede29c637f737fbbfb1574799301e628e8f8) (2025) - Important; venue: Behavioral Science &amp; Policy; citations: 0.
- [Large Language Models as agents for augmented democracy](https://royalsocietypublishing.org/rsta/article/382/2285/20240100/108429/Large-language-models-LLMs-as-agents-for-augmented) (2024) - Important; citations: n/a.

#### Policy translation and policy brief generation

- [The End of the Policy Analyst? Testing the Capability of Artificial Intelligence to Generate Plausible, Persuasive, and Useful Policy Analysis](https://www.semanticscholar.org/paper/22b39e38e2fd52591ca23904b474eb19dc17b610) (2023) - Important; venue: Digit. Gov. Res. Pract.; citations: 27.
- [Automating public policy: a comparative study of conversational artificial intelligence models and human expertise in crafting briefing notes](https://www.semanticscholar.org/paper/883be2ffec2fcb09f0854af0386a98196efc587c) (2024) - Important; venue: Ai & Society; citations: 2.

#### Policy persuasion and democratic deliberation

- [AI can help humans find common ground in democratic deliberation](https://www.semanticscholar.org/paper/5456e833710dba2bb3ae92621fa89c27733b1db0) (2024) - Important; venue: Science; citations: 208. A flagship empirical case for LLMs in democratic deliberation and policy communication.
- [LLM-generated messages can persuade humans on policy issues](https://www.semanticscholar.org/paper/da2ed9d7804f138a1108089891fd07df15a70a3a) (2025) - Important; venue: Nature Communications; citations: 67.
- [Opportunities and Risks of LLMs for Scalable Deliberation with Polis](https://www.semanticscholar.org/paper/ede87ffc69414d3ca86c5e57b96757d0245eab82) (2023) - Important; venue: arXiv.org; citations: 60.
- [Large Language Models Can Argue in Convincing Ways About Politics, But Humans Dislike AI Authors: Implications for Governance](https://collaborate.princeton.edu/en/publications/large-language-models-can-argue-in-convincing-ways-about-politics/) (n.d.) - Important; venue: Political science; citations: 36.
- [Can AI Truly Represent Your Voice in Deliberations? A Comprehensive Study of Large-Scale Opinion Aggregation with LLMs](https://www.semanticscholar.org/paper/29ecbb1c2fde56565ea283fb292f17dce21b2f0c) (2025) - Important; venue: arXiv.org; citations: 3.
- [An Emergent Understanding of Human-AI Collaboration in Deliberation](https://www.semanticscholar.org/paper/82fdc8bb274a1bc21b9e005c033a952883b8c3e9) (2025) - Important; venue: CSCW Companion; citations: 2.
- [DeliberationBench: A Normative Benchmark for the Influence of Large Language Models on Users'Views](https://www.semanticscholar.org/paper/c6ab228fd5f44cb3ec05705752f1135a15877387) (2026) - Important; venue: arXiv; citations: 2.
- [Bringing Everyone to the Table: An Experimental Study of LLM-Facilitated Group Decision Making](https://www.semanticscholar.org/paper/ea2fa853bcaa3a13880b9538c9a1edaa1d9d360f) (2025) - Important; venue: arXiv.org; citations: 1.

#### Strategic and institutional decision support

- [Biased LLMs can Influence Political Decision-Making](https://aclanthology.org/2025.acl-long.328/) (2025) - Important; venue: Annual Meeting of the Association for Computational Linguistics; citations: 22.
- [The LLM Effect: Are Humans Truly Using LLMs, or Are They Being Influenced By Them Instead?](https://www.semanticscholar.org/paper/4046475556d334a61612c63622a40676907c7b5d) (2024) - Important; venue: Conference on Empirical Methods in Natural Language Processing; citations: 20.

#### Public-sector decision support and institutional workflow

- [Human-AI Interactions in Public Sector Decision-Making:"Automation Bias"and"Selective Adherence"to Algorithmic Advice](https://www.semanticscholar.org/paper/6ad001313456f0bd4ddf7acde97cfe6911da0e7f) (2021) - Important; venue: arXiv; citations: 256.
- [What Makes LLM Agent Simulations Useful for Policy? Insights From an Iterative Design Engagement in Emergency Preparedness](https://www.semanticscholar.org/paper/c65e057b8d3d1fbf3d1b5e67a5fa9de9d739c10e) (2025) - Important; venue: arXiv.org; citations: 8.

### Geopolitics, Diplomacy, and Wargaming

Diplomatic agents, military decision support, escalation behavior, national security applications, and wargaming.

16 highlighted papers; 39 total in the full bibliography.

#### Diplomacy and international institutions

- [Human-level play in the game of Diplomacy by combining language models with strategic reasoning](https://www.semanticscholar.org/paper/e89ed6bb1864558e3889f5f2fb8931643c633479) (2022) - Important; venue: Science; citations: 548. Major demonstration of language-mediated strategic action in a diplomatic game.
- [Benchmarking LLMs for Political Science: A United Nations Perspective / United Nations Benchmark](https://arxiv.org/abs/2502.14122) (2025) - Important; venue: Proceedings of the AAAI Conference on Artificial Intelligence; citations: 5.
- [Critical Foreign Policy Decisions Benchmark: Measuring Diplomatic Preferences in Large Language Models](https://arxiv.org/abs/2503.06263) (2025) - Important; venue: arXiv.org; citations: 4.
- [Democratizing Diplomacy: A Harness for Evaluating Any Large Language Model on Full-Press Diplomacy](https://www.semanticscholar.org/paper/de50adf51dc109bb44e52d63490e7322ba50b1d7) (2025) - Important; venue: AAAI Conference on Artificial Intelligence; citations: 3.
- [UNSC-Bench: Evaluating LLM Diplomatic Role-Playing Through UN Security Council Vote Prediction](https://aclanthology.org/2026.mme-main.10.pdf) (2026) - Important; venue: Proceedings of the First Workshop on Multilingual Multicultural Evaluation; citations: 0.

#### Military decision-making and wargaming

- [Escalation Risks from Language Models in Military and Diplomatic Decision-Making](https://arxiv.org/abs/2401.03408) (2024) - Core; venue: Conference on Fairness, Accountability and Transparency; citations: 85. Core LLM crisis-simulation paper for military and diplomatic escalation behavior.
- [Behavioral Differences Between Expert Humans and Language Models in Wargame Simulations / Human vs. Machine](https://arxiv.org/html/2403.03407v4) (2024) - Core; venue: AAAI/ACM Conference on AI, Ethics, and Society; citations: 23.
- [Open-Ended Wargames with Large Language Models](https://arxiv.org/html/2404.11446v1) (2024) - Important; venue: arXiv.org; citations: 6.
- [The Prompt War: How AI Decides on a Military Intervention](https://www.semanticscholar.org/paper/5711422371477106fcb16ce63599a75a45477711) (2025) - Important; venue: arXiv.org; citations: 4.
- [Red Lines and Grey Zones in the Fog of War: Benchmarking Legal Risk, Moral Harm, and Regional Bias in Large Language Model Military Decision-Making](https://www.semanticscholar.org/paper/6a690b749ac5eaafc0918b452c8cec5cff72c723) (2025) - Important; venue: arXiv.org; citations: 1.
- [WARBENCH: A Comprehensive Benchmark for Evaluating LLMs in Military Decision-Making](https://www.semanticscholar.org/paper/0f12312d9802499773ef7adfa506937263c4f523) (2026) - Important; venue: arXiv; citations: 0.

#### Conflict, escalation, and geopolitical simulation

- [Hacking Nuclear Stability: Wargaming Technology, Uncertainty, and Escalation](https://www.semanticscholar.org/paper/a103bb75a51840687befa963ca37abc00b52caa3) (2023) - Important; venue: International Organization; citations: 10.
- [Simulating Influence Dynamics with LLM Agents](https://arxiv.org/html/2503.08709v1) (2025) - Important; venue: BigData Congress [Services Society]; citations: 5.
- [AI Arms and Influence: Frontier Models Exhibit Sophisticated Reasoning in Simulated Nuclear Crises](https://www.semanticscholar.org/paper/61159eaad2619f56621105de3670b54da562e340) (2026) - Core; venue: arXiv.org; citations: 4.
- [What is Escalation? Measuring Crisis Dynamics in International Relations with Human and LLM Generated Event Data](https://www.semanticscholar.org/paper/2fbeda24159ffccad81e33ced2c61c6f2f1ca236) (2024) - Important; venue: arXiv; citations: 3.
- [LLMs as Strategic Actors: Behavioral Alignment, Risk Calibration, and Argumentation Framing in Geopolitical Simulations](https://arxiv.org/abs/2603.02128) (2026) - Important; venue: arXiv; citations: 1.

### Forecasting and Foresight

Forecasting benchmarks, event-prediction systems, calibration studies, and geopolitical risk signals.

15 highlighted papers; 41 total in the full bibliography.

#### Forecasting benchmarks and datasets

- [ForecastBench: A Dynamic Benchmark of AI Forecasting Capabilities](https://arxiv.org/abs/2409.19839) (2024) - Core; venue: International Conference on Learning Representations; citations: 57. Central benchmark for evaluating AI forecasting across changing real-world questions.
- [MIRAI: Evaluating LLM Agents for Event Forecasting](https://arxiv.org/abs/2407.01231) (2024) - Core; venue: arXiv.org; citations: 33. Agent-oriented benchmark for event forecasting and temporal reasoning.
- [OpenEP: Open-Ended Future Event Prediction](https://arxiv.org/html/2408.06578v2) (2024) - Important; venue: ACM Transactions on Information Systems; citations: 12.
- [Forecasting Future International Events: A Reliable Dataset for Text-Based Event Modeling / WORLDREP](https://arxiv.org/abs/2411.14042) (2024) - Important; venue: Conference on Empirical Methods in Natural Language Processing; citations: 1.

#### Forecasting performance and aggregation

- [Approaching Human-Level Forecasting with Language Models](https://arxiv.org/abs/2402.18563) (2024) - Core; venue: Neural Information Processing Systems; citations: 77. Key reference for comparing LLM forecasting systems with human forecasting performance.
- [AI-Augmented Predictions: LLM Assistants Improve Human Forecasting Accuracy](https://www.semanticscholar.org/paper/38472e4242e0aa632ed594c3b0ed9c0bd6429c41) (2024) - Important; venue: ACM Trans. Interact. Intell. Syst.; citations: 43.
- [A Comprehensive Evaluation of Large Language Models on Temporal Event Forecasting](https://arxiv.org/html/2407.11638v2) (2024) - Important; venue: arXiv.org; citations: 12.
- [Pitfalls in Evaluating Language Model Forecasters](https://www.semanticscholar.org/paper/aceb94676d003e84cdc29a9c72259c3d412c7e61) (2025) - Important; venue: arXiv.org; citations: 12.
- [Simulated Ignorance Fails: A Systematic Study of LLM Behaviors on Forecasting Problems Before Model Knowledge Cutoff](https://www.semanticscholar.org/paper/9a08a05560778e664c3ae47108be0fc501385d63) (2026) - Important; venue: arXiv.org; citations: 3.
- [The Future Is Unevenly Distributed: Forecasting Ability of LLMs Depends on What We’re Asking](https://arxiv.org/abs/2511.18394) (2025) - Important; venue: arXiv.org; citations: 1.

#### Geopolitical event prediction systems

- [AutoCast++: Enhancing World Event Prediction with Zero-shot Ranking-based Context Retrieval](https://www.semanticscholar.org/paper/e0605eaba26fee093d972cc667770912c8d2eec9) (2023) - Important; venue: International Conference on Learning Representations; citations: 15.
- [ThinkTank-ME: A Multi-Expert Framework for Middle East Event Forecasting](https://www.semanticscholar.org/paper/a29b9d962c17189d7f122b02e5ed217499e19e5b) (2026) - Important; venue: Proceedings of the ACM Web Conference 2026; citations: 2.
- [LLM4Geopolitics: A Framework Leveraging Large Language Models for Predicting Geopolitical Events](https://onlinelibrary.wiley.com/doi/10.1111/exsy.70258) (2025) - Important; venue: Expert systems; citations: 0.

#### Geoeconomic and geopolitical risk signals

- [Geoeconomic Pressure](https://www.nber.org/papers/w34020) (n.d.) - Core; venue: Social Science Research Network; citations: 1.
- [The AI-GPR Index: Measuring Geopolitical Risk using Artificial Intelligence](https://www.matteoiacoviello.com/research_files/AI_GPR_PAPER.pdf) (n.d.) - Core; citations: n/a.

### Strategic Reasoning and Multi-Agent Games

LLM strategic reasoning in games, bargaining, negotiation, cooperation, and multi-agent social dilemmas.

3 highlighted papers; 12 total in the full bibliography.

#### Game-theoretic and strategic reasoning benchmarks

- [Playing repeated games with large language models](https://www.semanticscholar.org/paper/3f98cf521222c65522200037c0eb95a17081b2dd) (2023) - Important; venue: Nature Human Behaviour; citations: 243. Useful baseline for strategic behavior in repeated interaction.
- [Strategic behavior of large language models and the role of game structure versus contextual framing](https://www.semanticscholar.org/paper/e46db119b320df6ac4a5091e1561c54c5aece797) (2024) - Important; venue: Scientific Reports; citations: 57.
- [SPIN-Bench: How Well Do LLMs Plan Strategically and Reason Socially?](https://www.semanticscholar.org/paper/ec26efa475d105905d8553eedd141f7905967e5c) (2025) - Important; venue: arXiv.org; citations: 15.

### Social Simulation and Synthetic Populations

Generative agents, synthetic populations, and large-scale simulations of social networks or political behavior.

12 highlighted papers; 38 total in the full bibliography.

#### Generative agents and social simulation platforms

- [Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442) (2023) - Important; venue: ACM Symposium on User Interface Software and Technology; citations: 4046. Canonical generative-agent paper behind many social and political simulation systems.
- [S3: Social-network Simulation System with Large Language Model-Empowered Agents](https://arxiv.org/pdf/2307.14984) (2023) - Important; venue: Social Science Research Network; citations: 299.

#### Synthetic populations and human samples

- [Out of One, Many: Using Language Models to Simulate Human Samples](https://www.cambridge.org/core/journals/political-analysis/article/out-of-one-many-using-language-models-to-simulate-human-samples/035D7C8A55B237942FB6DBAD7CAA4E49) (2023) - Important; venue: Political Analysis; citations: 1023. High-impact foundation for synthetic samples and population-level opinion simulation.
- [Generative Agent Simulations of 1,000 People](https://arxiv.org/abs/2411.10109) (2024) - Core; venue: arXiv; citations: 304. Recent large-scale person-specific simulation reference with direct social-science relevance.
- [LLM Generated Persona is a Promise with a Catch](https://www.semanticscholar.org/paper/3ea29481ec11d1568fde727d236f71e44e4e2ad0) (2025) - Important; venue: arXiv.org; citations: 72.
- [Large Language Models as Subpopulation Representative Models: A Review](https://www.semanticscholar.org/paper/306f4aa90c2f2d3f55b81a99f0068d0e8ab8d359) (2023) - Important; venue: arXiv.org; citations: 22.
- [Vox Populi, Vox AI? Using Language Models to Estimate German Public Opinion](https://www.semanticscholar.org/paper/95a41d1598d3f888dbc38905817390bb70d65a66) (2024) - Important; venue: Social science computer review; citations: 12.
- [Valid Survey Simulations with Limited Human Data: The Roles of Prompting, Fine-Tuning, and Rectification](https://www.semanticscholar.org/paper/b3f15b5a6796ddf87045ba1f8db725ef101c8cac) (2025) - Important; venue: arXiv.org; citations: 6.
- [Simulating Public Opinion: Comparing Distributional and Individual-Level Predictions from LLMs and Random Forests](https://www.semanticscholar.org/paper/a4ec508e5e0de8fc07c7552c1e0012c2e712442a) (2025) - Important; venue: Entropy; citations: 2.
- [Before You Simulate: A Pre-Study Benchmark for Large Language Model Stability in Political Role-Playing Simulations](https://www.semanticscholar.org/paper/5881e53178afcf627e0e8b0225b93be8934596dc) (2026) - Important; venue: Applied Sciences; citations: 0.
- [Characterizing the ability of LLMs to recapitulate Americans'distributional responses to public opinion polling questions across political issues](https://www.semanticscholar.org/paper/d325f69c6ea6e829a4bb7cb8b870bddf77910ef9) (2026) - Important; venue: arXiv; citations: 0.

#### Social networks, movements, and polarization

- [Understanding Online Polarization Through Human-Agent Interaction in a Synthetic LLM-Based Social Network](https://www.semanticscholar.org/paper/2d71545ba1a2ff9f30703cef3df75a15d159b525) (2025) - Important; venue: International Conference on Web and Social Media; citations: 10.

### Risks, Bias, and Influence Operations

Political influence, persuasion risk, deception, bias, and social risks relevant to governance and strategy.

6 highlighted papers; 18 total in the full bibliography.

#### Influence operations and persuasion risk

- [Generative Language Models and Automated Influence Operations: Emerging Threats and Potential Mitigations](https://www.semanticscholar.org/paper/c9ad9d69d7568110dd5527598a92c7f8b335eef4) (2023) - Important; venue: arXiv.org; citations: 317. Core risk framing for automated influence operations and strategic information environments.
- [Evaluating the persuasive influence of political microtargeting with large language models](https://www.semanticscholar.org/paper/de9a0af5100600ff21a9ded6e42409e0de89de8a) (2024) - Important; venue: Proceedings of the National Academy of Sciences of the United States of America; citations: 116.
- [Characterizing the 2016 Russian IRA influence campaign](https://www.semanticscholar.org/paper/d73777af16df99b7c8e8fe4afc7748d66aeb9346) (2018) - Important; venue: Social Network Analysis and Mining; citations: 114.
- [Charting the Landscape of Nefarious Uses of Generative Artificial Intelligence for Online Election Interference](https://www.semanticscholar.org/paper/4af68a3cc8871dfe6fe68f91b93cfd17d81076f7) (2024) - Important; venue: First Monday; citations: 14.
- [Assessing the risks and opportunities posed by AI-enhanced influence operations on social media](https://www.semanticscholar.org/paper/5eb988d1926b80963c382abe0cfb623cc018c308) (2024) - Important; venue: Place Branding and Public Diplomacy; citations: 10.
- [Do Bots Do It Better? Analyzing the Effectiveness of Automated Agents in State-Sponsored Information Operations](https://www.semanticscholar.org/paper/66d045db96c75b6162c28f47e7afdda323307926) (2025) - Important; venue: International Conference on Web and Social Media; citations: 0.

## Data and Collection

- Total unique papers in the full thematic bibliography: 378
- Papers highlighted on this page: 159
- Label counts: Core 50, Important 109, Curated 162, Watchlist 57
- Source rows checked before merge: 400
- Duplicate source rows removed during merge: 22
- Core seed papers: 40
- Curated additions merged into themes: 338
- Initial citation/reference edges scanned: 3889
- Additional citation/reference edges scanned from priority papers: 2871
- Targeted strategic-decision related-work edges scanned: 119
- Fog-of-war related-work edges scanned: 49
- Critique-priority citation/reference edges scanned: 2009
- Critique-next citation/reference edges scanned: 144
- Critique-followup citation/reference edges scanned: 367
- Critique-followup Semantic Scholar query results screened: 98
- Critique-round-3 influence/diplomacy citation/reference edges scanned: 1064
- Critique-round-3 social-simulation citation/reference edges scanned: 304
- Critique-round-3 Semantic Scholar query results screened: 132
- Survey-readiness citation/reference edges scanned: 721
- Survey-readiness Semantic Scholar query results screened: 166
- Institutional-workflow citation/reference edges scanned: 273
- Institutional-workflow Semantic Scholar query results screened: 339

Data files:

- `docs/full-bibliography.md`: complete generated bibliography.
- `docs/selection-criteria.md`: inclusion rules, exclusion rules, labels, and provenance notes.
- `docs/survey_readiness_gap_analysis.md`: remaining gaps and validity taxonomy for turning the repository into a survey paper.
- `data/processed/thematic_papers.csv`: merged thematic paper table used to build the README and full bibliography.
- `data/raw/core_seed_papers.csv`: original core seed list.
- `data/raw/targeted_strategic_decisions_seed.csv`: targeted trace seed for the strategic-decision paper.
- `data/raw/classical_political_nlp_ie_seed.csv`: curated classical political NLP and information-extraction seed list.
- `data/raw/fog_of_war_related_work_seed.csv`: curated Fog of War related-work and foundation seed list.
- `data/raw/strategic_studies_foundation_seed.csv`: curated strategic-studies foundation seed list.
- `data/raw/critique_priority_expansion_seeds.csv`: critique-selected high-priority trace seeds.
- `data/raw/critique_next_expansion_seeds.csv`: next-round critique seed list for escalation risk and Political-LLM traces.
- `data/raw/critique_followup_expansion_seeds.csv`: critique-followup seeds for forecasting, democratic deliberation, and WARBENCH traces.
- `data/raw/critique_followup_search_queries.csv`: targeted Semantic Scholar query-search terms for the critique-followup pass.
- `data/raw/critique_round3_expansion_seeds.csv`: critique-round-3 seeds for influence operations, Diplomacy, and synthetic-population traces.
- `data/raw/critique_round3_search_queries.csv`: targeted Semantic Scholar query-search terms for influence operations, diplomacy, and social simulation.
- `data/raw/survey_readiness_expansion_seeds.csv`: critique-selected survey-readiness seeds for validity, multilingual/geopolitical bias, diplomacy, and strategic reasoning.
- `data/raw/survey_readiness_search_queries.csv`: targeted Semantic Scholar query-search terms for survey-readiness gaps.
- `data/raw/institutional_workflow_expansion_seeds.csv`: critique-selected seeds for public-sector and institutional decision-support workflows.
- `data/raw/institutional_workflow_search_queries.csv`: targeted Semantic Scholar query-search terms for public-sector workflow gaps.
- `data/processed/core_seed_papers_enriched.csv`: seed metadata with citation counts, authors, venues, abstracts, and resolution method.
- `data/processed/targeted_related_works_strategy.csv`: selected additions from the targeted strategic-decision trace.
- `data/processed/classical_political_nlp_ie_enriched.csv`: Semantic Scholar metadata for the classical political NLP and IE additions.
- `data/processed/fog_of_war_related_works_enriched.csv`: Semantic Scholar metadata for Fog of War related-work additions.
- `data/processed/strategic_studies_foundation_enriched.csv`: Semantic Scholar metadata for strategic-studies foundation additions.
- `data/processed/critique_priority_expansion/curated_additions.csv`: selected additions from critique-priority seed expansion.
- `data/processed/critique_next_expansion/curated_additions.csv`: selected additions from escalation-risk and Political-LLM seed expansion.
- `data/processed/critique_followup_expansion/curated_additions.csv`: selected additions from ForecastBench, democratic-deliberation, and WARBENCH follow-up expansion.
- `data/processed/critique_round3_expansion/curated_additions.csv`: selected additions from influence-operations, Diplomacy, and social-simulation expansion.
- `data/processed/survey_readiness_expansion/curated_additions.csv`: selected additions from validity, multilingual/geopolitical-bias, diplomacy, and strategic-reasoning expansion.
- `data/processed/institutional_workflow_expansion/curated_additions.csv`: selected additions from public-sector workflow, accountability, and policy-analysis expansion.
- `data/processed/targeted_strategic_decisions/run_summary.json`: targeted trace summary.
- `data/processed/fog_of_war/run_summary.json`: Fog of War trace summary.
- `data/processed/critique_priority_expansion/run_summary.json`: critique-priority trace summary.
- `data/processed/critique_next_expansion/run_summary.json`: critique-next trace summary.
- `data/processed/critique_followup_expansion/run_summary.json`: critique-followup trace summary.
- `data/processed/critique_followup_expansion/search_summary.json`: critique-followup query-search summary.
- `data/processed/critique_round3_expansion/run_summary.json`: critique-round-3 influence/diplomacy trace summary.
- `data/processed/critique_round3_expansion/search_summary.json`: critique-round-3 query-search summary.
- `data/processed/critique_round3_expansion/social_simulation_seed_trace_summary.json`: critique-round-3 social-simulation direct-trace summary.
- `data/processed/survey_readiness_expansion/run_summary.json`: survey-readiness trace summary.
- `data/processed/survey_readiness_expansion/search_summary.json`: survey-readiness query-search summary.
- `data/processed/institutional_workflow_expansion/run_summary.json`: institutional-workflow trace summary.
- `data/processed/institutional_workflow_expansion/search_summary.json`: institutional-workflow query-search summary.

Scripts:

- `scripts/expand_semantic_scholar.py`: resolves seeds, fetches citations/references, and writes candidate tables.
- `scripts/search_semantic_scholar.py`: runs targeted Semantic Scholar paper-search queries without fetching TLDR fields.
- `scripts/fetch_seed_metadata.py`: enriches seed papers with Semantic Scholar metadata.
- `scripts/build_targeted_related_works.py`: selects targeted related-work additions from a trace longlist.
- `scripts/build_critique_followup_expansion.py`: selects critique-reviewed additions from the ForecastBench, deliberation, and WARBENCH follow-up pass.
- `scripts/build_critique_round3_expansion.py`: selects critique-reviewed additions from the influence-operations, Diplomacy, and social-simulation pass.
- `scripts/build_survey_readiness_expansion.py`: selects critique-reviewed additions from the survey-readiness pass.
- `scripts/build_institutional_workflow_expansion.py`: selects critique-reviewed additions from the public-sector workflow pass.
- `scripts/build_readme.py`: rebuilds this README and validates that every curated paper is assigned to a theme.

## Contributing

Additions should clearly fit politics, geopolitics, policymaking, strategic studies, or decision-making. See [`CONTRIBUTING.md`](CONTRIBUTING.md) and [`docs/selection-criteria.md`](docs/selection-criteria.md) before proposing papers.
