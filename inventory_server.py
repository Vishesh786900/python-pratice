import html
import math
import os
import sqlite3
import uuid
from datetime import date
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, quote, urlencode, urlsplit


APP_DIRECTORY = Path(__file__).resolve().parent
DATABASE_PATH = Path(os.environ.get("INVENTORY_DB_PATH", APP_DIRECTORY / "inventory.db"))
MAX_QUANTITY = 9_007_199_254_740_991
MAX_FORM_BYTES = 16_384


class InventoryError(Exception):
    def __init__(self, status: int, message: str) -> None:
        super().__init__(message)
        self.status = status


def connect_database() -> sqlite3.Connection:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database() -> None:
    connection = connect_database()
    try:
        with connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS inventory (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL CHECK(length(name) BETWEEN 1 AND 80),
                    price REAL NOT NULL CHECK(price >= 0),
                    stock INTEGER NOT NULL CHECK(stock >= 0),
                    sold INTEGER NOT NULL CHECK(sold >= 0),
                    reorder INTEGER NOT NULL CHECK(reorder >= 0)
                )
                """
            )
    finally:
        connection.close()


def get_inventory() -> tuple[list[sqlite3.Row], sqlite3.Row]:
    connection = connect_database()
    try:
        items = connection.execute(
            "SELECT id, name, price, stock, sold, reorder FROM inventory ORDER BY rowid"
        ).fetchall()
        summary = connection.execute(
            """
            SELECT
                COUNT(*) AS products,
                COALESCE(SUM(stock), 0) AS units,
                COALESCE(SUM(stock * price), 0) AS inventory_value,
                COALESCE(SUM(sold * price), 0) AS revenue
            FROM inventory
            """
        ).fetchone()
        return items, summary
    finally:
        connection.close()


def parse_integer(value: str, field: str, *, minimum: int = 0) -> int:
    try:
        number = int(value)
    except (TypeError, ValueError) as error:
        raise InventoryError(400, f"{field} must be a whole number.") from error
    if number < minimum or number > MAX_QUANTITY:
        qualifier = "positive" if minimum == 1 else "non-negative"
        raise InventoryError(400, f"{field} must be a {qualifier} whole number.")
    return number


def add_item(form: dict[str, str]) -> None:
    name = form.get("name", "").strip()
    if not name or len(name) > 80:
        raise InventoryError(400, "Product name must contain 1 to 80 characters.")
    try:
        price = float(form.get("price", ""))
    except ValueError as error:
        raise InventoryError(400, "Price must be a valid non-negative number.") from error
    if not math.isfinite(price) or price < 0:
        raise InventoryError(400, "Price must be a valid non-negative number.")

    stock = parse_integer(form.get("stock", ""), "Stock")
    sold = parse_integer(form.get("sold", "0"), "Sold quantity")
    reorder = parse_integer(form.get("reorder", ""), "Reorder level")

    connection = connect_database()
    try:
        with connection:
            connection.execute(
                """
                INSERT INTO inventory (id, name, price, stock, sold, reorder)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (str(uuid.uuid4()), name, price, stock, sold, reorder),
            )
    finally:
        connection.close()


def update_quantity(item_id: str, action: str, quantity: int) -> None:
    connection = connect_database()
    try:
        with connection:
            item = connection.execute(
                "SELECT stock, sold FROM inventory WHERE id = ?",
                (item_id,),
            ).fetchone()
            if item is None:
                raise InventoryError(404, "Product not found.")
            if action == "sell":
                if quantity > item["stock"]:
                    raise InventoryError(409, "There isn't enough stock to complete that sale.")
                if item["sold"] + quantity > MAX_QUANTITY:
                    raise InventoryError(409, "The sold quantity would exceed the supported limit.")
                connection.execute(
                    "UPDATE inventory SET stock = stock - ?, sold = sold + ? WHERE id = ?",
                    (quantity, quantity, item_id),
                )
            elif action == "restock":
                if item["stock"] + quantity > MAX_QUANTITY:
                    raise InventoryError(409, "The stock quantity would exceed the supported limit.")
                connection.execute(
                    "UPDATE inventory SET stock = stock + ? WHERE id = ?",
                    (quantity, item_id),
                )
            else:
                raise InventoryError(404, "Not found.")
    finally:
        connection.close()


