"""XML-RPC client for a Neura WebDialog / biF heat pump.

The controller stays in charge of CAN, the TRS11 room terminal and the
compressor logic. This client only reads state and writes the same
configuration values the original web interface writes.
"""
from __future__ import annotations

import base64
import hashlib
import threading
import xmlrpc.client
from datetime import datetime
from typing import Any
from urllib.parse import urlparse

CALL_TIMEOUT = 12


class _TimeoutTransport(xmlrpc.client.Transport):
    def __init__(self, timeout):
        super().__init__()
        self._timeout = timeout

    def make_connection(self, host):
        connection = super().make_connection(host)
        connection.timeout = self._timeout
        return connection

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms

try:
    from cryptography.hazmat.decrepit.ciphers.modes import CFB
except ImportError:  # cryptography before the CFB move
    from cryptography.hazmat.primitives.ciphers.modes import CFB

try:
    from .menus import build_menus
except ImportError:
    from menus import build_menus

HASH_ROUNDS = 512
# Apache XML-RPC ClientFactory uses the Java interface name as prefix.
BIF_CLIENT = "com.bitservice.bifclient"
NEURA_CLIENT = "com.neura.interfclient"
RPC_CLIENT = f"{BIF_CLIENT}.ClientHandler"
RPC_CONFIG = f"{BIF_CLIENT}.ConfigurationClientHandler"
RPC_IO = f"{BIF_CLIENT}.IOClientHandler"
RPC_LOG = f"{BIF_CLIENT}.LogClientHandler"
RPC_TIME = f"{NEURA_CLIENT}.TimeProgClientHandler"
RPC_USER = f"{NEURA_CLIENT}.UserManagementClientHandler"

ROLES = {0: "Neura", 1: "Partner", 2: "Kunde"}
ERROR_LABELS = {
    "FROST": "Frostschutz",
    "HIGH_PRESSURE": "Hochdruck",
    "LOW_PRESSURE": "Niederdruck",
    "TMAX": "Temperaturbegrenzer",
    "P3": "Tarifabschaltung",
    "HP": "Hochdruck",
    "LP": "Niederdruck",
    "PCS": "Frequenzumrichter",
    "DEDEW": "Verdampfer vereist",
    "WW": "Störung Warmwasser",
}

ANALOG_LABELS = {
    "flow": "Vorlauf",
    "return": "Rücklauf",
    "room": "Raum",
    "cylinder": "Warmwasser",
    "comp_in": "Sauggas",
    "comp_out": "Heißgas",
    "screed": "Estrich",
    "hochdruck": "Hochdruck",
    "niederdruck": "Niederdruck",
    "outside": "Außen",
    "outdoor": "Außen",
    "source": "Quelle",
    "source_in": "Quelle ein",
    "source_out": "Quelle aus",
}
DIGITAL_OUT_LABELS = {
    "heatpump_2": "Wärmepumpe",
    "heatpump_1": "Wärmepumpe 1",
    "heatpump": "Wärmepumpe",
    "cylinder_pump": "Warmwasserpumpe",
    "circulator_pump": "Umwälzpumpe",
    "heater_rod": "Heizstab",
}
DIGITAL_IN_LABELS = {
    "high_pressure": "Hochdruckschalter",
    "low_pressure": "Niederdruckschalter",
    "tmax": "Temperaturbegrenzer",
    "three_phases": "EVU-Sperre",
}
HEAT_TARGET_KEY = "neura.heatcurve.hc_starttemp"
HEAT_TARGET_KEYS = (
    "neura.heatcurve.hc_starttemp",
    "neura.heatcurve.starttemp",
)
CYLINDER_TARGET_KEYS = (
    "neura.cylinder.timeframe_1_temp",
    "neura.cylinder.tmax",
)


class NeuraError(Exception):
    pass


def session_expired(text: str) -> bool:
    low = (text or "").lower()
    return "not authenticated" in low or "unknown session" in low or "invalid session" in low


def prepare_key(first: str, second: str) -> bytes:
    """16-byte AES key, matching AuthenticationMethods.prepareKey."""
    key = ["\0"] * 16
    copied = min(16, len(first))
    for i in range(copied):
        key[i] = first[i]
    if len(first) < 16:
        length = 16 - len(first) - 1
        for i in range(max(0, min(length, len(second)))):
            key[len(first) + i] = second[i]
    return bytes(ord(ch) & 0xFF for ch in key)


