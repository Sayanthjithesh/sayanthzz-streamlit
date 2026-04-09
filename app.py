import streamlit as st
import json
import os
from datetime import datetime, date

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Sayanthzz Arena",
    page_icon="🍽️",
    layout="wide"
)

# ── Custom CSS ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;700&family=DM+Sans:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

/* Dark background */
.stApp { background-color: #0A0A0B; color: #F0EDE8; }

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #141416 !important;
    border-right: 1px solid #2E2E33;
}
[data-testid="stSidebar"] * { color: #F0EDE8 !important; }

/* Buttons */
.stButton > button {
    background: #C9A84C !important;
    color: #0A0A0B !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-family: 'DM Sans', sans-serif !important;
    padding: 8px 20px !important;
}
.stButton > button:hover { background: #F0D080 !important; }

/* Inputs */
input, select, textarea {
    background-color: #1C1C1F !important;
    color: #F0EDE8 !important;
    border: 1px solid #3A3A40 !important;
    border-radius: 8px !important;
}

/* Metric cards */
[data-testid="metric-container"] {
    background: #141416;
    border: 1px solid #2E2E33;
    border-radius: 12px;
    padding: 16px;
}
[data-testid="metric-container"] label { color: #8A8790 !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #C9A84C !important;
    font-family: 'Playfair Display', serif !important;
}

/* Tables */
[data-testid="stDataFrame"] { border: 1px solid #2E2E33; border-radius: 12px; }

/* Tabs */
[data-testid="stTabs"] button {
    background: transparent !important;
    color: #8A8790 !important;
    border-bottom: 2px solid transparent !important;
    font-weight: 500 !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #C9A84C !important;
    border-bottom: 2px solid #C9A84C !important;
}

/* Title styling */
.gold-title {
    font-family: 'Playfair Display', serif;
    font-size: 28px;
    color: #C9A84C;
    margin-bottom: 0;
}
.page-sub { font-size: 13px; color: #8A8790; margin-bottom: 20px; }

/* Dish card */
.dish-card {
    background: #141416;
    border: 1px solid #2E2E33;
    border-radius: 14px;
    padding: 16px;
    text-align: center;
    cursor: pointer;
    transition: all .2s;
    margin-bottom: 10px;
}
.dish-card:hover { border-color: #C9A84C; }
.dish-name { font-weight: 600; font-size: 14px; color: #F0EDE8; margin: 8px 0 4px; }
.dish-price { color: #C9A84C; font-size: 16px; font-weight: 700; }
.dish-cat { font-size: 10px; color: #8A8790; text-transform: uppercase; letter-spacing: 1px; }
.avail-yes { color: #4CAF7D; font-size: 11px; }
.avail-no  { color: #E05252; font-size: 11px; }

/* Receipt box */
.receipt-box {
    background: #141416;
    border: 1px solid #2E2E33;
    border-radius: 16px;
    padding: 24px;
    max-width: 420px;
    margin: auto;
    font-family: 'DM Sans', sans-serif;
}
.receipt-title {
    font-family: 'Playfair Display', serif;
    font-size: 22px;
    color: #C9A84C;
    text-align: center;
}
.receipt-sub { font-size: 10px; color: #8A8790; text-align: center; letter-spacing: 3px; margin-bottom: 10px; }
.receipt-row { display: flex; justify-content: space-between; font-size: 13px; padding: 5px 0; border-bottom: 1px solid #1C1C1F; }
.receipt-total { display: flex; justify-content: space-between; font-size: 18px; font-weight: 700; color: #C9A84C; padding-top: 10px; margin-top: 6px; border-top: 1px dashed #3A3A40; }
.divider { border: none; border-top: 1px dashed #3A3A40; margin: 12px 0; }
</style>
""", unsafe_allow_html=True)


# ── Data helpers ─────────────────────────────────────────────
DATA_FILE  = "data.json"
ORDER_FILE = "orders.json"

DEFAULT_MENU = [
    {"id":1,"name":"Butter Chicken", "cat":"Main Course","price":280,"available":True, "emoji":"🍛"},
    {"id":2,"name":"Dal Makhani",    "cat":"Main Course","price":220,"available":True, "emoji":"🫘"},
    {"id":3,"name":"Garlic Naan",    "cat":"Breads",     "price":60, "available":True, "emoji":"🫓"},
    {"id":4,"name":"Paneer Tikka",   "cat":"Starters",   "price":260,"available":True, "emoji":"🍢"},
    {"id":5,"name":"Mango Lassi",    "cat":"Beverages",  "price":120,"available":True, "emoji":"🥤"},
    {"id":6,"name":"Gulab Jamun",    "cat":"Desserts",   "price":90, "available":True, "emoji":"🍮"},
    {"id":7,"name":"Tomato Soup",    "cat":"Soups",      "price":110,"available":False,"emoji":"🍲"},
    {"id":8,"name":"Chicken Biryani","cat":"Specials",   "price":320,"available":True, "emoji":"🍚"},
]

def load_menu():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return DEFAULT_MENU

def save_menu(menu):
    with open(DATA_FILE, "w") as f:
        json.dump(menu, f, indent=2)

def load_orders():
    if os.path.exists(ORDER_FILE):
        with open(ORDER_FILE) as f:
            return json.load(f)
    return []

def save_orders(orders):
    with open(ORDER_FILE, "w") as f:
        json.dump(orders, f, indent=2)

def next_order_id(orders):
    return max((o["id"] for o in orders), default=1000) + 1


# ── Session state ─────────────────────────────────────────────
if "menu"   not in st.session_state: st.session_state.menu   = load_menu()
if "orders" not in st.session_state: st.session_state.orders = load_orders()
if "cart"   not in st.session_state: st.session_state.cart   = {}


# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="gold-title">Sayanthzz Arena</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">RESTAURANT SYSTEM</div>', unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("Navigation", ["🏠 Dashboard", "🛒 POS / Order", "🍽 Menu Items", "⚙️ Manage Menu", "📊 Sales Report"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown('<div style="font-size:12px;color:#8A8790">Logged in as Admin</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# PAGE 1 — DASHBOARD
# ═══════════════════════════════════════════════════════
if page == "🏠 Dashboard":
    st.markdown('<div class="gold-title">Dashboard</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-sub">{datetime.now().strftime("%A, %d %B %Y")}</div>', unsafe_allow_html=True)

    orders = st.session_state.orders
    menu   = st.session_state.menu
    today  = date.today().isoformat()
    month  = today[:7]

    today_orders = [o for o in orders if o["date"] == today]
    month_orders = [o for o in orders if o["date"].startswith(month)]
    today_rev    = sum(o["total"] for o in today_orders)
    month_rev    = sum(o["total"] for o in month_orders)

    # top seller
    sold = {}
    for o in orders:
        for item in o["items"]:
            sold[item["name"]] = sold.get(item["name"], 0) + item["qty"]
    top = max(sold, key=sold.get) if sold else "—"

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("💰 Today's Revenue",  f"₹{today_rev:,}", f"{len(today_orders)} orders")
    c2.metric("🍽 Menu Items",        len(menu),          f"{sum(1 for m in menu if m['available'])} available")
    c3.metric("📊 This Month",        f"₹{month_rev:,}",  f"{len(month_orders)} orders")
    c4.metric("⭐ Top Seller",        top,                f"{sold.get(top,0)} sold" if sold else "No orders yet")

    st.markdown("#### Recent Orders")
    if orders:
        import pandas as pd
        recent = orders[-8:][::-1]
        df = pd.DataFrame([{
            "Order #": f"#{o['id']}",
            "Items":   len(o["items"]),
            "Amount":  f"₹{o['total']:,}",
            "Date":    o["date"],
            "Time":    o["time"],
        } for o in recent])
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No orders yet. Go to POS to place your first order!")


# ═══════════════════════════════════════════════════════
# PAGE 2 — POS / ORDER
# ═══════════════════════════════════════════════════════
elif page == "🛒 POS / Order":
    st.markdown('<div class="gold-title">Point of Sale</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Select dishes to add to cart</div>', unsafe_allow_html=True)

    menu = st.session_state.menu
    cart = st.session_state.cart

    # Category filter
    cats = ["All"] + sorted(set(m["cat"] for m in menu))
    cat  = st.selectbox("Filter by Category", cats, label_visibility="collapsed")

    filtered = [m for m in menu if (cat == "All" or m["cat"] == cat) and m["available"]]

    # Menu grid — 4 columns
    cols = st.columns(4)
    for i, item in enumerate(filtered):
        with cols[i % 4]:
            qty_in_cart = cart.get(item["id"], 0)
            label = f"{item['emoji']} **{item['name']}**\n₹{item['price']}"
            if qty_in_cart:
                label += f"  ✅ ×{qty_in_cart}"
            if st.button(label, key=f"add_{item['id']}", use_container_width=True):
                st.session_state.cart[item["id"]] = qty_in_cart + 1
                st.rerun()

    st.markdown("---")

    # ── CART ─────────────────────────────────────────
    st.markdown("### 🛒 Cart")

    if not cart:
        st.info("Cart is empty. Click a dish above to add it.")
    else:
        cart_items = []
        subtotal   = 0
        for item_id, qty in list(cart.items()):
            item = next((m for m in menu if m["id"] == item_id), None)
            if item:
                amt = item["price"] * qty
                subtotal += amt
                cart_items.append({"id": item_id, "name": item["name"], "emoji": item["emoji"], "price": item["price"], "qty": qty, "amt": amt})

        # Cart table with qty controls
        for ci in cart_items:
            c1, c2, c3, c4, c5 = st.columns([3, 1, 1, 1, 1])
            c1.write(f"{ci['emoji']} {ci['name']}")
            c2.write(f"₹{ci['price']}")
            if c3.button("➕", key=f"inc_{ci['id']}"):
                st.session_state.cart[ci["id"]] += 1
                st.rerun()
            c4.write(f"**{ci['qty']}**")
            if c5.button("➖", key=f"dec_{ci['id']}"):
                if st.session_state.cart[ci["id"]] > 1:
                    st.session_state.cart[ci["id"]] -= 1
                else:
                    del st.session_state.cart[ci["id"]]
                st.rerun()

        tax   = round(subtotal * 0.05)
        total = subtotal + tax

        st.markdown(f"""
        <div style="background:#1C1C1F;border-radius:10px;padding:14px 18px;margin-top:10px">
            <div style="display:flex;justify-content:space-between;color:#8A8790;font-size:13px;margin-bottom:6px"><span>Subtotal</span><span>₹{subtotal:,}</span></div>
            <div style="display:flex;justify-content:space-between;color:#8A8790;font-size:13px;margin-bottom:6px"><span>Tax (5%)</span><span>₹{tax:,}</span></div>
            <div style="display:flex;justify-content:space-between;color:#C9A84C;font-size:18px;font-weight:700;border-top:1px dashed #3A3A40;padding-top:8px;margin-top:4px"><span>TOTAL</span><span>₹{total:,}</span></div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🧾 Generate Receipt", use_container_width=True):
                st.session_state["show_receipt"] = True

        with col2:
            if st.button("🗑 Clear Cart", use_container_width=True):
                st.session_state.cart = {}
                st.session_state.pop("show_receipt", None)
                st.rerun()

        # ── RECEIPT ──────────────────────────────────
        if st.session_state.get("show_receipt"):
            now = datetime.now()
            order_num = next_order_id(st.session_state.orders)

            rows_html = "".join([
                f'<div class="receipt-row"><span>{ci["emoji"]} {ci["name"]} × {ci["qty"]}</span><span>₹{ci["amt"]:,}</span></div>'
                for ci in cart_items
            ])

            st.markdown(f"""
            <div class="receipt-box">
                <div class="receipt-title">Sayanthzz Arena</div>
                <div class="receipt-sub">FINE DINING EXPERIENCE</div>
                <div style="text-align:center;font-size:11px;color:#8A8790;margin-bottom:14px">
                    {now.strftime("%d %b %Y")} &nbsp;|&nbsp; {now.strftime("%I:%M %p")} &nbsp;|&nbsp; Order #{order_num}
                </div>
                <hr class="divider"/>
                <div style="display:flex;justify-content:space-between;font-size:10px;color:#8A8790;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px">
                    <span>Item</span><span>Amount</span>
                </div>
                {rows_html}
                <hr class="divider"/>
                <div style="display:flex;justify-content:space-between;font-size:12px;color:#8A8790;padding:3px 0"><span>Subtotal</span><span>₹{subtotal:,}</span></div>
                <div style="display:flex;justify-content:space-between;font-size:12px;color:#8A8790;padding:3px 0"><span>Tax (5%)</span><span>₹{tax:,}</span></div>
                <div class="receipt-total"><span>TOTAL</span><span>₹{total:,}</span></div>
                <hr class="divider"/>
                <div style="text-align:center;color:#8A8790;font-size:11px">Thank you for dining with us! ❤️</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("✅ Confirm Order & Clear Cart", use_container_width=True):
                new_order = {
                    "id":    order_num,
                    "date":  date.today().isoformat(),
                    "time":  now.strftime("%I:%M %p"),
                    "items": [{"name": ci["name"], "qty": ci["qty"], "price": ci["price"]} for ci in cart_items],
                    "subtotal": subtotal,
                    "tax":   tax,
                    "total": total,
                }
                st.session_state.orders.append(new_order)
                save_orders(st.session_state.orders)
                st.session_state.cart = {}
                st.session_state.pop("show_receipt", None)
                st.success(f"✅ Order #{order_num} confirmed!")
                st.rerun()


# ═══════════════════════════════════════════════════════
# PAGE 3 — MENU ITEMS
# ═══════════════════════════════════════════════════════
elif page == "🍽 Menu Items":
    st.markdown('<div class="gold-title">Menu Items</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">All dishes at a glance</div>', unsafe_allow_html=True)

    menu = st.session_state.menu
    cats = ["All"] + sorted(set(m["cat"] for m in menu))
    cat  = st.selectbox("Category", cats)
    filtered = [m for m in menu if cat == "All" or m["cat"] == cat]

    cols = st.columns(4)
    for i, item in enumerate(filtered):
        with cols[i % 4]:
            avail = "🟢 Available" if item["available"] else "🔴 Unavailable"
            st.markdown(f"""
            <div class="dish-card">
                <div style="font-size:40px">{item['emoji']}</div>
                <div class="dish-name">{item['name']}</div>
                <div class="dish-cat">{item['cat']}</div>
                <div class="dish-price">₹{item['price']}</div>
                <div style="font-size:11px;color:{'#4CAF7D' if item['available'] else '#E05252'};margin-top:4px">{avail}</div>
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# PAGE 4 — MANAGE MENU
# ═══════════════════════════════════════════════════════
elif page == "⚙️ Manage Menu":
    st.markdown('<div class="gold-title">Manage Menu</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Add, edit or remove items</div>', unsafe_allow_html=True)

    menu = st.session_state.menu
    tab1, tab2 = st.tabs(["📋 Edit Existing Items", "➕ Add New Item"])

    # ── Edit existing ────────────────────────────────
    with tab1:
        for item in menu:
            with st.expander(f"{item['emoji']}  {item['name']}  —  ₹{item['price']}  {'🟢' if item['available'] else '🔴'}"):
                c1, c2, c3 = st.columns(3)
                new_name  = c1.text_input("Name",  value=item["name"],  key=f"n_{item['id']}")
                new_price = c2.number_input("Price (₹)", value=item["price"], min_value=1, key=f"p_{item['id']}")
                new_avail = c3.selectbox("Available", ["Yes","No"], index=0 if item["available"] else 1, key=f"a_{item['id']}")

                cats_list = ["Starters","Main Course","Breads","Beverages","Desserts","Soups","Specials"]
                new_cat   = st.selectbox("Category", cats_list, index=cats_list.index(item["cat"]) if item["cat"] in cats_list else 0, key=f"c_{item['id']}")
                new_emoji = st.text_input("Emoji", value=item["emoji"], max_chars=4, key=f"e_{item['id']}")

                col_save, col_del = st.columns(2)
                if col_save.button("💾 Save", key=f"save_{item['id']}", use_container_width=True):
                    item["name"]      = new_name
                    item["price"]     = new_price
                    item["available"] = (new_avail == "Yes")
                    item["cat"]       = new_cat
                    item["emoji"]     = new_emoji
                    save_menu(menu)
                    st.success(f"'{new_name}' updated!")
                    st.rerun()

                if col_del.button("🗑 Delete", key=f"del_{item['id']}", use_container_width=True):
                    st.session_state.menu = [m for m in menu if m["id"] != item["id"]]
                    save_menu(st.session_state.menu)
                    st.warning(f"'{item['name']}' deleted.")
                    st.rerun()

    # ── Add new item ─────────────────────────────────
    with tab2:
        st.markdown("#### Add a New Dish")
        c1, c2 = st.columns(2)
        new_name  = c1.text_input("Dish Name", placeholder="e.g. Butter Chicken")
        new_price = c2.number_input("Price (₹)", min_value=1, value=100)
        c3, c4 = st.columns(2)
        cats_list = ["Starters","Main Course","Breads","Beverages","Desserts","Soups","Specials"]
        new_cat   = c3.selectbox("Category", cats_list)
        new_emoji = c4.text_input("Emoji", value="🍽️", max_chars=4)
        new_avail = st.selectbox("Available", ["Yes", "No"])

        if st.button("➕ Add Item", use_container_width=True):
            if not new_name.strip():
                st.error("Please enter a dish name.")
            else:
                new_id = max((m["id"] for m in menu), default=0) + 1
                st.session_state.menu.append({
                    "id": new_id, "name": new_name.strip(),
                    "cat": new_cat, "price": new_price,
                    "available": (new_avail == "Yes"), "emoji": new_emoji
                })
                save_menu(st.session_state.menu)
                st.success(f"'{new_name}' added to menu!")
                st.rerun()


# ═══════════════════════════════════════════════════════
# PAGE 5 — SALES REPORT
# ═══════════════════════════════════════════════════════
elif page == "📊 Sales Report":
    st.markdown('<div class="gold-title">Sales Report</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Revenue analytics</div>', unsafe_allow_html=True)

    import pandas as pd

    orders = st.session_state.orders
    today  = date.today().isoformat()

    period = st.selectbox("View by", ["Today", "This Month", "This Year", "Custom Range"])

    if period == "Today":
        filtered = [o for o in orders if o["date"] == today]
    elif period == "This Month":
        filtered = [o for o in orders if o["date"].startswith(today[:7])]
    elif period == "This Year":
        filtered = [o for o in orders if o["date"].startswith(today[:4])]
    else:
        c1, c2 = st.columns(2)
        from_d = c1.date_input("From")
        to_d   = c2.date_input("To")
        filtered = [o for o in orders if str(from_d) <= o["date"] <= str(to_d)]

    rev  = sum(o["total"] for o in filtered)
    avg  = round(rev / len(filtered)) if filtered else 0

    sold = {}
    for o in filtered:
        for item in o["items"]:
            sold[item["name"]] = sold.get(item["name"], 0) + item["qty"]
    top = max(sold, key=sold.get) if sold else "—"

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Revenue",   f"₹{rev:,}")
    c2.metric("Total Orders",    len(filtered))
    c3.metric("Avg Order Value", f"₹{avg:,}")
    c4.metric("Best Seller",     top)

    # Bar chart
    if filtered:
        st.markdown("#### Revenue Chart")
        df_chart = pd.DataFrame([{"Date": o["date"], "Revenue": o["total"]} for o in filtered])
        df_grouped = df_chart.groupby("Date")["Revenue"].sum().reset_index()
        st.bar_chart(df_grouped.set_index("Date"), color="#C9A84C")

    # Orders table
    st.markdown("#### All Orders")
    if filtered:
        df = pd.DataFrame([{
            "Order #":  f"#{o['id']}",
            "Date":     o["date"],
            "Time":     o["time"],
            "Items":    ", ".join(f"{i['name']}×{i['qty']}" for i in o["items"]),
            "Total":    f"₹{o['total']:,}",
        } for o in reversed(filtered)])
        st.dataframe(df, use_container_width=True, hide_index=True)

        # CSV export
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download CSV", csv, "sayanthzz_sales.csv", "text/csv", use_container_width=True)
    else:
        st.info("No orders found for this period.")