def format_currency(value: float) -> str:
    return f"₹{value:,.2f}"


def render_page(
    items: list[sqlite3.Row],
    summary: sqlite3.Row,
    *,
    search: str = "",
    message: str = "",
    message_kind: str = "success",
) -> str:
    safe_search = html.escape(search, quote=True)
    safe_message = html.escape(message)
    query = search.casefold()
    visible_items = [item for item in items if query in item["name"].casefold()]

    rows = []
    for index, item in enumerate(visible_items):
        if item["stock"] == 0:
            status, status_class, stock_class = "Out of stock", "out", "stock-empty"
        elif item["stock"] <= item["reorder"]:
            status, status_class, stock_class = "Low stock", "low", "stock-low"
        else:
            status, status_class, stock_class = "In stock", "", ""
        item_id = quote(item["id"], safe="")
        stock_limit = f' max="{item["stock"]}"' if item["stock"] else " disabled"
        rows.append(
            f"""
            <tr>
              <td><div class="product-name"><span class="product-avatar tone-{index % 4}" aria-hidden="true">{html.escape(item["name"][:1])}</span><span>{html.escape(item["name"])}</span></div></td>
              <td class="price-cell">{format_currency(item["price"])}</td>
              <td class="stock-cell {stock_class}">{item["stock"]:,}</td>
              <td>{item["sold"]:,}</td>
              <td>{item["reorder"]:,}</td>
              <td><span class="status-badge {status_class}">{status}</span></td>
              <td>
                <div class="row-actions">
                  <form class="quantity-form" action="/items/{item_id}/sell" method="post">
                    <label class="visually-hidden" for="sell-{item_id}">Quantity to sell of {html.escape(item["name"])}</label>
                    <input class="quantity-control" id="sell-{item_id}" name="quantity" type="number" min="1"{stock_limit} placeholder="Qty" required>
                    <button class="action-button sell-button" type="submit"{"" if item["stock"] else " disabled"}>Sell</button>
                  </form>
                  <form class="quantity-form" action="/items/{item_id}/restock" method="post">
                    <label class="visually-hidden" for="restock-{item_id}">Quantity to restock {html.escape(item["name"])}</label>
                    <input class="quantity-control" id="restock-{item_id}" name="quantity" type="number" min="1" max="{MAX_QUANTITY - item["stock"]}" placeholder="Qty" required>
                    <button class="action-button" type="submit">Restock</button>
                  </form>
                </div>
              </td>
            </tr>
            """
        )

    if visible_items:
        table_content = "\n".join(rows)
    elif items:
        table_content = '<tr><td colspan="7" class="empty-cell">No products match your search.</td></tr>'
    else:
        table_content = '<tr><td colspan="7" class="empty-cell">Add your first product to start keeping an eye on your stock.</td></tr>'

    message_html = (
        f'<div class="app-message {message_kind}" role="status">{safe_message}</div>'
        if message
        else ""
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#f5f6f8">
  <title>Stockroom | Inventory</title>
  <link rel="stylesheet" href="/inventory.css">
</head>
<body>
  <div class="app-shell">
    <aside class="sidebar">
      <a class="brand" href="/" aria-label="Stockroom home"><span class="brand-mark" aria-hidden="true">S</span><span>stockroom</span></a>
      <p class="nav-heading">WORKSPACE</p>
      <a class="nav-link active" href="#inventory" aria-current="page"><span class="nav-icon" aria-hidden="true">▦</span>Inventory</a>
      <div class="sidebar-note"><span class="note-icon" aria-hidden="true">✦</span><p>Your stock, all in one place.</p></div>
      <p class="sidebar-foot">Inventory dashboard</p>
    </aside>

    <main id="inventory" class="main-content">
      <header class="topbar">
        <div><p class="eyebrow">WORKSPACE / OVERVIEW</p><h1>Inventory</h1></div>
        <span class="storage-label"><span class="status-dot"></span> Saved in SQLite</span>
      </header>
      <section class="welcome-row" aria-label="Inventory overview">
        <div><h2>Good stock starts here.</h2><p>Keep track of what you have, what you've sold, and what needs a refill.</p></div>
        <span class="date-label">{date.today().strftime("%a, %d %b %Y")}</span>
      </section>
      <section class="stats-grid" aria-label="Inventory totals">
        <article class="stat-card"><div class="stat-top"><span class="stat-icon lavender" aria-hidden="true">▦</span><span class="stat-caption">CATALOG</span></div><p class="stat-value">{summary["products"]:,}</p><p class="stat-label">Total products</p></article>
        <article class="stat-card"><div class="stat-top"><span class="stat-icon mint" aria-hidden="true">↗</span><span class="stat-caption">ON HAND</span></div><p class="stat-value">{summary["units"]:,}</p><p class="stat-label">Units in stock</p></article>
        <article class="stat-card"><div class="stat-top"><span class="stat-icon peach" aria-hidden="true">₹</span><span class="stat-caption">STOCK VALUE</span></div><p class="stat-value">{format_currency(summary["inventory_value"])}</p><p class="stat-label">Current inventory value</p></article>
        <article class="stat-card"><div class="stat-top"><span class="stat-icon blue" aria-hidden="true">⌁</span><span class="stat-caption">SALES</span></div><p class="stat-value">{format_currency(summary["revenue"])}</p><p class="stat-label">Total revenue</p></article>
      </section>
      {message_html}
      <section class="workspace-grid">
        <section class="panel inventory-panel" aria-labelledby="inventory-heading">
          <div class="panel-heading">
            <div><p class="eyebrow">YOUR PRODUCTS</p><h2 id="inventory-heading">Stock overview <span class="count-pill">{summary["products"]}</span></h2></div>
            <form class="search-box" action="/" method="get">
              <span class="search-icon" aria-hidden="true">⌕</span>
              <label class="visually-hidden" for="search-input">Search inventory</label>
              <input id="search-input" name="search" type="search" value="{safe_search}" placeholder="Search products..." autocomplete="off">
              <button class="search-button" type="submit">Search</button>
            </form>
          </div>
          <div class="table-wrap">
            <table>
              <thead><tr><th scope="col">PRODUCT</th><th scope="col">PRICE</th><th scope="col">IN STOCK</th><th scope="col">SOLD</th><th scope="col">REORDER AT</th><th scope="col">STATUS</th><th scope="col">ACTIONS</th></tr></thead>
              <tbody>{table_content}</tbody>
            </table>
          </div>
          <div class="table-footer"><span>Stock updates are saved automatically.</span><span>{summary["products"]} {"product" if summary["products"] == 1 else "products"}</span></div>
        </section>
        <aside class="panel add-panel" aria-labelledby="add-heading">
          <div class="add-heading"><span class="add-icon" aria-hidden="true">＋</span><div><p class="eyebrow">CATALOG</p><h2 id="add-heading">Add a product</h2></div></div>
          <p class="form-intro">Enter the details below to add a new item to your inventory.</p>
          <form id="add-form" action="/items/add" method="post">
            <label class="field-label" for="item-name">Product name</label>
            <input class="form-control" id="item-name" name="name" type="text" placeholder="e.g. Everyday tote bag" maxlength="80" required>
            <label class="field-label" for="item-price">Unit price <span>(INR)</span></label>
            <div class="input-prefix"><span aria-hidden="true">₹</span><input class="form-control" id="item-price" name="price" type="number" min="0" step="0.01" placeholder="0.00" required></div>
            <div class="form-row">
              <div><label class="field-label" for="item-stock">Starting stock</label><input class="form-control" id="item-stock" name="stock" type="number" min="0" step="1" placeholder="0" required></div>
              <div><label class="field-label" for="item-sold">Already sold</label><input class="form-control" id="item-sold" name="sold" type="number" min="0" step="1" value="0" required></div>
            </div>
            <label class="field-label" for="item-reorder">Reorder level</label>
            <input class="form-control" id="item-reorder" name="reorder" type="number" min="0" step="1" placeholder="5" required>
            <button class="primary-button" type="submit"><span aria-hidden="true">＋</span> Add to inventory</button>
          </form>
          <div class="tip-box"><span aria-hidden="true">◎</span><p>You'll get a low-stock alert when an item reaches its reorder level.</p></div>
        </aside>
      </section>
      <footer class="page-footer">A little more clarity, one item at a time.</footer>
    </main>
  </div>
</body>
</html>"""


class InventoryRequestHandler(BaseHTTPRequestHandler):
    server_version = "Stockroom/1.0"

    def send_html(self, status: int, content: str) -> None:
        encoded = content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(encoded)

    def send_redirect(self, message: str) -> None:
        location = "/?" + urlencode({"message": message})
        self.send_response(303)
        self.send_header("Location", location)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def read_form(self) -> dict[str, str]:
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError as error:
            raise InventoryError(400, "Invalid request length.") from error
        if content_length <= 0 or content_length > MAX_FORM_BYTES:
            raise InventoryError(400, "Form is empty or too large.")
        if self.headers.get_content_type() != "application/x-www-form-urlencoded":
            raise InventoryError(415, "Expected a standard form submission.")
        try:
            values = parse_qs(
                self.rfile.read(content_length).decode("utf-8"),
                keep_blank_values=True,
                max_num_fields=20,
            )
        except (UnicodeDecodeError, ValueError) as error:
            raise InventoryError(400, "Invalid form data.") from error
        return {key: value[0] for key, value in values.items()}

    def render_inventory(self, status: int = 200, message: str = "", message_kind: str = "success") -> None:
        query = parse_qs(urlsplit(self.path).query, keep_blank_values=True)
        search = query.get("search", [""])[0][:120]
        if not message:
            message = query.get("message", [""])[0][:200]
        try:
            items, summary = get_inventory()
            self.send_html(status, render_page(items, summary, search=search, message=message, message_kind=message_kind))
        except sqlite3.Error:
            self.send_html(500, "<!doctype html><title>Inventory error</title><h1>Could not load inventory</h1>")

    def do_GET(self) -> None:
        path = urlsplit(self.path).path
        if path in {"/", "/inventory.html"}:
            self.render_inventory()
            return
        if path == "/inventory.css":
            try:
                content = (APP_DIRECTORY / "inventory.css").read_bytes()
            except OSError:
                self.send_html(500, "<!doctype html><title>Inventory error</title><h1>Could not load styles</h1>")
                return
            self.send_response(200)
            self.send_header("Content-Type", "text/css; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(content)
            return
        self.send_html(404, "<!doctype html><title>Not found</title><h1>Not found</h1>")

    def do_POST(self) -> None:
        path = urlsplit(self.path).path
        try:
            form = self.read_form()
            if path == "/items/add":
                add_item(form)
                self.send_redirect("Product added to inventory.")
                return

            parts = path.strip("/").split("/")
            if len(parts) == 3 and parts[0] == "items" and parts[2] in {"sell", "restock"}:
                quantity = parse_integer(form.get("quantity", ""), "Quantity", minimum=1)
                update_quantity(parts[1], parts[2], quantity)
                item_name = "Sale recorded." if parts[2] == "sell" else "Stock restocked."
                self.send_redirect(item_name)
                return
            raise InventoryError(404, "Not found.")
        except InventoryError as error:
            self.render_inventory(error.status, str(error), "error")
        except sqlite3.Error:
            self.render_inventory(500, "The inventory database could not complete this request.", "error")

    def log_message(self, format_string: str, *args: object) -> None:
        print(f"{self.address_string()} - {format_string % args}")


def main() -> None:
    initialize_database()
    server = ThreadingHTTPServer(("127.0.0.1", 8000), InventoryRequestHandler)
    print("Inventory app running at http://127.0.0.1:8000")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down inventory server.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
