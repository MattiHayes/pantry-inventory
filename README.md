# Pantry Inventory

From the project root, start the Flask development server with:

```bash
python -m flask --app src.app run --debug
```

Open <http://127.0.0.1:5000/> in your browser. The page reads and updates cupboards and items in the same `pantry.db` file used by the existing application. If the database or tables do not exist yet, the app creates the tables when it starts.

From the cupboard list, add a cupboard or open one to view its items. On the cupboard page, you can add an item, update its quantity or unit, and remove it. Adding an item with a name already in that cupboard increases its quantity when its unit matches.

Use **Appearance** in the top-right corner to adjust the accent, page background, and card colours. The browser saves those choices on this device. To change the default palette for everyone, edit the CSS variables near the top of `static/styles.css`.
