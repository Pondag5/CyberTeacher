"""
Risk level management for CTF and Story modes.
"""

from pydantic import BaseModel, Field


class RiskState(BaseModel):
    """Risk level and related methods."""
    
    risk_level: int = Field(default=0, ge=0, le=100)  # 0-100, increases on mistakes, decreases on success

    def increase_risk(self, amount: int = 10):
        """Increase risk level (on mistake/protection trigger)."""
        self.risk_level = min(100, self.risk_level + amount)

    def decrease_risk(self, amount: int = 5):
        """Decrease risk level (on success)."""
        self.risk_level = max(0, self.risk_level - amount)

    def reset_risk(self):
        """Reset risk level to zero."""
        self.risk_level = 0

    def get_risk_status(self) -> str:
        """Get textual risk status."""
        if self.risk_level < 20:
            return "🟢 Низкий"
        elif self.risk_level < 50:
            return "🟡 Умеренный"
        elif self.risk_level < 80:
            return "🟠 Высокий"
        else:
            return "🔴 Критический"

    model_config = {
        "validate_assignment": True
    }