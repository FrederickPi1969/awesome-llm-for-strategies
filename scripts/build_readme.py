#!/usr/bin/env python3
"""Build README and a merged thematic paper table."""

from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
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
STRATEGIC_STUDIES_FOUNDATION = ROOT / "data" / "processed" / "strategic_studies_foundation_enriched.csv"
RUN_SUMMARY = ROOT / "data" / "processed" / "run_summary.json"
SECOND_ORDER_SUMMARY = ROOT / "data" / "processed" / "second_order" / "run_summary.json"
TARGETED_SUMMARY = ROOT / "data" / "processed" / "targeted_strategic_decisions" / "run_summary.json"
FOG_OF_WAR_SUMMARY = ROOT / "data" / "processed" / "fog_of_war" / "run_summary.json"
CRITIQUE_PRIORITY_SUMMARY = ROOT / "data" / "processed" / "critique_priority_expansion" / "run_summary.json"
THEMATIC_PAPERS = ROOT / "data" / "processed" / "thematic_papers.csv"
README = ROOT / "README.md"

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
]

SUBTHEME_ORDER = {
    "Political Science and Strategic Judgment Foundations": [
        "Deterrence, coercion, and nuclear strategy",
        "Bargaining, signaling, and war",
        "International politics, intelligence, and crisis judgment",
        "Intelligence analysis and structured analytic techniques",
        "Forecasting, hindsight bias, and expert judgment",
    ],
    "Foundations, Surveys, and Methods": [
        "Political science and computational social science overviews",
        "Social simulation and agent-based modeling reviews",
        "Strategic reasoning and game-theoretic reviews",
    ],
    "Classical Political NLP and Information Extraction": [
        "Political text as data and policy-position extraction",
        "Legislative speech and policy text classification",
        "Political event data and conflict information extraction",
    ],
    "Politics, Democracy, Public Opinion, and Persuasion": [
        "Political ideology, representation, and bias",
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
Political Science and Strategic Judgment Foundations|Intelligence analysis and structured analytic techniques|Psychology of Intelligence Analysis
Political Science and Strategic Judgment Foundations|Intelligence analysis and structured analytic techniques|Structured Analytic Techniques for Intelligence Analysis
Political Science and Strategic Judgment Foundations|Intelligence analysis and structured analytic techniques|Pearl Harbor: Warning and Decision
Political Science and Strategic Judgment Foundations|Intelligence analysis and structured analytic techniques|Essence of Decision: Explaining the Cuban Missile Crisis
Political Science and Strategic Judgment Foundations|Intelligence analysis and structured analytic techniques|Victims of Groupthink
Political Science and Strategic Judgment Foundations|Intelligence analysis and structured analytic techniques|Analogies at War: Korea Munich Dien Bien Phu and the Vietnam Decisions of 1965
Political Science and Strategic Judgment Foundations|Intelligence analysis and structured analytic techniques|Intelligence Analysis: A Target-Centric Approach
Political Science and Strategic Judgment Foundations|Intelligence analysis and structured analytic techniques|Thinking in Time: The Uses of History for Decision-Makers
Political Science and Strategic Judgment Foundations|Forecasting, hindsight bias, and expert judgment|Hindsight (Not Equal To) Foresight: The Effect of Outcome Knowledge on Judgment Under Uncertainty.
Political Science and Strategic Judgment Foundations|Forecasting, hindsight bias, and expert judgment|Expert Political Judgment: How Good Is It? How Can We Know?
Political Science and Strategic Judgment Foundations|Forecasting, hindsight bias, and expert judgment|Superforecasting: The Art and Science of Prediction
Foundations, Surveys, and Methods|Political science and computational social science overviews|Political-LLM: Large Language Models in Political Science
Foundations, Surveys, and Methods|Political science and computational social science overviews|Large Language Models in Politics and Democracy: A Comprehensive Survey
Foundations, Surveys, and Methods|Political science and computational social science overviews|Can Large Language Models Transform Computational Social Science?
Foundations, Surveys, and Methods|Political science and computational social science overviews|Large language models and political science
Foundations, Surveys, and Methods|Social simulation and agent-based modeling reviews|Large language models empowered agent-based modeling and simulation: a survey and perspectives
Foundations, Surveys, and Methods|Social simulation and agent-based modeling reviews|From Individual to Society: A Survey on Social Simulation Driven by Large Language Model-based Agents
Foundations, Surveys, and Methods|Social simulation and agent-based modeling reviews|Validation is the central challenge for generative social simulation: a critical review of LLMs in agent-based modeling
Foundations, Surveys, and Methods|Strategic reasoning and game-theoretic reviews|LLM as a Mastermind: A Survey of Strategic Reasoning with Large Language Models
Foundations, Surveys, and Methods|Strategic reasoning and game-theoretic reviews|Game Theory Meets Large Language Models: A Systematic Survey
Foundations, Surveys, and Methods|Strategic reasoning and game-theoretic reviews|Multi-Agent, Human-Agent and Beyond: A Survey on Cooperation in Social Dilemmas
Foundations, Surveys, and Methods|Strategic reasoning and game-theoretic reviews|A Survey on Large Language Model-Based Social Agents in Game-Theoretic Scenarios
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
Classical Political NLP and Information Extraction|Legislative speech and policy text classification|Measuring Political Positions from Legislative Speech
Classical Political NLP and Information Extraction|Legislative speech and policy text classification|Get out the vote: Determining support or opposition from Congressional floor-debate transcripts
Classical Political NLP and Information Extraction|Legislative speech and policy text classification|Predicting Legislative Roll Calls from Text
Classical Political NLP and Information Extraction|Legislative speech and policy text classification|Textual Predictors of Bill Survival in Congressional Committees
Classical Political NLP and Information Extraction|Legislative speech and policy text classification|The Media Frames Corpus: Annotations of Frames Across Issues
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
Politics, Democracy, Public Opinion, and Persuasion|Political ideology, representation, and bias|Whose Opinions Do Language Models Reflect?
Politics, Democracy, Public Opinion, and Persuasion|Political ideology, representation, and bias|Large language models reflect the ideology of their creators
Politics, Democracy, Public Opinion, and Persuasion|Political ideology, representation, and bias|Echoes of Power: Investigating Geopolitical Bias in US and China Large Language Models
Politics, Democracy, Public Opinion, and Persuasion|Political ideology, representation, and bias|More human than human: measuring ChatGPT political bias
Politics, Democracy, Public Opinion, and Persuasion|Political ideology, representation, and bias|Should ChatGPT be Biased? Challenges and Risks of Bias in Large Language Models
Politics, Democracy, Public Opinion, and Persuasion|Political ideology, representation, and bias|The political ideology of conversational AI: Converging evidence on ChatGPT's pro-environmental, left-libertarian orientation
Politics, Democracy, Public Opinion, and Persuasion|Political ideology, representation, and bias|Cultural bias and cultural alignment of large language models
Politics, Democracy, Public Opinion, and Persuasion|Elections, voters, and campaign discourse|ElectionSim: Massive Population Election Simulation Powered by Large Language Model Driven Agents
Politics, Democracy, Public Opinion, and Persuasion|Elections, voters, and campaign discourse|Large-Scale Longitudinal Study of LLMs During the 2024 United States Election Season
Politics, Democracy, Public Opinion, and Persuasion|Elections, voters, and campaign discourse|A Public Dataset Tracking Social Media Discourse about the 2024 U.S. Presidential Election on Twitter/X
Politics, Democracy, Public Opinion, and Persuasion|Elections, voters, and campaign discourse|Hidden Persuaders: LLMs’ Political Leaning and Their Influence on Voters
Politics, Democracy, Public Opinion, and Persuasion|Public opinion, polling, and political annotation|Large language models as a substitute for human experts in annotating political text
Politics, Democracy, Public Opinion, and Persuasion|Public opinion, polling, and political annotation|Demonstrations of the Potential of AI-based Political Issue Polling
Politics, Democracy, Public Opinion, and Persuasion|Public opinion, polling, and political annotation|Performance and biases of Large Language Models in public opinion simulation
Politics, Democracy, Public Opinion, and Persuasion|Public opinion, polling, and political annotation|Random Silicon Sampling: Simulating Human Sub-Population Opinion Using a Large Language Model Based on Group-Level Demographic Information
Politics, Democracy, Public Opinion, and Persuasion|Public opinion, polling, and political annotation|ChatGPT-4 Outperforms Experts and Crowd Workers in Annotating Political Twitter Messages with Zero-Shot Learning
Politics, Democracy, Public Opinion, and Persuasion|Deliberation, persuasion, and information environments|Generative Echo Chamber? Effect of LLM-Powered Search Systems on Diverse Information Seeking
Politics, Democracy, Public Opinion, and Persuasion|Deliberation, persuasion, and information environments|Systematic Biases in LLM Simulations of Debates
Politics, Democracy, Public Opinion, and Persuasion|Deliberation, persuasion, and information environments|From Skepticism to Acceptance: Simulating the Attitude Dynamics Toward Fake News
Politics, Democracy, Public Opinion, and Persuasion|Legislative and political-agent simulation|Political Actor Agent: Simulating Legislative Politics with LLM Agents
Politics, Democracy, Public Opinion, and Persuasion|Legislative and political-agent simulation|LegiGPT: Party Politics and Transport Policy with Large Language Model
Politics, Democracy, Public Opinion, and Persuasion|Legislative and political-agent simulation|A Large-Scale Simulation on Large Language Models for Decision-Making in Political Science
Policymaking, Governance, and Institutional Decision Support|Democratic governance and augmentation|Large Language Models as agents for augmented democracy
Policymaking, Governance, and Institutional Decision Support|Policy translation and policy brief generation|Sci2Pol: Evaluating and Fine-tuning LLMs on Scientific-to-Policy Brief Generation
Policymaking, Governance, and Institutional Decision Support|Policy persuasion and democratic deliberation|AI can help humans find common ground in democratic deliberation
Policymaking, Governance, and Institutional Decision Support|Policy persuasion and democratic deliberation|Large Language Models Can Argue in Convincing Ways About Politics, But Humans Dislike AI Authors: Implications for Governance
Policymaking, Governance, and Institutional Decision Support|Policy persuasion and democratic deliberation|LLM-generated messages can persuade humans on policy issues
Policymaking, Governance, and Institutional Decision Support|Strategic and institutional decision support|Biased LLMs can Influence Political Decision-Making
Policymaking, Governance, and Institutional Decision Support|Strategic and institutional decision support|Generative Artificial Intelligence and Evaluating Strategic Decisions
Policymaking, Governance, and Institutional Decision Support|AI-assisted strategy and managerial decision-making|How Well Can AI Do Strategy? Empirical Benchmarking Using Strategy Simulations
Policymaking, Governance, and Institutional Decision Support|AI-assisted strategy and managerial decision-making|AI-Augmented Strategic Decision-Making Under Time Constraints: An Experimental Study on Mental Representations and Strategic Foresight
Policymaking, Governance, and Institutional Decision Support|AI-assisted strategy and managerial decision-making|Towards Using Prompt Engineering in Large Language Models to Assist Decision Making
Policymaking, Governance, and Institutional Decision Support|AI-assisted strategy and managerial decision-making|Beyond Black Boxes: Designing and Testing Agentic AI Systems for Strategy
Policymaking, Governance, and Institutional Decision Support|AI-assisted strategy and managerial decision-making|Can AI Do Strategy?
Policymaking, Governance, and Institutional Decision Support|AI-assisted strategy and managerial decision-making|Advancing Decision-Making through AI-Human Collaboration: A Systematic Review and Conceptual Framework
Policymaking, Governance, and Institutional Decision Support|AI-assisted strategy and managerial decision-making|Can AI Do Strategy? A Dialogue and Debate
Policymaking, Governance, and Institutional Decision Support|Strategic evaluation, bias, and foresight|Reproducing and Extending Experiments in Behavioral Strategy with Large Language Models
Policymaking, Governance, and Institutional Decision Support|Strategic evaluation, bias, and foresight|AI strategy under institutional pressure: strategic conformity and decision-making in large language models
Policymaking, Governance, and Institutional Decision Support|Strategic evaluation, bias, and foresight|Bias in, symbolic compliance out? GPT's reliance on gender and race in strategic evaluations
Policymaking, Governance, and Institutional Decision Support|Strategic evaluation, bias, and foresight|From Problems to Solutions in Strategic Decision-Making: The Effects of Generative AI on Problem Formulation
Geopolitics, Diplomacy, National Security, and Wargaming|Diplomacy and international institutions|Human-level play in the game of Diplomacy by combining language models with strategic reasoning
Geopolitics, Diplomacy, National Security, and Wargaming|Diplomacy and international institutions|Critical Foreign Policy Decisions Benchmark: Measuring Diplomatic Preferences in Large Language Models
Geopolitics, Diplomacy, National Security, and Wargaming|Diplomacy and international institutions|Benchmarking LLMs for Political Science: A United Nations Perspective / United Nations Benchmark
Geopolitics, Diplomacy, National Security, and Wargaming|Diplomacy and international institutions|UNSC-Bench: Evaluating LLM Diplomatic Role-Playing Through UN Security Council Vote Prediction
Geopolitics, Diplomacy, National Security, and Wargaming|Diplomacy and international institutions|DipLLM: Fine-Tuning LLM for Strategic Decision-making in Diplomacy
Geopolitics, Diplomacy, National Security, and Wargaming|Diplomacy and international institutions|Richelieu: Self-Evolving LLM-Based Agents for AI Diplomacy
Geopolitics, Diplomacy, National Security, and Wargaming|Diplomacy and international institutions|DiplomacyAgent: Do LLMs Balance Interests and Ethical Principles in International Events?
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
Geopolitics, Diplomacy, National Security, and Wargaming|Conflict, escalation, and geopolitical simulation|Simulating Influence Dynamics with LLM Agents
Geopolitics, Diplomacy, National Security, and Wargaming|Conflict, escalation, and geopolitical simulation|LLMs as Strategic Actors: Behavioral Alignment, Risk Calibration, and Argumentation Framing in Geopolitical Simulations
Geopolitics, Diplomacy, National Security, and Wargaming|Conflict, escalation, and geopolitical simulation|War and Peace (WarAgent): Large Language Model-based Multi-Agent Simulation of World Wars
Geopolitics, Diplomacy, National Security, and Wargaming|Conflict, escalation, and geopolitical simulation|Do Large Language Models Know Conflict? Investigating Parametric vs. Non-Parametric Knowledge of LLMs for Conflict Forecasting
Geopolitics, Diplomacy, National Security, and Wargaming|Conflict, escalation, and geopolitical simulation|When AI Navigates the Fog of War
Geopolitics, Diplomacy, National Security, and Wargaming|Conflict, escalation, and geopolitical simulation|Managing Escalation in Off-the-Shelf Large Language Models
Geopolitics, Diplomacy, National Security, and Wargaming|Conflict, escalation, and geopolitical simulation|AI Arms and Influence: Frontier Models Exhibit Sophisticated Reasoning in Simulated Nuclear Crises
Geopolitics, Diplomacy, National Security, and Wargaming|National security applications and doctrine|On Large Language Models in National Security Applications
Forecasting, Geopolitical Risk, and Foresight|Forecasting benchmarks and datasets|ForecastBench: A Dynamic Benchmark of AI Forecasting Capabilities
Forecasting, Geopolitical Risk, and Foresight|Forecasting benchmarks and datasets|MIRAI: Evaluating LLM Agents for Event Forecasting
Forecasting, Geopolitical Risk, and Foresight|Forecasting benchmarks and datasets|Forecasting Future International Events: A Reliable Dataset for Text-Based Event Modeling / WORLDREP
Forecasting, Geopolitical Risk, and Foresight|Forecasting benchmarks and datasets|OpenEP: Open-Ended Future Event Prediction
Forecasting, Geopolitical Risk, and Foresight|Forecasting benchmarks and datasets|Forecasting Future World Events with Neural Networks
Forecasting, Geopolitical Risk, and Foresight|Forecasting benchmarks and datasets|Bench to the Future: A Pastcasting Benchmark for Forecasting Agents
Forecasting, Geopolitical Risk, and Foresight|Forecasting benchmarks and datasets|The Future Outcome Reasoning and Confidence Assessment Benchmark
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
Forecasting, Geopolitical Risk, and Foresight|Geopolitical event prediction systems|LLM4Geopolitics: A Framework Leveraging Large Language Models for Predicting Geopolitical Events
Forecasting, Geopolitical Risk, and Foresight|Geopolitical event prediction systems|Multi-Source Models for Civil Unrest Forecasting
Forecasting, Geopolitical Risk, and Foresight|Geopolitical event prediction systems|Toward Better Temporal Structures for Geopolitical Events Forecasting
Forecasting, Geopolitical Risk, and Foresight|Geopolitical event prediction systems|Agentic Reasoning for Social Event Extrapolation: Integrating Knowledge Graphs and Language Models
Forecasting, Geopolitical Risk, and Foresight|Geopolitical event prediction systems|ThinkTank-ME: A Multi-Expert Framework for Middle East Event Forecasting
Forecasting, Geopolitical Risk, and Foresight|Geoeconomic and geopolitical risk signals|Geoeconomic Pressure
Forecasting, Geopolitical Risk, and Foresight|Geoeconomic and geopolitical risk signals|The AI-GPR Index: Measuring Geopolitical Risk using Artificial Intelligence
Strategic Reasoning, Games, Negotiation, and Cooperation|Game-theoretic and strategic reasoning benchmarks|Playing repeated games with large language models
Strategic Reasoning, Games, Negotiation, and Cooperation|Game-theoretic and strategic reasoning benchmarks|Strategic behavior of large language models and the role of game structure versus contextual framing
Strategic Reasoning, Games, Negotiation, and Cooperation|Game-theoretic and strategic reasoning benchmarks|GTBench: Uncovering the Strategic Reasoning Limitations of LLMs via Game-Theoretic Evaluations
Strategic Reasoning, Games, Negotiation, and Cooperation|Game-theoretic and strategic reasoning benchmarks|GameBench: Evaluating Strategic Reasoning Abilities of LLM Agents
Strategic Reasoning, Games, Negotiation, and Cooperation|Game-theoretic and strategic reasoning benchmarks|How Far Are We on the Decision-Making of LLMs? Evaluating LLMs' Gaming Ability in Multi-Agent Environments
Strategic Reasoning, Games, Negotiation, and Cooperation|Game-theoretic and strategic reasoning benchmarks|Game-theoretic LLM: Agent Workflow for Negotiation Games
Strategic Reasoning, Games, Negotiation, and Cooperation|Game-theoretic and strategic reasoning benchmarks|Decision-Making Behavior Evaluation Framework for LLMs under Uncertain Context
Strategic Reasoning, Games, Negotiation, and Cooperation|Game-theoretic and strategic reasoning benchmarks|SPIN-Bench: How Well Do LLMs Plan Strategically and Reason Socially?
Strategic Reasoning, Games, Negotiation, and Cooperation|Game-theoretic and strategic reasoning benchmarks|Multi-Agent Strategic Games with LLMs
Strategic Reasoning, Games, Negotiation, and Cooperation|Negotiation, bargaining, and communication games|SOTOPIA: Interactive Evaluation for Social Intelligence in Language Agents
Strategic Reasoning, Games, Negotiation, and Cooperation|Negotiation, bargaining, and communication games|Exploring Large Language Models for Communication Games: An Empirical Study on Werewolf
Strategic Reasoning, Games, Negotiation, and Cooperation|Negotiation, bargaining, and communication games|Improving Language Model Negotiation with Self-Play and In-Context Learning from AI Feedback
Strategic Reasoning, Games, Negotiation, and Cooperation|Negotiation, bargaining, and communication games|Measuring Bargaining Abilities of LLMs: A Benchmark and A Buyer-Enhancement Method
Strategic Reasoning, Games, Negotiation, and Cooperation|Cooperation and social dilemmas|Cooperate or Collapse: Emergence of Sustainable Cooperation in a Society of LLM Agents
Strategic Reasoning, Games, Negotiation, and Cooperation|Cooperation and social dilemmas|Nicer Than Humans: How do Large Language Models Behave in the Prisoner's Dilemma?
Strategic Reasoning, Games, Negotiation, and Cooperation|Cooperation and social dilemmas|Shall We Team Up: Exploring Spontaneous Cooperation of Competing LLM Agents
Strategic Reasoning, Games, Negotiation, and Cooperation|Cooperation and social dilemmas|Cultural Evolution of Cooperation among LLM Agents
Strategic Reasoning, Games, Negotiation, and Cooperation|Behavioral game tests and human-like strategy|A Turing test of whether AI chatbots are behaviorally similar to humans
Strategic Reasoning, Games, Negotiation, and Cooperation|Behavioral game tests and human-like strategy|Simulating Human Strategic Behavior: Comparing Single and Multi-agent LLMs
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
Multi-Agent Social Simulation and Synthetic Societies|Social networks, movements, and polarization|Network formation and dynamics among multi-LLMs
Multi-Agent Social Simulation and Synthetic Societies|Social networks, movements, and polarization|Emergence of human-like polarization among large language model agents
Multi-Agent Social Simulation and Synthetic Societies|Social networks, movements, and polarization|Unveiling the Truth and Facilitating Change: Towards Agent-based Large-scale Social Movement Simulation
Multi-Agent Social Simulation and Synthetic Societies|Social networks, movements, and polarization|Agent-Based Modelling Meets Generative AI in Social Network Simulations
Multi-Agent Social Simulation and Synthetic Societies|Social networks, movements, and polarization|Decoding Echo Chambers: LLM-Powered Simulations Revealing Polarization in Social Networks
AI Safety, Influence Operations, and Societal Risk|Influence operations and persuasion risk|Generative Language Models and Automated Influence Operations: Emerging Threats and Potential Mitigations
AI Safety, Influence Operations, and Societal Risk|Deception, multi-agent risk, and control|Multi-Agent Risks from Advanced AI
AI Safety, Influence Operations, and Societal Risk|Deception, multi-agent risk, and control|AI deception: A survey of examples, risks, and potential solutions
AI Safety, Influence Operations, and Societal Risk|Bias, toxicity, and cultural alignment risks|Generative Exaggeration in LLM Social Agents: Consistency, Bias, and Toxicity
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
    duplicate_count = source_count - len(output)
    return output, source_count, duplicate_count


def theme_sort_key(row: dict[str, str]) -> tuple[int, int, int, int, str]:
    theme_index = THEME_ORDER.index(row["theme"])
    subtheme_index = SUBTHEME_ORDER[row["theme"]].index(row["subtheme"])
    importance_rank = {"Core": 0, "Important": 1, "Optional": 2, "Optional / Engineering": 2, "Curated": 3}.get(
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


def paper_line(row: dict[str, str]) -> str:
    importance = row.get("importance", "")
    label = f"{importance}; " if importance and importance != "Curated" else ""
    citation_count = row.get("citationCount") or "n/a"
    return f"- {markdown_link(row['title'], row.get('url', ''))} ({row.get('year') or 'n.d.'}) - {label}citations: {citation_count}."


def build_readme() -> str:
    assignments = parse_assignments()
    rows, source_count, duplicate_count = merge_rows(source_rows(), assignments)
    rows = sorted(rows, key=theme_sort_key)
    write_thematic_csv(rows)

    by_theme: dict[str, dict[str, list[dict[str, str]]]] = defaultdict(lambda: defaultdict(list))
    for row in rows:
        by_theme[row["theme"]][row["subtheme"]].append(row)

    first_summary = json.loads(RUN_SUMMARY.read_text(encoding="utf-8"))
    second_summary = read_json_if_exists(SECOND_ORDER_SUMMARY)
    targeted_summary = read_json_if_exists(TARGETED_SUMMARY)
    fog_summary = read_json_if_exists(FOG_OF_WAR_SUMMARY)
    critique_priority_summary = read_json_if_exists(CRITIQUE_PRIORITY_SUMMARY)
    theme_counts = {theme: sum(len(items) for items in by_theme.get(theme, {}).values()) for theme in THEME_ORDER}

    lines = [
        "# Awesome LLM for Strategies",
        "",
        "A curated paper list on large language models for politics, geopolitics, policymaking, strategic studies, and decision-making.",
        "",
        "This repository focuses on how LLMs and LLM agents analyze political behavior, forecast events, support policy reasoning, simulate social and diplomatic systems, and behave in strategic environments.",
        "",
        "Out of scope: finance, trading, stock prediction, portfolio management, generic financial LLM benchmarks, and generic foundation-model papers unless they directly support one of the five focus areas above.",
        "",
        "Citation counts are from the Semantic Scholar Graph API, collected on 2026-05-21.",
        "",
        f"Current curated coverage: **{len(rows)} unique papers** organized into {len(THEME_ORDER)} themes.",
        "",
        "## Contents",
        "",
        "- [Papers by Theme](#papers-by-theme)",
        "- [Data and Collection](#data-and-collection)",
        "- [Contributing](#contributing)",
        "",
        "## Papers by Theme",
        "",
    ]

    for theme in THEME_ORDER:
        if theme not in by_theme:
            continue
        lines.extend([f"### {theme}", "", f"{theme_counts[theme]} papers.", ""])
        for subtheme in SUBTHEME_ORDER[theme]:
            papers = by_theme[theme].get(subtheme, [])
            if not papers:
                continue
            lines.extend([f"#### {subtheme}", ""])
            for row in papers:
                lines.append(paper_line(row))
            lines.append("")

    lines.extend(
        [
            "## Data and Collection",
            "",
            f"- Total unique papers in the thematic list: {len(rows)}",
            f"- Source rows checked before merge: {source_count}",
            f"- Duplicate source rows removed during merge: {duplicate_count}",
            f"- Core seed papers: {sum(1 for row in rows if row.get('source_tables') == 'core_seed_papers.csv')}",
            f"- Curated additions merged into themes: {sum(1 for row in rows if row.get('source_tables') != 'core_seed_papers.csv')}",
            f"- Initial citation/reference edges scanned: {first_summary.get('edge_count', 0)}",
            f"- Additional citation/reference edges scanned from priority papers: {second_summary.get('edge_count', 0)}",
            f"- Targeted strategic-decision related-work edges scanned: {targeted_summary.get('edge_count', 0)}",
            f"- Fog-of-war related-work edges scanned: {fog_summary.get('edge_count', 0)}",
            f"- Critique-priority citation/reference edges scanned: {critique_priority_summary.get('edge_count', 0)}",
            "",
            "Data files:",
            "",
            "- `data/processed/thematic_papers.csv`: merged thematic paper table used to build the homepage.",
            "- `data/raw/core_seed_papers.csv`: original core seed list.",
            "- `data/raw/targeted_strategic_decisions_seed.csv`: targeted trace seed for the strategic-decision paper.",
            "- `data/raw/classical_political_nlp_ie_seed.csv`: curated classical political NLP and information-extraction seed list.",
            "- `data/raw/fog_of_war_related_work_seed.csv`: curated Fog of War related-work and foundation seed list.",
            "- `data/raw/strategic_studies_foundation_seed.csv`: curated strategic-studies foundation seed list.",
            "- `data/raw/critique_priority_expansion_seeds.csv`: critique-selected high-priority trace seeds.",
            "- `data/processed/core_seed_papers_enriched.csv`: seed metadata with citation counts, authors, venues, abstracts, and resolution method.",
            "- `data/processed/targeted_related_works_strategy.csv`: selected additions from the targeted strategic-decision trace.",
            "- `data/processed/classical_political_nlp_ie_enriched.csv`: Semantic Scholar metadata for the classical political NLP and IE additions.",
            "- `data/processed/fog_of_war_related_works_enriched.csv`: Semantic Scholar metadata for Fog of War related-work additions.",
            "- `data/processed/strategic_studies_foundation_enriched.csv`: Semantic Scholar metadata for strategic-studies foundation additions.",
            "- `data/processed/critique_priority_expansion/curated_additions.csv`: selected additions from critique-priority seed expansion.",
            "- `data/processed/targeted_strategic_decisions/run_summary.json`: targeted trace summary.",
            "- `data/processed/fog_of_war/run_summary.json`: Fog of War trace summary.",
            "- `data/processed/critique_priority_expansion/run_summary.json`: critique-priority trace summary.",
            "",
            "Scripts:",
            "",
            "- `scripts/expand_semantic_scholar.py`: resolves seeds, fetches citations/references, and writes candidate tables.",
            "- `scripts/fetch_seed_metadata.py`: enriches seed papers with Semantic Scholar metadata.",
            "- `scripts/build_targeted_related_works.py`: selects targeted related-work additions from a trace longlist.",
            "- `scripts/build_readme.py`: rebuilds this README and validates that every curated paper is assigned to a theme.",
            "",
            "## Contributing",
            "",
            "Additions should clearly fit one of the five focus areas: politics, geopolitics, policymaking, strategic studies, or decision-making. Please include title, year, URL, category, citation count if available, and a short reason for inclusion.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    README.write_text(build_readme(), encoding="utf-8")


if __name__ == "__main__":
    main()
