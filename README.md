# LinkedIn Repository Role Recommender Agent

## 📌 Overview
This project implements an AI agent that leverages **MCP (Model Context Protocol)** and **LangGraph** to analyze the GitHub repositories of LinkedIn users.  
Based on the repository content and activity, the agent recommends the **top 3 IT roles** that best fit the user’s profile.  

The goal of this project is to showcase practical benchmarking of MCP-based agents with **web scraping** and **LLM-powered reasoning**.

---

## ⚙️ Features
- 🔍 Scrapes GitHub repositories of a LinkedIn user.
- 📊 Analyzes repository descriptions, topics, and activity.
- 🤖 Uses LLM reasoning to match skills with IT roles.
- 🎯 Recommends **top 3 IT roles** tailored to the user.

---

## 🛠️ Tech Stack
- **LangGraph** – for building the AI agent workflow  
- **MCP (Model Context Protocol)** – Firecrawl MCP or Apify MCP for scraping  
- **langchain-mcp-adapters** – optional, for easier integration  
- **LLM API** – for reasoning and recommendation  
