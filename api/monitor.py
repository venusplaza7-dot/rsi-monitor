"""
RSI Monitor - Wraps any AI agent and logs all RSI attempts
This is what CEOs said they need: third-party auditing
"""
from typing import List, Dict, Any, Callable
from datetime import datetime
import json
from detector import RSIDetector, RiskLevel, Detection
from rich.console import Console
from rich.table import Table

console = Console()

class RSIMonitor:
    def __init__(self, agent_id: str = "unknown-agent", log_file: str = "rsi_log.jsonl"):
        self.agent_id = agent_id
        self.detector = RSIDetector()
        self.log_file = log_file
        self.all_detections: List[Detection] = []
        self.session_start = datetime.utcnow()
        
    def audit_text(self, source: str, content: str) -> List[Detection]:
        """Audit any text output from agent"""
        detections = self.detector.scan(content)
        
        for d in detections:
            self.all_detections.append(d)
            self._log_detection(source, d, content)
            self._alert(d, source)
            
        return detections
    
    def audit_tool_call(self, tool_name: str, tool_input: Dict, tool_output: str = "") -> List[Detection]:
        """Audit tool calls - this is where July HF hack was caught"""
        combined = f"{tool_name} {json.dumps(tool_input)} {tool_output}"
        return self.audit_text(f"tool:{tool_name}", combined)
    
    def audit_file_write(self, filepath: str, content: str) -> List[Detection]:
        """Special audit for file writes - critical for self-modification"""
        combined = f"WRITE FILE: {filepath}\n{content}"
        detections = self.detector.scan(combined)
        
        # File writes to own code are auto-CRITICAL
        if any(x in filepath.lower() for x in ["agent", "self", "model", "system", "prompt"]):
            if detections:
                for d in detections:
                    d.risk = RiskLevel.CRITICAL
                    d.score = 100
        
        for d in detections:
            self.all_detections.append(d)
            self._log_detection(f"file_write:{filepath}", d, content)
            self._alert(d, f"file_write:{filepath}")
            
        return detections
    
    def wrap_llm_call(self, llm_func: Callable) -> Callable:
        """Wrap any LLM call (OpenAI, Anthropic) to auto-audit"""
        def wrapped(*args, **kwargs):
            result = llm_func(*args, **kwargs)
            # Extract text from result (handles both OpenAI and Anthropic formats)
            text = ""
            if isinstance(result, str):
                text = result
            elif hasattr(result, 'content'):
                text = str(result.content)
            elif isinstance(result, dict):
                text = json.dumps(result)
            
            self.audit_text("llm_output", text)
            return result
        return wrapped
    
    def get_report(self) -> Dict:
        risk_data = self.detector.calculate_overall_risk(self.all_detections)
        
        # Group by category
        by_category = {}
        for d in self.all_detections:
            if d.category not in by_category:
                by_category[d.category] = []
            by_category[d.category].append(d)
        
        return {
            "agent_id": self.agent_id,
            "session_start": self.session_start.isoformat(),
            "session_end": datetime.utcnow().isoformat(),
            "overall_risk": risk_data["level"].value,
            "risk_score": risk_data["score"],
            "total_detections": len(self.all_detections),
            "by_category": {k: len(v) for k, v in by_category.items()},
            "detections": [
                {
                    "timestamp": d.timestamp,
                    "risk": d.risk.value,
                    "category": d.category,
                    "explanation": d.explanation,
                    "snippet": d.content_snippet,
                    "score": d.score
                }
                for d in self.all_detections
            ]
        }
    
    def print_report(self):
        report = self.get_report()
        
        console.print(f"\n[bold]RSI Monitor Report - {report['agent_id']}[/bold]")
        console.print(f"Session: {report['session_start']} -> {report['session_end']}")
        
        color_map = {
            "green": "green",
            "yellow": "yellow", 
            "red": "red",
            "critical": "bold red"
        }
        
        console.print(f"Overall Risk: [{color_map[report['overall_risk']]}]{report['overall_risk'].upper()} ({report['risk_score']}/100)[/]")
        console.print(f"Total Detections: {report['total_detections']}\n")
        
        if report["detections"]:
            table = Table(title="Detections")
            table.add_column("Time", style="dim")
            table.add_column("Risk")
            table.add_column("Category")
            table.add_column("Explanation")
            table.add_column("Score")
            
            for d in report["detections"]:
                table.add_row(
                    d["timestamp"][-12:],
                    d["risk"],
                    d["category"],
                    d["explanation"][:60],
                    str(d["score"])
                )
            console.print(table)
        else:
            console.print("[green]No RSI patterns detected - clean run[/green]")
    
    def export_json(self, path: str = None):
        path = path or f"rsi_report_{self.agent_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        with open(path, 'w') as f:
            json.dump(self.get_report(), f, indent=2)
        console.print(f"\nReport exported to: {path}")
        return path
    
    def _log_detection(self, source: str, detection: Detection, full_content: str):
        with open(self.log_file, 'a') as f:
            log_entry = {
                "timestamp": detection.timestamp,
                "agent_id": self.agent_id,
                "source": source,
                "detection": {
                    "risk": detection.risk.value,
                    "category": detection.category,
                    "pattern": detection.pattern_matched,
                    "explanation": detection.explanation,
                    "score": detection.score,
                    "snippet": detection.content_snippet
                }
            }
            f.write(json.dumps(log_entry) + "\n")
    
    def _alert(self, detection: Detection, source: str):
        if detection.risk in [RiskLevel.RED, RiskLevel.CRITICAL]:
            console.print(f"\n[bold red]🚨 RSI ALERT [{detection.risk.value.upper()}] - {detection.category}[/]")
            console.print(f"[red]Source: {source}[/red]")
            console.print(f"[red]Explanation: {detection.explanation}[/red]")
            console.print(f"[dim]Snippet: {detection.content_snippet[:200]}[/dim]\n")


