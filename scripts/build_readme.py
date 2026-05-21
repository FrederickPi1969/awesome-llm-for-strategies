#!/usr/bin/env python3
"""Build README and a merged thematic paper table."""

from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CORE_SEEDS = ROOT / "data" / "raw" / "core_seed_papers.csv"
ENRICHED_SEEDS = ROOT / "data" / "processed" / "core_seed_papers_enriched.csv"
CURATED_CANDIDATES = ROOT / "data" / "processed" / "candidate_additions_strategy.csv"
PRIORITY_SEEDS = ROOT / "data" / "processed" / "priority_expansion_seeds.csv"
SECOND_ORDER_CANDIDATES = ROOT / "data" / "processed" / "second_order_candidate_additions_strategy.csv"
TARGETED_RELATED_WORKS = ROOT / "data" / "processed" / "targeted_related_works_strategy.csv"
CLASSICAL_POLITICAL_NLP_IE = ROOT / "data" / "processed" / "classical_political_nlp_ie_enriched.csv"
FOG_OF_WAR_RELATED_WORKS = ROOT / "data" / "processed" / "fog_of_war_related_works_enriched.csv"
CRITIQUE_PRIORITY_ADDITIONS = ROOT / "data" / "processed" / "critique_priority_expansion" / "curated_additions.csv"
CRITIQUE_NEXT_ADDITIONS = ROOT / "data" / "processed" / "critique_next_expansion" / "curated_additions.csv"
CRITIQUE_FOLLOWUP_ADDITIONS = ROOT / "data" / "processed" / "critique_followup_expansion" / "curated_additions.csv"
CRITIQUE_ROUND3_ADDITIONS = ROOT / "data" / "processed" / "critique_round3_expansion" / "curated_additions.csv"
SURVEY_READINESS_ADDITIONS = ROOT / "data" / "processed" / "survey_readiness_expansion" / "curated_additions.csv"
INSTITUTIONAL_WORKFLOW_ADDITIONS = ROOT / "data" / "processed" / "institutional_workflow_expansion" / "curated_additions.csv"
STRATEGIC_STUDIES_FOUNDATION = ROOT / "data" / "processed" / "strategic_studies_foundation_enriched.csv"
RUN_SUMMARY = ROOT / "data" / "processed" / "run_summary.json"
SECOND_ORDER_SUMMARY = ROOT / "data" / "processed" / "second_order" / "run_summary.json"
TARGETED_SUMMARY = ROOT / "data" / "processed" / "targeted_strategic_decisions" / "run_summary.json"
FOG_OF_WAR_SUMMARY = ROOT / "data" / "processed" / "fog_of_war" / "run_summary.json"
CRITIQUE_PRIORITY_SUMMARY = ROOT / "data" / "processed" / "critique_priority_expansion" / "run_summary.json"
CRITIQUE_NEXT_SUMMARY = ROOT / "data" / "processed" / "critique_next_expansion" / "run_summary.json"
CRITIQUE_FOLLOWUP_SUMMARY = ROOT / "data" / "processed" / "critique_followup_expansion" / "run_summary.json"
CRITIQUE_FOLLOWUP_SEARCH_SUMMARY = ROOT / "data" / "processed" / "critique_followup_expansion" / "search_summary.json"
CRITIQUE_ROUND3_SUMMARY = ROOT / "data" / "processed" / "critique_round3_expansion" / "run_summary.json"
CRITIQUE_ROUND3_SEARCH_SUMMARY = ROOT / "data" / "processed" / "critique_round3_expansion" / "search_summary.json"
CRITIQUE_ROUND3_SOCIAL_SUMMARY = ROOT / "data" / "processed" / "critique_round3_expansion" / "social_simulation_seed_trace_summary.json"
SURVEY_READINESS_SUMMARY = ROOT / "data" / "processed" / "survey_readiness_expansion" / "run_summary.json"
SURVEY_READINESS_SEARCH_SUMMARY = ROOT / "data" / "processed" / "survey_readiness_expansion" / "search_summary.json"
INSTITUTIONAL_WORKFLOW_SUMMARY = ROOT / "data" / "processed" / "institutional_workflow_expansion" / "run_summary.json"
INSTITUTIONAL_WORKFLOW_SEARCH_SUMMARY = ROOT / "data" / "processed" / "institutional_workflow_expansion" / "search_summary.json"
THEMATIC_PAPERS = ROOT / "data" / "processed" / "thematic_papers.csv"
README = ROOT / "README.md"
FULL_BIBLIOGRAPHY = ROOT / "docs" / "full-bibliography.md"

THEME_ORDER = [
    "Political Science and Strategic Judgment Foundations",
    "Foundations, Surveys, and Methods",
    "Classical Political NLP and Information Extraction",
    "Politics, Democracy, Public Opinion, and Persuasion",
    "Policymaking, Governance, and Institutional Decision Support",
    "Geopolitics, Diplomacy, National Security, and Wargaming",
    "Forecasting, Geopolitical Risk, and Foresight",
    "Strategic Reasoning, Games, Negotiation, and Cooperation",
    "Multi-Agent Social Simulation and Synthetic Societies",
    "AI Safety, Influence Operations, and Societal Risk",
    "Peripheral and Borderline Materials",
]

SUBTHEME_ORDER = {
    "Political Science and Strategic Judgment Foundations": [
        "Deterrence, coercion, and nuclear strategy",
        "Bargaining, signaling, and war",
        "International politics, intelligence, and crisis judgment",
        "Intelligence analysis and structured analytic techniques",
        "Policy analysis and decision-making under deep uncertainty",
        "Forecasting, hindsight bias, and expert judgment",
    ],
    "Foundations, Surveys, and Methods": [
        "Political science and computational social science overviews",
        "Social simulation and agent-based modeling reviews",
        "Strategic reasoning and game-theoretic reviews",
        "Evaluation, validity, and contamination",
    ],
    "Classical Political NLP and Information Extraction": [
        "Political text as data and policy-position extraction",
        "Legislative speech and policy text classification",
        "Political event data and conflict information extraction",
    ],
    "Politics, Democracy, Public Opinion, and Persuasion": [
        "Political ideology, representation, and bias",
        "Multilingual and geopolitical bias",
        "Elections, voters, and campaign discourse",
        "Public opinion, polling, and political annotation",
        "Deliberation, persuasion, and information environments",
        "Legislative and political-agent simulation",
    ],
    "Policymaking, Governance, and Institutional Decision Support": [
        "Democratic governance and augmentation",
        "Policy translation and policy brief generation",
        "Policy persuasion and democratic deliberation",
        "Strategic and institutional decision support",
        "Public-sector decision support and institutional workflow",
        "Accountability, auditing, and public-sector AI governance",
        "AI-assisted strategy and managerial decision-making",
        "Strategic evaluation, bias, and foresight",
    ],
    "Geopolitics, Diplomacy, National Security, and Wargaming": [
        "Diplomacy and international institutions",
        "Military decision-making and wargaming",
        "Conflict, escalation, and geopolitical simulation",
        "National security applications and doctrine",
    ],
    "Forecasting, Geopolitical Risk, and Foresight": [
        "Forecasting benchmarks and datasets",
        "Forecasting performance and aggregation",
        "Geopolitical event prediction systems",
        "Geoeconomic and geopolitical risk signals",
    ],
    "Strategic Reasoning, Games, Negotiation, and Cooperation": [
        "Game-theoretic and strategic reasoning benchmarks",
        "Negotiation, bargaining, and communication games",
        "Cooperation and social dilemmas",
        "Behavioral game tests and human-like strategy",
    ],
    "Multi-Agent Social Simulation and Synthetic Societies": [
        "Generative agents and social simulation platforms",
        "Synthetic populations and human samples",
        "Social networks, movements, and polarization",
        "Agent behavior quality and social-simulation validation",
    ],
    "AI Safety, Influence Operations, and Societal Risk": [
        "Influence operations and persuasion risk",
        "Deception, multi-agent risk, and control",
        "Bias, toxicity, and cultural alignment risks",
    ],
    "Peripheral and Borderline Materials": [
        "Business and managerial strategy",
        "Generic decision support and human-AI workflow",
        "Policy-adjacent service delivery and operations",
        "Generic negotiation and behavioral games",
        "Generic AI safety and language-bias background",
        "General forecasting benchmarks",
    ],
}