def password_hash(password: str, salt: bytes, rounds: int = HASH_ROUNDS) -> str:
    """SHA-1(salt || password), then `rounds` more SHA-1 passes. Base64, no newline."""
    digest = hashlib.sha1(salt + password.encode("utf-8")).digest()
    for _ in range(rounds):
        digest = hashlib.sha1(digest).digest()
    return base64.b64encode(digest).decode("ascii")


def aes_cfb_encrypt(data: bytes, hash_b64: str, salt_b64: str) -> bytes:
    """AES/CFB/NoPadding as used to wrap a login challenge."""
    key = prepare_key(hash_b64, salt_b64)
    iv = base64.b64decode(salt_b64)
    if len(iv) < 16:
        iv = iv + bytes(16 - len(iv))
    iv = iv[:16]
    encryptor = Cipher(algorithms.AES(key), CFB(iv)).encryptor()
    return encryptor.update(data) + encryptor.finalize()


def _binary(value: Any) -> bytes:
    if isinstance(value, xmlrpc.client.Binary):
        return value.data
    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        return value.encode("latin1")
    raise NeuraError("unerwartete Binärantwort")


def _number(value: Any) -> float | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        text = value.strip().replace(",", ".")
        if not text:
            return None
        try:
            return float(text)
        except ValueError:
            return None
    if isinstance(value, dict):
        for key in ("value", "val", "temperature", "current", "data"):
            if key in value:
                return _number(value[key])
    return None


def _bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        text = value.strip().lower()
        if text in ("1", "true", "yes", "on", "ein"):
            return True
        if text in ("0", "false", "no", "off", "aus"):
            return False
    if isinstance(value, dict):
        for key in ("value", "val", "state", "active"):
            if key in value:
                return _bool(value[key])
    return None


def _id_of(item: Any) -> str | None:
    if isinstance(item, str):
        return item
    if isinstance(item, dict):
        for key in ("id", "name", "key", "ioid"):
            if item.get(key):
                return str(item[key])
    return None


def _label(kind: str, ident: str) -> str:
    table = {"ai": ANALOG_LABELS, "di": DIGITAL_IN_LABELS, "do": DIGITAL_OUT_LABELS}[kind]
    return table.get(ident.lower(), ident.replace("_", " "))


def xmlrpc_endpoint(host: str, port: int = 80) -> tuple[str, int, str]:
    """Hostname, port and XML-RPC URL. Paths such as /neura are ignored."""
    text = (host or "").strip()
    if not text:
        raise NeuraError("Adresse fehlt")
    if "://" not in text:
        text = f"http://{text}"
    parsed = urlparse(text)
    hostname = parsed.hostname or host.split("/")[0].strip()
    if not hostname:
        raise NeuraError("Adresse fehlt")
    use_port = int(parsed.port or port or 80)
    return hostname, use_port, f"http://{hostname}:{use_port}/xmlrpc"


