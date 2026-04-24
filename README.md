# 🌍 AI Travel Budget Planner — Multi-Agent MCP Application

A multi-agent AI travel planning app built with **Model Context Protocol (MCP)**, **LangChain**, and **Groq LLM**.

It demonstrates how specialized agents can collaborate across multiple MCP servers to produce a consolidated, user-friendly travel plan.

---

## 📌 What This App Does

Given trip inputs like destination, budget, and duration, the app:

1. Collects destination research (weather, local tips, packing, accommodation)
2. Computes budget/currency insights
3. Synthesizes both reports into one final travel plan

Example prompt:

> "Plan a 7-day trip to Tokyo with a $3,000 budget."

---

## 🗂️ Project Structure

```text
MCP_App/
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

---

## 🤖 Agent Responsibilities

| Agent | Module | MCP Tools | Responsibility |
|---|---|---|---|
| Travel Research Agent | `agents/travel_agent.py` | `get_weather`, `get_climate_type`, `get_destination_info`, `get_packing_list`, `estimate_accommodation_cost` | Destination/weather research and stay guidance |
| Finance Agent | `agents/finance_agent.py` | `usd_to_currency`, `get_daily_budget`, `add`, `multiply` | Budget conversion, daily budget, arithmetic verification |
| Orchestrator Agent | `agents/orchestrator.py` | *(none)* | Merges specialist reports into a single final plan |

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

## 🔄 Execution Flow (Multi-Agent)

1. `multi_agent_multi_mcp_client.py` calls `plan_trip(destination, budget_usd, num_days)`
2. `utils.display.print_banner()` prints a trip header
3. `agents/travel_agent.py` returns a travel research report
4. `agents/finance_agent.py` returns a finance report
5. `agents/orchestrator.py` synthesizes both into the final plan
6. `utils.display.print_plan()` prints final output

---

## 🧩 Key Configuration

In `config/settings.py`:
- `get_llm()` builds a shared `ChatGroq` client
- `get_server_configs()` defines MCP transport config for all servers
- `CURRENCY_MAP` maps known destinations to local currency (fallback in client logic: `EUR`)

Current mapped destinations:
- `tokyo -> JPY`
- `paris -> EUR`
- `new york -> USD`
- `bali -> IDR`

---

## ➕ Extend the Project

### Add a new MCP server

1. Create a new server file in `servers/`.
2. Add its config in `config/settings.py` (`get_server_configs`).
3. Wire it into the relevant agent module in `agents/`.

### Add a new destination

Update the relevant dictionaries/constants in:
- `servers/weather_server.py`
- `servers/travel_tips_server.py`
- `config/settings.py` (`CURRENCY_MAP`)

---

## 🛠️ Troubleshooting

- `GROQ_API_KEY not set`:
  - Ensure `.env` exists and contains `GROQ_API_KEY=...`.
- Weather server connection issues:
  - Start `python servers/weather_server.py` first.
- Port conflict on 8000:
  - Stop the process using port 8000, then restart weather server.
- Import/dependency errors:
  - Reinstall dependencies from `requirements.txt` or run `uv sync`.

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
Processing request of type ListToolsRequest
Processing request of type CallToolRequest
Processing request of type CallToolRequest
Processing request of type ListToolsRequest
Processing request of type ListToolsRequest

✅ Travel Research Agent completed. Report:
Here’s your Tokyo trip summary:  

**1. Current Weather**  
🌤 Partly Cloudy | 18°C / 64°F | Humidity: 65%  

**2. Travel Info**  
📍 **Destination**: Tokyo, Japan  
- **Language**: Japanese  
- **Currency**: JPY (Japanese Yen)  
- **Visa**: Visa-free for most countries (up to 90 days)  
- **Best Season**: March–May (spring) or October–November (autumn)  
- **Tips**: Use Suica/Pasmo cards for transport, carry cash, remove shoes in traditional settings, and download offline Japanese translation.  

**3. Packing List**  
- Layers for temperate weather  
- Comfortable walking shoes  
- Light jacket  
- Umbrella (for potential rain)  

**4. Accommodation Estimate**  
- **Mid-range**: ~$120/night × 7 nights = **~$840 total**  

Safe travels! Let me know if you need more details. 😊
Processing request of type ListToolsRequest
Processing request of type ListToolsRequest
Processing request of type CallToolRequest
Processing request of type CallToolRequest
Processing request of type CallToolRequest
Processing request of type ListToolsRequest
Processing request of type ListToolsRequest
Processing request of type ListToolsRequest

✅ Finance Agent completed. Report:
Here's your travel budget analysis:

1. **USD to JPY Conversion**  
   $3000.00 USD = 448,500.00 JPY (exchange rate: 149.5)

2. **Daily Budget Calculation**  
   Total budget: $3000.00 | Trip duration: 7 days  
   Daily allowance: **$428.57/day**

3. **Verification (Daily × Days)**  
   Using the multiply tool: 428.57 × 7 = **$3000.00**  
   (Note: The earlier "2996" result used rounded values; precise calculation matches original budget)

Would you like help adjusting this for fees or currency fluctuations?

🤖 Orchestrator Agent synthesizing the final travel plan...

============================================================
  📋 YOUR PERSONALISED TRAVEL PLAN
============================================================
<think>
Okay, so the user wants a travel plan summary for a 7-day trip to Tokyo with a $3000 budget. Let me start by going through the provided research and finance reports to make sure I include all the necessary details.

First, the trip overview should mention the destination, duration, and maybe a fun fact or two about Tokyo to make it friendly. The current weather is partly cloudy at 18°C, so I should note that in the weather section. The best time to visit is mentioned as spring or autumn, so I'll highlight that March-May or October-November are ideal, and since they're visiting in a time that's not specified, maybe just mention the current weather as a reference.

For accommodation, the estimate is $120/night for mid-range, totaling $840. That's about 17,880 JPY. I need to convert that properly using the exchange rate given. Wait, the finance report says USD to JPY is 149.5, so $3000 equals 448,500 JPY. The daily budget is $428.57, which totals exactly $3000 when multiplied by 7 days. I should break down the budget into USD and JPY, maybe allocate the remaining $2160 (after accommodation) to other expenses like food, activities, transportation.

Packing essentials include layers, comfortable shoes, a light jacket, and an umbrella. That's straightforward. The top 3 local tips from the research are using Suica/Pasmo cards, carrying cash, and removing shoes in traditional settings. Also, the offline translation app is a good tip to add.

The quick checklist before departure should include things like passport, visa confirmation, travel insurance, Suica/Pasmo cards, packing list, and budget tracker. Let me make sure all the sections are covered and the numbers add up correctly.

Wait, the accommodation is $840, which is 120*7. Then the total budget is $3000, so the remaining $2160 is for other expenses. Converting the total budget to JPY is 448,500, so the daily budget in JPY would be 448,500 /7 = 64,071 per day. Let me check that calculation again. Yes, 428.57 USD per day is roughly 64,071 JPY daily. Should I mention that?

Also, the finance report mentions verifying the daily spend, so I should present that clearly. Make sure the budget breakdown is easy to understand, maybe in bullet points with both USD and JPY. The user might need to know how much they can spend each day in local currency.

I should also make the tone friendly and encouraging, using emojis where appropriate. Let me structure each section with the specified headings and ensure conciseness. Double-check that all the key points from the research and finance reports are included without adding any extra fluff. Finally, proofread for any errors and make sure the math checks out.
</think>

**🌸 Tokyo Travel Plan Summary**  

---

**✈️ Trip Overview**  
- **Destination**: Tokyo, Japan  
- **Duration**: 7 days  
- **Budget**: $3,000 USD (≈448,500 JPY)  

---

**🌤 Weather & Best Time to Visit**  
- **Current Conditions**: Partly cloudy, 18°C / 64°F, 65% humidity.  
- **Best Seasons**: Visit March–May (spring blossoms!) or October–November (cooler, fewer crowds).  

---

**🏨 Accommodation Estimate**  
- **Mid-range option**: ~$120/night (7 nights = **$840 total** / 17,880 JPY).  
- **Suggestion**: Stay in Shinjuku or Shibuya for easy access to attractions.  

---

**💵 Budget Breakdown**  
- **Total**: $3,000 USD (448,500 JPY).  
- **Daily Allowance**: $428.57 USD (~64,071 JPY/day).  
- **Allocation**:  
  - Accommodation: $840 ($120/night).  
  - Food/Transport/Activities: ~$300/day ($2,160 total).  

---

**🎒 Packing Essentials**  
- Layers for temperate weather.  
- Comfortable walking shoes.  
- Light jacket + umbrella (rain possible).  
- Suica/Pasmo card (for transit).  

---

**💡 Top 3 Local Tips**  
1. Use **Suica/Pasmo cards** for seamless public transport.  
2. Carry cash (JPY) – many smaller vendors don’t accept cards.  
3. **Remove shoes** in traditional settings (e.g., ryokans, some restaurants).  

---

**✅ Quick Checklist Before You Go**  
- ✅ Passport + visa confirmation (if required).  
- ✅ Travel insurance + emergency contacts.  
- ✅ Offline Japanese translation app (Google Translate!).  
- ✅ Pack light + check weather forecast.  
- ✅ Budget tracker (daily: ~$428 USD / 64k JPY).  

---

Safe travels and enjoy Tokyo’s blend of futuristic energy and traditional charm! Let me know if you need tweaks 😊
============================================================
```