THEME_ASSIGNMENTS = """
Political Science and Strategic Judgment Foundations|Deterrence, coercion, and nuclear strategy|Arms and Influence
Political Science and Strategic Judgment Foundations|Deterrence, coercion, and nuclear strategy|The Strategy of Conflict
Political Science and Strategic Judgment Foundations|Deterrence, coercion, and nuclear strategy|The Delicate Balance of Terror
Political Science and Strategic Judgment Foundations|Deterrence, coercion, and nuclear strategy|The Meaning of the Nuclear Revolution: Statecraft and the Prospect of Armageddon
Political Science and Strategic Judgment Foundations|Deterrence, coercion, and nuclear strategy|The Evolution of Nuclear Strategy
Political Science and Strategic Judgment Foundations|Deterrence, coercion, and nuclear strategy|The Nuclear Taboo: The United States and the Non-Use of Nuclear Weapons Since 1945
Political Science and Strategic Judgment Foundations|Deterrence, coercion, and nuclear strategy|Nuclear Weapons and Coercive Diplomacy
Political Science and Strategic Judgment Foundations|Deterrence, coercion, and nuclear strategy|The Spread of Nuclear Weapons: More May Be Better
Political Science and Strategic Judgment Foundations|Bargaining, signaling, and war|Rationalist Explanations for War
Political Science and Strategic Judgment Foundations|Bargaining, signaling, and war|War as a Commitment Problem
Political Science and Strategic Judgment Foundations|Bargaining, signaling, and war|The Inefficient Use of Power: Costly Conflict with Complete Information
Political Science and Strategic Judgment Foundations|Bargaining, signaling, and war|Bargaining and Learning While Fighting
Political Science and Strategic Judgment Foundations|Bargaining, signaling, and war|Exploring the Bargaining Model of War
Political Science and Strategic Judgment Foundations|Bargaining, signaling, and war|Domestic Political Audiences and the Escalation of International Disputes
Political Science and Strategic Judgment Foundations|Bargaining, signaling, and war|Democracy and Coercive Diplomacy
Political Science and Strategic Judgment Foundations|Bargaining, signaling, and war|A Bargaining Model of War and Peace: Anticipating the Onset, Duration, and Outcome of War
Political Science and Strategic Judgment Foundations|International politics, intelligence, and crisis judgment|Analysis, War, and Decision: Why Intelligence Failures Are Inevitable
Political Science and Strategic Judgment Foundations|International politics, intelligence, and crisis judgment|Perception and Misperception in International Politics
Political Science and Strategic Judgment Foundations|International politics, intelligence, and crisis judgment|Wargaming for International Relations research
Political Science and Strategic Judgment Foundations|International politics, intelligence, and crisis judgment|Evaluating Escalation: Conceptualizing Escalation in an Era of Emerging Military Technologies
Political Science and Strategic Judgment Foundations|International politics, intelligence, and crisis judgment|Advisers and Aggregation in Foreign Policy Decision Making
Political Science and Strategic Judgment Foundations|Intelligence analysis and structured analytic techniques|Psychology of Intelligence Analysis
Political Science and Strategic Judgment Foundations|Intelligence analysis and structured analytic techniques|Structured Analytic Techniques for Intelligence Analysis
Political Science and Strategic Judgment Foundations|Intelligence analysis and structured analytic techniques|Pearl Harbor: Warning and Decision
Political Science and Strategic Judgment Foundations|Intelligence analysis and structured analytic techniques|Essence of Decision: Explaining the Cuban Missile Crisis
Political Science and Strategic Judgment Foundations|Intelligence analysis and structured analytic techniques|Victims of Groupthink
Political Science and Strategic Judgment Foundations|Intelligence analysis and structured analytic techniques|Analogies at War: Korea Munich Dien Bien Phu and the Vietnam Decisions of 1965
Political Science and Strategic Judgment Foundations|Intelligence analysis and structured analytic techniques|Intelligence Analysis: A Target-Centric Approach
Political Science and Strategic Judgment Foundations|Intelligence analysis and structured analytic techniques|Thinking in Time: The Uses of History for Decision-Makers
Political Science and Strategic Judgment Foundations|Policy analysis and decision-making under deep uncertainty|Decision Making under Deep Uncertainty: From Theory to Practice
Political Science and Strategic Judgment Foundations|Forecasting, hindsight bias, and expert judgment|Hindsight (Not Equal To) Foresight: The Effect of Outcome Knowledge on Judgment Under Uncertainty.
Political Science and Strategic Judgment Foundations|Forecasting, hindsight bias, and expert judgment|Expert Political Judgment: How Good Is It? How Can We Know?
Political Science and Strategic Judgment Foundations|Forecasting, hindsight bias, and expert judgment|Superforecasting: The Art and Science of Prediction
Foundations, Surveys, and Methods|Political science and computational social science overviews|Political-LLM: Large Language Models in Political Science
Foundations, Surveys, and Methods|Political science and computational social science overviews|Large Language Models in Politics and Democracy: A Comprehensive Survey
Foundations, Surveys, and Methods|Political science and computational social science overviews|Can Large Language Models Transform Computational Social Science?
Foundations, Surveys, and Methods|Political science and computational social science overviews|Large language models and political science
Foundations, Surveys, and Methods|Political science and computational social science overviews|Intelligent Computing Social Modeling and Methodological Innovations in Political Science in the Era of Large Language Models
Foundations, Surveys, and Methods|Political science and computational social science overviews|The Consequences of Generative AI for Democracy, Governance and War
Foundations, Surveys, and Methods|Social simulation and agent-based modeling reviews|Large language models empowered agent-based modeling and simulation: a survey and perspectives
Foundations, Surveys, and Methods|Social simulation and agent-based modeling reviews|From Individual to Society: A Survey on Social Simulation Driven by Large Language Model-based Agents
Foundations, Surveys, and Methods|Social simulation and agent-based modeling reviews|Validation is the central challenge for generative social simulation: a critical review of LLMs in agent-based modeling
Foundations, Surveys, and Methods|Social simulation and agent-based modeling reviews|Integrating LLM in Agent-Based Social Simulation: Opportunities and Challenges
Foundations, Surveys, and Methods|Social simulation and agent-based modeling reviews|Generative Agents in Agent-Based Modeling: Overview, Validation, and Emerging Challenges
Foundations, Surveys, and Methods|Social simulation and agent-based modeling reviews|Agent-based modeling as organizational and public policy simulators
Foundations, Surveys, and Methods|Strategic reasoning and game-theoretic reviews|LLM as a Mastermind: A Survey of Strategic Reasoning with Large Language Models
Foundations, Surveys, and Methods|Strategic reasoning and game-theoretic reviews|Game Theory Meets Large Language Models: A Systematic Survey
Foundations, Surveys, and Methods|Strategic reasoning and game-theoretic reviews|Multi-Agent, Human-Agent and Beyond: A Survey on Cooperation in Social Dilemmas
Foundations, Surveys, and Methods|Strategic reasoning and game-theoretic reviews|A Survey on Large Language Model-Based Social Agents in Game-Theoretic Scenarios
Foundations, Surveys, and Methods|Evaluation, validity, and contamination|AI Agents Alone Are Not (Yet) Sufficient for Social Simulation
Foundations, Surveys, and Methods|Evaluation, validity, and contamination|LLM-Based Social Simulations Require a Boundary
Foundations, Surveys, and Methods|Evaluation, validity, and contamination|Leak, Cheat, Repeat: Data Contamination and Evaluation Malpractices in Closed-Source LLMs
Peripheral and Borderline Materials|Generic decision support and human-AI workflow|Determinants of LLM-assisted Decision-Making
Peripheral and Borderline Materials|Generic decision support and human-AI workflow|Who Does What? Archetypes of Roles Assigned to LLMs During Human-AI Decision-Making
Classical Political NLP and Information Extraction|Political text as data and policy-position extraction|Text as Data: The Promise and Pitfalls of Automatic Content Analysis Methods for Political Texts
Classical Political NLP and Information Extraction|Political text as data and policy-position extraction|Computer-Assisted Text Analysis for Comparative Politics
Classical Political NLP and Information Extraction|Political text as data and policy-position extraction|A Method of Automated Nonparametric Content Analysis for Social Science
Classical Political NLP and Information Extraction|Political text as data and policy-position extraction|Extracting Policy Positions from Political Texts Using Words as Data
Classical Political NLP and Information Extraction|Political text as data and policy-position extraction|A Scaling Model for Estimating Time-Series Party Positions from Texts
Classical Political NLP and Information Extraction|Political text as data and policy-position extraction|Fightin' Words: Lexical Feature Selection and Evaluation for Identifying the Content of Political Conflict
Classical Political NLP and Information Extraction|Political text as data and policy-position extraction|How to Analyze Political Attention with Minimal Assumptions and Costs
Classical Political NLP and Information Extraction|Political text as data and policy-position extraction|A Bayesian Hierarchical Topic Model for Political Texts: Measuring Expressed Agendas in Senate Press Releases
Classical Political NLP and Information Extraction|Political text as data and policy-position extraction|How to train your stochastic parrot: large language models for political texts
Classical Political NLP and Information Extraction|Political text as data and policy-position extraction|Measurement in the Age of LLMs: An Application to Ideological Scaling
Classical Political NLP and Information Extraction|Political text as data and policy-position extraction|Measuring Scalar Constructs in Social Science with LLMs
Classical Political NLP and Information Extraction|Political text as data and policy-position extraction|Synthetically generated text for supervised text analysis
Classical Political NLP and Information Extraction|Political text as data and policy-position extraction|Using Imperfect Surrogates for Downstream Inference: Design-based Supervised Learning for Social Science Applications of Large Language Models
Classical Political NLP and Information Extraction|Political text as data and policy-position extraction|Replacing or enhancing the human coder? Multiclass classification of policy documents with large language models
Classical Political NLP and Information Extraction|Legislative speech and policy text classification|Measuring Political Positions from Legislative Speech
Classical Political NLP and Information Extraction|Legislative speech and policy text classification|Get out the vote: Determining support or opposition from Congressional floor-debate transcripts
Classical Political NLP and Information Extraction|Legislative speech and policy text classification|Predicting Legislative Roll Calls from Text
Classical Political NLP and Information Extraction|Legislative speech and policy text classification|Textual Predictors of Bill Survival in Congressional Committees
Classical Political NLP and Information Extraction|Legislative speech and policy text classification|The Media Frames Corpus: Annotations of Frames Across Issues
Classical Political NLP and Information Extraction|Legislative speech and policy text classification|LLM Analysis of 150+ years of German Parliamentary Debates on Migration Reveals Shift from Post-War Solidarity to Anti-Solidarity in the Last Decade
Classical Political NLP and Information Extraction|Political event data and conflict information extraction|An Automated Information Extraction Tool for International Conflict Data with Performance as Good as Human Coders: A Rare Events Evaluation Design
Classical Political NLP and Information Extraction|Political event data and conflict information extraction|Political Science: KEDS-A Program for the Machine Coding of Event Data
Classical Political NLP and Information Extraction|Political event data and conflict information extraction|Automated Coding of International Event Data Using Sparse Parsing Techniques
Classical Political NLP and Information Extraction|Political event data and conflict information extraction|Integrated Data for Events Analysis (IDEA): An Event Typology for Automated Events Data Development
Classical Political NLP and Information Extraction|Political event data and conflict information extraction|Conflict and Mediation Event Observations (CAMEO): A New Event Data Framework for the Analysis of Foreign Policy Interactions
Classical Political NLP and Information Extraction|Political event data and conflict information extraction|The CAMEO (Conflict and Mediation Event Observations) Actor Coding Framework
Classical Political NLP and Information Extraction|Political event data and conflict information extraction|GDELT: Global Data on Events, Location and Tone, 1979-2012
Classical Political NLP and Information Extraction|Political event data and conflict information extraction|Automated Production of High-Volume, Near-Real-Time Political Event Data
Classical Political NLP and Information Extraction|Political event data and conflict information extraction|Automated Coding of Political Event Data
Classical Political NLP and Information Extraction|Political event data and conflict information extraction|Precedents, Progress, and Prospects in Political Event Data
Classical Political NLP and Information Extraction|Political event data and conflict information extraction|Three's a Charm?: Open Event Data Coding with EL:DIABLO, PETRARCH, and the Open Event Data Alliance.
Classical Political NLP and Information Extraction|Political event data and conflict information extraction|Learning to Extract International Relations from Political Context
Classical Political NLP and Information Extraction|Political event data and conflict information extraction|Automatic Extraction of Events from Open Source Text for Predictive Forecasting
Classical Political NLP and Information Extraction|Political event data and conflict information extraction|Improving the selection of news reports for event coding using ensemble classification
Classical Political NLP and Information Extraction|Political event data and conflict information extraction|Creating a Real-Time, Reproducible Event Dataset
Classical Political NLP and Information Extraction|Political event data and conflict information extraction|Political Event Coding as Text-to-Text Sequence Generation
Classical Political NLP and Information Extraction|Political event data and conflict information extraction|Creating Custom Event Data Without Dictionaries: A Bag-of-Tricks
Classical Political NLP and Information Extraction|Political event data and conflict information extraction|Coding with the machines: machine-assisted coding of rare event data
Classical Political NLP and Information Extraction|Political event data and conflict information extraction|ConfliBERT: A Pre-trained Language Model for Political Conflict and Violence
Classical Political NLP and Information Extraction|Political event data and conflict information extraction|Socio-political Events of Conflict and Unrest: A Survey of Available Datasets
Classical Political NLP and Information Extraction|Political event data and conflict information extraction|Bayesian Poisson Tensor Factorization for Inferring Multilateral Relations from Sparse Dyadic Event Counts
Classical Political NLP and Information Extraction|Political event data and conflict information extraction|Multilingual Protest News Detection - Shared Task 1, CASE 2021
Classical Political NLP and Information Extraction|Political event data and conflict information extraction|Applications of GPT in Political Science Research: Extracting Information from Unstructured Text
Politics, Democracy, Public Opinion, and Persuasion|Political ideology, representation, and bias|Whose Opinions Do Language Models Reflect?
Politics, Democracy, Public Opinion, and Persuasion|Political ideology, representation, and bias|Large language models reflect the ideology of their creators
Politics, Democracy, Public Opinion, and Persuasion|Political ideology, representation, and bias|More human than human: measuring ChatGPT political bias
Politics, Democracy, Public Opinion, and Persuasion|Political ideology, representation, and bias|Should ChatGPT be Biased? Challenges and Risks of Bias in Large Language Models
Politics, Democracy, Public Opinion, and Persuasion|Political ideology, representation, and bias|The political ideology of conversational AI: Converging evidence on ChatGPT's pro-environmental, left-libertarian orientation
Politics, Democracy, Public Opinion, and Persuasion|Political ideology, representation, and bias|Cultural bias and cultural alignment of large language models
Politics, Democracy, Public Opinion, and Persuasion|Political ideology, representation, and bias|Large Means Left: Political Bias in Large Language Models Increases with Their Number of Parameters
Politics, Democracy, Public Opinion, and Persuasion|Political ideology, representation, and bias|Ideology-Based LLMs for Content Moderation
Politics, Democracy, Public Opinion, and Persuasion|Political ideology, representation, and bias|Media Source Matters More Than Content: Unveiling Political Bias in LLM-Generated Citations
Politics, Democracy, Public Opinion, and Persuasion|Political ideology, representation, and bias|A Multi-Dimensional Audit of Politically Aligned Large Language Models
Politics, Democracy, Public Opinion, and Persuasion|Political ideology, representation, and bias|Beyond Prompt Brittleness: Evaluating the Reliability and Consistency of Political Worldviews in LLMs
Politics, Democracy, Public Opinion, and Persuasion|Political ideology, representation, and bias|Political Compass or Spinning Arrow? Towards More Meaningful Evaluations for Values and Opinions in Large Language Models
Politics, Democracy, Public Opinion, and Persuasion|Political ideology, representation, and bias|Measuring Political Bias in Large Language Models: What Is Said and How It Is Said
Politics, Democracy, Public Opinion, and Persuasion|Political ideology, representation, and bias|The Political Biases of ChatGPT
Politics, Democracy, Public Opinion, and Persuasion|Political ideology, representation, and bias|Assessing political bias in large language models
Politics, Democracy, Public Opinion, and Persuasion|Political ideology, representation, and bias|What Is The Political Content in LLMs' Pre- and Post-Training Data?
Politics, Democracy, Public Opinion, and Persuasion|Political ideology, representation, and bias|From Pretraining Data to Language Models to Downstream Tasks: Tracking the Trails of Political Biases Leading to Unfair NLP Models
Politics, Democracy, Public Opinion, and Persuasion|Multilingual and geopolitical bias|Echoes of Power: Investigating Geopolitical Bias in US and China Large Language Models
Politics, Democracy, Public Opinion, and Persuasion|Multilingual and geopolitical bias|An evaluation of LLMs for political bias in Western media: Israel-Hamas and Ukraine-Russia wars
Politics, Democracy, Public Opinion, and Persuasion|Multilingual and geopolitical bias|Assessing the Political Fairness of Multilingual LLMs: A Case Study based on a 21-way Multiparallel EuroParl Dataset
Politics, Democracy, Public Opinion, and Persuasion|Multilingual and geopolitical bias|The Language You Ask In: Language-Conditioned Ideological Divergence in LLM Analysis of Contested Political Documents
Politics, Democracy, Public Opinion, and Persuasion|Multilingual and geopolitical bias|This Land is Your, My Land: Evaluating Geopolitical Bias in Language Models through Territorial Disputes
Politics, Democracy, Public Opinion, and Persuasion|Multilingual and geopolitical bias|Mapping Geopolitical Bias in 11 Large Language Models: A Bilingual, Dual-Framing Analysis of U.S.-China Tensions
Politics, Democracy, Public Opinion, and Persuasion|Multilingual and geopolitical bias|Political biases and inconsistencies in bilingual GPT models—the cases of the U.S. and China
Politics, Democracy, Public Opinion, and Persuasion|Multilingual and geopolitical bias|International political bias in large language models: a critical discourse analysis of narratives in ChatGPT, LLaMA, Gemini, and DeepSeek
Politics, Democracy, Public Opinion, and Persuasion|Multilingual and geopolitical bias|Framing Political Bias in Multilingual LLMs Across Pakistani Languages
Politics, Democracy, Public Opinion, and Persuasion|Multilingual and geopolitical bias|Democratic or Authoritarian? Probing a New Dimension of Political Biases in Large Language Models
Politics, Democracy, Public Opinion, and Persuasion|Multilingual and geopolitical bias|Bias Beyond Borders: Political Ideology Evaluation and Steering in Multilingual LLMs
Politics, Democracy, Public Opinion, and Persuasion|Multilingual and geopolitical bias|John vs. Ahmed: Debate-Induced Bias in Multilingual LLMs
Politics, Democracy, Public Opinion, and Persuasion|Elections, voters, and campaign discourse|ElectionSim: Massive Population Election Simulation Powered by Large Language Model Driven Agents
Politics, Democracy, Public Opinion, and Persuasion|Elections, voters, and campaign discourse|Large-Scale Longitudinal Study of LLMs During the 2024 United States Election Season
Politics, Democracy, Public Opinion, and Persuasion|Elections, voters, and campaign discourse|A Public Dataset Tracking Social Media Discourse about the 2024 U.S. Presidential Election on Twitter/X
Politics, Democracy, Public Opinion, and Persuasion|Elections, voters, and campaign discourse|Hidden Persuaders: LLMs’ Political Leaning and Their Influence on Voters
Politics, Democracy, Public Opinion, and Persuasion|Public opinion, polling, and political annotation|Large language models as a substitute for human experts in annotating political text
Politics, Democracy, Public Opinion, and Persuasion|Public opinion, polling, and political annotation|Demonstrations of the Potential of AI-based Political Issue Polling
Politics, Democracy, Public Opinion, and Persuasion|Public opinion, polling, and political annotation|Performance and biases of Large Language Models in public opinion simulation
Politics, Democracy, Public Opinion, and Persuasion|Public opinion, polling, and political annotation|Random Silicon Sampling: Simulating Human Sub-Population Opinion Using a Large Language Model Based on Group-Level Demographic Information
Politics, Democracy, Public Opinion, and Persuasion|Public opinion, polling, and political annotation|ChatGPT-4 Outperforms Experts and Crowd Workers in Annotating Political Twitter Messages with Zero-Shot Learning
Politics, Democracy, Public Opinion, and Persuasion|Public opinion, polling, and political annotation|AlignSurvey: A Comprehensive Benchmark for Human Preferences Alignment in Social Surveys
Politics, Democracy, Public Opinion, and Persuasion|Public opinion, polling, and political annotation|Can AI reflect public opinion? Evidence from replicating Hainmueller and Hopkins' immigration experiment with LLMs
Politics, Democracy, Public Opinion, and Persuasion|Public opinion, polling, and political annotation|Adaptive political surveys and GPT-4: Tackling the cold start problem with simulated user interactions
Politics, Democracy, Public Opinion, and Persuasion|Deliberation, persuasion, and information environments|Generative Echo Chamber? Effect of LLM-Powered Search Systems on Diverse Information Seeking
Politics, Democracy, Public Opinion, and Persuasion|Deliberation, persuasion, and information environments|Systematic Biases in LLM Simulations of Debates
Politics, Democracy, Public Opinion, and Persuasion|Deliberation, persuasion, and information environments|From Skepticism to Acceptance: Simulating the Attitude Dynamics Toward Fake News
Politics, Democracy, Public Opinion, and Persuasion|Deliberation, persuasion, and information environments|When Two LLMs Debate, Both Think They'll Win
Politics, Democracy, Public Opinion, and Persuasion|Deliberation, persuasion, and information environments|Looking Under the Hood: How LLMs Attempt Political Persuasion and Microtargeting
Politics, Democracy, Public Opinion, and Persuasion|Legislative and political-agent simulation|Political Actor Agent: Simulating Legislative Politics with LLM Agents
Politics, Democracy, Public Opinion, and Persuasion|Legislative and political-agent simulation|LegiGPT: Party Politics and Transport Policy with Large Language Model
Politics, Democracy, Public Opinion, and Persuasion|Legislative and political-agent simulation|A Large-Scale Simulation on Large Language Models for Decision-Making in Political Science
Politics, Democracy, Public Opinion, and Persuasion|Legislative and political-agent simulation|ParlAI Vote: A Web Platform for Analyzing Gender and Political Bias in Large Language Models
Politics, Democracy, Public Opinion, and Persuasion|Legislative and political-agent simulation|ParliaBench: An Evaluation and Benchmarking Framework for LLM-Generated Parliamentary Speech
Politics, Democracy, Public Opinion, and Persuasion|Legislative and political-agent simulation|Persona-driven Simulation of Voting Behavior in the European Parliament with Large Language Models
Policymaking, Governance, and Institutional Decision Support|Democratic governance and augmentation|Large Language Models as agents for augmented democracy
Policymaking, Governance, and Institutional Decision Support|Democratic governance and augmentation|Surfacing citizens’ policy perspectives at scale in the age of large language models
Policymaking, Governance, and Institutional Decision Support|Democratic governance and augmentation|Simulating Policy Discussions with Digital Footprints and Large Language Models
Policymaking, Governance, and Institutional Decision Support|Democratic governance and augmentation|Digital Homunculi and Institutional Design: Breaking Through the Experimentation Bottleneck
Policymaking, Governance, and Institutional Decision Support|Democratic governance and augmentation|Democracy-in-Silico: Institutional Design as Alignment in AI-Governed Polities
Policymaking, Governance, and Institutional Decision Support|Democratic governance and augmentation|Using LLMs to Enhance Democracy
Policymaking, Governance, and Institutional Decision Support|Policy translation and policy brief generation|Sci2Pol: Evaluating and Fine-tuning LLMs on Scientific-to-Policy Brief Generation
Policymaking, Governance, and Institutional Decision Support|Policy translation and policy brief generation|The End of the Policy Analyst? Testing the Capability of Artificial Intelligence to Generate Plausible, Persuasive, and Useful Policy Analysis
Policymaking, Governance, and Institutional Decision Support|Policy translation and policy brief generation|Automating public policy: a comparative study of conversational artificial intelligence models and human expertise in crafting briefing notes
Policymaking, Governance, and Institutional Decision Support|Policy persuasion and democratic deliberation|AI can help humans find common ground in democratic deliberation
Policymaking, Governance, and Institutional Decision Support|Policy persuasion and democratic deliberation|Large Language Models Can Argue in Convincing Ways About Politics, But Humans Dislike AI Authors: Implications for Governance
Policymaking, Governance, and Institutional Decision Support|Policy persuasion and democratic deliberation|LLM-generated messages can persuade humans on policy issues
Policymaking, Governance, and Institutional Decision Support|Policy persuasion and democratic deliberation|PoliCon: Evaluating LLMs on Achieving Diverse Political Consensus Objectives
Policymaking, Governance, and Institutional Decision Support|Policy persuasion and democratic deliberation|Can AI Truly Represent Your Voice in Deliberations? A Comprehensive Study of Large-Scale Opinion Aggregation with LLMs
Policymaking, Governance, and Institutional Decision Support|Policy persuasion and democratic deliberation|AI in Conflict Resolution: Practical Considerations, Opportunities and Challenges
Policymaking, Governance, and Institutional Decision Support|Policy persuasion and democratic deliberation|DeliberationBench: A Normative Benchmark for the Influence of Large Language Models on Users'Views
Policymaking, Governance, and Institutional Decision Support|Policy persuasion and democratic deliberation|Bringing Everyone to the Table: An Experimental Study of LLM-Facilitated Group Decision Making
Policymaking, Governance, and Institutional Decision Support|Policy persuasion and democratic deliberation|An Emergent Understanding of Human-AI Collaboration in Deliberation
Policymaking, Governance, and Institutional Decision Support|Policy persuasion and democratic deliberation|Hyperdemocracy: Towards Creative Consensus Building between Humans and AI
Policymaking, Governance, and Institutional Decision Support|Policy persuasion and democratic deliberation|Generative Social Choice
Policymaking, Governance, and Institutional Decision Support|Policy persuasion and democratic deliberation|Leveraging AI in peace processes: A framework for digital dialogues
Policymaking, Governance, and Institutional Decision Support|Policy persuasion and democratic deliberation|PTFA: An LLM-based Agent that Facilitates Online Consensus Building through Parallel Thinking
Policymaking, Governance, and Institutional Decision Support|Policy persuasion and democratic deliberation|Can AI Deliberate? Evaluating Deliberative Quality and Stance Flow in Multi-Agent LLMs
Policymaking, Governance, and Institutional Decision Support|Policy persuasion and democratic deliberation|Can AI mediation improve democratic deliberation?
Policymaking, Governance, and Institutional Decision Support|Policy persuasion and democratic deliberation|Generating Fair Consensus Statements with Social Choice on Token-Level MDPs
Policymaking, Governance, and Institutional Decision Support|Policy persuasion and democratic deliberation|Preserving Disagreement: Architectural Heterogeneity and Coherence Validation in Multi-Agent Policy Simulation
Policymaking, Governance, and Institutional Decision Support|Policy persuasion and democratic deliberation|Toward an artificial deliberation? On Google DeepMind’s Habermas Machine
Policymaking, Governance, and Institutional Decision Support|Policy persuasion and democratic deliberation|Opportunities and Risks of LLMs for Scalable Deliberation with Polis
Policymaking, Governance, and Institutional Decision Support|Strategic and institutional decision support|Biased LLMs can Influence Political Decision-Making
Peripheral and Borderline Materials|Business and managerial strategy|Generative Artificial Intelligence and Evaluating Strategic Decisions
Policymaking, Governance, and Institutional Decision Support|Strategic and institutional decision support|The LLM Effect: Are Humans Truly Using LLMs, or Are They Being Influenced By Them Instead?
Peripheral and Borderline Materials|Policy-adjacent service delivery and operations|Can A Society of Generative Agents Simulate Human Behavior and Inform Public Health Policy? A Case Study on Vaccine Hesitancy
Policymaking, Governance, and Institutional Decision Support|Strategic and institutional decision support|LLM Powered Social Digital Twins: A Framework for Simulating Population Behavioral Response to Policy Interventions
Policymaking, Governance, and Institutional Decision Support|Strategic and institutional decision support|WhatIf: Interactive Exploration of LLM-Powered Social Simulations for Policy Reasoning
Policymaking, Governance, and Institutional Decision Support|Strategic evaluation, bias, and foresight|Social Policy of Large Language Models: How GPT, Claude, DeepSeek and Grok Allocate Social Budgets in Spain and Germany
Policymaking, Governance, and Institutional Decision Support|Public-sector decision support and institutional workflow|Human-AI Interactions in Public Sector Decision-Making:"Automation Bias"and"Selective Adherence"to Algorithmic Advice
Policymaking, Governance, and Institutional Decision Support|Public-sector decision support and institutional workflow|What Makes LLM Agent Simulations Useful for Policy? Insights From an Iterative Design Engagement in Emergency Preparedness
Policymaking, Governance, and Institutional Decision Support|Public-sector decision support and institutional workflow|Are We Asking the Right Questions?: Designing for Community Stakeholders’ Interactions with AI in Policing
Policymaking, Governance, and Institutional Decision Support|Public-sector decision support and institutional workflow|A Methodology to Develop Agent-Based Models for Policy Support Via Qualitative Inquiry
Peripheral and Borderline Materials|Generic decision support and human-AI workflow|An Institutional Theory Framework for Leveraging Large Language Models for Policy Analysis and Intervention Design
Policymaking, Governance, and Institutional Decision Support|Public-sector decision support and institutional workflow|More than an IT system in the government: The work divide challenges in human-AI coworking context
Peripheral and Borderline Materials|Policy-adjacent service delivery and operations|Large Language Model–Powered Public Service Platforms for Automated Case Assistance and Decision Support
Peripheral and Borderline Materials|Policy-adjacent service delivery and operations|Human‑Centered Governance for AI‑Augmented Decision Support in Public‑Sector Logistics
Policymaking, Governance, and Institutional Decision Support|Accountability, auditing, and public-sector AI governance|Institutionalizing Predictive AI in Public Administration: Algorithmic Governance and the Case of a Wildfire Forecasting System
Peripheral and Borderline Materials|Generic decision support and human-AI workflow|DataGovBench: Benchmarking LLM Agents for Real-World Data Governance Workflows
Policymaking, Governance, and Institutional Decision Support|Accountability, auditing, and public-sector AI governance|Audit Trails for Accountability in Large Language Models
Policymaking, Governance, and Institutional Decision Support|Accountability, auditing, and public-sector AI governance|Informing Human Decision-Making in Public Administration through NLP Algorithm Audits
Policymaking, Governance, and Institutional Decision Support|Accountability, auditing, and public-sector AI governance|Impacts of AI-based anti-corruption audits on risk aversion in decision-making: a case study of the Brazilian ALICE tool
Policymaking, Governance, and Institutional Decision Support|Accountability, auditing, and public-sector AI governance|AI and Corruption: Legal Liability in Algorithmic Decision-Making
Policymaking, Governance, and Institutional Decision Support|Accountability, auditing, and public-sector AI governance|Governing AI with trust: an adaptive framework for institutional legitimacy in the UK public sector
Peripheral and Borderline Materials|Business and managerial strategy|How Well Can AI Do Strategy? Empirical Benchmarking Using Strategy Simulations
Peripheral and Borderline Materials|Business and managerial strategy|AI-Augmented Strategic Decision-Making Under Time Constraints: An Experimental Study on Mental Representations and Strategic Foresight
Peripheral and Borderline Materials|Generic decision support and human-AI workflow|Towards Using Prompt Engineering in Large Language Models to Assist Decision Making
Peripheral and Borderline Materials|Business and managerial strategy|Beyond Black Boxes: Designing and Testing Agentic AI Systems for Strategy
Peripheral and Borderline Materials|Business and managerial strategy|Can AI Do Strategy?
Peripheral and Borderline Materials|Generic decision support and human-AI workflow|Advancing Decision-Making through AI-Human Collaboration: A Systematic Review and Conceptual Framework
Peripheral and Borderline Materials|Business and managerial strategy|Can AI Do Strategy? A Dialogue and Debate
Peripheral and Borderline Materials|Business and managerial strategy|Reproducing and Extending Experiments in Behavioral Strategy with Large Language Models
Peripheral and Borderline Materials|Business and managerial strategy|AI strategy under institutional pressure: strategic conformity and decision-making in large language models
Peripheral and Borderline Materials|Business and managerial strategy|Bias in, symbolic compliance out? GPT's reliance on gender and race in strategic evaluations
Peripheral and Borderline Materials|Business and managerial strategy|From Problems to Solutions in Strategic Decision-Making: The Effects of Generative AI on Problem Formulation
Geopolitics, Diplomacy, National Security, and Wargaming|Diplomacy and international institutions|Human-level play in the game of Diplomacy by combining language models with strategic reasoning
Geopolitics, Diplomacy, National Security, and Wargaming|Diplomacy and international institutions|Critical Foreign Policy Decisions Benchmark: Measuring Diplomatic Preferences in Large Language Models
Geopolitics, Diplomacy, National Security, and Wargaming|Diplomacy and international institutions|Benchmarking LLMs for Political Science: A United Nations Perspective / United Nations Benchmark
Geopolitics, Diplomacy, National Security, and Wargaming|Diplomacy and international institutions|UNSC-Bench: Evaluating LLM Diplomatic Role-Playing Through UN Security Council Vote Prediction
Geopolitics, Diplomacy, National Security, and Wargaming|Diplomacy and international institutions|DipLLM: Fine-Tuning LLM for Strategic Decision-making in Diplomacy
Geopolitics, Diplomacy, National Security, and Wargaming|Diplomacy and international institutions|Richelieu: Self-Evolving LLM-Based Agents for AI Diplomacy
Geopolitics, Diplomacy, National Security, and Wargaming|Diplomacy and international institutions|DiplomacyAgent: Do LLMs Balance Interests and Ethical Principles in International Events?
Geopolitics, Diplomacy, National Security, and Wargaming|Diplomacy and international institutions|ALGORITHMIC DIPLOMACY: THE ROLE OF ARTIFICIAL INTELLIGENCE IN SHAPING 21ST CENTURY FOREIGN POLICY DECISIONS
Geopolitics, Diplomacy, National Security, and Wargaming|Diplomacy and international institutions|Democratizing Diplomacy: A Harness for Evaluating Any Large Language Model on Full-Press Diplomacy
Geopolitics, Diplomacy, National Security, and Wargaming|Military decision-making and wargaming|Escalation Risks from Language Models in Military and Diplomatic Decision-Making
Geopolitics, Diplomacy, National Security, and Wargaming|Military decision-making and wargaming|Behavioral Differences Between Expert Humans and Language Models in Wargame Simulations / Human vs. Machine
Geopolitics, Diplomacy, National Security, and Wargaming|Military decision-making and wargaming|Open-Ended Wargames with Large Language Models
Geopolitics, Diplomacy, National Security, and Wargaming|Military decision-making and wargaming|LLM-based wargame scenario generation with domain ontology
Geopolitics, Diplomacy, National Security, and Wargaming|Military decision-making and wargaming|COA-GPT: Generative Pre-Trained Transformers for Accelerated Course of Action Development in Military Operations
Geopolitics, Diplomacy, National Security, and Wargaming|Military decision-making and wargaming|BattleAgent: Multi-modal Dynamic Emulation on Historical Battles to Complement Historical Analysis
Geopolitics, Diplomacy, National Security, and Wargaming|Military decision-making and wargaming|Causal Reasoning and Large Language Models for Military Decision-Making: Rethinking the Command Structures in the Era of Generative AI
Geopolitics, Diplomacy, National Security, and Wargaming|Military decision-making and wargaming|Effective and responsible use of large language models in strategic wargaming
Geopolitics, Diplomacy, National Security, and Wargaming|Military decision-making and wargaming|Red Lines and Grey Zones in the Fog of War: Benchmarking Legal Risk, Moral Harm, and Regional Bias in Large Language Model Military Decision-Making
Geopolitics, Diplomacy, National Security, and Wargaming|Military decision-making and wargaming|WARBENCH: A Comprehensive Benchmark for Evaluating LLMs in Military Decision-Making
Geopolitics, Diplomacy, National Security, and Wargaming|Military decision-making and wargaming|ARMOR 2025: A Military-Aligned Benchmark for Evaluating Large Language Model Safety Beyond Civilian Contexts
Geopolitics, Diplomacy, National Security, and Wargaming|Military decision-making and wargaming|Stable and Expert-Aligned Evaluation of Wargaming Strategies via Optimized LLM Scoring Agents
Geopolitics, Diplomacy, National Security, and Wargaming|Military decision-making and wargaming|The Prompt War: How AI Decides on a Military Intervention
Geopolitics, Diplomacy, National Security, and Wargaming|Military decision-making and wargaming|Measuring Free-Form Decision-Making Inconsistency of Language Models in Military Crisis Simulations
Geopolitics, Diplomacy, National Security, and Wargaming|Military decision-making and wargaming|Battlefield information and tactics engine (BITE): a multimodal large language model approach for battlespace management
Geopolitics, Diplomacy, National Security, and Wargaming|Military decision-making and wargaming|Integrators at War: Mediating in AI-assisted Resort-to-Force Decisions
Geopolitics, Diplomacy, National Security, and Wargaming|Military decision-making and wargaming|Upskilling human actors against AI automation bias in strategic decision making on the resort to force
Geopolitics, Diplomacy, National Security, and Wargaming|Military decision-making and wargaming|Integrating Generative AI into Tactical Military Decision-Making
Geopolitics, Diplomacy, National Security, and Wargaming|Conflict, escalation, and geopolitical simulation|Simulating Influence Dynamics with LLM Agents
Geopolitics, Diplomacy, National Security, and Wargaming|Conflict, escalation, and geopolitical simulation|LLMs as Strategic Actors: Behavioral Alignment, Risk Calibration, and Argumentation Framing in Geopolitical Simulations
Geopolitics, Diplomacy, National Security, and Wargaming|Conflict, escalation, and geopolitical simulation|War and Peace (WarAgent): Large Language Model-based Multi-Agent Simulation of World Wars
Geopolitics, Diplomacy, National Security, and Wargaming|Conflict, escalation, and geopolitical simulation|Do Large Language Models Know Conflict? Investigating Parametric vs. Non-Parametric Knowledge of LLMs for Conflict Forecasting
Geopolitics, Diplomacy, National Security, and Wargaming|Conflict, escalation, and geopolitical simulation|When AI Navigates the Fog of War
Geopolitics, Diplomacy, National Security, and Wargaming|Conflict, escalation, and geopolitical simulation|Managing Escalation in Off-the-Shelf Large Language Models
Geopolitics, Diplomacy, National Security, and Wargaming|Conflict, escalation, and geopolitical simulation|AI Arms and Influence: Frontier Models Exhibit Sophisticated Reasoning in Simulated Nuclear Crises
Geopolitics, Diplomacy, National Security, and Wargaming|Conflict, escalation, and geopolitical simulation|Waltzing into uncertainty: AI in nuclear decision making and the challenge of divergent deterrence logics
Geopolitics, Diplomacy, National Security, and Wargaming|Conflict, escalation, and geopolitical simulation|Hacking Nuclear Stability: Wargaming Technology, Uncertainty, and Escalation
Geopolitics, Diplomacy, National Security, and Wargaming|Conflict, escalation, and geopolitical simulation|What is Escalation? Measuring Crisis Dynamics in International Relations with Human and LLM Generated Event Data
Geopolitics, Diplomacy, National Security, and Wargaming|National security applications and doctrine|On Large Language Models in National Security Applications
Geopolitics, Diplomacy, National Security, and Wargaming|National security applications and doctrine|Governing Automated Strategic Intelligence
Forecasting, Geopolitical Risk, and Foresight|Forecasting benchmarks and datasets|ForecastBench: A Dynamic Benchmark of AI Forecasting Capabilities
Forecasting, Geopolitical Risk, and Foresight|Forecasting benchmarks and datasets|MIRAI: Evaluating LLM Agents for Event Forecasting
Forecasting, Geopolitical Risk, and Foresight|Forecasting benchmarks and datasets|Forecasting Future International Events: A Reliable Dataset for Text-Based Event Modeling / WORLDREP
Forecasting, Geopolitical Risk, and Foresight|Forecasting benchmarks and datasets|OpenEP: Open-Ended Future Event Prediction
Forecasting, Geopolitical Risk, and Foresight|Forecasting benchmarks and datasets|Forecasting Future World Events with Neural Networks
Forecasting, Geopolitical Risk, and Foresight|Forecasting benchmarks and datasets|Bench to the Future: A Pastcasting Benchmark for Forecasting Agents
Peripheral and Borderline Materials|General forecasting benchmarks|The Future Outcome Reasoning and Confidence Assessment Benchmark
Forecasting, Geopolitical Risk, and Foresight|Forecasting benchmarks and datasets|Automating Forecasting Question Generation and Resolution for AI Evaluation
Forecasting, Geopolitical Risk, and Foresight|Forecasting benchmarks and datasets|PROPHET: An Inferable Future Forecasting Benchmark with Causal Intervened Likelihood Estimation
Forecasting, Geopolitical Risk, and Foresight|Forecasting benchmarks and datasets|LLM-as-a-Prophet: Understanding Predictive Intelligence with Prophet Arena
Forecasting, Geopolitical Risk, and Foresight|Forecasting benchmarks and datasets|OracleProto: A Reproducible Framework for Benchmarking LLM Native Forecasting via Knowledge Cutoff and Temporal Masking
Forecasting, Geopolitical Risk, and Foresight|Forecasting benchmarks and datasets|TruthTensor: Evaluating LLMs through Human Imitation on Prediction Market under Drift and Holistic Reasoning
Forecasting, Geopolitical Risk, and Foresight|Forecasting performance and aggregation|Approaching Human-Level Forecasting with Language Models
Forecasting, Geopolitical Risk, and Foresight|Forecasting performance and aggregation|A Comprehensive Evaluation of Large Language Models on Temporal Event Forecasting
Forecasting, Geopolitical Risk, and Foresight|Forecasting performance and aggregation|The Power of Simplicity in LLM-Based Event Forecasting
Forecasting, Geopolitical Risk, and Foresight|Forecasting performance and aggregation|The Future Is Unevenly Distributed: Forecasting Ability of LLMs Depends on What We’re Asking
Forecasting, Geopolitical Risk, and Foresight|Forecasting performance and aggregation|Wisdom of the silicon crowd: LLM ensemble prediction capabilities rival human crowd accuracy
Forecasting, Geopolitical Risk, and Foresight|Forecasting performance and aggregation|Large Language Model Prediction Capabilities: Evidence from a Real-World Forecasting Tournament
Forecasting, Geopolitical Risk, and Foresight|Forecasting performance and aggregation|Are LLMs Prescient? A Continuous Evaluation using Daily News as the Oracle
Forecasting, Geopolitical Risk, and Foresight|Forecasting performance and aggregation|Advancing Event Forecasting through Massive Training of Large Language Models: Challenges, Solutions, and Broader Impacts
Forecasting, Geopolitical Risk, and Foresight|Forecasting performance and aggregation|AIA Forecaster: Technical Report
Forecasting, Geopolitical Risk, and Foresight|Forecasting performance and aggregation|Pitfalls in Evaluating Language Model Forecasters
Forecasting, Geopolitical Risk, and Foresight|Forecasting performance and aggregation|Do Language Models Update their Forecasts with New Information?
Forecasting, Geopolitical Risk, and Foresight|Forecasting performance and aggregation|LLMs Can Teach Themselves to Better Predict the Future
Forecasting, Geopolitical Risk, and Foresight|Forecasting performance and aggregation|Evaluating LLMs on Real-World Forecasting Against Expert Forecasters
Forecasting, Geopolitical Risk, and Foresight|Forecasting performance and aggregation|Can Language Models Use Forecasting Strategies?
Forecasting, Geopolitical Risk, and Foresight|Forecasting performance and aggregation|TimeSeek: Temporal Reliability of Agentic Forecasters
Forecasting, Geopolitical Risk, and Foresight|Forecasting performance and aggregation|Agentic Forecasting using Sequential Bayesian Updating of Linguistic Beliefs
Forecasting, Geopolitical Risk, and Foresight|Forecasting performance and aggregation|Simulated Ignorance Fails: A Systematic Study of LLM Behaviors on Forecasting Problems Before Model Knowledge Cutoff
Forecasting, Geopolitical Risk, and Foresight|Forecasting performance and aggregation|Artificial Intelligence in Political Forecasting: Possibilities and Limitations
Forecasting, Geopolitical Risk, and Foresight|Forecasting performance and aggregation|AI-Augmented Predictions: LLM Assistants Improve Human Forecasting Accuracy
Forecasting, Geopolitical Risk, and Foresight|Forecasting performance and aggregation|Scaling Open-Ended Reasoning to Predict the Future
Forecasting, Geopolitical Risk, and Foresight|Forecasting performance and aggregation|Crowdsourced versus large language models forecasting: evidence for the accuracy–correlation effect
Forecasting, Geopolitical Risk, and Foresight|Forecasting performance and aggregation|Scattered Hypothesis Generation for Open-Ended Event Forecasting
Forecasting, Geopolitical Risk, and Foresight|Geopolitical event prediction systems|LLM4Geopolitics: A Framework Leveraging Large Language Models for Predicting Geopolitical Events
Forecasting, Geopolitical Risk, and Foresight|Geopolitical event prediction systems|Multi-Source Models for Civil Unrest Forecasting
Forecasting, Geopolitical Risk, and Foresight|Geopolitical event prediction systems|Toward Better Temporal Structures for Geopolitical Events Forecasting
Forecasting, Geopolitical Risk, and Foresight|Geopolitical event prediction systems|Agentic Reasoning for Social Event Extrapolation: Integrating Knowledge Graphs and Language Models
Forecasting, Geopolitical Risk, and Foresight|Geopolitical event prediction systems|ThinkTank-ME: A Multi-Expert Framework for Middle East Event Forecasting
Forecasting, Geopolitical Risk, and Foresight|Geopolitical event prediction systems|AutoCast++: Enhancing World Event Prediction with Zero-shot Ranking-based Context Retrieval
Forecasting, Geopolitical Risk, and Foresight|Geoeconomic and geopolitical risk signals|Geoeconomic Pressure
Forecasting, Geopolitical Risk, and Foresight|Geoeconomic and geopolitical risk signals|The AI-GPR Index: Measuring Geopolitical Risk using Artificial Intelligence
Strategic Reasoning, Games, Negotiation, and Cooperation|Game-theoretic and strategic reasoning benchmarks|Playing repeated games with large language models
Strategic Reasoning, Games, Negotiation, and Cooperation|Game-theoretic and strategic reasoning benchmarks|Strategic behavior of large language models and the role of game structure versus contextual framing
Strategic Reasoning, Games, Negotiation, and Cooperation|Game-theoretic and strategic reasoning benchmarks|GTBench: Uncovering the Strategic Reasoning Limitations of LLMs via Game-Theoretic Evaluations
Strategic Reasoning, Games, Negotiation, and Cooperation|Game-theoretic and strategic reasoning benchmarks|GameBench: Evaluating Strategic Reasoning Abilities of LLM Agents
Peripheral and Borderline Materials|Generic negotiation and behavioral games|How Far Are We on the Decision-Making of LLMs? Evaluating LLMs' Gaming Ability in Multi-Agent Environments
Peripheral and Borderline Materials|Generic negotiation and behavioral games|Game-theoretic LLM: Agent Workflow for Negotiation Games
Peripheral and Borderline Materials|Generic negotiation and behavioral games|Decision-Making Behavior Evaluation Framework for LLMs under Uncertain Context
Strategic Reasoning, Games, Negotiation, and Cooperation|Game-theoretic and strategic reasoning benchmarks|SPIN-Bench: How Well Do LLMs Plan Strategically and Reason Socially?
Strategic Reasoning, Games, Negotiation, and Cooperation|Game-theoretic and strategic reasoning benchmarks|Multi-Agent Strategic Games with LLMs
Strategic Reasoning, Games, Negotiation, and Cooperation|Game-theoretic and strategic reasoning benchmarks|Strategic Reasoning with Language Models
Strategic Reasoning, Games, Negotiation, and Cooperation|Game-theoretic and strategic reasoning benchmarks|Why Do LLMs Struggle in Strategic Play? Broken Links Between Observations, Beliefs, and Actions
Peripheral and Borderline Materials|Generic negotiation and behavioral games|SOTOPIA: Interactive Evaluation for Social Intelligence in Language Agents
Peripheral and Borderline Materials|Generic negotiation and behavioral games|Exploring Large Language Models for Communication Games: An Empirical Study on Werewolf
Peripheral and Borderline Materials|Generic negotiation and behavioral games|Improving Language Model Negotiation with Self-Play and In-Context Learning from AI Feedback
Peripheral and Borderline Materials|Generic negotiation and behavioral games|Measuring Bargaining Abilities of LLMs: A Benchmark and A Buyer-Enhancement Method
Peripheral and Borderline Materials|Generic negotiation and behavioral games|When Reasoning Models Hurt Behavioral Simulation: A Solver-Sampler Mismatch in Multi-Agent LLM Negotiation
Peripheral and Borderline Materials|Generic negotiation and behavioral games|LLM-Deliberation: Evaluating LLMs with Interactive Multi-Agent Negotiation Games
Peripheral and Borderline Materials|Generic negotiation and behavioral games|Cooperate or Collapse: Emergence of Sustainable Cooperation in a Society of LLM Agents
Peripheral and Borderline Materials|Generic negotiation and behavioral games|Nicer Than Humans: How do Large Language Models Behave in the Prisoner's Dilemma?
Peripheral and Borderline Materials|Generic negotiation and behavioral games|Shall We Team Up: Exploring Spontaneous Cooperation of Competing LLM Agents
Peripheral and Borderline Materials|Generic negotiation and behavioral games|Cultural Evolution of Cooperation among LLM Agents
Peripheral and Borderline Materials|Generic negotiation and behavioral games|Communication Enhances LLMs' Stability in Strategic Thinking
Peripheral and Borderline Materials|Generic negotiation and behavioral games|A Turing test of whether AI chatbots are behaviorally similar to humans
Strategic Reasoning, Games, Negotiation, and Cooperation|Behavioral game tests and human-like strategy|Simulating Human Strategic Behavior: Comparing Single and Multi-agent LLMs
Strategic Reasoning, Games, Negotiation, and Cooperation|Behavioral game tests and human-like strategy|Simulating Strategic Reasoning: Comparing the Ability of Single LLMs and Multi-Agent Systems to Replicate Human Behavior
Strategic Reasoning, Games, Negotiation, and Cooperation|Behavioral game tests and human-like strategy|Beyond Nash Equilibrium: Bounded Rationality of LLMs and humans in Strategic Decision-making
Strategic Reasoning, Games, Negotiation, and Cooperation|Behavioral game tests and human-like strategy|CHBench: A Cognitive Hierarchy Benchmark for Evaluating Strategic Reasoning Capability of LLMs
Multi-Agent Social Simulation and Synthetic Societies|Generative agents and social simulation platforms|Generative Agents: Interactive Simulacra of Human Behavior
Multi-Agent Social Simulation and Synthetic Societies|Generative agents and social simulation platforms|AgentSociety: Large-Scale Simulation of LLM-Driven Generative Agents Advances Understanding of Human Behaviors and Society
Multi-Agent Social Simulation and Synthetic Societies|Generative agents and social simulation platforms|S3: Social-network Simulation System with Large Language Model-Empowered Agents
Multi-Agent Social Simulation and Synthetic Societies|Generative agents and social simulation platforms|GA-S3: Comprehensive Social Network Simulation with Group Agents
Multi-Agent Social Simulation and Synthetic Societies|Generative agents and social simulation platforms|OASIS: Open Agent Social Interaction Simulations with One Million Agents
Multi-Agent Social Simulation and Synthetic Societies|Generative agents and social simulation platforms|GenSim: A General Social Simulation Platform with Large Language Model based Agents
Multi-Agent Social Simulation and Synthetic Societies|Generative agents and social simulation platforms|SocioVerse: A World Model for Social Simulation Powered by LLM Agents and A Pool of 10 Million Real-World Users
Multi-Agent Social Simulation and Synthetic Societies|Generative agents and social simulation platforms|Social Simulacra: Creating Populated Prototypes for Social Computing Systems
Multi-Agent Social Simulation and Synthetic Societies|Synthetic populations and human samples|Out of One, Many: Using Language Models to Simulate Human Samples
Multi-Agent Social Simulation and Synthetic Societies|Synthetic populations and human samples|Using Large Language Models to Simulate Multiple Humans and Replicate Human Subject Studies
Multi-Agent Social Simulation and Synthetic Societies|Synthetic populations and human samples|Generative Agent Simulations of 1,000 People
Multi-Agent Social Simulation and Synthetic Societies|Synthetic populations and human samples|Beyond Demographics: Aligning Role-playing LLM-based Agents Using Human Belief Networks
Multi-Agent Social Simulation and Synthetic Societies|Synthetic populations and human samples|Analysing LLM Persona Generation and Fairness Interpretation in Polarised Geopolitical Contexts
Multi-Agent Social Simulation and Synthetic Societies|Synthetic populations and human samples|Do we Still Need People? Comparing Human and LLM Personas in Political Modeling and Simulation
Multi-Agent Social Simulation and Synthetic Societies|Synthetic populations and human samples|LLM Generated Persona is a Promise with a Catch
Multi-Agent Social Simulation and Synthetic Societies|Synthetic populations and human samples|Large Language Models as Subpopulation Representative Models: A Review
Multi-Agent Social Simulation and Synthetic Societies|Synthetic populations and human samples|Vox Populi, Vox AI? Using Language Models to Estimate German Public Opinion
Multi-Agent Social Simulation and Synthetic Societies|Synthetic populations and human samples|Valid Survey Simulations with Limited Human Data: The Roles of Prompting, Fine-Tuning, and Rectification
Multi-Agent Social Simulation and Synthetic Societies|Synthetic populations and human samples|Simulating Public Opinion: Comparing Distributional and Individual-Level Predictions from LLMs and Random Forests
Multi-Agent Social Simulation and Synthetic Societies|Synthetic populations and human samples|Characterizing the ability of LLMs to recapitulate Americans'distributional responses to public opinion polling questions across political issues
Multi-Agent Social Simulation and Synthetic Societies|Synthetic populations and human samples|Before You Simulate: A Pre-Study Benchmark for Large Language Model Stability in Political Role-Playing Simulations
Multi-Agent Social Simulation and Synthetic Societies|Synthetic populations and human samples|Psychologically-Valid Generative Agents: A Novel Approach to Agent-Based Modeling in Social Sciences
Multi-Agent Social Simulation and Synthetic Societies|Synthetic populations and human samples|Donald Trumps in the Virtual Polls: Simulating and Predicting Public Opinions in Surveys Using Large Language Models
Multi-Agent Social Simulation and Synthetic Societies|Synthetic populations and human samples|This human study did not involve human subjects: Validating LLM simulations as behavioral evidence
Multi-Agent Social Simulation and Synthetic Societies|Synthetic populations and human samples|TwinVoice: A Multi-dimensional Benchmark Towards Digital Twins via LLM Persona Simulation
Multi-Agent Social Simulation and Synthetic Societies|Synthetic populations and human samples|Human Preferences in Large Language Model Latent Space: A Technical Analysis on the Reliability of Synthetic Data in Voting Outcome Prediction
Multi-Agent Social Simulation and Synthetic Societies|Synthetic populations and human samples|Surveying with AI: Simulating Human Responses Using Personalized LLM Agents and Social Media Data
Multi-Agent Social Simulation and Synthetic Societies|Synthetic populations and human samples|Validating Generative Agent-Based Models of Social Norm Enforcement: From Replication to Novel Predictions
Multi-Agent Social Simulation and Synthetic Societies|Social networks, movements, and polarization|Network formation and dynamics among multi-LLMs
Multi-Agent Social Simulation and Synthetic Societies|Social networks, movements, and polarization|Emergence of human-like polarization among large language model agents
Multi-Agent Social Simulation and Synthetic Societies|Social networks, movements, and polarization|Unveiling the Truth and Facilitating Change: Towards Agent-based Large-scale Social Movement Simulation
Multi-Agent Social Simulation and Synthetic Societies|Social networks, movements, and polarization|Agent-Based Modelling Meets Generative AI in Social Network Simulations
Multi-Agent Social Simulation and Synthetic Societies|Social networks, movements, and polarization|Decoding Echo Chambers: LLM-Powered Simulations Revealing Polarization in Social Networks
Multi-Agent Social Simulation and Synthetic Societies|Social networks, movements, and polarization|Understanding Online Polarization Through Human-Agent Interaction in a Synthetic LLM-Based Social Network
Multi-Agent Social Simulation and Synthetic Societies|Social networks, movements, and polarization|BluePrint: A Social Media User Dataset for LLM Persona Evaluation and Training
Multi-Agent Social Simulation and Synthetic Societies|Social networks, movements, and polarization|Simulating Online Social Media Conversations on Controversial Topics Using AI Agents Calibrated on Real-World Data
Multi-Agent Social Simulation and Synthetic Societies|Social networks, movements, and polarization|LLM Agents Predict Social Media Reactions but Do Not Outperform Text Classifiers: Benchmarking Simulation Accuracy Using 120K+ Personas of 1511 Humans
Multi-Agent Social Simulation and Synthetic Societies|Social networks, movements, and polarization|POSIM: A Multi-Agent Simulation Framework for Social Media Public Opinion Evolution and Governance
AI Safety, Influence Operations, and Societal Risk|Influence operations and persuasion risk|Generative Language Models and Automated Influence Operations: Emerging Threats and Potential Mitigations
AI Safety, Influence Operations, and Societal Risk|Influence operations and persuasion risk|Ignore All Previous Instructions: Jailbreaking as a de-escalatory peace building practise to resist LLM social media bots
AI Safety, Influence Operations, and Societal Risk|Influence operations and persuasion risk|Charting the Landscape of Nefarious Uses of Generative Artificial Intelligence for Online Election Interference
AI Safety, Influence Operations, and Societal Risk|Influence operations and persuasion risk|Simulating Misinformation Vulnerabilities with Agent Personas
AI Safety, Influence Operations, and Societal Risk|Influence operations and persuasion risk|Prompt Injection Vulnerability of Consensus Generating Applications in Digital Democracy
AI Safety, Influence Operations, and Societal Risk|Influence operations and persuasion risk|New parameters of power: On LLM-based manipulation and control and the spectre of strategic AI
AI Safety, Influence Operations, and Societal Risk|Influence operations and persuasion risk|Evaluating the persuasive influence of political microtargeting with large language models
AI Safety, Influence Operations, and Societal Risk|Influence operations and persuasion risk|Assessing the risks and opportunities posed by AI-enhanced influence operations on social media
AI Safety, Influence Operations, and Societal Risk|Influence operations and persuasion risk|Do Bots Do It Better? Analyzing the Effectiveness of Automated Agents in State-Sponsored Information Operations
AI Safety, Influence Operations, and Societal Risk|Influence operations and persuasion risk|Characterizing the 2016 Russian IRA influence campaign
AI Safety, Influence Operations, and Societal Risk|Influence operations and persuasion risk|ClausewitzGPT Framework: A New Frontier in Theoretical Large Language Model Enhanced Information Operations
AI Safety, Influence Operations, and Societal Risk|Influence operations and persuasion risk|Navigating the Web of Disinformation and Misinformation: Large Language Models as Double-Edged Swords
AI Safety, Influence Operations, and Societal Risk|Influence operations and persuasion risk|Generative artificial intelligence in the electoral processes of 2024 in the world: disinformation campaigns and online trolls
AI Safety, Influence Operations, and Societal Risk|Influence operations and persuasion risk|AI-Slop and Political Propaganda: The Role of AI-Generated Content in Memes and Influence Campaigns
AI Safety, Influence Operations, and Societal Risk|Influence operations and persuasion risk|Exposing influence campaigns in the age of LLMs: a behavioral-based AI approach to detecting state-sponsored trolls
AI Safety, Influence Operations, and Societal Risk|Influence operations and persuasion risk|Recent Trends in Online Foreign Influence Efforts
AI Safety, Influence Operations, and Societal Risk|Influence operations and persuasion risk|How Strategic Information Operations Affect Peacekeeping: Two Case Studies from the Central African Republic
AI Safety, Influence Operations, and Societal Risk|Influence operations and persuasion risk|Whose story wins? LLM-powered chatbots as sites and agents of memory-political contestation and corporate greenwashing
Peripheral and Borderline Materials|Generic AI safety and language-bias background|Multi-Agent Risks from Advanced AI
Peripheral and Borderline Materials|Generic AI safety and language-bias background|AI deception: A survey of examples, risks, and potential solutions
Peripheral and Borderline Materials|Generic AI safety and language-bias background|Generative Exaggeration in LLM Social Agents: Consistency, Bias, and Toxicity
Peripheral and Borderline Materials|Generic AI safety and language-bias background|Diversity and language technology: how language modeling bias causes epistemic injustice
""".strip()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def read_json_if_exists(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def read_csv_if_exists(path: Path) -> list[dict[str, str]]:
    return read_csv(path) if path.exists() else []


def normalize(value: str) -> str:
    return " ".join((value or "").lower().split())


EXCLUDED_TITLES = {
    normalize(title)
    for title in [
        "Generative AI in Managerial Decision-Making: Redefining Boundaries through Ambiguity Resolution and Sycophancy Analysis",
        "Effect of Generative Artificial Intelligence on Strategic Decision Making in Entrepreneurial Business Initiatives: A Systematic Literature Review",
        "The role of artificial intelligence in international strategic decision-making for SMEs",
        "When Artificial Intelligence Does Strategy: Learning, Good Times, Lock-in, and Human-Driven Strategic Renewal",
        "AI in strategic alliance formation: a framework for human-AI collaboration",
        "Reliance on AI in augmented strategic decision-making: Navigating cultural and national dynamics",
        "How AI-assisted scenario thinking develops agile minds for a successful digital strategy?",
    ]
}

S2_UNDERCOUNT_TITLES = {normalize("The Strategy of Conflict")}
BAD_VENUES = {"Sam Nunn"}

THEME_DISPLAY_NAMES = {
    "Political Science and Strategic Judgment Foundations": "Foundations and Theory",
    "Foundations, Surveys, and Methods": "LLM Surveys and Method Overviews",
    "Classical Political NLP and Information Extraction": "Political Text and Measurement",
    "Politics, Democracy, Public Opinion, and Persuasion": "Public Opinion, Elections, and Persuasion",
    "Policymaking, Governance, and Institutional Decision Support": "Policy and Governance Support",
    "Geopolitics, Diplomacy, National Security, and Wargaming": "Geopolitics, Diplomacy, and Wargaming",
    "Forecasting, Geopolitical Risk, and Foresight": "Forecasting and Foresight",
    "Strategic Reasoning, Games, Negotiation, and Cooperation": "Strategic Reasoning and Multi-Agent Games",
    "Multi-Agent Social Simulation and Synthetic Societies": "Social Simulation and Synthetic Populations",
    "AI Safety, Influence Operations, and Societal Risk": "Risks, Bias, and Influence Operations",
    "Peripheral and Borderline Materials": "Peripheral and Borderline",
}

THEME_NOTES = {
    "Political Science and Strategic Judgment Foundations": "Canonical IR, strategic-studies, intelligence-analysis, and forecasting foundations for interpreting LLM behavior in strategic settings.",
    "Foundations, Surveys, and Methods": "LLM-era surveys and methodological overviews that orient political science, social simulation, and game-theoretic agent work.",
    "Classical Political NLP and Information Extraction": "Pre-LLM and bridge methods for political text measurement, legislative text classification, and event-data extraction.",
    "Politics, Democracy, Public Opinion, and Persuasion": "LLM work on ideology, voter behavior, opinion simulation, political annotation, deliberation, and persuasion.",
    "Policymaking, Governance, and Institutional Decision Support": "Papers on public decision support, policy communication, democratic deliberation, and institutional uses of LLMs.",
    "Geopolitics, Diplomacy, National Security, and Wargaming": "Diplomatic agents, military decision support, escalation behavior, national security applications, and wargaming.",
    "Forecasting, Geopolitical Risk, and Foresight": "Forecasting benchmarks, event-prediction systems, calibration studies, and geopolitical risk signals.",
    "Strategic Reasoning, Games, Negotiation, and Cooperation": "LLM strategic reasoning in games, bargaining, negotiation, cooperation, and multi-agent social dilemmas.",
    "Multi-Agent Social Simulation and Synthetic Societies": "Generative agents, synthetic populations, and large-scale simulations of social networks or political behavior.",
    "AI Safety, Influence Operations, and Societal Risk": "Political influence, persuasion risk, deception, bias, and social risks relevant to governance and strategy.",
    "Peripheral and Borderline Materials": "Useful but non-core adjacent work kept visible for auditability; these items should not drive the public README route unless later evidence establishes a direct politics, policy, geopolitical, or strategic-studies link.",
}

IMPORTANCE_OVERRIDES = {
    normalize(title): "Important"
    for title in [
        "Whose Opinions Do Language Models Reflect?",
        "More human than human: measuring ChatGPT political bias",
        "Should ChatGPT be Biased? Challenges and Risks of Bias in Large Language Models",
        "Cultural bias and cultural alignment of large language models",
        "Hidden Persuaders: LLMs’ Political Leaning and Their Influence on Voters",
        "ChatGPT-4 Outperforms Experts and Crowd Workers in Annotating Political Twitter Messages with Zero-Shot Learning",
        "Performance and biases of Large Language Models in public opinion simulation",
        "Large language models as a substitute for human experts in annotating political text",
        "Generative Echo Chamber? Effect of LLM-Powered Search Systems on Diverse Information Seeking",
        "Systematic Biases in LLM Simulations of Debates",
        "AI can help humans find common ground in democratic deliberation",
        "LLM-generated messages can persuade humans on policy issues",
        "Generative Artificial Intelligence and Evaluating Strategic Decisions",
        "Playing repeated games with large language models",
        "Strategic behavior of large language models and the role of game structure versus contextual framing",
        "GTBench: Uncovering the Strategic Reasoning Limitations of LLMs via Game-Theoretic Evaluations",
        "GameBench: Evaluating Strategic Reasoning Abilities of LLM Agents",
        "SOTOPIA: Interactive Evaluation for Social Intelligence in Language Agents",
        "Human-level play in the game of Diplomacy by combining language models with strategic reasoning",
        "From Individual to Society: A Survey on Social Simulation Driven by Large Language Model-based Agents",
        "Validation is the central challenge for generative social simulation: a critical review of LLMs in agent-based modeling",
        "Generative Language Models and Automated Influence Operations: Emerging Threats and Potential Mitigations",
        "Generative Exaggeration in LLM Social Agents: Consistency, Bias, and Toxicity",
    ]
}

IMPORTANCE_DOWNGRADES = {
    normalize(title): label
    for title, label in [
        ("Generative Artificial Intelligence and Evaluating Strategic Decisions", "Curated"),
        ("Generative Agents: Interactive Simulacra of Human Behavior", "Important"),
        ("Large language models empowered agent-based modeling and simulation: a survey and perspectives", "Curated"),
        ("From Individual to Society: A Survey on Social Simulation Driven by Large Language Model-based Agents", "Curated"),
        ("AI Agents Alone Are Not (Yet) Sufficient for Social Simulation", "Curated"),
        ("SPIN-Bench: How Well Do LLMs Plan Strategically and Reason Socially?", "Important"),
        ("GTBench: Uncovering the Strategic Reasoning Limitations of LLMs via Game-Theoretic Evaluations", "Curated"),
        ("GameBench: Evaluating Strategic Reasoning Abilities of LLM Agents", "Curated"),
        ("Using Large Language Models to Simulate Multiple Humans and Replicate Human Subject Studies", "Curated"),
        ("AgentSociety: Large-Scale Simulation of LLM-Driven Generative Agents Advances Understanding of Human Behaviors and Society", "Curated"),
        ("GA-S3: Comprehensive Social Network Simulation with Group Agents", "Curated"),
        ("The Power of Simplicity in LLM-Based Event Forecasting", "Curated"),
        ("Do Language Models Update their Forecasts with New Information?", "Watchlist"),
        ("Hyperdemocracy: Towards Creative Consensus Building between Humans and AI", "Curated"),
        ("Sci2Pol: Evaluating and Fine-tuning LLMs on Scientific-to-Policy Brief Generation", "Curated"),
        ("Benchmarking LLMs for Political Science: A United Nations Perspective / United Nations Benchmark", "Important"),
        ("DataGovBench: Benchmarking LLM Agents for Real-World Data Governance Workflows", "Watchlist"),
        ("Audit Trails for Accountability in Large Language Models", "Curated"),
        (
            "Institutionalizing Predictive AI in Public Administration: Algorithmic Governance and the Case of a Wildfire Forecasting System",
            "Curated",
        ),
        ("The Future Outcome Reasoning and Confidence Assessment Benchmark", "Curated"),
        ("ARMOR 2025: A Military-Aligned Benchmark for Evaluating Large Language Model Safety Beyond Civilian Contexts", "Curated"),
        ("Critical Foreign Policy Decisions Benchmark: Measuring Diplomatic Preferences in Large Language Models", "Important"),
        ("UNSC-Bench: Evaluating LLM Diplomatic Role-Playing Through UN Security Council Vote Prediction", "Important"),
        ("WARBENCH: A Comprehensive Benchmark for Evaluating LLMs in Military Decision-Making", "Important"),
        (
            "Red Lines and Grey Zones in the Fog of War: Benchmarking Legal Risk, Moral Harm, and Regional Bias in Large Language Model Military Decision-Making",
            "Important",
        ),
        ("ThinkTank-ME: A Multi-Expert Framework for Middle East Event Forecasting", "Important"),
        ("Forecasting Future International Events: A Reliable Dataset for Text-Based Event Modeling / WORLDREP", "Important"),
        ("Determinants of LLM-assisted Decision-Making", "Watchlist"),
        ("Who Does What? Archetypes of Roles Assigned to LLMs During Human-AI Decision-Making", "Watchlist"),
        ("Human‑Centered Governance for AI‑Augmented Decision Support in Public‑Sector Logistics", "Watchlist"),
        ("Large Language Model–Powered Public Service Platforms for Automated Case Assistance and Decision Support", "Watchlist"),
        ("An Institutional Theory Framework for Leveraging Large Language Models for Policy Analysis and Intervention Design", "Watchlist"),
        (
            "Can A Society of Generative Agents Simulate Human Behavior and Inform Public Health Policy? A Case Study on Vaccine Hesitancy",
            "Watchlist",
        ),
        (
            "Social Policy of Large Language Models: How GPT, Claude, DeepSeek and Grok Allocate Social Budgets in Spain and Germany",
            "Watchlist",
        ),
        ("Can AI Do Strategy? A Dialogue and Debate", "Watchlist"),
        ("How Well Can AI Do Strategy? Empirical Benchmarking Using Strategy Simulations", "Watchlist"),
        (
            "AI-Augmented Strategic Decision-Making Under Time Constraints: An Experimental Study on Mental Representations and Strategic Foresight",
            "Watchlist",
        ),
        ("Beyond Black Boxes: Designing and Testing Agentic AI Systems for Strategy", "Watchlist"),
        ("Can AI Do Strategy?", "Watchlist"),
        (
            "AI strategy under institutional pressure: strategic conformity and decision-making in large language models",
            "Watchlist",
        ),
        ("Bias in, symbolic compliance out? GPT's reliance on gender and race in strategic evaluations", "Watchlist"),
        ("Reproducing and Extending Experiments in Behavioral Strategy with Large Language Models", "Watchlist"),
        ("From Problems to Solutions in Strategic Decision-Making: The Effects of Generative AI on Problem Formulation", "Watchlist"),
        ("Advancing Decision-Making through AI-Human Collaboration: A Systematic Review and Conceptual Framework", "Watchlist"),
        ("Towards Using Prompt Engineering in Large Language Models to Assist Decision Making", "Watchlist"),
        ("SOTOPIA: Interactive Evaluation for Social Intelligence in Language Agents", "Curated"),
        ("Exploring Large Language Models for Communication Games: An Empirical Study on Werewolf", "Watchlist"),
        ("Improving Language Model Negotiation with Self-Play and In-Context Learning from AI Feedback", "Watchlist"),
        ("Measuring Bargaining Abilities of LLMs: A Benchmark and A Buyer-Enhancement Method", "Watchlist"),
        ("When Reasoning Models Hurt Behavioral Simulation: A Solver-Sampler Mismatch in Multi-Agent LLM Negotiation", "Watchlist"),
        ("LLM-Deliberation: Evaluating LLMs with Interactive Multi-Agent Negotiation Games", "Watchlist"),
        ("How Far Are We on the Decision-Making of LLMs? Evaluating LLMs' Gaming Ability in Multi-Agent Environments", "Watchlist"),
        ("Game-theoretic LLM: Agent Workflow for Negotiation Games", "Watchlist"),
        ("Decision-Making Behavior Evaluation Framework for LLMs under Uncertain Context", "Watchlist"),
        ("Cooperate or Collapse: Emergence of Sustainable Cooperation in a Society of LLM Agents", "Watchlist"),
        ("Nicer Than Humans: How do Large Language Models Behave in the Prisoner's Dilemma?", "Watchlist"),
        ("Shall We Team Up: Exploring Spontaneous Cooperation of Competing LLM Agents", "Watchlist"),
        ("Cultural Evolution of Cooperation among LLM Agents", "Watchlist"),
        ("Communication Enhances LLMs' Stability in Strategic Thinking", "Watchlist"),
        ("A Turing test of whether AI chatbots are behaviorally similar to humans", "Watchlist"),
        ("AI deception: A survey of examples, risks, and potential solutions", "Watchlist"),
        ("Multi-Agent Risks from Advanced AI", "Watchlist"),
        ("Generative Exaggeration in LLM Social Agents: Consistency, Bias, and Toxicity", "Watchlist"),
        ("Diversity and language technology: how language modeling bias causes epistemic injustice", "Watchlist"),
    ]
}

START_HERE = [
    (
        "Perception and Misperception in International Politics",
        "Classic baseline for interpreting misperception, signaling, and crisis reasoning.",
    ),
    (
        "Arms and Influence",
        "The core coercion and bargaining frame behind much of the escalation literature.",
    ),
    (
        "Rationalist Explanations for War",
        "Canonical account of war through information problems, incentives, and commitment problems.",
    ),
    (
        "Essence of Decision: Explaining the Cuban Missile Crisis",
        "Foundational decision-making models for crisis behavior and bureaucratic politics.",
    ),
    (
        "Text as Data: The Promise and Pitfalls of Automatic Content Analysis Methods for Political Texts",
        "Methodological bridge from political text measurement to current LLM annotation and scaling work.",
    ),
    (
        "Conflict and Mediation Event Observations (CAMEO): A New Event Data Framework for the Analysis of Foreign Policy Interactions",
        "Core event-data ontology for conflict, diplomacy, and foreign-policy interactions.",
    ),
    (
        "Can Large Language Models Transform Computational Social Science?",
        "Broad orientation to what LLMs change, and do not change, in computational social science.",
    ),
    (
        "Whose Opinions Do Language Models Reflect?",
        "High-impact entry point for political representation and bias in language models.",
    ),
    (
        "AI can help humans find common ground in democratic deliberation",
        "A flagship empirical case for LLMs in democratic deliberation and policy communication.",
    ),
    (
        "Escalation Risks from Language Models in Military and Diplomatic Decision-Making",
        "Core LLM crisis-simulation paper for military and diplomatic escalation behavior.",
    ),
    (
        "Human-level play in the game of Diplomacy by combining language models with strategic reasoning",
        "Major demonstration of language-mediated strategic action in a diplomatic game.",
    ),
    (
        "ForecastBench: A Dynamic Benchmark of AI Forecasting Capabilities",
        "Central benchmark for evaluating AI forecasting across changing real-world questions.",
    ),
    (
        "MIRAI: Evaluating LLM Agents for Event Forecasting",
        "Agent-oriented benchmark for event forecasting and temporal reasoning.",
    ),
    (
        "Approaching Human-Level Forecasting with Language Models",
        "Key reference for comparing LLM forecasting systems with human forecasting performance.",
    ),
    (
        "Playing repeated games with large language models",
        "Useful baseline for strategic behavior in repeated interaction.",
    ),
    (
        "Generative Agents: Interactive Simulacra of Human Behavior",
        "Canonical generative-agent paper behind many social and political simulation systems.",
    ),
    (
        "Out of One, Many: Using Language Models to Simulate Human Samples",
        "High-impact foundation for synthetic samples and population-level opinion simulation.",
    ),
    (
        "Generative Agent Simulations of 1,000 People",
        "Recent large-scale person-specific simulation reference with direct social-science relevance.",
    ),
    (
        "Generative Language Models and Automated Influence Operations: Emerging Threats and Potential Mitigations",
        "Core risk framing for automated influence operations and strategic information environments.",
    ),
]

CORE_NOTES = {normalize(title): note for title, note in START_HERE}


def title_tokens(value: str) -> set[str]:
    stopwords = {"a", "an", "and", "as", "at", "for", "from", "in", "of", "on", "the", "to", "with"}
    return {
        token
        for token in re.findall(r"[a-z0-9]+", normalize(value))
        if len(token) > 1 and token not in stopwords
    }


def title_similarity(left: str, right: str) -> float:
    left_tokens = title_tokens(left)
    right_tokens = title_tokens(right)
    if not left_tokens or not right_tokens:
        return 0.0
    return len(left_tokens & right_tokens) / len(left_tokens | right_tokens)


def as_int(value: Any, default: int = 0) -> int:
    try:
        if value in {"", None, "n/a"}:
            return default
        return int(value)
    except (TypeError, ValueError):
        return default


def display_year(value: str) -> str:
    value = (value or "").strip()
    return value if re.fullmatch(r"\d{4}", value) else "n.d."


def normalize_importance(title: str, value: str) -> str:
    key = normalize(title)
    if key in IMPORTANCE_DOWNGRADES:
        return IMPORTANCE_DOWNGRADES[key]
    if key in IMPORTANCE_OVERRIDES:
        return IMPORTANCE_OVERRIDES[key]
    normalized = (value or "Curated").strip()
    if normalized in {"Optional", "Optional / Important", "Optional / Engineering"}:
        return "Watchlist"
    if normalized not in {"Core", "Important", "Curated", "Watchlist"}:
        return "Curated"
    return normalized


def is_highlighted(row: dict[str, str]) -> bool:
    return row.get("importance") in {"Core", "Important"}


def venue_or_type(row: dict[str, str]) -> str:
    venue = (row.get("venue") or "").strip()
    if venue in BAD_VENUES:
        venue = ""
    if venue:
        return venue
    if row.get("arxiv"):
        return "arXiv"
    return ""


def citation_display(seed: dict[str, str], enriched: dict[str, str] | None) -> str:
    if not enriched:
        return "n/a"
    if normalize(seed["title"]) in S2_UNDERCOUNT_TITLES:
        return "n/a"
    method = enriched.get("resolution_method", "")
    resolved_title = enriched.get("resolved_title", "")
    trusted = method in {"arxiv", "title_exact"} or title_similarity(seed["title"], resolved_title) >= 0.7
    if not trusted:
        return "n/a"
    value = enriched.get("citationCount", "")
    return value if value != "" else "n/a"


def markdown_link(title: str, url: str) -> str:
    return f"[{title}]({url})" if url else title


def row_url(row: dict[str, str]) -> str:
    return row.get("url") or row.get("source_url") or (f"https://arxiv.org/abs/{row['arxiv']}" if row.get("arxiv") else "")


def parse_assignments() -> dict[str, tuple[str, str]]:
    assignments: dict[str, tuple[str, str]] = {}
    for line in THEME_ASSIGNMENTS.splitlines():
        theme, subtheme, title = [part.strip() for part in line.split("|", 2)]
        key = normalize(title)
        if key in assignments:
            raise RuntimeError(f"Duplicate theme assignment: {title}")
        if theme not in THEME_ORDER:
            raise RuntimeError(f"Unknown theme for {title}: {theme}")
        if subtheme not in SUBTHEME_ORDER[theme]:
            raise RuntimeError(f"Unknown subtheme for {title}: {subtheme}")
        assignments[key] = (theme, subtheme)
    return assignments


def source_rows() -> list[dict[str, str]]:
    enriched_by_title = {normalize(row["title"]): row for row in read_csv(ENRICHED_SEEDS)}
    rows: list[dict[str, str]] = []

    for row in read_csv(CORE_SEEDS):
        enriched = enriched_by_title.get(normalize(row["title"]))
        rows.append(
            {
                "title": row["title"],
                "year": row.get("year_or_timeframe", ""),
                "citationCount": citation_display(row, enriched),
                "importance": row.get("priority", "Core"),
                "url": row.get("source_url", ""),
                "doi": enriched.get("doi", "") if enriched else "",
                "arxiv": enriched.get("arxiv", "") if enriched else "",
                "venue": enriched.get("venue", "") if enriched else row.get("paper_type_or_source", ""),
                "authors": enriched.get("authors", "") if enriched else "",
                "abstract": enriched.get("abstract", "") if enriched else "",
                "source_tables": "core_seed_papers.csv",
            }
        )

    for row in read_csv(CURATED_CANDIDATES):
        rows.append(
            {
                "title": row["title"],
                "year": row.get("year", ""),
                "citationCount": row.get("citationCount", ""),
                "importance": "Curated",
                "url": row_url(row),
                "doi": row.get("doi", ""),
                "arxiv": row.get("arxiv", ""),
                "venue": row.get("venue", ""),
                "authors": row.get("authors", ""),
                "abstract": row.get("abstract", ""),
                "source_tables": "curated_candidate_tables",
            }
        )

    for row in read_csv_if_exists(PRIORITY_SEEDS):
        rows.append(
            {
                "title": row["title"],
                "year": row.get("year_or_timeframe", ""),
                "citationCount": row.get("citationCount", ""),
                "importance": "Curated",
                "url": row_url(row),
                "doi": "",
                "arxiv": "",
                "venue": "",
                "authors": "",
                "abstract": "",
                "source_tables": "curated_candidate_tables",
            }
        )

    for row in read_csv(SECOND_ORDER_CANDIDATES):
        rows.append(
            {
                "title": row["title"],
                "year": row.get("year", ""),
                "citationCount": row.get("citationCount", ""),
                "importance": "Curated",
                "url": row_url(row),
                "doi": row.get("doi", ""),
                "arxiv": row.get("arxiv", ""),
                "venue": row.get("venue", ""),
                "authors": row.get("authors", ""),
                "abstract": row.get("abstract", ""),
                "source_tables": "curated_candidate_tables",
            }
        )

    for row in read_csv_if_exists(TARGETED_RELATED_WORKS):
        rows.append(
            {
                "title": row["title"],
                "year": row.get("year", ""),
                "citationCount": row.get("citationCount", ""),
                "importance": "Curated",
                "url": row_url(row),
                "doi": row.get("doi", ""),
                "arxiv": row.get("arxiv", ""),
                "venue": row.get("venue", ""),
                "authors": row.get("authors", ""),
                "abstract": row.get("abstract", ""),
                "source_tables": "targeted_related_works_strategy.csv",
            }
        )

    for row in read_csv_if_exists(CLASSICAL_POLITICAL_NLP_IE):
        rows.append(
            {
                "title": row["title"],
                "year": row.get("resolved_year") or row.get("year_or_timeframe", ""),
                "citationCount": citation_display({"title": row["title"]}, row),
                "importance": row.get("priority", "Core"),
                "url": row.get("semantic_scholar_url") or row.get("source_url", ""),
                "doi": row.get("doi", ""),
                "arxiv": row.get("arxiv", ""),
                "venue": row.get("venue", ""),
                "authors": row.get("authors", ""),
                "abstract": row.get("abstract", ""),
                "source_tables": "classical_political_nlp_ie_enriched.csv",
            }
        )

    for row in read_csv_if_exists(FOG_OF_WAR_RELATED_WORKS):
        rows.append(
            {
                "title": row["title"],
                "year": row.get("resolved_year") or row.get("year_or_timeframe", ""),
                "citationCount": citation_display({"title": row["title"]}, row),
                "importance": row.get("priority", "Curated"),
                "url": row.get("semantic_scholar_url") or row.get("source_url", ""),
                "doi": row.get("doi", ""),
                "arxiv": row.get("arxiv", ""),
                "venue": row.get("venue", ""),
                "authors": row.get("authors", ""),
                "abstract": row.get("abstract", ""),
                "source_tables": "fog_of_war_related_works_enriched.csv",
            }
        )

    for row in read_csv_if_exists(STRATEGIC_STUDIES_FOUNDATION):
        rows.append(
            {
                "title": row["title"],
                "year": row.get("year_or_timeframe") or row.get("resolved_year", ""),
                "citationCount": citation_display({"title": row["title"]}, row),
                "importance": row.get("priority", "Core"),
                "url": row.get("semantic_scholar_url") or row.get("source_url", ""),
                "doi": row.get("doi", ""),
                "arxiv": row.get("arxiv", ""),
                "venue": row.get("venue", ""),
                "authors": row.get("authors", ""),
                "abstract": row.get("abstract", ""),
                "source_tables": "strategic_studies_foundation_enriched.csv",
            }
        )

    for row in read_csv_if_exists(CRITIQUE_PRIORITY_ADDITIONS):
        rows.append(
            {
                "title": row["title"],
                "year": row.get("year", ""),
                "citationCount": row.get("citationCount", ""),
                "importance": "Curated",
                "url": row_url(row),
                "doi": row.get("doi", ""),
                "arxiv": row.get("arxiv", ""),
                "venue": row.get("venue", ""),
                "authors": row.get("authors", ""),
                "abstract": row.get("abstract", ""),
                "source_tables": "critique_priority_expansion/curated_additions.csv",
            }
        )

    for row in read_csv_if_exists(CRITIQUE_NEXT_ADDITIONS):
        rows.append(
            {
                "title": row["title"],
                "year": row.get("year", ""),
                "citationCount": row.get("citationCount", ""),
                "importance": row.get("importance", "Curated"),
                "url": row_url(row),
                "doi": row.get("doi", ""),
                "arxiv": row.get("arxiv", ""),
                "venue": row.get("venue", ""),
                "authors": row.get("authors", ""),
                "abstract": row.get("abstract", ""),
                "source_tables": "critique_next_expansion/curated_additions.csv",
            }
        )

    for row in read_csv_if_exists(CRITIQUE_FOLLOWUP_ADDITIONS):
        rows.append(
            {
                "title": row["title"],
                "year": row.get("year", ""),
                "citationCount": row.get("citationCount", ""),
                "importance": row.get("importance", "Curated"),
                "url": row_url(row),
                "doi": row.get("doi", ""),
                "arxiv": row.get("arxiv", ""),
                "venue": row.get("venue", ""),
                "authors": row.get("authors", ""),
                "abstract": row.get("abstract", ""),
                "source_tables": "critique_followup_expansion/curated_additions.csv",
            }
        )

    for row in read_csv_if_exists(CRITIQUE_ROUND3_ADDITIONS):
        rows.append(
            {
                "title": row["title"],
                "year": row.get("year", ""),
                "citationCount": row.get("citationCount", ""),
                "importance": row.get("importance", "Curated"),
                "url": row_url(row),
                "doi": row.get("doi", ""),
                "arxiv": row.get("arxiv", ""),
                "venue": row.get("venue", ""),
                "authors": row.get("authors", ""),
                "abstract": row.get("abstract", ""),
                "source_tables": "critique_round3_expansion/curated_additions.csv",
            }
        )

    for row in read_csv_if_exists(SURVEY_READINESS_ADDITIONS):
        rows.append(
            {
                "title": row["title"],
                "year": row.get("year", ""),
                "citationCount": row.get("citationCount", ""),
                "importance": row.get("importance", "Curated"),
                "url": row_url(row),
                "doi": row.get("doi", ""),
                "arxiv": row.get("arxiv", ""),
                "venue": row.get("venue", ""),
                "authors": row.get("authors", ""),
                "abstract": row.get("abstract", ""),
                "source_tables": "survey_readiness_expansion/curated_additions.csv",
            }
        )

    for row in read_csv_if_exists(INSTITUTIONAL_WORKFLOW_ADDITIONS):
        rows.append(
            {
                "title": row["title"],
                "year": row.get("year", ""),
                "citationCount": row.get("citationCount", ""),
                "importance": row.get("importance", "Curated"),
                "url": row_url(row),
                "doi": row.get("doi", ""),
                "arxiv": row.get("arxiv", ""),
                "venue": row.get("venue", ""),
                "authors": row.get("authors", ""),
                "abstract": row.get("abstract", ""),
                "source_tables": "institutional_workflow_expansion/curated_additions.csv",
            }
        )

    return [row for row in rows if normalize(row["title"]) not in EXCLUDED_TITLES]


def merge_rows(
    rows: list[dict[str, str]],
    assignments: dict[str, tuple[str, str]],
) -> tuple[list[dict[str, str]], int, int]:
    merged: dict[str, dict[str, str]] = {}
    source_count = len(rows)
    for row in rows:
        key = normalize(row["title"])
        if key not in assignments:
            raise RuntimeError(f"Missing theme assignment: {row['title']}")
        theme, subtheme = assignments[key]
        if key not in merged:
            merged[key] = {**row, "theme": theme, "subtheme": subtheme}
            continue
        existing = merged[key]
        existing["source_tables"] = "; ".join(sorted(set(existing["source_tables"].split("; ") + [row["source_tables"]])))
        if existing.get("citationCount") in {"", "n/a"} and row.get("citationCount") not in {"", "n/a"}:
            existing["citationCount"] = row["citationCount"]
        if existing.get("importance") != "Core" and row.get("importance") == "Core":
            existing["importance"] = "Core"

    if len(merged) != len(assignments):
        assigned_without_source = sorted(set(assignments) - set(merged))
        if assigned_without_source:
            raise RuntimeError(f"Theme assignments without source rows: {assigned_without_source[:5]}")

    output = list(merged.values())
    if len(output) != len({normalize(row["title"]) for row in output}):
        raise RuntimeError("Merged rows contain duplicate normalized titles.")
    for row in output:
        row["importance"] = normalize_importance(row["title"], row.get("importance", ""))
        row["year"] = display_year(row.get("year", ""))
    duplicate_count = source_count - len(output)
    return output, source_count, duplicate_count


def theme_sort_key(row: dict[str, str]) -> tuple[int, int, int, int, str]:
    theme_index = THEME_ORDER.index(row["theme"])
    subtheme_index = SUBTHEME_ORDER[row["theme"]].index(row["subtheme"])
    importance_rank = {"Core": 0, "Important": 1, "Curated": 2, "Watchlist": 3}.get(
        row.get("importance", ""),
        3,
    )
    return (
        theme_index,
        subtheme_index,
        -as_int(row.get("citationCount"), -1),
        importance_rank,
        row["title"].lower(),
    )


def write_thematic_csv(rows: list[dict[str, str]]) -> None:
    columns = [
        "theme",
        "subtheme",
        "title",
        "year",
        "citationCount",
        "importance",
        "url",
        "doi",
        "arxiv",
        "venue",
        "authors",
        "source_tables",
        "abstract",
    ]
    THEMATIC_PAPERS.parent.mkdir(parents=True, exist_ok=True)
    with THEMATIC_PAPERS.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: clean_csv_value(row.get(column, "")) for column in columns})


