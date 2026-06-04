# JavaScript Routing Architecture & Client-Side Engine — agent.md ⚙️🧠

Welcome to the internal technical documentation for Team PRISM. This file outlines the design, programmatic architecture, and client-side routing strategy powering the **Before You Go Assistant** using pure JavaScript (Vanilla JS / Fetch API) and a Flask backend.

---

## 🛠️ System Architecture Overview

Our system utilizes a **Deterministic Rule-Based Routing Architecture**. Instead of relying on an LLM (which can introduce latency and hallucinate strict document rules), our system pairs a responsive JavaScript engine with targeted Flask backend routes. 

```text
+-------------------------------------------------------------------------+
|                  User Interface: Dropdown / Selection                   |
|       [ Passport ]   [ Income Certificate ]   [ Ration Card ]  etc.      |
+-------------------------------------------------------------------------+
                                     |
                                     v (User clicks/selects a service)
+-------------------------------------------------------------------------+
|                     JavaScript Event & Fetch Handler                    |
|  - Captures the exact service token selected by the user.               |
|  - Maps choice to the unique Python backend endpoint (e.g., `/api/data`) |
|  - Dispatches an asynchronous HTTP fetch() request to the server.        |
+-------------------------------------------------------------------------+
                                     |
                                     v (Asynchronous JSON Request with Service Key)
+-------------------------------------------------------------------------+
|                    Flask Backend Controller (`app.py`)                  |
|  - Listens at endpoints for incoming service key requests.              |
|  - Matches keys against internal Python dictionaries/data modules.       |
|  - Packages requirements, pricing, schedules, and pitfall safety lists.  |
+-------------------------------------------------------------------------+
                                     |
                                     v (Structured JSON Payload Response)
+-------------------------------------------------------------------------+
|                     JavaScript DOM Update Engine                       |
|  - Parses the incoming structured data containing the 4 core pillars.  |
|  - Dynamically builds and updates the HTML panels instantly.            |
|  - Renders content to the browser viewport without a page reload.      |
+-------------------------------------------------------------------------+
                                     |
                                     v (Immediate Output)
+-------------------------------------------------------------------------+
|                         Live UI Output Blocks                           |
|  1. Documents Needed   2. Exact Fees   3. Estimated Time   4. Pitfalls  |
+-------------------------------------------------------------------------+

---

## Routing Strategy

To ensure deterministic, highly reliable, and zero-latency execution during our 2-day hackathon, the application bypasses external network API calls entirely. The JavaScript engine handles intent delivery programmatically.

### The Routing Matrix

When a user selects or searches for a service, JavaScript map functions or conditional routers instantly process the request against the following baseline service paths managed by the Flask controller:

* `/services/passport_new` (Fresh applications)
* `/services/passport_renew` (Expired passports)
* `/services/ration_card_new` (Food/ration cards)
* `/services/ration_card_correction` (Name, address, or spelling updates)
* `/services/income_certificate` (State income evaluation proofs)

#### CRITICAL APPLICATION RULES:

1. **Zero Hallucination:** Rules are explicitly coded. The user receives exact, legally sound paperwork checklists every single time.
2. **Asynchronous DOM Manipulation:** No full page refreshes. JavaScript catches user choices and updates the viewport instantly.
3. **Fail-Safe Processing:** If a user searches for an unmapped keyword, a catch-all route elegantly serves a unified directory alternative instead of breaking.

---

## Application Execution Pipelines

### Flow A: Asynchronous Request-Response (The Ideal Path)

* **Input:** User interacts with the UI: *"My kid was just born, how do I get him a ration card?"*
* **Engine Processing:** JavaScript captures the event, maps the intent to the food card registration identifier, and fires a `fetch()` request or local state transition for `ration_card_new`.
* **Data Fetching:** The Flask backend serves the verified dataset for that exact route, returning a clean package back to the frontend.
* **UI Render:** JavaScript receives the backend payload and cleanly overwrites the checklist container with zero lag.

### Flow B: Fallback Directory (The Exception Path)

If a user requests or searches for a valid government service that falls outside Team PRISM's primary pre-mapped modules (e.g., *"Driving License"*):

* **Input:** User types or requests: *"What do I bring for a motorcycle driving test?"*
* **Route Validation:** The application detects that an explicit isolated route for that exact parameter is not active.
* **Fallback Resolution:** Instead of failing, the client-side engine catches the unmapped request and gracefully renders an interactive master dashboard menu. This guides the user securely back to verified workflows rather than showing a raw error page.

---

## Guardrails & Performance Parameters

To ensure the system remains completely bulletproof under judging pressure, Team PRISM implemented the following architecture guardrails:

* **Instantaneous Latency (0.0ms API Overhead):** By eliminating external REST APIs (like Gemini), the application avoids token limits, network throttling, or API key expiration issues, making it 100% stable during live presentations.
* **Input Sanitization Middleware:** JavaScript intercepts search variables, formatting them safely into uniform strings before interacting with Flask route endpoints. This prevents malicious string execution or app crashes.
* **Modular Cleanliness:** Frontend templates and backend controllers are distinct. Developers can add new services simply by appending a new function inside `app.py` and updating the JavaScript event listeners.

---

## Project Status

**Completed & Optimized.** Team PRISM has effectively eliminated the risks of third-party API dependencies by building a robust, high-performance web architecture driven entirely by native Python and JavaScript.

```

```