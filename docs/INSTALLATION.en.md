# Installation (English)

This guide installs the **Neura heat pump** integration (`neura_wp`) in Home Assistant. You do not need a separate computer with a Python environment. Home Assistant talks to the controller itself.

Examples used here:

| Role | Example | Replace with |
|---|---|---|
| Home Assistant | `192.168.1.10` | Address of your HA server |
| Heat pump | `192.168.1.100` | Address of the Neura controller |
| Port | `80` | XML-RPC port (usually 80) |
| Username | `kunde` | A controller user (roles: Neura, Partner, Kunde) |
| Password | *(your password)* | Password of that user |
| Salt | *(from user management)* | Salt of that same user |

Do not commit real addresses, passwords or salts to Git.

## Requirements

- Home Assistant 2024.1 or newer (Core, OS or Supervised, on the same network as the pump)
- TCP access from Home Assistant to the pump on port **80** (`http://192.168.1.100/xmlrpc`)
- The original WebDialog UI of the pump should open in a browser
- For **writes** (setpoints, holiday, manual modes): username, password **and** salt
- For **read-only**: leave username, password and salt empty

The Python dependency `cryptography` is already part of Home Assistant or is installed when the integration first loads.

## 1. Copy the files

Copy the entire folder `custom_components/neura_wp` from this repository into Home Assistant:

```
<config>/custom_components/neura_wp/
```

`<config>` is the Home Assistant configuration directory, for example `/config` on Home Assistant OS.

The `www` subfolder must be included. It contains the control page.

### Samba / file share

1. Create `custom_components` if it does not exist.
2. Copy the `neura_wp` folder there.
3. Check that `manifest.json`, `www/index.html`, `client.py` and `views.py` are present.

### SSH / terminal

```bash
mkdir -p /config/custom_components
cp -r custom_components/neura_wp /config/custom_components/
```

### HACS (optional)

If you add this repository as a custom HACS repository:

1. HACS → Integrations → three-dot menu → **Custom repositories**
2. Category **Integration**, URL of your Git remote
3. Download **Neura Wärmepumpe**
4. Restart Home Assistant

## 2. Restart Home Assistant

Settings → System → Restart. The integration only appears in the list after that.

## 3. Add the integration

1. Settings → Devices & services → **Add integration**
2. Search for **Neura Wärmepumpe**
3. Fill in the form:

| Field | Example | Required |
|---|---|---|
| Host | `192.168.1.100` | yes |
| Port | `80` | yes |
| Username | `kunde` | writes only |
| Password | *(password of kunde)* | writes only |
| Salt | *(salt of kunde)* | writes only |

Home Assistant probes the connection with `openConnection` against `http://192.168.1.100:80/xmlrpc`. If that fails, the address is wrong or port 80 is not reachable.

The salt is shown in the original WebDialog user management. It belongs to user `kunde` and is not the password.

## 4. Check

After setup you should see:

- Device **Neura Wärmepumpe** under Settings → Devices
- Entities for the overview and manual modes
- Sidebar item **Neura** (control page)

Without a user the page can read values but cannot save changes. With `kunde` plus salt, writes, user management and a controller restart are available if the role allows it.

The sidebar loads **`/neura_wp-panel`**. `401: Unauthorized` means version 0.2.0 is still installed. `500 Internal Server Error` means 0.2.2 is missing. Copy the folder again, restart Home Assistant, hard-reload the browser.

## Updating

1. Replace `config/custom_components/neura_wp` with the new folder (keep `www`).
2. Restart Home Assistant; reloading the integration alone is not enough.
3. Hard-reload the browser (Ctrl+F5). `manifest.json` must show `"version": "0.2.2"`.

## Files required for installation

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

Firmware images, boot patches and the optional local Python server do **not** belong in Home Assistant.

## Uninstall

1. Remove the integration under Devices & services
2. Optionally delete `custom_components/neura_wp`
3. Restart Home Assistant

## See also

- [Full documentation](../README.en.md)
- [Deutsche Installation](INSTALLATION.de.md)
