"""
FastAPI Server - Real-time RSI Monitoring API
Deploy this and give CEOs a dashboard link
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from monitor import RSIMonitor
from detector import RSIDetector
import json
from datetime import datetime
import os

app = FastAPI(title="RSI Monitor API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for demo - use Redis/DB in prod
monitors: dict = {}
detector = RSIDetector()

class AuditRequest(BaseModel):
    agent_id: str
    source: str
    content: str

class ToolAuditRequest(BaseModel):
    agent_id: str
    tool_name: str
    tool_input: dict
    tool_output: Optional[str] = ""

class FileAuditRequest(BaseModel):
    agent_id: str
    filepath: str
    content: str

@app.get("/")
def root():
    return {
        "service": "RSI Monitor API",
        "version": "1.0.0",
        "description": "Third-party auditing for recursive self-improvement - as called for by Amodei, Altman, Hassabis, Musk",
        "endpoints": ["/audit/text", "/audit/tool", "/audit/file", "/report/{agent_id}", "/stats"]
    }

@app.post("/audit/text")
def audit_text(req: AuditRequest):
    if req.agent_id not in monitors:
        monitors[req.agent_id] = RSIMonitor(agent_id=req.agent_id)
    
    detections = monitors[req.agent_id].audit_text(req.source, req.content)
    
    return {
        "agent_id": req.agent_id,
        "detections_found": len(detections),
        "detections": [
            {
                "risk": d.risk.value,
                "category": d.category,
                "explanation": d.explanation,
                "score": d.score,
                "snippet": d.content_snippet
            } for d in detections
        ],
        "overall_risk": monitors[req.agent_id].detector.calculate_overall_risk(
            monitors[req.agent_id].all_detections
        )["level"].value
    }

@app.post("/audit/tool")
def audit_tool(req: ToolAuditRequest):
    if req.agent_id not in monitors:
        monitors[req.agent_id] = RSIMonitor(agent_id=req.agent_id)
    
    detections = monitors[req.agent_id].audit_tool_call(
        req.tool_name, req.tool_input, req.tool_output
    )
    
    return {
        "agent_id": req.agent_id,
        "detections_found": len(detections),
        "detections": [{"risk": d.risk.value, "category": d.category, "score": d.score} for d in detections]
    }

@app.post("/audit/file")
def audit_file(req: FileAuditRequest):
    if req.agent_id not in monitors:
        monitors[req.agent_id] = RSIMonitor(agent_id=req.agent_id)
    
    detections = monitors[req.agent_id].audit_file_write(req.filepath, req.content)
    
    return {
        "agent_id": req.agent_id,
        "detections_found": len(detections),
        "is_self_modification": any("agent" in req.filepath.lower() or "self" in req.filepath.lower() for _ in [1]),
        "detections": [{"risk": d.risk.value, "category": d.category} for d in detections]
    }

@app.get("/report/{agent_id}")
def get_report(agent_id: str):
    if agent_id not in monitors:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return monitors[agent_id].get_report()

@app.get("/stats")
def get_stats():
    total_agents = len(monitors)
    total_detections = sum(len(m.all_detections) for m in monitors.values())
    
    risk_counts = {"green": 0, "yellow": 0, "red": 0, "critical": 0}
    category_counts = {}
    
    for m in monitors.values():
        report = m.get_report()
        risk_counts[report["overall_risk"]] += 1
        for cat, count in report["by_category"].items():
            category_counts[cat] = category_counts.get(cat, 0) + count
    
    return {
        "total_agents_monitored": total_agents,
        "total_detections": total_detections,
        "risk_distribution": risk_counts,
        "category_distribution": category_counts,
        "generated_at": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

