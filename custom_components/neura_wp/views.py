"""Serve the Neura web panel and JSON API from Home Assistant."""
from __future__ import annotations

import json
import logging

from aiohttp import web
from homeassistant.components.http import HomeAssistantView
from homeassistant.core import HomeAssistant

from .client import NeuraError
from .const import DOMAIN, PANEL_ICON, PANEL_RESOURCE, PANEL_TITLE, PANEL_URL_PATH
from .coordinator import NeuraCoordinator
from .panel import panel_html

_LOGGER = logging.getLogger(__name__)
_HTTP_FLAG = "_http"
_PANEL_FLAG = "_panel"


def hass_from(request) -> HomeAssistant:
    app = request.app
    hass = app.get("hass")
    if hass is not None:
        return hass
    for module in (
        "homeassistant.components.http",
        "homeassistant.components.http.const",
    ):
        try:
            key = __import__(module, fromlist=["KEY_HASS"]).KEY_HASS
            return app[key]
        except Exception:
            continue
    raise RuntimeError("hass missing from request")


def coordinator_from(hass: HomeAssistant) -> NeuraCoordinator | None:
    store = hass.data.get(DOMAIN) or {}
    for key, value in store.items():
        if str(key).startswith("_"):
            continue
        return value
    return None


def json_response(payload, status: int = 200) -> web.Response:
    try:
        body = json.dumps(payload, ensure_ascii=False, default=str)
    except Exception as exc:
        _LOGGER.exception("Neura JSON")
        body = json.dumps({"error": str(exc)}, ensure_ascii=False)
        status = 500
    return web.Response(body=body.encode("utf-8"), status=status, content_type="application/json")


def async_setup_http(hass: HomeAssistant) -> None:
    if hass.data.setdefault(DOMAIN, {}).get(_HTTP_FLAG):
        return
    hass.http.register_view(NeuraPanelView())
    hass.http.register_view(NeuraApiView())
    hass.data[DOMAIN][_HTTP_FLAG] = True


def async_register_panel(hass: HomeAssistant) -> None:
    from homeassistant.components import frontend

    store = hass.data.setdefault(DOMAIN, {})
    if store.get(_PANEL_FLAG):
        return
    try:
        kwargs = {
            "component_name": "iframe",
            "sidebar_title": PANEL_TITLE,
            "sidebar_icon": PANEL_ICON,
            "frontend_url_path": PANEL_URL_PATH,
            "config": {"url": PANEL_RESOURCE},
            "require_admin": False,
        }
        try:
            frontend.async_register_built_in_panel(hass, update=True, **kwargs)
        except TypeError:
            try:
                frontend.async_register_built_in_panel(hass, **kwargs)
            except ValueError:
                frontend.async_remove_panel(hass, PANEL_URL_PATH)
                frontend.async_register_built_in_panel(hass, **kwargs)
    except ValueError:
        _LOGGER.debug("Neura sidebar panel already registered")
    store[_PANEL_FLAG] = True


def async_unregister_panel(hass: HomeAssistant) -> None:
    store = hass.data.get(DOMAIN) or {}
    remaining = [key for key in store if not str(key).startswith("_")]
    if remaining or not store.get(_PANEL_FLAG):
        return
    from homeassistant.components import frontend

    try:
        frontend.async_remove_panel(hass, PANEL_URL_PATH)
    except (AttributeError, ValueError, KeyError):
        _LOGGER.debug("Neura sidebar panel was already gone")
    store[_PANEL_FLAG] = False


class NeuraPanelView(HomeAssistantView):
    """HTML for the sidebar iframe.

    Document loads in an iframe have no Bearer token, so this view is
    public. JSON under /api/neura_wp still requires a Home Assistant login.
    """

    url = PANEL_RESOURCE
    name = "neura_wp:panel"
    requires_auth = False

    async def get(self, request):
        try:
            html = panel_html()
        except OSError as exc:
            _LOGGER.exception("Neura panel HTML fehlt")
            html = (
                "<!DOCTYPE html><html lang='de'><body>"
                "<p>Neura-Seite nicht gefunden. Den Ordner www mitkopieren und Home Assistant neu starten.</p>"
                f"<pre>{exc}</pre></body></html>"
            )
        return web.Response(body=html.encode("utf-8"), content_type="text/html")