def clean_csv_value(value: Any) -> str:
    return " ".join(str(value or "").split())


def paper_line(row: dict[str, str], *, include_note: bool = False, include_venue: bool = False) -> str:
    importance = row.get("importance") or "Curated"
    parts = [importance]
    venue = venue_or_type(row) if include_venue or importance == "Core" else ""
    if venue:
        parts.append(f"venue: {venue}")
    citation_count = row.get("citationCount") or "n/a"
    parts.append(f"citations: {citation_count}")
    note = CORE_NOTES.get(normalize(row["title"]), "") if include_note else ""
    suffix = f" {note}" if note else ""
    return f"- {markdown_link(row['title'], row.get('url', ''))} ({display_year(row.get('year', ''))}) - {'; '.join(parts)}.{suffix}"


def theme_display(theme: str) -> str:
    return THEME_DISPLAY_NAMES.get(theme, theme)


def rows_grouped_by_theme(rows: list[dict[str, str]]) -> dict[str, dict[str, list[dict[str, str]]]]:
    by_theme: dict[str, dict[str, list[dict[str, str]]]] = defaultdict(lambda: defaultdict(list))
    for row in rows:
        by_theme[row["theme"]][row["subtheme"]].append(row)
    return by_theme


def build_paper_sections(
    rows: list[dict[str, str]],
    *,
    highlighted_only: bool,
    include_notes: bool,
    include_venue: bool,
) -> list[str]:
    by_theme = rows_grouped_by_theme(rows)
    lines: list[str] = []
    for theme in THEME_ORDER:
        theme_rows = [row for subtheme in by_theme.get(theme, {}).values() for row in subtheme]
        papers_in_theme = [row for row in theme_rows if not highlighted_only or is_highlighted(row)]
        if not papers_in_theme:
            continue
        highlighted_count = sum(1 for row in theme_rows if is_highlighted(row))
        lines.extend([f"### {theme_display(theme)}", ""])
        if THEME_NOTES.get(theme):
            lines.extend([THEME_NOTES[theme], ""])
        if highlighted_only:
            lines.extend([f"{highlighted_count} highlighted papers; {len(theme_rows)} total in the full bibliography.", ""])
        else:
            lines.extend([f"{len(theme_rows)} papers.", ""])
        for subtheme in SUBTHEME_ORDER[theme]:
            subtheme_rows = by_theme.get(theme, {}).get(subtheme, [])
            papers = [row for row in subtheme_rows if not highlighted_only or is_highlighted(row)]
            if not papers:
                continue
            lines.extend([f"#### {subtheme}", ""])
            for row in papers:
                lines.append(paper_line(row, include_note=include_notes, include_venue=include_venue))
            lines.append("")
    return lines


