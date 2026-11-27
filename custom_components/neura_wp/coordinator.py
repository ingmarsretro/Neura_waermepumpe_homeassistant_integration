"""Polling bridge between Home Assistant and the heat pump."""

from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any, Callable

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .client import NeuraClient, NeuraError
from .const import DOMAIN, SCAN_INTERVAL_SECONDS

_LOGGER = logging.getLogger(__name__)


class NeuraCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, client: NeuraClient):
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=SCAN_INTERVAL_SECONDS),
        )
        self.client = client

    def _snapshot(self) -> dict:
        try:
            return self.client.snapshot()
        except NeuraError:
            self.client.disconnect()
            return self.client.snapshot()

    async def _async_update_data(self) -> dict:
        try:
            return await self.hass.async_add_executor_job(self._snapshot)
        except NeuraError as err:
            raise UpdateFailed(str(err)) from err

    async def async_call(self, func: Callable[..., Any], *args: Any) -> Any:
        def _do():
            return func(*args)

        try:
            result = await self.hass.async_add_executor_job(_do)
        except NeuraError:
            raise
        await self.async_request_refresh()
        return result
