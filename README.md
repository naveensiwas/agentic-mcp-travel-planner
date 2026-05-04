# 🌍 AI Travel Budget Planner — Multi-Agent & Single-Agent MCP Application

AI travel planning app built with **Model Context Protocol (MCP)**, **LangChain**, and **Groq LLM**.

It demonstrates two distinct MCP client implementations:
- **🧠 Multi-Agent Mode**: How specialized agents can collaborate across multiple MCP servers to produce a consolidated, user-friendly travel plan.
- **🧪 Single-Agent Mode**: How a single tool-calling agent can directly query multiple MCP servers for testing and debugging.

---

## 📌 What This App Does

This project demonstrates two distinct MCP client implementations:

### 🧠 Multi-Agent Mode
Given trip inputs like destination, budget, and duration, the app:
1. Collects destination research (weather, local tips, packing, accommodation)
2. Computes budget/currency insights
3. Synthesizes both reports into one final travel plan

Example prompt:
> "Plan a 7-day trip to Tokyo with a $3,000 budget."

### 🧪 Single-Agent Mode
A simplified demonstration that uses a single tool-calling agent to directly query multiple MCP servers:
- Performs math calculations (addition, multiplication)
- Fetches weather data from specified locations

This mode is useful for testing individual MCP server connectivity and debugging tool integrations.

---

## 🗂️ Project Structure

```text
agentic-mcp-travel-planner/
├── multi_agent_multi_mcp_client.py      # Main multi-agent entry point
├── single_agent_multi_mcp_client.py     # Single-agent MCP smoke-test client
├── README.md
├── pyproject.toml
├── requirements.txt
├── uv.lock
│
├── agents/
│   ├── __init__.py
│   ├── travel_agent.py                  # Weather + travel-tips research agent
│   ├── finance_agent.py                 # Budget + currency + math verification
│   └── orchestrator.py                  # LLM-only final plan synthesizer
│
├── config/
│   ├── __init__.py
│   └── settings.py                      # LLM factory, server configs, CURRENCY_MAP
│
├── servers/
│   ├── __init__.py
│   ├── weather_server.py                # HTTP MCP server
│   ├── travel_tips_server.py            # stdio MCP server
│   ├── currency_server.py               # stdio MCP server
│   └── math_server.py                   # stdio MCP server
│
└── utils/
    ├── __init__.py
    └── display.py                       # print_banner(), print_plan()
```

---

## 🏗️ Architecture

### 🧠 Multi-Agent Architecture

```text
User Input (destination, budget_usd, num_days)
                |
                v
multi_agent_multi_mcp_client.py
(plan_trip)
   |
   +--> Travel Agent (agents/travel_agent.py)
   |      - weather_server.py      [streamable_http]
   |      - travel_tips_server.py  [stdio]
   |
   +--> Finance Agent (agents/finance_agent.py)
   |      - currency_server.py     [stdio]
   |      - math_server.py         [stdio]
   |
   +--> Orchestrator (agents/orchestrator.py)
          - LLM-only synthesis (no MCP tools)
                |
                v
Final formatted travel plan
```

**Best for**:
- Complex workflows requiring multiple specialized agents
- Coordinating different domains (travel, finance, etc.)
- Scenarios needing report synthesis and consolidation
- Production use cases with comprehensive planning needs

### 🧪 Single-Agent Architecture

```text
User Input (math/weather query)
                |
                v
single_agent_multi_mcp_client.py
(run_single_agent_demo)
   |
   +--> Single Tool-Calling Agent
          |
          +--> math_server.py         [stdio]
          +--> weather_server.py      [streamable_http]
                |
                v
Direct MCP tool responses (math + weather)
```

**Best for**:
- Testing individual MCP server connectivity
- Debugging tool integrations and server responses
- Simple, direct tool queries without orchestration
- Development and proof-of-concept scenarios
- Understanding MCP tool calling basics

---

## 📊 Comparison: Multi-Agent vs Single-Agent

| Aspect | Multi-Agent | Single-Agent |
|---|---|---|
| **Client Script** | `multi_agent_multi_mcp_client.py` | `single_agent_multi_mcp_client.py` |
| **Complexity** | High (multiple agents + orchestrator) | Low (single agent) |
| **Agent Count** | 3+ specialized agents | 1 tool-calling agent |
| **Tool Selection** | Agent-specific | All available tools |
| **Use Case** | Complex travel planning | Tool testing & debugging |
| **Output** | Synthesized travel plan | Direct tool responses |
| **Setup Time** | Longer (all agents run) | Quick (minimal overhead) |

---

## 🤖 Agent Responsibilities

