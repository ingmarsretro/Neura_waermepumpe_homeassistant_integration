"""Domestic hot water. Writes the first cylinder time-window temperature."""

from __future__ import annotations

from homeassistant.components.water_heater import (
    WaterHeaterEntity,
    WaterHeaterEntityFeature,
)
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .client import NeuraError
from .entity import NeuraEntity


async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator = hass.data["neura_wp"][entry.entry_id]
    async_add_entities([NeuraCylinder(coordinator)])


class NeuraCylinder(NeuraEntity, WaterHeaterEntity):
    _attr_name = "Warmwasser"
    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_supported_features = WaterHeaterEntityFeature.TARGET_TEMPERATURE
    _attr_operation_list = ["Zeitfenster"]
    _attr_min_temp = 30
    _attr_max_temp = 60

    def __init__(self, coordinator):
        super().__init__(coordinator, "cylinder")

    @property
    def current_operation(self):
        return "Zeitfenster"

    @property
    def current_temperature(self):
        return self._cylinder().get("current")

    @property
    def target_temperature(self):
        return self._cylinder().get("target")

    @property
    def extra_state_attributes(self):
        cylinder = self._cylinder()
        return {
            "enabled": cylinder.get("enabled"),
            "running": cylinder.get("running"),
            "target_key": cylinder.get("target_key"),
        }

    async def async_set_temperature(self, **kwargs) -> None:
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is None:
            return
        try:
            await self.coordinator.async_call(self.coordinator.client.set_cylinder_target, float(temperature))
        except NeuraError:
            raise

    async def async_set_operation_mode(self, operation_mode: str) -> None:
        return
