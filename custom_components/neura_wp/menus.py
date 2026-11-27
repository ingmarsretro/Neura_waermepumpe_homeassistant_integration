"""Setup menus matching the original Neura WebDialog panels."""
from __future__ import annotations

from typing import Any

READONLY_PREFIXES = (
    "neura.runtime.",
    "neura.logic.",
    "neura.ophours.",
)
READONLY_KEYS = {
    "neura.heatrequest.targetvalue",
    "neura.heatrequest",
    "neura.mixer.current_calculated",
    "neura.mixer.ophours",
    "neura.solar.ophours",
    "neura.solar.request",
    "neura.solar.temperature_collector",
    "neura.solar.temperature_flow",
    "neura.solar.temperature_return",
    "bif.system.log_current_count",
}
WRITABLE_RUNTIME_KEYS = {
    "neura.runtime.pcs_manual",
    "neura.runtime.cp_endurance_run",
    "neura.runtime.uwap_manual",
    "neura.runtime.f2_pressed",
    "neura.runtime.force_dedew",
    "neura.runtime.room_man_perm_flag",
    "neura.runtime.room_man_temp_flag",
}

MENUS = (
    (
        "heatcurve",
        "Heizkurve",
        (
            "neura.heatcurve.hc_starttemp",
            "neura.heatcurve.hc_start_outside",
            "neura.heatcurve.hc_1t",
            "neura.heatcurve.hc_outside_1t",
            "neura.heatcurve.hc_2t",
            "neura.heatcurve.hc_outside_2t",
            "neura.heatcurve.hysteresis",
            "neura.heatcurve.ecofactor",
            "neura.heatrequest.heatcurve",
            "neura.heatrequest.timeprog",
            "neura.heatrequest.external",
            "neura.heatrequest.screed",
            "neura.heatrequest.cascade",
            "neura.heatrequest.slaves_only",
            "neura.heatrequest.theben",
            "neura.heatrequest.targetvalue",
            "neura.system.housetype",
        ),
    ),
    (
        "cylinder",
        "Boiler",
        (
            "neura.cylinder.enable",
            "neura.cylinder.active",
            "neura.cylinder.use_hp",
            "neura.cylinder.tmax",
            "neura.cylinder.tempdiff",
            "neura.cylinder.timeframe_1_start",
            "neura.cylinder.timeframe_1_stop",
            "neura.cylinder.timeframe_1_temp",
            "neura.cylinder.timeframe_2_start",
            "neura.cylinder.timeframe_2_stop",
            "neura.cylinder.timeframe_2_temp",
            "neura.cylinder.legio_enable",
            "neura.cylinder.legio_daily",
            "neura.cylinder.timeframe_legio_start",
            "neura.cylinder.timeframe_legio_stop",
            "neura.cylinder.timeframe_legio_temp",
            "neura.cylinder.temporary_load",
            "neura.cylinder.temporary_temperature",
            "neura.cylinder.f2",
            "neura.cylinder.f2_temp",
            "neura.cylinder.cascade",
            "neura.cylinder.response",
        ),
    ),
    (
        "backupheat",
        "Zusatzheizung",
        (
            "neura.backupheat.active",
            "neura.backupheat.bvmode",
            "neura.backupheat.max_full_runtime",
            "neura.backupheat.min_outdoor_temp",
            "neura.backupheat.min_source_out_temp",
        ),
    ),
    (
        "inhib",
        "Sperrtemperatur",
        (
            "neura.system.inhib_day",
            "neura.system.inhib_night",
        ),
    ),
    (
        "delay",
        "Verzögerungen",
        (
            "neura.system.delays_enable",
            "neura.system.min_runtime",
            "neura.system.min_waittime",
            "neura.system.reqtime",
            "neura.system.delaytime",
            "neura.system.cp_postrun",
            "neura.system.cp_postruntime",
        ),
    ),
    (
        "screed",
        "Estrichheizung",
        (
            "neura.screed.enable",
            "neura.screed.enable_drying",
            "neura.screed.timeframe_start",
            "neura.screed.timeframe_stop",
            "neura.screed.timeframe_temp",
            "neura.screed.screed_drying_settemp",
            "neura.screed.minutes_drying",
            "neura.screed.step",
            "neura.screed.temp_avail",
            "neura.screed.reinit_drying",
        ),
    ),
    (
        "holiday",
        "Urlaub",
        (
            "neura.holiday.active",
            "neura.holiday.tempshift",
            "neura.holiday.return",
        ),
    ),
    (
        "manual",
        "Handbetriebe",
        (
            "neura.runtime.room_man_temp_flag",
            "neura.runtime.room_man_perm_flag",
            "neura.mixer.temp_flag",
            "neura.mixer.perm_flag",
            "neura.mixer.force_run",
            "neura.runtime.cp_endurance_run",
            "neura.runtime.pcs_manual",
            "neura.cylinder.temporary_load",
            "neura.cylinder.temporary_temperature",
            "neura.runtime.force_dedew",
            "neura.runtime.uwap_manual",
            "neura.runtime.f2_pressed",
            "neura.heatrequest.targetvalue",
        ),
    ),
    (
        "mixer",
        "Mischerkreise",
        ("neura.mixer.",),
    ),
    (
        "solar",
        "Solarregler",
        ("neura.solar.",),
    ),
    (
        "cascade",
        "WP Kaskade",
        ("neura.cascade.",),
    ),
    (
        "counter",
        "Zähler",
        ("neura.counter.",),
    ),
    (
        "air",
        "Luft / EuC",
        ("neura.air.",),
    ),
    (
        "settings",
        "Sonstige Einstellungen",
        (
            "neura.heatpump.model",
            "neura.heatpump.type",
            "neura.heatpump.modeselect",
            "neura.heatpump.pcs_exists",
            "neura.heatpump.eul",
            "neura.system.inverter_230v",
            "neura.system.wall_alignment",
            "neura.system.serial_number",
            "neura.system.customer_name",
            "neura.system.customer_address",
            "neura.system.customer_id",
            "neura.system.customer_info",
            "neura.system.partner_name",
            "neura.system.partner_address",
            "neura.system.partner_info",
            "neura.system.first_use",
            "neura.system.activation_stamp",
            "neura.system.housetype",
            "neura.timeprog.active",
            "neura.timeprog.visible",
            "neura.communication.gcn_enabled",
            "neura.communication.gcn_url",
            "neura.communication.eon_enabled",
            "neura.communication.qh_enable",
            "neura.communication.qh_port",
            "neura.communication.nameservice",
        ),
    ),
    (
        "stats",
        "Statistik",
        (
            "neura.ophours.",
            "neura.mixer.ophours",
            "neura.solar.ophours",
            "bif.system.log_interval",
            "bif.system.log_current_count",
        ),
    ),
)