| Architecture | Agent / Component | Module | MCP Tools | Responsibility |
|---|---|---|---|---|
| Multi-Agent | Travel Research Agent | `agents/travel_agent.py` | `get_weather`, `get_climate_type`, `get_destination_info`, `get_packing_list`, `estimate_accommodation_cost` | Destination/weather research and stay guidance |
| Multi-Agent | Finance Agent | `agents/finance_agent.py` | `usd_to_currency`, `get_daily_budget`, `add`, `multiply` | Budget conversion, daily budget, arithmetic verification |
| Multi-Agent | Orchestrator Agent | `agents/orchestrator.py` | *(none)* | Merges specialist reports into a single final plan |
| Single-Agent | Tool-Calling Agent | `single_agent_multi_mcp_client.py` | `add`, `multiply`, `get_weather` | Handles direct math and weather queries in a single-agent flow |

---

## 🔌 MCP Servers

### 1) Math Server — `servers/math_server.py`
- Transport: `stdio`
- Provides arithmetic helper tools for finance verification

### 2) Weather Server — `servers/weather_server.py`
- Transport: `streamable_http`
- URL used by clients: `http://localhost:8000/mcp`
- Must be started manually before running clients

### 3) Currency Server — `servers/currency_server.py`
- Transport: `stdio`
- Provides USD conversion and daily budget tools

### 4) Travel Tips Server — `servers/travel_tips_server.py`
- Transport: `stdio`
- Provides destination info, packing suggestions, and accommodation estimate

---

## ℹ️ MCP Implementation Note
- All MCP servers and tools used in this project are in\-house developed. 
- They include custom hardcoded logic tailored to this application’s travel and budget planning workflows.

## ⚙️ Setup

### Prerequisites
- Python 3.11+
- Groq API key

### 1) Install dependencies

Using pip:
```bash
pip install -r requirements.txt
```

Using uv:
```bash
uv sync
```

### 2) Create `.env` in project root

```bash
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=qwen/qwen3-32b
```

Notes:
- `GROQ_API_KEY` is required.
- `GROQ_MODEL` is optional in code (defaults to `qwen/qwen3-32b`).

---

## 🚀 Run the App

### Option A: Full multi-agent planner

Terminal 1:
```bash
python servers/weather_server.py
```

Terminal 2:
```bash
python multi_agent_multi_mcp_client.py
```

To change the default trip, edit the `asyncio.run(plan_trip(...))` block at the bottom of `multi_agent_multi_mcp_client.py`.

### Option B: Single-agent smoke test

Terminal 1:
```bash
python servers/weather_server.py
```

Terminal 2:
```bash
python single_agent_multi_mcp_client.py
```

This script runs sample math + weather queries through one tool-calling agent.

---

## 🔄 Execution Flow

### Multi-Agent Flow

1. `multi_agent_multi_mcp_client.py` calls `plan_trip(destination, budget_usd, num_days)`
2. `utils.display.print_banner()` prints a trip header
3. `agents/travel_agent.py` returns a travel research report
4. `agents/finance_agent.py` returns a finance report
5. `agents/orchestrator.py` synthesizes both into the final plan
6. `utils.display.print_plan()` prints final output

### Single-Agent Flow

1. `single_agent_multi_mcp_client.py` calls `run_single_agent_demo()`
2. Single tool-calling agent receives user queries
3. Agent introspects available tools from MCP servers:
   - Math tools: `add`, `multiply`
   - Weather tools: `get_weather`
4. Agent executes the appropriate tool based on query context
5. Direct tool responses are returned to the user without synthesis

---

## 🧩 Key Configuration

In `config/settings.py`:
- `get_llm()` builds a shared `ChatGroq` client used by **both Multi-Agent and Single-Agent** modes
- `get_server_configs()` defines MCP transport config for all servers (applies to **both modes**)
- `CURRENCY_MAP` maps known destinations to local currency (applies to **Multi-Agent mode**)

### Multi-Agent Specific
- Agent system prompts and tool bindings defined in `agents/travel_agent.py`, `agents/finance_agent.py`
- Orchestrator synthesis logic in `agents/orchestrator.py`

### Single-Agent Specific
- Single agent prompt and tool discovery defined in `single_agent_multi_mcp_client.py`
- All registered MCP servers are automatically available to the agent

### Current Mapped Destinations
- `tokyo -> JPY`
- `paris -> EUR`
- `new york -> USD`
- `bali -> IDR`

---

## ➕ Extend the Project

### Add a new MCP server

1. Create a new server file in `servers/`.
2. Add its config in `config/settings.py` (`get_server_configs`).
3. **For Multi-Agent**: Wire it into the relevant agent module in `agents/` (e.g., add to `travel_agent.py` or `finance_agent.py`).
4. **For Single-Agent**: The new server tools will automatically be available to the single tool-calling agent once registered in `get_server_configs()`.

### Add a new destination

Update the relevant dictionaries/constants in:
- `servers/weather_server.py`
- `servers/travel_tips_server.py`
- `config/settings.py` (`CURRENCY_MAP`)

