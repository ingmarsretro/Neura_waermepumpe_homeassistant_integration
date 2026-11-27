# Neura Wärmepumpe

Local Home Assistant integration for Neura WebDialog / biF heat pumps. Version **0.2.2**.

Lokale Home-Assistant-Integration für Neura-Wärmepumpen mit WebDialog / biF. Version **0.2.2**.

The sidebar UI is `/neura_wp-panel`. JSON is `/api/neura_wp` with a Home Assistant token. An iframe on `/api/neura_wp/panel` returns 401. Version 0.2.2 fixes a 500 from the HTML response.

Die Bedienseite liegt unter `/neura_wp-panel`. JSON unter `/api/neura_wp` mit Home-Assistant-Token. Ein Iframe auf `/api/neura_wp/panel` liefert 401. Version 0.2.2 behebt den 500 der HTML-Antwort.

Examples in the documentation use host `192.168.1.100` and user `kunde`. Replace them with your own values.