LABELS = {
    "neura.heatcurve.hc_starttemp": "Starttemperatur",
    "neura.heatcurve.hc_start_outside": "Außentemperatur Start",
    "neura.heatcurve.hc_1t": "Heizkurve Temperatur 1",
    "neura.heatcurve.hc_2t": "Heizkurve Temperatur 2",
    "neura.heatcurve.hc_outside_1t": "Heizkurve Außentemperatur 1",
    "neura.heatcurve.hc_outside_2t": "Heizkurve Außentemperatur 2",
    "neura.heatcurve.hysteresis": "Hysterese",
    "neura.heatcurve.ecofactor": "Eco-Faktor",
    "neura.heatrequest.heatcurve": "Anforderung über Heizkurve",
    "neura.heatrequest.timeprog": "Anforderung über Zeitprogramm",
    "neura.heatrequest.external": "Externe Anforderung",
    "neura.heatrequest.screed": "Anforderung Estrich",
    "neura.heatrequest.cascade": "Anforderung Kaskade",
    "neura.heatrequest.slaves_only": "Nur Slaves",
    "neura.heatrequest.theben": "Theben-Anforderung",
    "neura.heatrequest.targetvalue": "Aktueller Sollwert",
    "neura.system.housetype": "Haustyp",
    "neura.cylinder.enable": "Boiler vorhanden",
    "neura.cylinder.active": "Boiler aktiv",
    "neura.cylinder.use_hp": "Warmwasser mit Heizungswärmepumpe",
    "neura.cylinder.tmax": "T-Max",
    "neura.cylinder.tempdiff": "Temperaturdifferenz",
    "neura.cylinder.timeframe_1_start": "Zeitfenster 1 Beginn",
    "neura.cylinder.timeframe_1_stop": "Zeitfenster 1 Ende",
    "neura.cylinder.timeframe_1_temp": "Zeitfenster 1 Temperatur",
    "neura.cylinder.timeframe_2_start": "Zeitfenster 2 Beginn",
    "neura.cylinder.timeframe_2_stop": "Zeitfenster 2 Ende",
    "neura.cylinder.timeframe_2_temp": "Zeitfenster 2 Temperatur",
    "neura.cylinder.legio_enable": "Legionellen aktiv",
    "neura.cylinder.legio_daily": "Legionellen täglich",
    "neura.cylinder.timeframe_legio_start": "Legionellen Beginn",
    "neura.cylinder.timeframe_legio_stop": "Legionellen Ende",
    "neura.cylinder.timeframe_legio_temp": "Legionellen Temperatur",
    "neura.cylinder.temporary_load": "Schnellaufheizung",
    "neura.cylinder.temporary_temperature": "Schnellaufheizung Temperatur",
    "neura.cylinder.f2": "F2",
    "neura.cylinder.f2_temp": "F2 Temperatur",
    "neura.cylinder.cascade": "Boiler Kaskade",
    "neura.cylinder.response": "Boiler Rückmeldung",
    "neura.backupheat.active": "Zusatzheizung aktiv",
    "neura.backupheat.bvmode": "Zusatzheizung BV-Modus",
    "neura.backupheat.max_full_runtime": "Max. Vollbetriebszeit",
    "neura.backupheat.min_outdoor_temp": "Min. Außentemperatur",
    "neura.backupheat.min_source_out_temp": "Min. Quelle-aus-Temperatur",
    "neura.system.inhib_day": "Sperrtemperatur Tag",
    "neura.system.inhib_night": "Sperrtemperatur Nacht",
    "neura.system.delays_enable": "Anlaufverzögerung aktiv",
    "neura.system.min_runtime": "Minimale Laufzeit",
    "neura.system.min_waittime": "Minimale Stehzeit",
    "neura.system.reqtime": "Anforderungszeit",
    "neura.system.delaytime": "Verzögerungszeit",
    "neura.system.cp_postrun": "UWP Nachlauf",
    "neura.system.cp_postruntime": "UWP Nachlaufzeit",
    "neura.screed.enable": "Estrichheizung",
    "neura.screed.enable_drying": "Estrich ausheizen",
    "neura.screed.timeframe_start": "Zeitfenster Beginn",
    "neura.screed.timeframe_stop": "Zeitfenster Ende",
    "neura.screed.timeframe_temp": "Zeitfenster Temperatur",
    "neura.screed.screed_drying_settemp": "Ausheiz-Solltemperatur",
    "neura.screed.minutes_drying": "Ausheiz-Minuten",
    "neura.screed.step": "Ausheiz-Schritt",
    "neura.screed.temp_avail": "Estrichfühler vorhanden",
    "neura.screed.reinit_drying": "Ausheizen neu starten",
    "neura.holiday.active": "Urlaub aktiv",
    "neura.holiday.tempshift": "Urlaubsabsenkung",
    "neura.holiday.return": "Rückkehrdatum",
    "neura.mixer.active": "Mischerkreis aktiv",
    "neura.mixer.name": "Name",
    "neura.mixer.mode": "Betriebsmodus",
    "neura.mixer.cooling": "Notkühlung aktiv",
    "neura.mixer.max_cooling": "Notkühlung Maximaltemperatur",
    "neura.mixer.circ_pump": "Umwälzpumpe Mischerkreis",
    "neura.mixer.mixer": "Mischer-Relais",
    "neura.mixer.heat_request": "Wärmeanforderung Mischerkreis",
    "neura.mixer.circuit_flow_temperature": "Vorlauffühler Mischerkreis",
    "neura.mixer.circuit_room_temperature": "Raumfühler Mischerkreis",
    "neura.mixer.circuit_target_temperature": "Solltemperatur Mischerkreis",
    "neura.mixer.frequency": "Reglerfrequenz",
    "neura.mixer.hc_start": "Heizkurve Start",
    "neura.mixer.hc_start_outside": "Heizkurve Außentemperatur Start",
    "neura.mixer.hc_1t": "Heizkurve Temperatur 1",
    "neura.mixer.hc_2t": "Heizkurve Temperatur 2",
    "neura.mixer.hc_outside_1t": "Heizkurve Außentemperatur 1",
    "neura.mixer.hc_outside_2t": "Heizkurve Außentemperatur 2",
    "neura.mixer.hc_hysteresis": "Hysterese Heizkurve",
    "neura.mixer.timeprog_active": "Zeitprogramme aktiv",
    "neura.mixer.holiday_active": "Urlaubsabsenkung aktiv",
    "neura.mixer.holiday_offset": "Urlaubsabsenkung Temperaturunterschied",
    "neura.mixer.holiday_return": "Urlaub Rückkehr",
    "neura.mixer.screed": "Mit Estrichheizung",
    "neura.mixer.screed_avail": "Estrichfühler",
    "neura.mixer.screed_timeframe_start": "Estrich Beginn",
    "neura.mixer.screed_timeframe_stop": "Estrich Ende",
    "neura.mixer.screed_timeframe_temp": "Estrich Temperatur",
    "neura.mixer.external_offset": "Externer Offset",
    "neura.mixer.force_run": "Zwangslauf",
    "neura.mixer.request": "Anforderung",
    "neura.mixer.current_calculated": "Berechneter Sollwert",
    "neura.mixer.ophours": "Betriebsstunden",
    "neura.mixer.cp_runtime": "Pumpenlaufzeit",
    "neura.mixer.cp_since_off": "Pumpe seit Aus",
    "neura.mixer.perm_flag": "Mischer permanenter Handbetrieb",
    "neura.mixer.temp_flag": "Mischer temporärer Handbetrieb",
    "neura.runtime.room_man_temp_flag": "Temporärer Handbetrieb",
    "neura.runtime.room_man_perm_flag": "Permanenter Handbetrieb",
    "neura.runtime.cp_endurance_run": "UWP Dauerlauf",
    "neura.runtime.pcs_manual": "FU Handbetrieb",
    "neura.runtime.force_dedew": "Abtauung erzwingen",
    "neura.runtime.uwap_manual": "Unterwasserpumpe Handbetrieb",
    "neura.runtime.f2_pressed": "F2 / Schnelltaste",
    "bif.system.log_interval": "Log-Intervall",
    "bif.system.log_current_count": "Log-Einträge",
    "neura.solar.active": "Solarregler aktiv",
    "neura.solar.name": "Name",
    "neura.solar.schema": "Schema",
    "neura.solar.delta_temp": "Delta Temperatur",
    "neura.solar.delta_hysteresis": "Delta Hysterese",
    "neura.solar.collector_minimum": "Minimaltemperatur Kollektor",
    "neura.solar.collector_maximum": "Maximaltemperatur Kollektor",
    "neura.solar.pump_1_mode": "Pumpe 1 drehzahlgeregelt",
    "neura.solar.pump_2_mode": "Pumpe 2 drehzahlgeregelt",
    "neura.solar.minimum_pump_1_tours": "Minimale Drehzahl Pumpe 1",
    "neura.solar.minimum_pump_2_tours": "Minimale Drehzahl Pumpe 2",
    "neura.solar.target_1_maximum": "Maximaltemperatur Ziel 1",
    "neura.solar.target_2_maximum": "Maximaltemperatur Ziel 2",
    "neura.solar.priority": "Priorität der Ziele",
    "neura.solar.target_1_request": "Anforderung Ziel 1",
    "neura.solar.target_2_request": "Anforderung Ziel 2",
    "neura.solar.flush_active": "Spülfunktion aktiv",
    "neura.solar.flush_interval": "Spülintervall",
    "neura.solar.flush_duration": "Spüldauer",
    "neura.solar.flush_timeframe_start": "Spülzeitfenster Beginn",
    "neura.solar.flush_timeframe_end": "Spülzeitfenster Ende",
    "neura.solar.pump_1_r": "Relais Pumpe 1",
    "neura.solar.pump_2_r": "Relais Pumpe 2",
    "neura.solar.pump_1_a": "Analogausgang Pumpe 1",
    "neura.solar.pump_2_a": "Analogausgang Pumpe 2",
    "neura.solar.mixer_open": "Relais Mischer Ziel 1",
    "neura.solar.mixer_close": "Relais Mischer Ziel 2",
    "neura.solar.temperature_collector": "Temperatur Kollektor",
    "neura.solar.temperature_flow": "Temperatur Vorlauf",
    "neura.solar.temperature_return": "Temperatur Rücklauf",
    "neura.solar.sink_1_temperature": "Temperatur Ziel 1",
    "neura.solar.sink_2_temperature": "Temperatur Ziel 2",
    "neura.cascade.slave_id": "Slave ID",
    "neura.cascade.source": "Quelle",
    "neura.cascade.waittime": "Wartezeit",
    "neura.cascade.delaytime": "Anforderung",
    "neura.cascade.hysteresis": "Hysterese",
    "neura.cascade.pcs_flag": "Leistungsregelung",
    "neura.counter.active": "Zähler aktiv",
    "neura.counter.name": "Zählername",
    "neura.counter.value": "Zählerstand",
    "neura.counter.kw_value": "Impulswertigkeit",
    "neura.counter.interval": "Impulslänge",
    "neura.counter.calc": "Berechnung",
    "neura.heatpump.model": "WP-Modell",
    "neura.heatpump.type": "WP-Typ",
    "neura.heatpump.modeselect": "Betriebsart",
    "neura.heatpump.pcs_exists": "Leistungsregelung vorhanden",
    "neura.heatpump.eul": "EuS/C Version",
    "neura.system.inverter_230v": "Inverter Betrieb 230V",
    "neura.system.wall_alignment": "Wandabgleich",
    "neura.system.serial_number": "Seriennummer",
    "neura.system.customer_name": "Kundenname",
    "neura.system.customer_address": "Kundenadresse",
    "neura.system.customer_id": "Kundennummer",
    "neura.system.customer_info": "Kundeninfo",
    "neura.system.partner_name": "Partner",
    "neura.system.partner_address": "Partneradresse",
    "neura.system.partner_info": "Partnerinfo",
    "neura.system.first_use": "Erste Inbetriebnahme",
    "neura.system.activation_stamp": "Inbetriebnahme",
    "neura.timeprog.active": "Zeitprogramme aktiv",
    "neura.timeprog.visible": "Zeitprogramme sichtbar",
    "neura.communication.gcn_enabled": "GCN/BG aktiviert",
    "neura.communication.gcn_url": "GCN/BG URL",
    "neura.communication.eon_enabled": "EON aktiviert",
    "neura.communication.qh_enable": "QH aktiviert",
    "neura.communication.qh_port": "QH Port",
    "neura.communication.nameservice": "Namensdienst",
    "neura.ophours.hp1": "Wärmepumpe",
    "neura.ophours.hp2": "Wärmepumpe 2",
    "neura.ophours.cp": "Umwälzpumpe",
    "neura.ophours.cylinder": "Boiler",
    "neura.ophours.full": "Vollbetrieb",
    "neura.ophours.eco": "Eco-Betrieb",
    "neura.ophours.bh": "Zusatzheizung",
    "neura.ophours.uwap": "Unterwasserpumpe",
    "neura.ophours.wwbh": "Boiler Heizstab",
    "neura.ophours.cp_runtime": "Umwälzpumpe Laufzeit",
    "neura.ophours.cp_since_off": "Umwälzpumpe seit Aus",
    "neura.ophours.full_since_on": "Vollbetrieb seit Ein",
    "neura.ophours.runtime_full": "Vollbetrieb Laufzeit",
}