class NeuraApiView(HomeAssistantView):
    url = "/api/neura_wp/{action}"
    name = "api:neura_wp"
    requires_auth = True

    async def get(self, request, action):
        if action != "status":
            return json_response({"error": "unbekannt"}, 404)
        return await self._status(request)

    async def post(self, request, action):
        try:
            hass = hass_from(request)
        except Exception:
            _LOGGER.exception("Home Assistant request")
            return json_response({"error": "Home Assistant nicht erreichbar"}, 500)
        coordinator = coordinator_from(hass)
        if coordinator is None:
            return json_response({"error": "Noch nicht verbunden"}, 409)
        try:
            data = await request.json()
        except Exception:
            data = {}
        if not isinstance(data, dict):
            data = {}
        client = coordinator.client
        try:
            if action == "connect":
                await coordinator.async_request_refresh()
                return json_response(coordinator.data or {})
            if action == "status":
                return await self._status(request)
            if action == "heating":
                temperature = data.get("temperature")
                if temperature is None:
                    return json_response({"error": "Temperatur fehlt"}, 400)
                key = await coordinator.async_call(client.set_heating_target, float(temperature))
                return json_response({"ok": True, "key": key, **(coordinator.data or {})})
            if action == "cylinder":
                temperature = data.get("temperature")
                if temperature is None:
                    return json_response({"error": "Temperatur fehlt"}, 400)
                key = await coordinator.async_call(client.set_cylinder_target, float(temperature))
                return json_response({"ok": True, "key": key, **(coordinator.data or {})})
            if action == "holiday":
                await coordinator.async_call(client.set_holiday, bool(data.get("active")))
                return json_response(coordinator.data or {})
            if action == "config":
                key = str(data.get("key") or "")
                if not key.startswith("neura."):
                    return json_response({"error": "Nur neura.* Werte können gesetzt werden"}, 400)
                await coordinator.async_call(client.set_value, key, data.get("value"))
                return json_response(coordinator.data or {})
            if action == "user":
                if not client.privileged:
                    return json_response({"error": "Benutzerverwaltung braucht eine Anmeldung"}, 403)
                return await self._user(coordinator, data)
            if action == "power":
                if not client.privileged:
                    return json_response({"error": "Neustart braucht eine Anmeldung"}, 403)
                return await self._power(hass, client, data)
            return json_response({"error": "unbekannt"}, 404)
        except (TypeError, ValueError, KeyError):
            return json_response({"error": "Angaben unvollständig"}, 400)
        except NeuraError as exc:
            return json_response({"error": str(exc)}, 502)

    async def _status(self, request):
        try:
            hass = hass_from(request)
        except Exception:
            _LOGGER.exception("Home Assistant request")
            return json_response({"error": "Home Assistant nicht erreichbar"}, 500)
        coordinator = coordinator_from(hass)
        if coordinator is None:
            return json_response({"error": "Noch nicht verbunden"}, 409)
        if coordinator.data:
            return json_response(coordinator.data)
        last = getattr(coordinator, "last_exception", None)
        if last:
            return json_response({"error": str(last)}, 502)
        await coordinator.async_request_refresh()
        return json_response(coordinator.data or {})

    async def _user(self, coordinator: NeuraCoordinator, data: dict):
        client = coordinator.client
        action = str(data.get("action") or "")
        username = str(data.get("username") or "").strip()
        if action == "add":
            await coordinator.async_call(
                client.add_user,
                username,
                int(data.get("group") or 2),
                str(data.get("password") or ""),
                str(data.get("information") or ""),
            )
        elif action == "delete":
            await coordinator.async_call(client.delete_user, username)
        elif action == "password":
            await coordinator.async_call(client.set_user_password, username, str(data.get("password") or ""))
        elif action == "lock":
            await coordinator.async_call(client.set_user_locked, username, True)
        elif action == "unlock":
            await coordinator.async_call(client.set_user_locked, username, False)
        else:
            return json_response({"error": "Unbekannte Benutzeraktion"}, 400)
        return json_response(coordinator.data or {})

    async def _power(self, hass: HomeAssistant, client, data: dict):
        action = str(data.get("action") or "")
        if action == "shutdown":
            return json_response(
                {
                    "error": "Die XML-RPC-Schnittstelle kennt kein Herunterfahren des Rechners. "
                    "Im Original-WebDialog gibt es nur den Neustart der Regelung."
                },
                400,
            )
        if action != "restart":
            return json_response({"error": "Nur restart ist möglich"}, 400)
        await hass.async_add_executor_job(client.restart)
        return json_response({"ok": True, "message": "Neustart der Regelung ausgelöst."})
