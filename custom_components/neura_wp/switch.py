"""Holiday mode and Handbetriebe. This does not stop the compressor by hand."""

from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .client import NeuraError, _bool
from .const import MANUAL_SWITCHES
from .entity import NeuraEntity


async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator = hass.data["neura_wp"][entry.entry_id]
    entities = [NeuraHolidaySwitch(coordinator)]
    entities.extend(
        NeuraConfigSwitch(coordinator, key, name, suffix, icon)
        for key, name, suffix, icon in MANUAL_SWITCHES
    )
    async_add_entities(entities)


class NeuraHolidaySwitch(NeuraEntity, SwitchEntity):
    _attr_name = "Urlaub"
    _attr_icon = "mdi:bag-suitcase"

    def __init__(self, coordinator):
        super().__init__(coordinator, "holiday")

    @property
    def is_on(self) -> bool:
        return bool(self._heating().get("holiday"))

    async def async_turn_on(self, **kwargs) -> None:
        await self._set(True)

    async def async_turn_off(self, **kwargs) -> None:
        await self._set(False)

    async def _set(self, active: bool) -> None:
        try:
            await self.coordinator.async_call(self.coordinator.client.set_holiday, active)
        except NeuraError:
            raise


class NeuraConfigSwitch(NeuraEntity, SwitchEntity):
    def __init__(self, coordinator, key: str, name: str, suffix: str, icon: str):
        super().__init__(coordinator, suffix)
        self._key = key
        self._attr_name = name
        self._attr_icon = icon

    @property
    def available(self) -> bool:
        return super().available and self._key in self._config()

    @property
    def is_on(self) -> bool:
        return bool(_bool(self._config().get(self._key)))

    async def async_turn_on(self, **kwargs) -> None:
        await self._set(True)

    async def async_turn_off(self, **kwargs) -> None:
        await self._set(False)

    async def _set(self, active: bool) -> None:
        try:
            await self.coordinator.async_call(self.coordinator.client.set_value, self._key, bool(active))
        except NeuraError:
            raise