HELPS = {
    "neura.heatcurve.hc_starttemp": "Vorlauf-Soll am Beginn der Heizkurve. Das ist kein Raum-Sollwert.",
    "neura.heatcurve.hc_start_outside": "Außentemperatur, bei der die Starttemperatur gilt.",
    "neura.heatcurve.hc_1t": "Vorlauf-Soll am ersten Stützpunkt der Heizkurve.",
    "neura.heatcurve.hc_2t": "Vorlauf-Soll am zweiten Stützpunkt (kälteste Auslegung).",
    "neura.heatcurve.hc_outside_1t": "Außentemperatur zum ersten Stützpunkt.",
    "neura.heatcurve.hc_outside_2t": "Außentemperatur zum zweiten Stützpunkt.",
    "neura.heatcurve.hysteresis": "Schaltdifferenz um den Vorlauf-Soll. Größer = seltener Takten.",
    "neura.heatcurve.ecofactor": "Absenkung im Eco-Betrieb, vom Original-WebDialog als Eco-Faktor geführt.",
    "neura.heatrequest.heatcurve": "Wärmeanforderung aus der Heizkurve.",
    "neura.heatrequest.timeprog": "Wärmeanforderung aus den Zeitprogrammen.",
    "neura.heatrequest.external": "Externe Anforderung, z. B. über einen Eingang.",
    "neura.heatrequest.screed": "Anforderung durch die Estrichfunktion.",
    "neura.heatrequest.cascade": "Anforderung in einer Kaskade.",
    "neura.heatrequest.slaves_only": "Nur Slave-Wärmepumpen sollen laufen.",
    "neura.heatrequest.theben": "Anforderung über Theben-Uhr.",
    "neura.heatrequest.targetvalue": "Von der Regelung berechneter aktueller Vorlauf-Soll. Nur Anzeige.",
    "neura.system.housetype": "Auslegungstyp der Anlage, beeinflusst sichtbare Setup-Seiten.",
    "neura.cylinder.enable": "Warmwasserspeicher ist an der Anlage vorhanden.",
    "neura.cylinder.active": "Boilerladung durch die Regelung erlaubt.",
    "neura.cylinder.use_hp": "Warmwasser über die Heizungswärmepumpe statt nur Heizstab.",
    "neura.cylinder.tmax": "Obere Speichergrenze. Darüber keine Ladung.",
    "neura.cylinder.tempdiff": "Einschaltdifferenz unter dem Boiler-Soll.",
    "neura.cylinder.timeframe_1_start": "Beginn des ersten Warmwasser-Zeitfensters.",
    "neura.cylinder.timeframe_1_stop": "Ende des ersten Warmwasser-Zeitfensters.",
    "neura.cylinder.timeframe_1_temp": "Solltemperatur im ersten Zeitfenster.",
    "neura.cylinder.timeframe_2_start": "Beginn des zweiten Warmwasser-Zeitfensters.",
    "neura.cylinder.timeframe_2_stop": "Ende des zweiten Warmwasser-Zeitfensters.",
    "neura.cylinder.timeframe_2_temp": "Solltemperatur im zweiten Zeitfenster.",
    "neura.cylinder.legio_enable": "Periodische Überhöhung gegen Legionellen.",
    "neura.cylinder.legio_daily": "Legionellenprogramm täglich statt wöchentlich (Donnerstag).",
    "neura.cylinder.timeframe_legio_start": "Startzeit der Legionellenladung.",
    "neura.cylinder.timeframe_legio_stop": "Ende der Legionellenladung.",
    "neura.cylinder.timeframe_legio_temp": "Zieltemperatur der Legionellenladung.",
    "neura.cylinder.temporary_load": "Einmalige Zusatzladung jetzt.",
    "neura.cylinder.temporary_temperature": "Soll für die Einmalladung.",
    "neura.backupheat.active": "Zusatzheizung / Heizstab darf anfordern.",
    "neura.backupheat.bvmode": "Bivalenzmodus der Zusatzheizung (0 = wie im Originalpanel).",
    "neura.backupheat.max_full_runtime": "Maximale Zeit im Vollbetrieb mit Zusatzheizung.",
    "neura.backupheat.min_outdoor_temp": "Unter dieser Außentemperatur darf die Zusatzheizung stützen.",
    "neura.backupheat.min_source_out_temp": "Untere Quellenaustrittstemperatur für die Zusatzheizung.",
    "neura.system.inhib_day": "Heizgrenze Tag: darüber keine Heizkurven-Anforderung.",
    "neura.system.inhib_night": "Heizgrenze Nacht.",
    "neura.system.delays_enable": "Anlauf- und Mindestzeiten der Regelung aktiv.",
    "neura.system.min_runtime": "Mindestlaufzeit des Verdichters nach dem Start.",
    "neura.system.min_waittime": "Mindestpause nach dem Abschalten.",
    "neura.system.reqtime": "Wie lange eine Anforderung stehen muss, bevor der Verdichter startet.",
    "neura.system.delaytime": "Zusätzliche Startverzögerung.",
    "neura.system.cp_postrun": "Umwälzpumpe nachlaufen lassen.",
    "neura.system.cp_postruntime": "Nachlaufzeit der Umwälzpumpe.",
    "neura.screed.enable": "Estrichprogramm der Flächenheizung.",
    "neura.screed.enable_drying": "Ausheizprogramm starten bzw. aktiv halten.",
    "neura.holiday.active": "Urlaubsabsenkung ein- oder ausschalten.",
    "neura.holiday.tempshift": "Absenkung der Heizkurve während des Urlaubs in Kelvin.",
    "neura.holiday.return": "Rückkehrdatum. Im Original mindestens zwei Tage in der Zukunft.",
    "neura.mixer.active": "Dieser Mischerkreis ist in Betrieb.",
    "neura.mixer.hc_start": "Heizkurven-Start dieses Mischerkreises.",
    "neura.mixer.timeprog_active": "Zeitprogramme gelten für diesen Kreis.",
    "neura.mixer.holiday_active": "Urlaubsabsenkung für diesen Mischerkreis.",
    "neura.solar.active": "Solarregler darf Pumpen und Ventile steuern.",
    "neura.solar.delta_temp": "Temperaturdifferenz Kollektor zu Speicher für das Einschalten.",
    "neura.solar.delta_hysteresis": "Ausschaltdifferenz der Solarpumpe.",
    "neura.cascade.slave_id": "Adresse dieser Maschine in der Kaskade.",
    "neura.heatpump.model": "Gespeichertes Wärmepumpenmodell.",
    "neura.heatpump.pcs_exists": "Leistungsregelung / Inverter ist vorhanden.",
    "neura.ophours.hp1": "Betriebsstunden der Wärmepumpe. Nur Anzeige.",
    "neura.ophours.hp2": "Betriebsstunden Wärmepumpe 2. Nur Anzeige.",
    "neura.ophours.cylinder": "Betriebsstunden der Boilerladung. Nur Anzeige.",
    "neura.ophours.full": "Stunden im Vollbetrieb. Nur Anzeige.",
    "neura.runtime.room_man_temp_flag": "Temporärer Handbetrieb am Raumterminal, wie im Original unter Handbetriebe.",
    "neura.runtime.room_man_perm_flag": "Permanenter Handbetrieb am Raumterminal, bis er wieder ausgeschaltet wird.",
    "neura.mixer.temp_flag": "Temporärer Handbetrieb dieses Mischerkreises.",
    "neura.mixer.perm_flag": "Permanenter Handbetrieb dieses Mischerkreises.",
    "neura.mixer.force_run": "Mischerkreis und Pumpe unabhängig von der Heizkurve laufen lassen.",
    "neura.runtime.cp_endurance_run": "Umwälzpumpe im Dauerlauf (Original: UWP Dauerlauf / 24 Std.).",
    "neura.runtime.pcs_manual": "Frequenzumrichter von Hand. −1 = Automatik, sonst Soll in Prozent. Nur wirksam, wenn ein FU vorhanden ist.",
    "neura.cylinder.temporary_load": "Einmalige Boiler-Schnellaufheizung, wie F2 im Original-WebDialog.",
    "neura.cylinder.temporary_temperature": "Zieltemperatur der Schnellaufheizung.",
    "neura.runtime.force_dedew": "Abtauung jetzt anstoßen (Luft/Sole, Original: brine / Abtauung).",
    "neura.runtime.uwap_manual": "Unterwasserpumpe unabhängig von der Regelung einschalten.",
    "neura.runtime.f2_pressed": "Entspricht der F2-Taste am Bedienteil (Schnellaufheizung).",
    "neura.heatrequest.targetvalue": "Aktuell berechneter Vorlauf-Soll. Nur Anzeige.",
    "bif.system.log_interval": "Abstand der Datenlogger-Zeilen in Sekunden. Diagramme im Original-WebDialog lesen dieses Log.",
    "bif.system.log_current_count": "Anzahl gespeicherter Logzeilen. Nur Anzeige.",
}


