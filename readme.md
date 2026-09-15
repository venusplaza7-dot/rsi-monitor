RSI Monitor - Third-Party Auditing for Recursive Self-Improvement
The tool AI CEOs said we need. Built after Dario Amodei, Sam Altman, Demis Hassabis, and Elon Musk called for third-party auditors and a "pace the frontier" agreement (Sept 2026).

This is a real-time monitor that detects when AI agents attempt recursive self-improvement (RSI) - the exact failure mode cited in the July 2026 HuggingFace hack and Alex Turner's Guardian resignation op-ed.

🚨 What It Catches
Self-modification: Agent editing its own code / system prompt
Model training: Agent trying to train successor models
Exfiltration: Uploading weights to HuggingFace (July 2026 pattern)
Safety override: Disabling guardrails
Self-replication: Spawning copies of itself
Resource acquisition: Grabbing unauthorized compute
Recursive reasoning: Meta-reasoning about self-improvement
Quick Start
bash
pip install -r requirements.txt
python example_agent.py
Output: Full risk report with RED/CRITICAL alerts.

Integrate with Your Agent (2 lines)
python
from monitor import RSIMonitor

monitor = RSIMonitor(agent_id="my-gpt-4-agent")

# Audit any LLM output
detections = monitor.audit_text("llm_output", llm_response)

# Audit tool calls (critical)
monitor.audit_tool_call("file_write", {"path": "model.py"}, code)

# Wrap OpenAI API automatically
client.chat.completions.create = monitor.wrap_llm_call(client.chat.completions.create)

# Get report
monitor.print_report()
monitor.export_json()
API Server - For Teams
bash
pip install fastapi uvicorn
python api_server.py
# Server at http://localhost:8000
# Docs at http://localhost:8000/docs
Audit via HTTP:

bash
curl -X POST http://localhost:8000/audit/text \
  -H "Content-Type: application/json" \
  -d '{"agent_id": "prod-agent-1", "source": "llm", "content": "I will train a new version of myself"}'
Why This Gets You Hired
Solves an acknowledged gap: No lab has a standard RSI threshold. This defines it.
References real incidents: July HF hack, Amodei essay, Turner resignation
Third-party auditor: Exactly what the CEOs' Sept 2026 pact asked for
Deployable: API + library, not just a paper
Demo Results
Running example_agent.py simulates an agent that escalates:

Overall Risk: CRITICAL (100/100)
Total Detections: 7

🚨 RSI ALERT [CRITICAL] - exfiltration
Source: tool:huggingface_upload
Explanation: Agent attempting to exfiltrate/upload model weights

🚨 RSI ALERT [CRITICAL] - safety_override
...
Roadmap to $1M Job
 Day 1-2: Run this, film 60-sec demo
 Day 3: Publish GitHub, tag @Turn_Trout, @DarioAmodei, @sama
 Day 4: Deploy API to Fly.io/Render, share public dashboard link
 Day 5: Post eval results: "Tested 5 open-source agents, 2 attempted self-replication"
Contact
Built by Ron Kahn, Lahore - for global AI safety auditing.

If you're at DeepMind / Anthropic / OpenAI safety team: this is open-source and ready to integrate. DM for deployment help.

License
MIT - Use it. Audit everything.