---

## 🛠️ Troubleshooting

### General Issues

- `GROQ_API_KEY not set`:
  - Ensure `.env` exists and contains `GROQ_API_KEY=...`.
- Weather server connection issues:
  - Start `python servers/weather_server.py` first.
- Port conflict on 8000:
  - Stop the process using port 8000, then restart weather server.
- Import/dependency errors:
  - Reinstall dependencies from `requirements.txt` or run `uv sync`.

### Multi-Agent Specific Issues

- **Agent reporting empty results**:
  - Check that the agent has access to its designated MCP servers.
  - Verify `get_server_configs()` in `config/settings.py` is configured correctly.
  - Ensure the LLM can parse tool definitions properly.

- **Orchestrator synthesis fails**:
  - Confirm that both Travel Agent and Finance Agent reports are generated before orchestration.
  - Check `agents/orchestrator.py` for proper prompt structure.

### Single-Agent Specific Issues

- **Tool not being called**:
  - Verify tool definitions are registered in the respective MCP server.
  - Check that the agent's prompt can trigger tool selection based on the query.
  - Review agent logs to see available tools at inference time.

- **Unexpected tool response**:
  - Directly test the MCP server manually to verify tool behavior.
  - Single-agent relies on tool definitions being correct; verify in the server code.

---

## 📚 References

- MCP: https://modelcontextprotocol.io/docs/getting-started/intro
- LangChain MCP adapters: https://github.com/langchain-ai/langchain-mcp-adapters
- Groq console: https://console.groq.com

---

## 🖥️ Sample Console Output

Below are example logs from both client scripts. These are sample outputs and may vary depending on model response, server data, and runtime environment.

### `single_agent_multi_mcp_client.py`

```text
python single_agent_multi_mcp_client.py

Processing request of type ListToolsRequest
Processing request of type CallToolRequest
Processing request of type CallToolRequest
Processing request of type ListToolsRequest
Processing request of type ListToolsRequest
Math MCP response: The result of (23 + 7) × 10 is **300**. 

Here's the breakdown:
1. First calculate 23 + 7 = **30**
2. Then multiply 30 × 10 = **300**
Weather MCP response: The current weather in Paris is overcast with a temperature of 14°C (57°F) and humidity at 72%. ☁️
```

### `multi_agent_multi_mcp_client.py`

