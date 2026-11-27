# Installation (Deutsch)

Diese Anleitung installiert die Integration **Neura Wärmepumpe** (`neura_wp`) in Home Assistant. Ein eigener Rechner mit Python ist nicht nötig. Home Assistant spricht danach selbst mit der Regelung.

In den Beispielen:

| Rolle | Beispielwert | Ersetzen durch |
|---|---|---|
| Home Assistant | `192.168.1.10` | Adresse Ihres HA-Servers |
| Wärmepumpe | `192.168.1.100` | Adresse der Neura-Regelung |
| Port | `80` | XML-RPC-Port (meist 80) |
| Benutzer | `kunde` | Ein Benutzer der Regelung (Rollen: Neura, Partner, Kunde) |
| Passwort | *(Ihr Passwort)* | Passwort dieses Benutzers |
| Salt | *(aus der Benutzerverwaltung)* | Salt genau dieses Benutzers |

Legen Sie echte Adressen, Passwörter oder Salts nicht in Git-Repositories ab.

## Voraussetzungen

- Home Assistant 2024.1 oder neuer (Core, OS oder Supervised, im selben Netz wie die Pumpe)
- TCP-Zugang von Home Assistant zur Pumpe, Port **80** (`http://192.168.1.100/xmlrpc`)
- Die Original-WebDialog-Oberfläche der Pumpe sollte im Browser erreichbar sein
- Für **Schreiben** (Sollwerte, Urlaub, Handbetriebe): Benutzer, Passwort **und** Salt
- Für **nur Lesen**: Felder Benutzer/Passwort/Salt leer lassen

Die Python-Abhängigkeit `cryptography` kommt mit Home Assistant bzw. wird beim ersten Start der Integration nachgeladen.

## 1. Dateien kopieren

Den kompletten Ordner `custom_components/neura_wp` aus diesem Repository nach Home Assistant kopieren:

```
<config>/custom_components/neura_wp/
```

`<config>` ist das Home-Assistant-Konfigurationsverzeichnis, zum Beispiel `/config` unter Home Assistant OS.

Der Unterordner `www` muss mitkopiert werden. Darin liegt die Bedienseite.

### Samba / Dateifreigabe

1. `custom_components` anlegen, falls er fehlt.
2. Den Ordner `neura_wp` dorthin kopieren.
3. Inhalt prüfen: `manifest.json`, `www/index.html`, `client.py`, `views.py` müssen vorhanden sein.

### SSH / Terminal

```bash
mkdir -p /config/custom_components
cp -r custom_components/neura_wp /config/custom_components/
```

### HACS (optional)

Falls Sie dieses Repository als benutzerdefiniertes Repository in HACS einbinden:

1. HACS → Integrationen → Drei-Punkte-Menü → **Benutzerdefinierte Repositories**
2. Kategorie **Integration**, URL Ihres Git-Remotes
3. **Neura Wärmepumpe** herunterladen
4. Home Assistant neu starten

## 2. Home Assistant neu starten

Einstellungen → System → Neu starten. Erst danach erscheint die Integration in der Liste.

## 3. Integration einrichten

1. Einstellungen → Geräte und Dienste → **Integration hinzufügen**
2. **Neura Wärmepumpe** suchen
3. Formular ausfüllen:

| Feld | Beispiel | Pflicht |
|---|---|---|
| Adresse | `192.168.1.100` | ja |
| Port | `80` | ja |
| Benutzer | `kunde` | nur zum Schreiben |
| Passwort | *(Passwort von kunde)* | nur zum Schreiben |
| Salt | *(Salt von kunde)* | nur zum Schreiben |

Home Assistant prüft die Verbindung mit `openConnection` gegen `http://192.168.1.100:80/xmlrpc`. Schlägt der Test fehl, ist die Adresse falsch oder Port 80 nicht erreichbar.

Das Salt steht in der Original-Benutzerverwaltung der Regelung (WebDialog). Es gehört zum Benutzer `kunde` und ist kein Passwort.

## 4. Prüfen

Nach dem Anlegen:

- Gerät **Neura Wärmepumpe** unter Einstellungen → Geräte
- Entitäten für Übersicht und Handbetriebe
- Eintrag **Neura** in der linken Seitenleiste (Bedienseite)

Ohne Benutzer sieht die Seite Werte, speichert aber keine Änderungen. Mit `kunde` plus Salt sind Schreiben, Benutzerverwaltung und Regelungsneustart möglich, sofern die Rolle das erlaubt.

Die Seitenleiste lädt **`/neura_wp-panel`**. Zeigt der Iframe `401: Unauthorized`, ist noch Version 0.2.0 installiert. Zeigt er `500 Internal Server Error`, fehlt 0.2.2. Ordner neu kopieren, Home Assistant neu starten, Browser hart neu laden.

## Aktualisieren

1. Alten Ordner `config/custom_components/neura_wp` durch den neuen ersetzen (`www` nicht weglassen).
2. Home Assistant neu starten, nicht nur die Integration neu laden.
3. Im Browser Strg+F5. In `manifest.json` muss `"version": "0.2.2"` stehen.

## Dateien, die zur Installation gehören

```
custom_components/neura_wp/
  __init__.py
  manifest.json
  config_flow.py
  const.py
  client.py
  coordinator.py
  views.py
  panel.py
  menus.py
  entity.py
  climate.py
  water_heater.py
  sensor.py
  binary_sensor.py
  switch.py
  number.py
  strings.json
  translations/de.json
  translations/en.json
  www/index.html
```

Firmware-Abbilder, Boot-Patches und der optionale lokale Python-Server gehören **nicht** in Home Assistant.

## Deinstallation

1. Integration unter Geräte und Dienste entfernen
2. Optional den Ordner `custom_components/neura_wp` löschen
3. Home Assistant neu starten

## Weiterlesen

- [Vollständige Dokumentation](../README.de.md)
- [English installation](INSTALLATION.en.md)
