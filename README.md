# Pantry Inventory

## Run with Flask

From the project root, start the development server with:

```bash
python -m flask --app src.app run --debug
```

Open <http://127.0.0.1:5000/> in your browser. The page reads and updates cupboards and items in the same `pantry.db` file used by the existing application. If the database or tables do not exist yet, the app creates the tables when it starts.

From the cupboard list, add a cupboard or open one to view its items. On the cupboard page, you can add an item, update its quantity or unit, and remove it. Adding an item with a name already in that cupboard increases its quantity when its unit matches.

Use **Appearance** in the top-right corner to adjust the accent, page background, and card colours. The browser saves those choices on this device. To change the default palette for everyone, edit the CSS variables near the top of `static/styles.css`.

## Run with Docker on a Raspberry Pi

Install Docker Engine and the Docker Compose plugin on the Pi, then place this project on the Pi. From the project root:

1. Copy `.env.example` to `.env`, generate a long random secret with `openssl rand -hex 32`, and put that value after `PANTRY_SECRET_KEY=` in `.env`.

   ```bash
   cp .env.example .env
   openssl rand -hex 32
   ```
2. Build and start the app:

   ```bash
   docker compose up --build -d
   ```

3. Find the Pi's local address with `hostname -I`, then open `http://<raspberry-pi-local-ip>:5000` on devices connected to your home network. For example, if the Pi's local IP is `192.168.1.20`, visit `http://192.168.1.20:5000`.

The app runs under Waitress, a production WSGI server, and runs as a non-root user inside the container. Docker Compose stores `pantry.db` in the named `pantry_data` volume, so data survives container rebuilds and restarts. To stop the app, run `docker compose down`; **do not add `-v`** unless you intend to delete the stored pantry data.

View the app logs with `docker compose logs -f pantry`.

To back up the database to the current directory:

```bash
docker compose cp pantry:/data/pantry.db ./pantry-backup.db
```

The web app has no sign-in yet. Keep it on your trusted home network and don’t forward its port from your router to the public internet.
