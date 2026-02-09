import json
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, model_validator

class ClaimType(str, Enum):
    AUTO = "auto"
    PROPERTY = "property"
    INJURY = "injury"

class ExtractedFields(BaseModel):
    policy_number: Optional[str] = None
    policyholder_name: Optional[str] = None
    effective_dates: Optional[str] = None
    incident_date: Optional[str] = None
    incident_time: Optional[str] = None
    incident_location: Optional[str] = None
    incident_description: Optional[str] = None
    claimant: Optional[str] = None
    third_parties: List[str] = []
    asset_type: Optional[str] = None
    asset_id: Optional[str] = None
    estimated_damage: float = 0.0
    claim_type: Optional[ClaimType] = None
    initial_estimate: float = 0.0

class ClaimResponse(BaseModel):
    extractedFields: ExtractedFields
    missingFields: List[str] = []
    recommendedRoute: str = ""
    reasoning: str = ""

    @model_validator(mode="after")
    def apply_routing_rules(self) -> "ClaimResponse":
        fields = self.extractedFields
        reasons = []

        # 1. Logic: Identify Missing Mandatory Fields
        mandatory = {
            "policy_number": fields.policy_number,
            "policyholder_name": fields.policyholder_name,
            "incident_date": fields.incident_date,
            "claim_type": fields.claim_type
        }
        self.missingFields = [k for k, v in mandatory.items() if not v]
        
        if self.missingFields:
            self.recommendedRoute = "Manual Review"
            reasons.append(f"Missing mandatory fields: {', '.join(self.missingFields)}")

        # 2. Logic: Fraud/Investigation Flag
        fraud_keywords = ["fraud", "staged", "inconsistent", "suspicious"]
        desc = (fields.incident_description or "").lower()
        if any(word in desc for word in fraud_keywords):
            self.recommendedRoute = "Investigation Flag"
            reasons.append("Potential fraud indicators detected in incident description.")

        # 3. Logic: Specialist Queue (Injury)
        elif fields.claim_type == ClaimType.INJURY:
            self.recommendedRoute = "Specialist Queue"
            reasons.append("Claim categorized as Injury; routing to specialist.")

        # 4. Logic: Fast-Track (Low Damage)
        elif not self.recommendedRoute:
            if fields.estimated_damage < 25000:
                self.recommendedRoute = "Fast-track"
                reasons.append(f"Damage estimate (${fields.estimated_damage}) is below the $25,000 threshold.")
            else:
                self.recommendedRoute = "Standard Workflow"
                reasons.append("High-value claim requires standard processing.")

        self.reasoning = " | ".join(reasons)
        return self
