"""Digital inputs, controller outputs and overview flags, read only."""

from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .client import DIGITAL_IN_LABELS, DIGITAL_OUT_LABELS, _bool
from .const import INPUT_POINTS
from .entity import NeuraEntity

_INPUT_CLASS = {
    "high_pressure": BinarySensorDeviceClass.PROBLEM,
    "low_pressure": BinarySensorDeviceClass.PROBLEM,
    "tmax": BinarySensorDeviceClass.PROBLEM,
    "three_phases": BinarySensorDeviceClass.POWER,
}
_OUTPUT_CLASS = {
    "heatpump_2": BinarySensorDeviceClass.RUNNING,
    "heatpump": BinarySensorDeviceClass.RUNNING,
    "cylinder_pump": BinarySensorDeviceClass.RUNNING,
    "circulator_pump": BinarySensorDeviceClass.RUNNING,
    "heater_rod": BinarySensorDeviceClass.HEAT,
}


async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator = hass.data["neura_wp"][entry.entry_id]
    data = coordinator.data or {}
    inputs = [point["id"] for point in data.get("digital_in") or []] or list(INPUT_POINTS)
    outputs = [point["id"] for point in data.get("digital_out") or []] or [
        "heatpump_2",
        "cylinder_pump",
        "circulator_pump",
        "heater_rod",
    ]
    entities = [NeuraBinary(coordinator, ident.lower(), "di") for ident in inputs]
    entities.extend(NeuraBinary(coordinator, ident.lower(), "do") for ident in outputs)
    entities.append(NeuraCylinderEnabled(coordinator))
    entities.append(NeuraWriteAccess(coordinator))
    async_add_entities(entities)


class NeuraBinary(NeuraEntity, BinarySensorEntity):
    def __init__(self, coordinator, ident: str, kind: str):
        super().__init__(coordinator, f"{kind}-{ident}")
        self._ident = ident
        self._kind = kind
        if kind == "di":
            self._attr_name = DIGITAL_IN_LABELS.get(ident, ident)
            self._attr_device_class = _INPUT_CLASS.get(ident)
        else:
            self._attr_name = DIGITAL_OUT_LABELS.get(ident, ident)
            self._attr_device_class = _OUTPUT_CLASS.get(ident)

    @property
    def is_on(self):
        key = "digital_in" if self._kind == "di" else "digital_out"
        for point in (self.coordinator.data or {}).get(key) or []:
            if point["id"].lower() == self._ident and point["value"] is not None:
                return bool(point["value"])
        return None

    @property
    def available(self) -> bool:
        return super().available and self.is_on is not None


class NeuraCylinderEnabled(NeuraEntity, BinarySensorEntity):
    _attr_name = "Warmwasser aktiv"
    _attr_icon = "mdi:water-boiler"

    def __init__(self, coordinator):
        super().__init__(coordinator, "cylinder-enabled")

    @property
    def is_on(self):
        enabled = self._cylinder().get("enabled")
        if enabled is not None:
            return bool(enabled)
        return _bool(self._config().get("neura.cylinder.enable"))


class NeuraWriteAccess(NeuraEntity, BinarySensorEntity):
    _attr_name = "Schreibzugriff"
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_icon = "mdi:key"

    def __init__(self, coordinator):
        super().__init__(coordinator, "privileged")

    @property
    def is_on(self):
        return bool((self.coordinator.data or {}).get("privileged"))