class NeuraClient:
    def __init__(self, host: str, port: int = 80, username: str = "", password: str = "", salt: str = ""):
        self.host, self.port, url = xmlrpc_endpoint(host, port)
        self.username = username.strip()
        self.password = password
        self.salt = salt.strip()
        self.token = ""
        self.privileged = False
        self.login_error = ""
        self._lock = threading.Lock()
        self._proxy = xmlrpc.client.ServerProxy(
            url,
            allow_none=True,
            use_builtin_types=False,
            transport=_TimeoutTransport(CALL_TIMEOUT),
        )

    def call(self, method: str, *args: Any) -> Any:
        try:
            return getattr(self._proxy, method)(*args)
        except xmlrpc.client.Fault as exc:
            raise NeuraError(exc.faultString or str(exc)) from exc
        except (OSError, xmlrpc.client.ProtocolError, xmlrpc.client.ResponseError) as exc:
            text = str(exc)
            if "timed out" in text.lower():
                raise NeuraError(f"{self.host} antwortet nicht") from exc
            raise NeuraError(text) from exc

    def rpc(self, method: str, *args: Any) -> Any:
        """Session method: current token is sent first, expired sessions are reopened."""
        with self._lock:
            self._ensure_locked()
            try:
                return self.call(method, self.token, *args)
            except NeuraError as exc:
                if not session_expired(str(exc)) or self._session_still_valid_locked():
                    raise
                self._reopen_locked()
                return self.call(method, self.token, *args)

    def connect(self) -> None:
        with self._lock:
            self._connect_locked()

    def disconnect(self) -> None:
        with self._lock:
            self._disconnect_locked()

    def _disconnect_locked(self) -> None:
        token = self.token
        self.token = ""
        self.privileged = False
        if not token:
            return
        try:
            self.call(f"{RPC_CLIENT}.closeConnection", token)
        except NeuraError:
            pass

    def _connect_locked(self) -> None:
        self._disconnect_locked()
        self.token = str(self.call(f"{RPC_CLIENT}.openConnection"))
        self.privileged = False
        self.login_error = ""
        if self.username and self.password:
            try:
                self._login()
            except NeuraError as exc:
                self.login_error = str(exc)

    def _session_still_valid_locked(self) -> bool:
        """A refused call is not a dead session while doPing still accepts the token."""
        if not self.token:
            return False
        try:
            self.call(f"{RPC_CLIENT}.doPing", self.token)
        except NeuraError as exc:
            return not session_expired(str(exc))
        return True

    def _reopen_locked(self) -> None:
        self._connect_locked()

    def _login(self) -> None:
        salt_b64 = self.salt
        if not salt_b64:
            info = self._user_info()
            salt_b64 = str(info.get("salt") or info.get("s") or "")
        if not salt_b64:
            raise NeuraError(
                "Für Schreibzugriff wird das Salt des Benutzers gebraucht. "
                "Die öffentliche Sitzung kann Werte lesen, sofern die Regelung das erlaubt."
            )
        if len(self.password) >= 27 and self.password.endswith("="):
            hashed = self.password
        else:
            hashed = password_hash(self.password, base64.b64decode(salt_b64))
        public_token = self.token
        challenge = _binary(self.call(f"{RPC_CLIENT}.getChallenge", self.username))
        cipher = aes_cfb_encrypt(challenge, hashed, salt_b64)
        token = self.call(f"{RPC_CLIENT}.testChallenge", self.username, xmlrpc.client.Binary(cipher))
        if not token:
            raise NeuraError("Anmeldung abgelehnt")
        token = str(token)
        if public_token and public_token != token:
            try:
                self.call(f"{RPC_CLIENT}.closeConnection", public_token)
            except NeuraError:
                pass
        self.token = token
        self.privileged = True

    def _user_info(self) -> dict:
        try:
            info = self.call(f"{RPC_USER}.getUser", self.token, self.username)
        except NeuraError:
            return {}
        return info if isinstance(info, dict) else {}

    def ensure(self) -> None:
        with self._lock:
            if not self.token:
                self._connect_locked()
                return
            try:
                self.call(f"{RPC_CLIENT}.doPing", self.token)
            except NeuraError as exc:
                if session_expired(str(exc)):
                    self._reopen_locked()

    def _ensure_locked(self) -> None:
        if not self.token:
            self._connect_locked()

    def _ids(self, method: str) -> list[str]:
        raw = self.rpc(method)
        if not isinstance(raw, list):
            return []
        ids = []
        for item in raw:
            ident = _id_of(item)
            if ident:
                ids.append(ident)
        return ids

    def _points(self, kind: str, list_method: str, value_method: str) -> list[dict]:
        ids = self._ids(list_method)
        if not ids:
            return []
        raw = self.rpc(value_method, ids)
        values: dict[str, Any] = {}
        if isinstance(raw, dict):
            values = raw
        elif isinstance(raw, list):
            for item, ident in zip(raw, ids):
                if isinstance(item, dict) and _id_of(item):
                    values[_id_of(item)] = item
                else:
                    values[ident] = item
        points = []
        for ident in ids:
            payload = values.get(ident, values.get(ident.lower()))
            points.append(
                {
                    "id": ident,
                    "label": _label(kind, ident),
                    "value": _number(payload) if kind == "ai" else _bool(payload),
                    "raw": _plain(payload),
                }
            )
        return points

    def configuration(self) -> dict[str, Any]:
        keys = self.rpc(f"{RPC_CONFIG}.getAllKeys")
        if not isinstance(keys, list) or not keys:
            return {}
        raw = self.rpc(f"{RPC_CONFIG}.getConfiguration", [str(k) for k in keys])
        if not isinstance(raw, dict):
            return {}
        return {str(k): _config_entry(v) for k, v in raw.items()}

    def time_programs(self) -> list:
        raw = self.rpc(f"{RPC_TIME}.doListTimePrograms")
        return _plain(raw) if isinstance(raw, list) else []

    def last_error(self) -> Any:
        try:
            return format_log_entry(self.rpc(f"{RPC_LOG}.getLastErrorLogEntry"))
        except NeuraError:
            return None

    def error_log(self) -> list[dict[str, Any]]:
        try:
            stamps = self.rpc(f"{RPC_LOG}.getAllErrorLogStamps")
        except NeuraError:
            return []
        if not isinstance(stamps, list) or not stamps:
            return []
        try:
            raw = self.rpc(f"{RPC_LOG}.getErrorLogEntries", [str(s) for s in stamps])
        except NeuraError:
            return []
        if not isinstance(raw, list):
            return []
        entries = [format_log_entry(item) for item in raw]
        return [item for item in entries if item]

    def users(self) -> list[dict[str, Any]]:
        raw = self.rpc(f"{RPC_USER}.getUsers")
        if not isinstance(raw, list):
            return []
        users = []
        for item in raw:
            if not isinstance(item, dict):
                continue
            group = item.get("group")
            try:
                group_id = int(group)
            except (TypeError, ValueError):
                group_id = group
            users.append(
                {
                    "username": str(item.get("username") or ""),
                    "group": group_id,
                    "role": ROLES.get(group_id, str(group)),
                    "active": _bool(item.get("active")),
                    "information": str(item.get("information") or ""),
                    "salt": str(item.get("salt") or ""),
                }
            )
        users.sort(key=lambda row: (row["group"] if isinstance(row["group"], int) else 99, row["username"]))
        return users

    def add_user(self, username: str, group: int, password: str, information: str = "") -> None:
        if not self.rpc(f"{RPC_USER}.doAddUser", username, int(group), password, information):
            raise NeuraError("Benutzer konnte nicht angelegt werden")

    def delete_user(self, username: str) -> None:
        if not self.rpc(f"{RPC_USER}.doDeleteUser", username):
            raise NeuraError("Benutzer konnte nicht gelöscht werden")

    def set_user_password(self, username: str, password: str) -> None:
        if not self.rpc(f"{RPC_USER}.setPassword", username, password):
            raise NeuraError("Passwort konnte nicht gesetzt werden")

    def set_user_locked(self, username: str, locked: bool) -> None:
        method = f"{RPC_USER}.doLockUser" if locked else f"{RPC_USER}.doUnlockUser"
        if not self.rpc(method, username):
            raise NeuraError("Sperre konnte nicht geändert werden")

    def restart(self) -> None:
        self.rpc(f"{RPC_CLIENT}.doRestart")

    def snapshot(self) -> dict:
        self.ensure()
        data = {
            "connected": True,
            "host": self.host,
            "privileged": self.privileged,
            "login_error": self.login_error,
            "config": {},
            "analogs": [],
            "digital_in": [],
            "digital_out": [],
            "timeprograms": [],
            "last_error": None,
            "error_log": [],
            "users": [],
            "warnings": [],
        }
        for key, fn in (
            ("config", self.configuration),
            ("analogs", lambda: self._points("ai", f"{RPC_IO}.getAnalogInputs", f"{RPC_IO}.getAnalogInValues")),
            ("digital_in", lambda: self._points("di", f"{RPC_IO}.getDigitalInputs", f"{RPC_IO}.getDigitalInValues")),
            ("digital_out", lambda: self._points("do", f"{RPC_IO}.getDigitalOutputs", f"{RPC_IO}.getDigitalOutValues")),
            ("timeprograms", self.time_programs),
            ("last_error", self.last_error),
            ("error_log", self.error_log),
            ("users", self.users),
        ):
            try:
                data[key] = fn()
            except NeuraError as exc:
                data["warnings"].append(f"{key}: {exc}")
        data["heating"] = heating_view(data)
        data["cylinder"] = cylinder_view(data)
        data["menus"] = build_menus(data.get("config") or {})
        return data

    def set_value(self, key: str, value: Any) -> None:
        if isinstance(value, bool):
            self.rpc(f"{RPC_CONFIG}.setBooleanValue", key, value)
            return
        number = _number(value)
        if number is not None and not isinstance(value, str):
            try:
                self.rpc(f"{RPC_CONFIG}.setDoubleValue", key, float(number))
                return
            except NeuraError:
                pass
        self.rpc(f"{RPC_CONFIG}.setStringValue", key, str(value))

    def set_heating_target(self, temperature: float) -> str:
        config = self.configuration()
        key = choose_setpoint(config)
        self.set_value(key, float(temperature))
        return key

    def set_cylinder_target(self, temperature: float) -> str:
        config = self.configuration()
        key = choose_cylinder_target(config)
        self.set_value(key, float(temperature))
        return key

    def set_holiday(self, active: bool) -> None:
        self.set_value("neura.holiday.active", bool(active))


