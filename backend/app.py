"""
backend/app.py  —  The API Gateway
==================================

One authenticated, accountable interface to the back-end services (Chapter 45).
Robots, the front-end surfaces, and developers all interact with the back end through
this single API. Every request is authenticated, authorised, and logged, and its
messages are the schemas of the series (see schemas/).

Run with:   python3 -m backend.app        (serves API + static front ends on :8000)
       or:   uvicorn backend.app:app --reload

Requires fastapi + uvicorn (see requirements.txt). The pure-Python examples/ do not
need this — they exercise the same components in-process.
"""
from __future__ import annotations
import os

try:
    from fastapi import FastAPI, Depends, HTTPException
    from fastapi.staticfiles import StaticFiles
    from fastapi.responses import RedirectResponse
    from pydantic import BaseModel
except ImportError:  # pragma: no cover
    raise SystemExit(
        "This module needs fastapi + uvicorn. Install with `pip install -r requirements.txt`, "
        "or run the pure-Python examples/ to see the system work without any dependencies."
    )

from platform.marketplace import Marketplace
from backend.services import TrustService, ProvenanceService, FleetService, ModelRegistry

# --- wire up the services (in-memory for the scaffold) ---
trust = TrustService()
provenance = ProvenanceService()
fleet = FleetService()
registry = ModelRegistry()
market = Marketplace(trust=trust)

app = FastAPI(title="Self-Teaching Humanoid Platform API", version="1.0")


# --- a stand-in for real authentication (every call is 'authed' + logged) ---
def auth() -> str:
    # A real gateway verifies strong credentials and scopes here.
    return "authenticated-caller"


# --- health ---
@app.get("/v1/health")
def health():
    return {"status": "ok", "service": "platform-api"}


# --- teaching (studio) ---
class Contribution(BaseModel):
    teacher: str
    skill: str
    modality: str
    consent: str = "training-only"


@app.post("/v1/contributions")
def submit_contribution(c: Contribution, who: str = Depends(auth)):
    provenance.record("teaching_contribution", teacher=c.teacher, skill=c.skill,
                      modality=c.modality, consent=c.consent)
    return {"status": "accepted", "skill": c.skill}


# --- marketplace ---
@app.get("/v1/skills")
def discover_skills(needs: str = "", who: str = Depends(auth)):
    return {"skills": market.discover(needs)}


@app.post("/v1/skills/{skill_id}/recall")
def recall_skill(skill_id: str, who: str = Depends(auth)):
    affected = provenance.robots_with(skill_id)
    for rid in affected:
        fleet.halt(rid)                      # contain first
    result = trust.recall(skill_id)          # then withdraw across the ecosystem
    return {**result, "affected_robots": affected}


# --- fleet (operator) ---
@app.get("/v1/fleet")
def fleet_status(who: str = Depends(auth)):
    return {"fleet": fleet.status()}


@app.post("/v1/fleet/halt")
def fleet_halt(robot_id: str | None = None, who: str = Depends(auth)):
    return fleet.halt(robot_id) if robot_id else fleet.halt_all()


# --- provenance (accountability) ---
@app.get("/v1/provenance")
def provenance_log(who: str = Depends(auth)):
    return {"records": provenance.all()}


# --- serve the static front-end surfaces ---
_here = os.path.dirname(__file__)
_frontend = os.path.join(_here, "..", "frontend")
if os.path.isdir(_frontend):
    app.mount("/studio", StaticFiles(directory=os.path.join(_frontend, "studio"), html=True), name="studio")
    app.mount("/market", StaticFiles(directory=os.path.join(_frontend, "marketplace"), html=True), name="market")
    app.mount("/fleet-ui", StaticFiles(directory=os.path.join(_frontend, "dashboard"), html=True), name="fleet-ui")


@app.get("/")
def index():
    return {
        "message": "Self-Teaching Humanoid Platform API",
        "surfaces": {"studio": "/studio", "marketplace": "/market", "dashboard": "/fleet-ui"},
        "docs": "/docs",
    }


if __name__ == "__main__":
    try:
        import uvicorn
    except ImportError:  # pragma: no cover
        raise SystemExit("Install uvicorn: pip install -r requirements.txt")
    uvicorn.run(app, host="0.0.0.0", port=8000)