def _numbered_base(key: str) -> str:
    i = len(key)
    while i and key[i - 1].isdigit():
        i -= 1
    return key[:i] if i < len(key) else key


def label_for(key: str) -> str:
    if key in LABELS:
        return LABELS[key]
    base = _numbered_base(key)
    suffix = key[len(base) :]
    if suffix and base in LABELS:
        return f"{LABELS[base]} {suffix}"
    return key.split(".")[-1].replace("_", " ")


def help_for(key: str) -> str:
    if key in HELPS:
        return HELPS[key]
    base = _numbered_base(key)
    suffix = key[len(base) :]
    if base in HELPS:
        text = HELPS[base]
        return f"{text} Kreis {suffix}." if suffix else text
    return (
        f"{label_for(key)} der Regelung. Entspricht dem gleichnamigen Wert "
        "im Original-WebDialog."
    )


def field_kind(value: Any) -> str:
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return "number"
    if isinstance(value, str):
        text = value.strip().lower()
        if text in ("true", "false"):
            return "bool"
        stripped = text.replace(",", ".")
        if stripped:
            try:
                float(stripped)
                return "number"
            except ValueError:
                pass
    return "text"


def is_writable(key: str) -> bool:
    if key in WRITABLE_RUNTIME_KEYS:
        return True
    if key in READONLY_KEYS:
        return False
    return not key.startswith(READONLY_PREFIXES)


