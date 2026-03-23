from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List


@dataclass
class TraceEvent:
    timestamp: str
    router: str
    event: str
    details: Dict[str, Any]


class TraceLogger:
    def __init__(self) -> None:
        self.events: List[TraceEvent] = []

    def log(self, router: str, event: str, **details: Any) -> None:
        self.events.append(
            TraceEvent(
                timestamp=datetime.now(timezone.utc).isoformat(),
                router=router,
                event=event,
                details=details,
            )
        )

    def to_dict(self) -> List[Dict[str, Any]]:
        return [asdict(event) for event in self.events]
