"""Heating circuit. The target is the heat-curve start flow temperature."""

from __future__ import annotations

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACAction,
    HVACMode,
)
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .client import NeuraError
from .entity import NeuraEntity


async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator = hass.data["neura_wp"][entry.entry_id]
    async_add_entities([NeuraClimate(coordinator)])


class NeuraClimate(NeuraEntity, ClimateEntity):
    _attr_name = "Heizkurve"
    _attr_hvac_modes = [HVACMode.HEAT]
    _attr_supported_features = ClimateEntityFeature.TARGET_TEMPERATURE
    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_min_temp = 15
    _attr_max_temp = 50
    _attr_target_temperature_step = 0.5

    def __init__(self, coordinator):
        super().__init__(coordinator, "climate")

    @property
    def hvac_mode(self) -> HVACMode:
        return HVACMode.HEAT

    @property
    def hvac_action(self) -> HVACAction:
        if self._heating().get("running"):
            return HVACAction.HEATING
        return HVACAction.IDLE

    @property
    def current_temperature(self):
        heating = self._heating()
        return heating.get("flow") if heating.get("flow") is not None else heating.get("current")

    @property
    def target_temperature(self):
        return self._heating().get("target")

    @property
    def extra_state_attributes(self):
        heating = self._heating()
        return {
            "outdoor": heating.get("outdoor"),
            "room": heating.get("room"),
            "holiday": heating.get("holiday"),
            "target_key": heating.get("target_key"),
            "slope": heating.get("slope"),
            "curve": heating.get("curve"),
        }

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """The controller has no off switch here. Heat stays selected."""
        return

    async def async_set_temperature(self, **kwargs) -> None:
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is None:
            return
        try:
            await self.coordinator.async_call(self.coordinator.client.set_heating_target, float(temperature))
        except NeuraError:
            raise