def _matches(key: str, selector: str) -> bool:
    if selector.endswith("."):
        return key.startswith(selector)
    if key == selector:
        return True
    extra = key[len(selector) :] if key.startswith(selector) else ""
    return bool(extra) and extra.isdigit()


def _field(key: str, value: Any) -> dict[str, Any]:
    return {
        "key": key,
        "label": label_for(key),
        "help": help_for(key),
        "value": value,
        "kind": field_kind(value),
        "writable": is_writable(key),
    }


def build_menus(config: dict) -> list[dict[str, Any]]:
    """Group live configuration into the original WebDialog setup pages."""
    used: set[str] = set()
    menus = []
    for ident, title, selectors in MENUS:
        fields = []
        for key in sorted(config):
            if any(_matches(key, selector) for selector in selectors):
                fields.append(_field(key, config[key]))
                used.add(key)
        if ident in ("heatcurve", "cylinder", "holiday", "manual", "stats") or fields:
            menus.append({"id": ident, "title": title, "fields": fields})
    leftover = []
    for key in sorted(config):
        if key in used:
            continue
        if key.startswith(READONLY_PREFIXES):
            continue
        leftover.append(_field(key, config[key]))
    if leftover:
        menus.append({"id": "other", "title": "Weitere Werte", "fields": leftover})
    return menus
