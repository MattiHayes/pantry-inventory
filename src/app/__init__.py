import math
import os

from flask import Flask, abort, flash, redirect, render_template, request, url_for

from src.database.cupboard import (
    cupboard_exists,
    get_cupboard,
    get_cupboards,
    get_items_in_cupboard,
    insert_cupboard,
)
from src.database.item import (
    change_item_unit,
    insert_item,
    remove_item,
    update_item_quantity,
)
from src.database.utils import initialise_database


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("PANTRY_SECRET_KEY", "local-development-key")
    )

    if test_config is not None:
        app.config.update(test_config)

    # Ensure the pantry tables exist before the first page request.
    initialise_database()

    @app.get("/")
    def index():
        cupboards = get_cupboards()
        item_counts = {
            cupboard["id"]: len(get_items_in_cupboard(cupboard["id"]))
            for cupboard in cupboards
        }
        return render_template(
            "cupboards.html", cupboards=cupboards, item_counts=item_counts
        )

    @app.post("/cupboards")
    def create_cupboard():
        name = request.form.get("name", "").strip().lower()
        if not name:
            flash("Give your cupboard a name first.", "error")
        elif cupboard_exists(name):
            flash(f"A cupboard called {name.title()} already exists.", "error")
        else:
            insert_cupboard(name)
            flash(f"{name.title()} is ready to fill.", "success")
        return redirect(url_for("index"))

    @app.get("/cupboards/<int:cupboard_id>")
    def cupboard_detail(cupboard_id):
        cupboard = get_cupboard(cupboard_id)
        if cupboard is None:
            abort(404)
        items = get_items_in_cupboard(cupboard_id)
        return render_template("cupboard.html", cupboard=cupboard, items=items)

    @app.post("/cupboards/<int:cupboard_id>/items")
    def create_item(cupboard_id):
        cupboard = get_cupboard(cupboard_id)
        if cupboard is None:
            abort(404)

        name = request.form.get("name", "").strip().lower()
        unit = request.form.get("unit", "").strip()
        quantity = _read_quantity(request.form.get("quantity", ""))
        if not name:
            flash("Give the item a name first.", "error")
        elif quantity is None:
            flash("Enter a valid quantity of zero or more.", "error")
        else:
            existing = next(
                (item for item in get_items_in_cupboard(cupboard_id)
                 if item["name"] == name),
                None,
            )
            if existing is not None and existing["unit"] != unit:
                flash(
                    f"{name.title()} is already measured in {existing['unit'] or 'no unit'}.",
                    "error",
                )
            elif existing is not None:
                update_item_quantity(
                    existing["id"], existing["quantity"] + quantity
                )
                flash(f"Added to {name.title()}.", "success")
            else:
                insert_item(name, quantity, unit, cupboard_id)
                flash(f"{name.title()} added to the cupboard.", "success")
        return redirect(url_for("cupboard_detail", cupboard_id=cupboard_id))

    @app.post("/cupboards/<int:cupboard_id>/items/<int:item_id>/quantity")
    def set_item_quantity(cupboard_id, item_id):
        item = _get_item_in_cupboard(cupboard_id, item_id)
        quantity = _read_quantity(request.form.get("quantity", ""))
        if quantity is None:
            flash("Enter a valid quantity of zero or more.", "error")
        else:
            update_item_quantity(item["id"], quantity)
            flash(f"{item['name'].title()} quantity updated.", "success")
        return redirect(url_for("cupboard_detail", cupboard_id=cupboard_id))

    @app.post("/cupboards/<int:cupboard_id>/items/<int:item_id>/unit")
    def set_item_unit(cupboard_id, item_id):
        item = _get_item_in_cupboard(cupboard_id, item_id)
        unit = request.form.get("unit", "").strip()
        change_item_unit(item["id"], unit)
        flash(f"{item['name'].title()} unit updated.", "success")
        return redirect(url_for("cupboard_detail", cupboard_id=cupboard_id))

    @app.post("/cupboards/<int:cupboard_id>/items/<int:item_id>/delete")
    def delete_item(cupboard_id, item_id):
        item = _get_item_in_cupboard(cupboard_id, item_id)
        remove_item(item["id"])
        flash(f"{item['name'].title()} removed.", "success")
        return redirect(url_for("cupboard_detail", cupboard_id=cupboard_id))

    return app


def _read_quantity(raw_value):
    try:
        quantity = float(raw_value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(quantity) or quantity < 0:
        return None
    return quantity


def _get_item_in_cupboard(cupboard_id, item_id):
    cupboard = get_cupboard(cupboard_id)
    if cupboard is None:
        abort(404)
    item = next(
        (item for item in get_items_in_cupboard(cupboard_id)
         if item["id"] == item_id),
        None,
    )
    if item is None:
        abort(404)
    return item