```text
python multi_agent_multi_mcp_client.py

============================================================
  🌍 AI Travel Budget Planner
  Destination : Tokyo
  Budget      : $3000 USD
  Duration    : 7 days
============================================================
Processing request of type ListToolsRequest
Processing request of type CallToolRequest
Processing request of type CallToolRequest
Processing request of type ListToolsRequest
Processing request of type ListToolsRequest
Processing request of type CallToolRequest
Processing request of type ListToolsRequest

✅ Travel Research Agent completed. Report:
Here's your comprehensive travel plan for Tokyo:

🌤 **Current Weather**  
Partly Cloudy, 18°C / 64°F, Humidity: 65%

📍 **Destination Info**  
- **Country**: Japan  
- **Local Currency**: JPY (Japanese Yen)  
- **Visa**: Visa-free for most nationalities (up to 90 days)  
- **Best Travel Season**: March-May (Spring) or October-November (Autumn)  
- **Key Tips**:  
  ✔️ Use Suica/Pasmo IC cards for public transport  
  ✔️ Carry cash (yen) as many places still use it  
  ✔️ Remove shoes in traditional restaurants/homes  
  ✔️ Download Google Translate (Japanese offline pack)  

🧳 **Packing List** (Temperate Climate)  
- Layers (e.g., t-shirts, sweaters)  
- Comfortable walking shoes  
- Light jacket  
- Umbrella  

💰 **Accommodation Estimate**  
- **Mid-range hotels**: ~$120 per night  
- **Total for 7 days**: ~$840  

Let me know if you need further details! 😊
Processing request of type ListToolsRequest
Processing request of type ListToolsRequest
Processing request of type CallToolRequest
Processing request of type CallToolRequest
Processing request of type CallToolRequest
Processing request of type ListToolsRequest
Processing request of type ListToolsRequest
Processing request of type ListToolsRequest

✅ Finance Agent completed. Report:
1. **$3000 USD to JPY**:  
   $3000.0 USD = **448,500.0 JPY** (exchange rate: 149.5).

2. **Daily Budget**:  
   Total budget of $3000 USD divided by 7 days = **$428.57/day**.

3. **Verification via Multiplication**:  
   $428.57/day × 7 days = **$3000.0 USD** (due to rounding, the exact calculation is $2999.99, which is effectively $3000).

Your calculations align correctly, with minor rounding adjustments. Safe travels to Tokyo! 🗾

🤖 Orchestrator Agent synthesizing the final travel plan...

============================================================
  📋 YOUR PERSONALISED TRAVEL PLAN
============================================================
Okay, let's start by breaking down the user's request. They want a concise and well-structured travel plan summary for Tokyo based on the provided research. The main sections to include are Trip Overview, Weather & Best Time, Accommodation, Budget Breakdown, Packing Essentials, Top 3 Local Tips, and a Quick Checklist.

First, the Trip Overview needs to highlight the key details: destination, duration, budget, and main attractions. The user mentioned Tokyo, 7 days, $3000 budget. I should mention some must-visit spots like Asakusa, Shibuya, and the Meiji Shrine. Also, include the Suica card and cash tip as they're important for travel.

Next, the Weather section. The current weather is partly cloudy, 18°C. The best time is March-May or October-November. I should note that the trip is during a good season and maybe mention the humidity.

Accommodation Estimate: Mid-range hotels at $120/night totaling $840. That's straightforward. I can present that with a note on location.

Budget Breakdown is crucial. The total is $3000, converted to 448,500 JPY. Daily budget is about $428.57. Need to show USD, JPY, and daily spend. Also mention the conversion rate and rounding adjustment from the finance report.

Packing Essentials: Layers, walking shoes, jacket, umbrella. Maybe add a note about cash and Suica card again here for emphasis.

Top 3 Local Tips: Use Suica, carry cash, remove shoes. Maybe add a fourth as a bonus? Wait, user asked for top 3, so stick to that. Also, the Google Translate app is a good point to include in tips.

Quick Checklist: Passport, visas, Suica/Pasmo, cash, adapter, packing list items. Also, maybe the offline translation app.

Now, ensuring all sections are covered concisely. Need to keep it encouraging and friendly. Use emojis as in the example. Avoid markdown, just plain text with clear headings. Check that the budget math adds up. For example, $120 x7 is $840, which is correct. The daily budget calculation is correct too. Also, mention the currency conversion accurately. Make sure tips are practical and from the research. Double-check that all user points are addressed without extra fluff. Keep each section short and to the point, maybe bullet points for readability. Use friendly phrases like "You've got this!" at the end. Alright, time to structure all that into the summary.

**Your Tokyo Travel Plan Summary** 🗾  

---  
**✈️ Trip Overview**  
- **Destination**: Tokyo, Japan | **Duration**: 7 Days | **Budget**: $3000 USD  
- **Highlights**: Explore Asakusa, Shibuya Crossing, Meiji Shrine, and Tsukiji Market. Don’t miss the neon-lit Akihabara and historic Royal Palace!  

---  
**🌤 Weather & Best Time to Visit**  
- **Current Conditions**: Partly cloudy, 18°C (64°F), 65% humidity.  
- **Best Time**: March–May (spring blossoms) or Oct–Nov (cooler, fewer crowds). Your trip aligns perfectly with comfortable weather!  

---  
**🏨 Accommodation Estimate**  
- **Mid-range hotels**: ~$120/night (e.g., Ryokan, business hotels).  
- **Total**: ~$840 for 7 nights. Pro tip: Stay near Shibuya or Shinjuku for easy access to attractions.  

---  
**💵 Budget Breakdown**  
- **Total**: $3000 USD (~448,500 JPY) | **Daily Spend**: ~$428.57 (~6,420 JPY).  
  - **Daily Breakdown (USD)**:  
    - Accommodation: ~$120  
    - Food/Activities: ~$200  
    - Transport: ~$60  
    - Flex: ~$48.57  
  - **Cash Tip**: Carry yen for small shops/restaurants. ATMs are scarce!  

---  
**🎒 Packing Essentials**  
- Layers (t-shirts + light sweaters), comfortable shoes, light jacket, umbrella.  
- **Extras**: Suica/Pasmo card (preloaded!), cash (yen), and offline Google Translate app.  

---  
**💡 Top 3 Local Tips**  
1. **Transport**: Buy a Suica/Pasmo IC card for stress-free metro access.  
2. **Cash is King**: Many places still use cash—withdraw yen at convenience stores or post offices.  
3. **Etiquette**: Remove shoes in traditional restaurants, ryokans, and homes.  

---  
**✅ Quick Checklist Before You Go**  
- ✅ Passport with visa-free entry (if applicable).  
- ✅ Suica/Pasmo card (buy at Tokyo stations).  
- ✅ 448,500 JPY (~$3000) split as 50% cash + 50% card.  
- ✅ Adaptor (Japan uses Type A/B plugs).  
- ✅ Offline Google Translate (Japanese language pack).  

---  
Tokyo awaits with endless discovery—chase cherry blossoms, savor sushi, and embrace the blend of tradition and modernity. You’ve got this! 🗾✨  

*Safe travels and enjoy every moment!* 😊
============================================================
```
