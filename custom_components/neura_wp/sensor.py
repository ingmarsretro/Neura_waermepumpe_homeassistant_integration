"""Temperatures, pressures, operating hours and overview setpoints."""

from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import UnitOfPressure, UnitOfTemperature, UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .client import ANALOG_LABELS, _number
from .const import HOUR_SENSORS, OVERVIEW_SENSORS, PRESSURE_POINTS
from .entity import NeuraEntity


async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator = hass.data["neura_wp"][entry.entry_id]
    analogs = (coordinator.data or {}).get("analogs") or []
    found = [point["id"] for point in analogs]
    if not found:
        found = ["flow", "return", "room", "cylinder", "comp_in", "comp_out", "screed"]
    entities = []
    for ident in found:
        entities.append(
            NeuraAnalogSensor(coordinator, ident, pressure=ident.lower() in PRESSURE_POINTS)
        )
    entities.extend(NeuraHourSensor(coordinator, key, name, suffix) for key, name, suffix in HOUR_SENSORS)
    entities.extend(
        NeuraConfigSensor(coordinator, key, name, suffix) for key, name, suffix in OVERVIEW_SENSORS
    )
    entities.append(NeuraFaultSensor(coordinator))
    entities.append(NeuraProgramsSensor(coordinator))
    async_add_entities(entities)


class NeuraAnalogSensor(NeuraEntity, SensorEntity):
    def __init__(self, coordinator, ident: str, pressure: bool):
        super().__init__(coordinator, f"ai-{ident.lower()}")
        self._ident = ident.lower()
        self._attr_name = ANALOG_LABELS.get(self._ident, ident)
        if pressure:
            self._attr_device_class = SensorDeviceClass.PRESSURE
            self._attr_native_unit_of_measurement = UnitOfPressure.BAR
        else:
            self._attr_device_class = SensorDeviceClass.TEMPERATURE
            self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self):
        for point in (self.coordinator.data or {}).get("analogs") or []:
            if point["id"].lower() == self._ident:
                return point["value"]
        return None

    @property
    def available(self) -> bool:
        return super().available and self.native_value is not None


class NeuraHourSensor(NeuraEntity, SensorEntity):
    _attr_device_class = SensorDeviceClass.DURATION
    _attr_native_unit_of_measurement = UnitOfTime.HOURS
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator, key: str, name: str, suffix: str):
        super().__init__(coordinator, suffix)
        self._key = key
        self._attr_name = name

    @property
    def native_value(self):
        return _number(self._config().get(self._key))

    @property
    def available(self) -> bool:
        return super().available and self.native_value is not None


class NeuraConfigSensor(NeuraEntity, SensorEntity):
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator, key: str, name: str, suffix: str):
        super().__init__(coordinator, suffix)
        self._key = key
        self._attr_name = name

    @property
    def native_value(self):
        return _number(self._config().get(self._key))

    @property
    def available(self) -> bool:
        return super().available and self.native_value is not None


class NeuraFaultSensor(NeuraEntity, SensorEntity):
    _attr_name = "Letzter Fehler"
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_icon = "mdi:alert-circle-outline"

    def __init__(self, coordinator):
        super().__init__(coordinator, "last-error")

    @property
    def native_value(self):
        error = (self.coordinator.data or {}).get("last_error")
        if not error:
            return "keiner"
        if isinstance(error, dict):
            if error.get("historic"):
                return "keiner"
            return str(error.get("text") or error.get("label") or error.get("code") or "keiner")[:255]
        return str(error)[:255]

    @property
    def extra_state_attributes(self):
        error = (self.coordinator.data or {}).get("last_error")
        if not isinstance(error, dict):
            return {}
        return {
            "code": error.get("code"),
            "when": error.get("when"),
            "historic": error.get("historic"),
            "log": error.get("text"),
        }


class NeuraProgramsSensor(NeuraEntity, SensorEntity):
    _attr_name = "Zeitprogramme"
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_icon = "mdi:calendar-clock"

    def __init__(self, coordinator):
        super().__init__(coordinator, "timeprograms")

    @property
    def native_value(self):
        programs = (self.coordinator.data or {}).get("timeprograms") or []
        return len(programs) if isinstance(programs, list) else 0

    @property
    def extra_state_attributes(self):
        return {"programs": (self.coordinator.data or {}).get("timeprograms") or []}