def choose_setpoint(config: dict) -> str:
    """Flow-temperature start of the heat curve.

    Mixer keys such as circuit_room_temperature1 store an I/O name (RT1),
    not a temperature. This firmware stores the start as hc_starttemp.
    """
    for key in HEAT_TARGET_KEYS:
        if not config or key in config:
            return key
    return HEAT_TARGET_KEYS[0]


def choose_cylinder_target(config: dict) -> str:
    for key in CYLINDER_TARGET_KEYS:
        if key in config:
            return key
    return CYLINDER_TARGET_KEYS[-1]


def _point(points: list[dict], *names: str) -> float | None:
    wanted = {name.lower() for name in names}
    for point in points:
        if point["id"].lower() in wanted and point["value"] is not None:
            return float(point["value"])
    return None


def _running(points: list[dict], *names: str) -> bool | None:
    wanted = {name.lower() for name in names}
    found = None
    for point in points:
        if point["id"].lower() in wanted and point["value"] is not None:
            if bool(point["value"]):
                return True
            found = False
    return found


def heating_view(data: dict) -> dict:
    config = data.get("config") or {}
    analogs = data.get("analogs") or []
    outputs = data.get("digital_out") or []
    key = choose_setpoint(config)
    curve = heat_curve_points(config)
    return {
        "current": _point(analogs, "flow", "return", "room"),
        "flow": _point(analogs, "flow"),
        "room": _point(analogs, "room"),
        "target": _number(config.get(key)),
        "target_key": key,
        "slope": _number(config.get("neura.heatcurve.slope")),
        "running": _running(outputs, "heatpump_2", "heatpump_1", "heatpump"),
        "holiday": _bool(config.get("neura.holiday.active")),
        "outdoor": _point(analogs, "outside", "outdoor"),
        "curve": curve,
    }


