Autonomous Insurance Claims Processing AgentAn intelligent, lightweight agent designed to automate the First Notice of Loss (FNOL) workflow. 
This agent extracts structured data from unstructured claim documents, validates mandatory information, identifies potential fraud, and routes claims to the appropriate department using a hybrid LLM-and-Logic approach.
 OverviewThis project solves the challenge of high-volume, low-complexity insurance claims by:Extracting 15+ key fields (Policy, Incident, Assets, Parties) from raw text.Validating data integrity (identifying missing mandatory fields).Reasoning through business rules to determine the optimal workflow.Formatting the result into a clean, system-ready JSON output.
 Technical StackLanguage: Python 3.10+AI Model: OpenAI GPT-4o-mini (chosen for speed and cost-efficiency)Data Validation: Pydantic (ensures 100% schema compliance)Environment: python-dotenv for secure API management🏗️ Project StructurePlaintextautonomous-claims-agent/
├── data/               # Sample FNOL documents (PDF/TXT)
├── src/
│   ├── agent.py        # Core Pydantic models & Routing Logic
│   └── processor.py    # LLM orchestration and data cleanup
├── main.py             # Entry point / CLI
├── requirements.txt    # Dependencies
├── .env.example        # Environment template
└── README.md           # Documentation
⚙️ Routing LogicThe agent follows a deterministic hierarchy to ensure safety and accuracy:TriggerResulting RouteMissing Mandatory FieldsManual ReviewFraud Keywords (e.g., "staged", "inconsistent")Investigation FlagClaim Type = InjurySpecialist QueueEstimated Damage < $25,000Fast-trackEstimated Damage > $25,000Standard Workflow🚦 Getting Started1. PrerequisitesEnsure you have an OpenAI API Key.2. InstallationBash# Clone the repository
git clone https://github.com/your-username/autonomous-claims-agent.git
cd autonomous-claims-agent

# Install dependencies
pip install -r requirements.txt
3. ConfigurationCreate a .env file in the root directory:BashOPENAI_API_KEY=your_actual_api_key_here
4. Running the AgentTo process the sample claims provided in the data/ folder:Bashpython main.py
📊 Sample Output FormatJSON{
  "extractedFields": {
    "policy_number": "POL-88291",
    "policyholder_name": "John Doe",
    "estimated_damage": 1200.50,
    "claim_type": "auto"
  },
  "missingFields": [],
  "recommendedRoute": "Fast-track",
  "reasoning": "Damage estimate ($1200.5) is below $25,000 threshold."
}
🧠 Approach & Design DecisionsHybrid Logic: Rather than asking the LLM to "decide" the route (which can hallucinate), the LLM is used strictly for extraction. The routing logic is handled by Python (Pydantic) to ensure 100% consistency with business rules.Schema Enforcement: By using Pydantic, the agent automatically fails or flags data if the "estimated_damage" isn't a number or "claim_type" is invalid.Auditability: Every decision includes a reasoning string, making the agent's "thought process" transparent to human adjusters.
