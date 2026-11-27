"""Constants for the Neura heat pump integration."""

DOMAIN = "neura_wp"
PANEL_URL_PATH = "neura_wp"
PANEL_RESOURCE = "/neura_wp-panel"
PANEL_ICON = "mdi:heat-pump"
PANEL_TITLE = "Neura"

CONF_SALT = "salt"

DEFAULT_HOST = "192.168.1.100"
DEFAULT_PORT = 80
SCAN_INTERVAL_SECONDS = 30

PLATFORMS = [
    "climate",
    "water_heater",
    "sensor",
    "binary_sensor",
    "switch",
    "number",
]

TEMPERATURE_POINTS = (
    "flow",
    "return",
    "room",
    "cylinder",
    "comp_in",
    "comp_out",
    "screed",
    "outside",
    "outdoor",
    "source",
    "source_in",
    "source_out",
)
PRESSURE_POINTS = ("hochdruck", "niederdruck")
OUTPUT_POINTS = ("heatpump_2", "heatpump", "cylinder_pump", "circulator_pump", "heater_rod")
INPUT_POINTS = ("high_pressure", "low_pressure", "tmax", "three_phases")

HOUR_SENSORS = (
    ("neura.ophours.hp2", "Betriebsstunden Wärmepumpe", "hours_hp"),
    ("neura.ophours.cylinder", "Betriebsstunden Warmwasser", "hours_cylinder"),
    ("neura.ophours.cp", "Betriebsstunden Kompressor", "hours_cp"),
    ("neura.mixer.ophours", "Betriebsstunden Mischer", "hours_mixer"),
)

OVERVIEW_SENSORS = (
    ("neura.heatrequest.targetvalue", "Aktueller Heizsollwert", "heat-target"),
)

NUMBER_SETTINGS = (
    ("neura.heatcurve.slope", "Steigung", 0.0, 3.0, 0.1, "slope"),
    ("neura.heatcurve.hysteresis", "Hysterese", 0.5, 15.0, 0.5, "hysteresis"),
    ("neura.system.inhib_day", "Heizgrenze Tag", 0.0, 40.0, 1.0, "inhib_day"),
    ("neura.system.inhib_night", "Heizgrenze Nacht", 0.0, 40.0, 1.0, "inhib_night"),
)

# Handbetriebe from the original WebDialog ManualModeMenu.
MANUAL_SWITCHES = (
    ("neura.runtime.room_man_temp_flag", "Temporärer Handbetrieb", "man-room-temp", "mdi:hand-back-right"),
    ("neura.runtime.room_man_perm_flag", "Permanenter Handbetrieb", "man-room-perm", "mdi:hand-okay"),
    ("neura.mixer.temp_flag", "Mischer temporärer Handbetrieb", "man-mixer-temp", "mdi:valve"),
    ("neura.mixer.perm_flag", "Mischer permanenter Handbetrieb", "man-mixer-perm", "mdi:valve"),
    ("neura.mixer.force_run", "Mischer Zwangslauf", "man-mixer-force", "mdi:pump"),
    ("neura.runtime.cp_endurance_run", "UWP Dauerlauf", "man-cp", "mdi:pump"),
    ("neura.cylinder.temporary_load", "Boiler Schnellaufheizung", "man-cylinder-load", "mdi:water-boiler"),
    ("neura.runtime.force_dedew", "Abtauung erzwingen", "man-dedew", "mdi:snowflake-melt"),
    ("neura.runtime.uwap_manual", "Unterwasserpumpe Handbetrieb", "man-uwap", "mdi:water-pump"),
    ("neura.runtime.f2_pressed", "F2 / Schnelltaste", "man-f2", "mdi:gesture-tap-button"),
)

MANUAL_NUMBERS = (
    ("neura.runtime.pcs_manual", "FU Handbetrieb", -1.0, 100.0, 1.0, "man-pcs"),
    ("neura.cylinder.temporary_temperature", "Schnellaufheizung Temperatur", 30.0, 65.0, 0.5, "man-cylinder-temp"),
)