def heat_curve_points(config: dict) -> list[dict[str, Any]]:
    points = [
        {
            "name": "Start",
            "outside": _number(config.get("neura.heatcurve.hc_start_outside")),
            "flow": _number(config.get("neura.heatcurve.hc_starttemp")),
        },
        {
            "name": "Punkt 1",
            "outside": _number(config.get("neura.heatcurve.hc_outside_1t")),
            "flow": _number(config.get("neura.heatcurve.hc_1t")),
        },
        {
            "name": "Punkt 2",
            "outside": _number(config.get("neura.heatcurve.hc_outside_2t")),
            "flow": _number(config.get("neura.heatcurve.hc_2t")),
        },
    ]
    return [point for point in points if point["outside"] is not None and point["flow"] is not None]


def format_log_entry(raw: Any) -> dict[str, Any] | None:
    if not isinstance(raw, dict):
        return None
    code = str(raw.get("error") or raw.get("message") or "").strip()
    if not code and raw.get("timestamp") in (None, "", 0, "0"):
        return None
    stamp = raw.get("timestamp")
    when = ""
    historic = False
    try:
        millis = float(stamp)
        seconds = millis / 1000.0 if millis > 10_000_000_000 else millis
        moment = datetime.fromtimestamp(seconds)
        when = moment.strftime("%d.%m.%Y %H:%M")
        historic = (datetime.now() - moment).days >= 2
    except (TypeError, ValueError, OSError):
        when = str(stamp or "")
    label = ERROR_LABELS.get(code.upper(), code or "Unbekannt")
    text = f"{label} am {when}" if when else label
    if historic:
        text += " — gespeicherter Logeintrag, kein aktueller Alarm."
    return {
        "code": code,
        "label": label,
        "when": when,
        "historic": historic,
        "text": text,
        "raw": _plain(raw),
    }


def cylinder_view(data: dict) -> dict:
    config = data.get("config") or {}
    key = choose_cylinder_target(config)
    return {
        "current": _point(data.get("analogs") or [], "cylinder"),
        "target": _number(config.get(key)),
        "target_key": key,
        "enabled": _bool(config.get("neura.cylinder.enable")),
        "running": _running(data.get("digital_out") or [], "cylinder_pump", "heater_rod"),
    }


def _config_entry(value: Any) -> Any:
    if isinstance(value, dict) and "value" in value:
        return _plain(value["value"])
    return _plain(value)


def _plain(value: Any) -> Any:
    if isinstance(value, xmlrpc.client.Binary):
        return value.data.hex()
    if isinstance(value, dict):
        return {str(k): _plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(v) for v in value]
    if isinstance(value, bytes):
        return value.hex()
    return value
