"""Heat-curve numbers and Handbetrieb setpoints the original panel also edits."""

from __future__ import annotations

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.const import PERCENTAGE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .client import NeuraError, _number
from .const import MANUAL_NUMBERS, NUMBER_SETTINGS
from .entity import NeuraEntity


async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator = hass.data["neura_wp"][entry.entry_id]
    entities = [
        NeuraSetting(coordinator, key, name, minimum, maximum, step, suffix)
        for key, name, minimum, maximum, step, suffix in NUMBER_SETTINGS
    ]
    entities.extend(
        NeuraManualNumber(coordinator, key, name, minimum, maximum, step, suffix)
        for key, name, minimum, maximum, step, suffix in MANUAL_NUMBERS
    )
    async_add_entities(entities)


class NeuraSetting(NeuraEntity, NumberEntity):
    _attr_mode = NumberMode.BOX

    def __init__(self, coordinator, key, name, minimum, maximum, step, suffix):
        super().__init__(coordinator, suffix)
        self._key = key
        self._attr_name = name
        self._attr_native_min_value = minimum
        self._attr_native_max_value = maximum
        self._attr_native_step = step

    @property
    def native_value(self):
        return _number(self._config().get(self._key))

    async def async_set_native_value(self, value: float) -> None:
        try:
            await self.coordinator.async_call(self.coordinator.client.set_value, self._key, float(value))
        except NeuraError:
            raise


class NeuraManualNumber(NeuraSetting):
    def __init__(self, coordinator, key, name, minimum, maximum, step, suffix):
        super().__init__(coordinator, key, name, minimum, maximum, step, suffix)
        if key.endswith("temporary_temperature"):
            self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
            self._attr_icon = "mdi:thermometer-water"
        else:
            self._attr_native_unit_of_measurement = PERCENTAGE
            self._attr_icon = "mdi:sine-wave"

    @property
    def available(self) -> bool:
        return super().available and self._key in self._config()