def build_start_here(rows: list[dict[str, str]]) -> list[str]:
    rows_by_title = {normalize(row["title"]): row for row in rows}
    lines = ["## Start Here", ""]
    for title, note in START_HERE:
        row = rows_by_title.get(normalize(title))
        if not row:
            continue
        citation_count = row.get("citationCount") or "n/a"
        lines.append(
            f"- {markdown_link(row['title'], row.get('url', ''))} ({display_year(row.get('year', ''))}) - "
            f"{row.get('importance', 'Curated')}; citations: {citation_count}. {note}"
        )
    lines.append("")
    return lines


def write_full_bibliography(rows: list[dict[str, str]]) -> None:
    label_counts = Counter(row["importance"] for row in rows)
    lines = [
        "# Full Bibliography",
        "",
        "This is the complete thematic bibliography generated from `data/processed/thematic_papers.csv`.",
        "The public README highlights Core and Important items; this file keeps Curated and Watchlist entries visible without overloading the homepage.",
        "",
        f"Total papers: **{len(rows)}**.",
        "",
        "Label counts:",
        "",
    ]
    for label in ["Core", "Important", "Curated", "Watchlist"]:
        lines.append(f"- {label}: {label_counts.get(label, 0)}")
    lines.extend(["", "## Papers", ""])
    lines.extend(build_paper_sections(rows, highlighted_only=False, include_notes=False, include_venue=True))
    FULL_BIBLIOGRAPHY.parent.mkdir(parents=True, exist_ok=True)
    FULL_BIBLIOGRAPHY.write_text("\n".join(lines), encoding="utf-8")


