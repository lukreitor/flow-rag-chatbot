from __future__ import annotations

from typing import Any, Dict

import httpx

from app.core.config import Settings, get_settings


class FlowClient:
    """HTTP client for CI&T Flow chat completions."""

    def __init__(self, settings: Settings | None = None):
        self._settings = settings or get_settings()

    def _headers(self) -> dict[str, str]:
        headers = {
            "FlowTenant": self._settings.flow_tenant,
            "FlowAgent": self._settings.flow_agent,
            "FlowAgentSecret": self._settings.flow_agent_secret,
            "Content-Type": "application/json",
        }
        if self._settings.flow_channel:
            headers["FlowChannel"] = self._settings.flow_channel
        return headers

    def chat_completion(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self._settings.flow_base_url}/openai/chat/completions"
        with httpx.Client(timeout=30.0) as client:
            response = client.post(url, headers=self._headers(), json=payload)
            response.raise_for_status()
            return response.json()
