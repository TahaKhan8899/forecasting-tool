# Project Overview: AI-Powered Forecasting Tool

## Objective
To develop a robust backend system and associated tools to automate the collection, calculation, and forecasting of key business metrics currently managed via manual spreadsheets. This system will provide timely, accurate data and predictive insights to support strategic decision-making for e-commerce businesses using Shopify.

## Core Problem
Manual spreadsheet-based forecasting is time-consuming, error-prone, and lacks the ability to easily perform scenario analysis or integrate real-time data sources like ad spend effectively.

## High-Level Goals
- Automate data collection from Shopify (multiple stores) and major ad platforms (Meta, Google, TikTok, Amazon).
- Automate calculation of key e-commerce metrics (aMER, AOV, repeat rates, etc.).
- Develop an AI layer for predictive forecasting of spend, revenue, and profitability.
- Enable "what-if" scenario analysis.
- Provide an intuitive interface/dashboard for insights and reporting (future phase).

## Current State (Start of Project)
An existing CLI MVP application exists which connects to a single Shopify store via API key, makes GraphQL requests, calculates some metrics, and saves to CSV. This needs to be replaced by a scalable, multi-store API service with database persistence.