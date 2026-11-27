"""Shared device info."""

from __future__ import annotations

from typing import Any

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import NeuraCoordinator


class NeuraEntity(CoordinatorEntity[NeuraCoordinator]):
    _attr_has_entity_name = True

    def __init__(self, coordinator: NeuraCoordinator, unique_suffix: str):
        super().__init__(coordinator)
        host = coordinator.client.host
        self._attr_unique_id = f"{host}-{unique_suffix}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, host)},
            name="Neura Wärmepumpe",
            manufacturer="Neura",
            model="EUS",
            configuration_url=f"http://{host}/neura/mobile",
        )

    @property
    def available(self) -> bool:
        return super().available and bool(self.coordinator.data)

    def _config(self) -> dict[str, Any]:
        return (self.coordinator.data or {}).get("config") or {}

    def _heating(self) -> dict[str, Any]:
        return (self.coordinator.data or {}).get("heating") or {}

    def _cylinder(self) -> dict[str, Any]:
        return (self.coordinator.data or {}).get("cylinder") or {}