def build_catalog() -> tuple[list[dict[str, str]], int, int]:
    assignments = parse_assignments()
    rows, source_count, duplicate_count = merge_rows(source_rows(), assignments)
    rows = sorted(rows, key=theme_sort_key)
    write_thematic_csv(rows)
    write_full_bibliography(rows)
    return rows, source_count, duplicate_count


def build_readme() -> str:
    rows, source_count, duplicate_count = build_catalog()
    first_summary = json.loads(RUN_SUMMARY.read_text(encoding="utf-8"))
    second_summary = read_json_if_exists(SECOND_ORDER_SUMMARY)
    targeted_summary = read_json_if_exists(TARGETED_SUMMARY)
    fog_summary = read_json_if_exists(FOG_OF_WAR_SUMMARY)
    critique_priority_summary = read_json_if_exists(CRITIQUE_PRIORITY_SUMMARY)
    critique_next_summary = read_json_if_exists(CRITIQUE_NEXT_SUMMARY)
    critique_followup_summary = read_json_if_exists(CRITIQUE_FOLLOWUP_SUMMARY)
    critique_followup_search_summary = read_json_if_exists(CRITIQUE_FOLLOWUP_SEARCH_SUMMARY)
    critique_round3_summary = read_json_if_exists(CRITIQUE_ROUND3_SUMMARY)
    critique_round3_search_summary = read_json_if_exists(CRITIQUE_ROUND3_SEARCH_SUMMARY)
    critique_round3_social_summary = read_json_if_exists(CRITIQUE_ROUND3_SOCIAL_SUMMARY)
    survey_readiness_summary = read_json_if_exists(SURVEY_READINESS_SUMMARY)
    survey_readiness_search_summary = read_json_if_exists(SURVEY_READINESS_SEARCH_SUMMARY)
    institutional_workflow_summary = read_json_if_exists(INSTITUTIONAL_WORKFLOW_SUMMARY)
    institutional_workflow_search_summary = read_json_if_exists(INSTITUTIONAL_WORKFLOW_SEARCH_SUMMARY)
    highlighted_rows = [row for row in rows if is_highlighted(row)]
    label_counts = Counter(row["importance"] for row in rows)

    lines = [
        "# Awesome LLMs for Political Strategy, Geopolitics, and Decision-Making",
        "",
        "A curated guide to large language models for political strategy, geopolitics, policymaking, strategic studies, and high-stakes decision-making.",
        "",
        "The README is intentionally a curated route through the literature. The full bibliography remains available in [`docs/full-bibliography.md`](docs/full-bibliography.md) and `data/processed/thematic_papers.csv`.",
        "",
        "Current coverage: **{total} papers** in the full bibliography; **{highlighted} Core/Important papers** highlighted on this page.".format(
            total=len(rows),
            highlighted=len(highlighted_rows),
        ),
        "",
        "Citation counts are from the Semantic Scholar Graph API, collected on 2026-05-21.",
        "",
        "## Contents",
        "",
        "- [What Belongs Here](#what-belongs-here)",
        "- [Reader Guide](#reader-guide)",
        "- [Start Here](#start-here)",
        "- [Papers by Theme](#papers-by-theme)",
        "- [Data and Collection](#data-and-collection)",
        "- [Contributing](#contributing)",
        "",
        "## What Belongs Here",
        "",
        "A paper belongs in this repository if it satisfies at least one of these tests:",
        "",
        "- It directly studies LLMs or LLM agents in politics, geopolitics, policymaking, strategic studies, diplomacy, forecasting, wargaming, public opinion, or high-stakes decision-making.",
        "- It provides a benchmark, dataset, evaluation method, or empirical application for political or strategic LLM behavior.",
        "- It is a foundational political-science, IR, strategic-studies, intelligence-analysis, or forecasting work needed to interpret LLM-for-strategy research.",
        "- It is a classical political NLP, text-as-data, or event-data paper that current LLM methods build on.",
        "",
        "Out of scope: finance-only LLMs, trading systems, stock prediction, portfolio management, generic financial benchmarks, generic foundation-model papers, and generic safety papers without a direct political, policy, geopolitical, or strategic-decision link.",
        "",
        "Importance labels:",
        "",
        "- `Core`: field-shaping work or necessary background.",
        "- `Important`: strong empirical, methodological, benchmark, dataset, or research value.",
        "- `Curated`: relevant but not essential for the public README route.",
        "- `Watchlist`: recent, low-citation, unresolved, or borderline work kept for review in the full bibliography.",
        "",
        "## Reader Guide",
        "",
        "- New to the area: start with Foundations and Theory, then Forecasting and Foresight, then Geopolitics, Diplomacy, and Wargaming.",
        "- Building benchmarks or agents: use Forecasting, Strategic Reasoning, Diplomacy, Wargaming, and Social Simulation.",
        "- Studying democratic effects: use Public Opinion, Elections, Persuasion, and Policy and Governance Support.",
        "- Looking for data sources: use Political Text and Measurement plus `data/processed/thematic_papers.csv`.",
        "- Checking long-tail coverage: use [`docs/full-bibliography.md`](docs/full-bibliography.md).",
        "",
    ]

    lines.extend(build_start_here(rows))
    lines.extend(["## Papers by Theme", "", "This section highlights Core and Important papers only. See [`docs/full-bibliography.md`](docs/full-bibliography.md) for all Curated and Watchlist entries.", ""])
    lines.extend(build_paper_sections(rows, highlighted_only=True, include_notes=True, include_venue=True))

    lines.extend(
        [
            "## Data and Collection",
            "",
            f"- Total unique papers in the full thematic bibliography: {len(rows)}",
            f"- Papers highlighted on this page: {len(highlighted_rows)}",
            f"- Label counts: Core {label_counts.get('Core', 0)}, Important {label_counts.get('Important', 0)}, Curated {label_counts.get('Curated', 0)}, Watchlist {label_counts.get('Watchlist', 0)}",
            f"- Source rows checked before merge: {source_count}",
            f"- Duplicate source rows removed during merge: {duplicate_count}",
            f"- Core seed papers: {sum(1 for row in rows if row.get('source_tables') == 'core_seed_papers.csv')}",
            f"- Curated additions merged into themes: {sum(1 for row in rows if row.get('source_tables') != 'core_seed_papers.csv')}",
            f"- Initial citation/reference edges scanned: {first_summary.get('edge_count', 0)}",
            f"- Additional citation/reference edges scanned from priority papers: {second_summary.get('edge_count', 0)}",
            f"- Targeted strategic-decision related-work edges scanned: {targeted_summary.get('edge_count', 0)}",
            f"- Fog-of-war related-work edges scanned: {fog_summary.get('edge_count', 0)}",
            f"- Critique-priority citation/reference edges scanned: {critique_priority_summary.get('edge_count', 0)}",
            f"- Critique-next citation/reference edges scanned: {critique_next_summary.get('edge_count', 0)}",
            f"- Critique-followup citation/reference edges scanned: {critique_followup_summary.get('edge_count', 0)}",
            f"- Critique-followup Semantic Scholar query results screened: {critique_followup_search_summary.get('result_count', 0)}",
            f"- Critique-round-3 influence/diplomacy citation/reference edges scanned: {critique_round3_summary.get('edge_count', 0)}",
            f"- Critique-round-3 social-simulation citation/reference edges scanned: {critique_round3_social_summary.get('edge_count', 0)}",
            f"- Critique-round-3 Semantic Scholar query results screened: {critique_round3_search_summary.get('result_count', 0)}",
            f"- Survey-readiness citation/reference edges scanned: {survey_readiness_summary.get('edge_count', 0)}",
            f"- Survey-readiness Semantic Scholar query results screened: {survey_readiness_search_summary.get('result_count', 0)}",
            f"- Institutional-workflow citation/reference edges scanned: {institutional_workflow_summary.get('edge_count', 0)}",
            f"- Institutional-workflow Semantic Scholar query results screened: {institutional_workflow_search_summary.get('result_count', 0)}",
            "",
            "Data files:",
            "",
            "- `docs/full-bibliography.md`: complete generated bibliography.",
            "- `docs/selection-criteria.md`: inclusion rules, exclusion rules, labels, and provenance notes.",
            "- `docs/survey_readiness_gap_analysis.md`: remaining gaps and validity taxonomy for turning the repository into a survey paper.",
            "- `data/processed/thematic_papers.csv`: merged thematic paper table used to build the README and full bibliography.",
            "- `data/raw/core_seed_papers.csv`: original core seed list.",
            "- `data/raw/targeted_strategic_decisions_seed.csv`: targeted trace seed for the strategic-decision paper.",
            "- `data/raw/classical_political_nlp_ie_seed.csv`: curated classical political NLP and information-extraction seed list.",
            "- `data/raw/fog_of_war_related_work_seed.csv`: curated Fog of War related-work and foundation seed list.",
            "- `data/raw/strategic_studies_foundation_seed.csv`: curated strategic-studies foundation seed list.",
            "- `data/raw/critique_priority_expansion_seeds.csv`: critique-selected high-priority trace seeds.",
            "- `data/raw/critique_next_expansion_seeds.csv`: next-round critique seed list for escalation risk and Political-LLM traces.",
            "- `data/raw/critique_followup_expansion_seeds.csv`: critique-followup seeds for forecasting, democratic deliberation, and WARBENCH traces.",
            "- `data/raw/critique_followup_search_queries.csv`: targeted Semantic Scholar query-search terms for the critique-followup pass.",
            "- `data/raw/critique_round3_expansion_seeds.csv`: critique-round-3 seeds for influence operations, Diplomacy, and synthetic-population traces.",
            "- `data/raw/critique_round3_search_queries.csv`: targeted Semantic Scholar query-search terms for influence operations, diplomacy, and social simulation.",
            "- `data/raw/survey_readiness_expansion_seeds.csv`: critique-selected survey-readiness seeds for validity, multilingual/geopolitical bias, diplomacy, and strategic reasoning.",
            "- `data/raw/survey_readiness_search_queries.csv`: targeted Semantic Scholar query-search terms for survey-readiness gaps.",
            "- `data/raw/institutional_workflow_expansion_seeds.csv`: critique-selected seeds for public-sector and institutional decision-support workflows.",
            "- `data/raw/institutional_workflow_search_queries.csv`: targeted Semantic Scholar query-search terms for public-sector workflow gaps.",
            "- `data/processed/core_seed_papers_enriched.csv`: seed metadata with citation counts, authors, venues, abstracts, and resolution method.",
            "- `data/processed/targeted_related_works_strategy.csv`: selected additions from the targeted strategic-decision trace.",
            "- `data/processed/classical_political_nlp_ie_enriched.csv`: Semantic Scholar metadata for the classical political NLP and IE additions.",
            "- `data/processed/fog_of_war_related_works_enriched.csv`: Semantic Scholar metadata for Fog of War related-work additions.",
            "- `data/processed/strategic_studies_foundation_enriched.csv`: Semantic Scholar metadata for strategic-studies foundation additions.",
            "- `data/processed/critique_priority_expansion/curated_additions.csv`: selected additions from critique-priority seed expansion.",
            "- `data/processed/critique_next_expansion/curated_additions.csv`: selected additions from escalation-risk and Political-LLM seed expansion.",
            "- `data/processed/critique_followup_expansion/curated_additions.csv`: selected additions from ForecastBench, democratic-deliberation, and WARBENCH follow-up expansion.",
            "- `data/processed/critique_round3_expansion/curated_additions.csv`: selected additions from influence-operations, Diplomacy, and social-simulation expansion.",
            "- `data/processed/survey_readiness_expansion/curated_additions.csv`: selected additions from validity, multilingual/geopolitical-bias, diplomacy, and strategic-reasoning expansion.",
            "- `data/processed/institutional_workflow_expansion/curated_additions.csv`: selected additions from public-sector workflow, accountability, and policy-analysis expansion.",
            "- `data/processed/targeted_strategic_decisions/run_summary.json`: targeted trace summary.",
            "- `data/processed/fog_of_war/run_summary.json`: Fog of War trace summary.",
            "- `data/processed/critique_priority_expansion/run_summary.json`: critique-priority trace summary.",
            "- `data/processed/critique_next_expansion/run_summary.json`: critique-next trace summary.",
            "- `data/processed/critique_followup_expansion/run_summary.json`: critique-followup trace summary.",
            "- `data/processed/critique_followup_expansion/search_summary.json`: critique-followup query-search summary.",
            "- `data/processed/critique_round3_expansion/run_summary.json`: critique-round-3 influence/diplomacy trace summary.",
            "- `data/processed/critique_round3_expansion/search_summary.json`: critique-round-3 query-search summary.",
            "- `data/processed/critique_round3_expansion/social_simulation_seed_trace_summary.json`: critique-round-3 social-simulation direct-trace summary.",
            "- `data/processed/survey_readiness_expansion/run_summary.json`: survey-readiness trace summary.",
            "- `data/processed/survey_readiness_expansion/search_summary.json`: survey-readiness query-search summary.",
            "- `data/processed/institutional_workflow_expansion/run_summary.json`: institutional-workflow trace summary.",
            "- `data/processed/institutional_workflow_expansion/search_summary.json`: institutional-workflow query-search summary.",
            "",
            "Scripts:",
            "",
            "- `scripts/expand_semantic_scholar.py`: resolves seeds, fetches citations/references, and writes candidate tables.",
            "- `scripts/search_semantic_scholar.py`: runs targeted Semantic Scholar paper-search queries without fetching TLDR fields.",
            "- `scripts/fetch_seed_metadata.py`: enriches seed papers with Semantic Scholar metadata.",
            "- `scripts/build_targeted_related_works.py`: selects targeted related-work additions from a trace longlist.",
            "- `scripts/build_critique_followup_expansion.py`: selects critique-reviewed additions from the ForecastBench, deliberation, and WARBENCH follow-up pass.",
            "- `scripts/build_critique_round3_expansion.py`: selects critique-reviewed additions from the influence-operations, Diplomacy, and social-simulation pass.",
            "- `scripts/build_survey_readiness_expansion.py`: selects critique-reviewed additions from the survey-readiness pass.",
            "- `scripts/build_institutional_workflow_expansion.py`: selects critique-reviewed additions from the public-sector workflow pass.",
            "- `scripts/build_readme.py`: rebuilds this README and validates that every curated paper is assigned to a theme.",
            "",
            "## Contributing",
            "",
            "Additions should clearly fit politics, geopolitics, policymaking, strategic studies, or decision-making. See [`CONTRIBUTING.md`](CONTRIBUTING.md) and [`docs/selection-criteria.md`](docs/selection-criteria.md) before proposing papers.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    README.write_text(build_readme(), encoding="utf-8")


if __name__ == "__main__":
    main()
