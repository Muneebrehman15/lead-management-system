"""Prime Properties Karachi — Lead Management System."""

from __future__ import annotations

from datetime import date, datetime

import pandas as pd
import plotly.express as px
import streamlit as st

from database import (
    LOCATIONS,
    PROPERTY_TYPES,
    SOURCES,
    STATUSES,
    add_lead,
    delete_lead,
    fetch_followups,
    fetch_leads,
    get_lead,
    init_db,
    update_lead,
)

st.set_page_config(
    page_title="Prime Properties Karachi | Leads",
    page_icon="🏢",
    layout="wide",
)

init_db()

st.markdown(
    """
    <style>
    :root {
        --app-bg: #f4f7f8;
        --surface: #ffffff;
        --text: #183b4a;
        --muted: #607582;
        --border: #d7e0e5;
        --accent: #0d7182;
        --sidebar-hover: #eef5f8;
    }
    [data-theme="dark"],
    html[data-theme="dark"],
    body[data-theme="dark"],
    .stApp[data-theme="dark"] {
        --app-bg: #111a20;
        --surface: #19252c;
        --text: #e9f1f3;
        --muted: #b0c1c8;
        --border: #34464f;
        --accent: #67c4d0;
        --sidebar-hover: #263941;
    }
    .stApp { background: var(--app-bg); color: var(--text); }
    .block-container { max-width: 1500px; padding: 2rem 3.2rem 3.5rem; }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stSidebar"] { background: var(--surface); border-right: 1px solid var(--border); }
    [data-testid="stSidebar"] > div:first-child { padding: 2.2rem 1.25rem; }
    [data-testid="stSidebar"] [role="radiogroup"] label {
        border-radius: 8px;
        padding: 0.55rem 0.7rem;
        margin: 0.2rem 0;
        color: var(--text) !important;
    }
    [data-testid="stSidebar"] [role="radiogroup"] label:hover { background: var(--sidebar-hover); }
    [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
        background: var(--sidebar-hover);
        color: var(--text) !important;
    }
    [data-testid="stSidebar"] [role="radiogroup"] label p,
    [data-testid="stSidebar"] [role="radiogroup"] label span,
    [data-testid="stSidebar"] .stMarkdown p { color: var(--text) !important; }
    [data-testid="stSidebar"] [role="radiogroup"] label p { font-size: 0.92rem; }
    .stApp p,
    .stApp label,
    .stApp [data-testid="stWidgetLabel"] p,
    .stApp [data-testid="stMarkdownContainer"] p,
    .stApp [data-testid="stCaptionContainer"] p,
    .stApp [data-testid="stAlert"] p { color: var(--text) !important; }
    .stApp [data-testid="stCaptionContainer"] p { color: var(--muted) !important; }
    .stApp input,
    .stApp textarea,
    .stApp [data-baseweb="select"] > div,
    .stApp [data-baseweb="input"] > div,
    .stApp [data-baseweb="textarea"] > div {
        background: var(--surface) !important;
        border-color: var(--border) !important;
        color: var(--text) !important;
    }
    .stApp input,
    .stApp textarea { caret-color: var(--text) !important; }
    .stApp input:focus,
    .stApp textarea:focus,
    .stApp [data-baseweb="select"] > div:focus-within,
    .stApp [data-baseweb="input"] > div:focus-within,
    .stApp [data-baseweb="textarea"] > div:focus-within {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 2px color-mix(in srgb, var(--accent) 22%, transparent) !important;
        outline: none !important;
    }
    .stApp input::placeholder,
    .stApp textarea::placeholder { color: var(--muted) !important; opacity: 1; }
    .stApp [data-baseweb="select"] span,
    .stApp [data-baseweb="select"] input,
    .stApp [data-baseweb="input"] input,
    .stApp [data-baseweb="textarea"] textarea { color: var(--text) !important; }
    .stApp [data-baseweb="select"],
    .stApp [data-baseweb="select"] * { cursor: pointer !important; }
    .stApp [data-baseweb="select"] svg { fill: var(--muted) !important; color: var(--muted) !important; }
    .stApp [data-baseweb="select"]:hover > div { border-color: var(--accent) !important; }
    .stApp [role="listbox"],
    .stApp [role="option"] { background: var(--surface) !important; color: var(--text) !important; }
    .stApp [role="option"]:hover { background: var(--sidebar-hover) !important; }
    .stApp button {
        background: var(--surface);
        color: var(--text) !important;
        border-color: var(--border);
        transition: background 120ms ease, border-color 120ms ease, color 120ms ease;
    }
    .stApp button p,
    .stApp button span { color: inherit !important; }
    .stApp button:hover,
    .stApp button:focus-visible {
        background: var(--sidebar-hover) !important;
        border-color: var(--accent) !important;
        color: var(--text) !important;
    }
    .stApp button:focus-visible {
        box-shadow: 0 0 0 2px color-mix(in srgb, var(--accent) 22%, transparent) !important;
        outline: none !important;
    }
    .stApp button[kind="primary"] {
        color: #ffffff !important;
        background: var(--accent) !important;
        border-color: var(--accent) !important;
    }
    .stApp button[kind="primary"]:hover,
    .stApp button[kind="primary"]:focus-visible {
        color: #ffffff !important;
        background: #095968 !important;
        border-color: #095968 !important;
    }
    .stApp button[kind="secondary"]:hover,
    .stApp button[kind="secondary"]:focus-visible {
        color: #ffffff !important;
        background: #b42318 !important;
        border-color: #b42318 !important;
    }
    .stApp [data-testid="stExpander"] button:hover,
    .stApp [data-testid="stExpander"] button:focus-visible {
        color: #ffffff !important;
        background: #b42318 !important;
        border-color: #b42318 !important;
    }
    .stApp [data-testid="stExpander"] button:hover p,
    .stApp [data-testid="stExpander"] button:focus-visible p,
    .stApp [data-testid="stExpander"] button:hover span,
    .stApp [data-testid="stExpander"] button:focus-visible span { color: #ffffff !important; }
    .stApp [data-testid="stDownloadButton"] button {
        color: var(--text) !important;
        background: var(--surface) !important;
    }
    .stApp [data-testid="stNumberInput"] button {
        min-width: 2.25rem;
        background: var(--surface) !important;
        color: var(--text) !important;
        border-color: var(--border) !important;
        font-size: 1rem;
        font-weight: 700;
    }
    .stApp [data-testid="stNumberInput"] button:hover,
    .stApp [data-testid="stNumberInput"] button:focus-visible {
        background: var(--sidebar-hover) !important;
        color: var(--accent) !important;
    }
    .stApp [data-testid="stNumberInput"] button svg { fill: currentColor !important; }
    .stApp [data-testid="stCheckbox"] label span { color: var(--text) !important; }
    .stApp [data-testid="stMetricLabel"] p,
    .stApp [data-testid="stMetricValue"] { color: var(--text) !important; }
    .stApp [data-testid="stExpander"] summary,
    .stApp [data-testid="stExpander"] summary p { color: var(--text) !important; }
    .stApp [data-testid="stExpander"] summary:hover { color: var(--accent) !important; }
    .brand-mark {
        color: var(--accent);
        font-size: 1.3rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        margin-bottom: 0.1rem;
    }
    .brand-subtitle {
        color: var(--muted);
        font-size: 0.78rem;
        margin-bottom: 1.8rem;
    }
    h1 {
        color: var(--text);
        font-size: 2.25rem !important;
        letter-spacing: -0.025em;
        line-height: 1.15;
        margin: 0 0 0.4rem;
    }
    h2, h3 { color: var(--text); }
    .page-kicker {
        color: var(--accent);
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.11em;
        text-transform: uppercase;
        margin-bottom: 0.35rem;
    }
    .page-description { color: var(--muted); font-size: 0.98rem; margin-bottom: 1.35rem; }
    .section-label {
        border-bottom: 1px solid var(--border);
        color: var(--text);
        font-size: 1.05rem;
        font-weight: 700;
        margin: 1.35rem 0 0.75rem;
        padding-bottom: 0.45rem;
    }
    .kpi-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-left: 4px solid var(--accent);
        border-radius: 8px;
        min-height: 6.4rem;
        padding: 0.95rem 1rem;
        box-shadow: 0 2px 8px rgba(24, 59, 74, 0.06);
    }
    .kpi-label { color: var(--muted); font-size: 0.82rem; font-weight: 600; }
    .kpi-value {
        color: var(--text);
        font-size: 1.45rem;
        font-weight: 700;
        line-height: 1.2;
        margin-top: 0.5rem;
        overflow-wrap: anywhere;
    }
    .dashboard-panel {
        background: #ffffff;
        border: 1px solid #dce3ea;
        border-radius: 8px;
        padding: 0.35rem 0.6rem 0.15rem;
    }
    div[data-testid="stDataFrame"] { border: 1px solid var(--border); border-radius: 8px; }
    div[data-testid="stForm"] { border-color: var(--border); }
    @media (max-width: 900px) {
        .block-container { padding: 1.5rem 1.25rem 2.5rem; }
        [data-testid="stSidebar"] > div:first-child { padding: 1.4rem 0.9rem; }
        h1 { font-size: 1.9rem !important; }
        .kpi-card { min-height: 5.8rem; padding: 0.8rem; }
        .kpi-label { font-size: 0.75rem; }
        .kpi-value { font-size: 1.25rem; }
    }
    @media (max-width: 640px) {
        .block-container { padding: 1.25rem 0.85rem 2rem; }
        .page-description { font-size: 0.9rem; }
        .kpi-card { min-height: 5.2rem; }
        .kpi-value { font-size: 1.1rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def _page_header(kicker: str, title: str, description: str) -> None:
    st.markdown(f'<div class="page-kicker">{kicker}</div>', unsafe_allow_html=True)
    st.title(title)
    st.markdown(f'<div class="page-description">{description}</div>', unsafe_allow_html=True)


def _section_label(text: str) -> None:
    st.markdown(f'<div class="section-label">{text}</div>', unsafe_allow_html=True)


def _kpi_card(label: str, value: str) -> str:
    return (
        '<div class="kpi-card">'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div>'
        '</div>'
    )


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    text = str(value)[:10]
    try:
        return datetime.strptime(text, "%Y-%m-%d").date()
    except ValueError:
        return None


def _date_to_str(value: date | None) -> str:
    return value.isoformat() if value else ""


def _format_pkr(value) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return "—"
    try:
        return f"PKR {int(value):,}"
    except (TypeError, ValueError):
        return "—"


def _lead_priority(lead: dict, *, today: date | None = None) -> str:
    """Calculate a simple, dynamic priority from the lead's current details.

    Closed leads are always Low. Active leads earn points for sales momentum,
    budget size, and a follow-up that is due or overdue.
    """
    if lead.get("status") in {"Converted", "Lost"}:
        return "Low"

    score = {
        "New": 0,
        "Contacted": 1,
        "Site Visit": 2,
        "Negotiation": 3,
    }.get(lead.get("status"), 0)

    try:
        budget = float(lead.get("budget") or 0)
    except (TypeError, ValueError):
        budget = 0
    if budget >= 50_000_000:
        score += 2
    elif budget >= 20_000_000:
        score += 1

    followup = _parse_date(lead.get("next_followup"))
    if followup and followup <= (today or date.today()):
        score += 2

    if score >= 5:
        return "High"
    if score >= 2:
        return "Medium"
    return "Low"


def _leads_frame() -> pd.DataFrame:
    rows = fetch_leads()
    columns = [
        "id",
        "name",
        "phone",
        "email",
        "property",
        "budget",
        "location",
        "status",
        "priority",
        "source",
        "created_at",
        "last_contact",
        "next_followup",
        "notes",
    ]
    if not rows:
        return pd.DataFrame(columns=columns)
    frame = pd.DataFrame(rows)
    frame["priority"] = frame.apply(_lead_priority, axis=1)
    return frame[columns]


def _display_frame(frame: pd.DataFrame) -> pd.DataFrame:
    if frame.empty:
        return frame
    view = frame.copy()
    view["budget"] = view["budget"].map(_format_pkr)
    view = view.rename(
        columns={
            "id": "ID",
            "name": "Name",
            "phone": "Phone",
            "email": "Email",
            "property": "Property",
            "budget": "Budget",
            "location": "Location",
            "status": "Status",
            "priority": "Priority",
            "source": "Source",
            "created_at": "Created",
            "last_contact": "Last contact",
            "next_followup": "Next follow-up",
            "notes": "Notes",
        }
    )
    return view


def _chart_layout(figure, height: int = 340):
    figure.update_layout(
        height=height,
        margin=dict(l=10, r=10, t=40, b=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="Aptos, Segoe UI, sans-serif", size=12, color="#183b4a"),
        title_font=dict(size=16, color="#183b4a"),
        legend=dict(font=dict(size=11, color="#506875")),
        xaxis=dict(tickfont=dict(color="#506875"), title_font=dict(color="#506875")),
        yaxis=dict(tickfont=dict(color="#506875"), title_font=dict(color="#506875")),
    )
    return figure


def render_dashboard() -> None:
    _page_header(
        "Overview",
        "Lead dashboard",
        "A clear view of current opportunities, activity, and the next client conversations.",
    )

    frame = _leads_frame()
    today = date.today()
    followups = fetch_followups()
    overdue = [
        row
        for row in followups
        if _parse_date(row.get("next_followup")) is not None
        and _parse_date(row.get("next_followup")) <= today
    ]

    total = len(frame)
    converted = int((frame["status"] == "Converted").sum()) if total else 0
    open_leads = (
        int((~frame["status"].isin(["Converted", "Lost"])).sum()) if total else 0
    )
    pipeline = (
        float(frame.loc[~frame["status"].isin(["Converted", "Lost"]), "budget"].fillna(0).sum())
        if total
        else 0.0
    )

    kpi_columns = st.columns(4)
    kpi_values = [
        ("Total leads", str(total)),
        ("Open leads", str(open_leads)),
        ("Converted leads", str(converted)),
        ("Follow-ups due", str(len(overdue))),
    ]
    for column, (label, value) in zip(kpi_columns, kpi_values):
        column.markdown(_kpi_card(label, value), unsafe_allow_html=True)
    pipeline_column, _ = st.columns([1, 3])
    pipeline_column.markdown(
        _kpi_card("Open pipeline value", _format_pkr(pipeline)),
        unsafe_allow_html=True,
    )

    if frame.empty:
        st.info("No leads yet. Add the first inquiry from **Add Lead**.")
        return

    priority_counts = frame["priority"].value_counts().reindex(
        ["High", "Medium", "Low"], fill_value=0
    )
    _section_label("Priority snapshot")
    priority_columns = st.columns(3)
    for column, priority in zip(priority_columns, ["High", "Medium", "Low"]):
        column.markdown(
            _kpi_card(f"{priority} priority", str(int(priority_counts[priority]))),
            unsafe_allow_html=True,
        )

    _section_label("Priority leads")
    priority_to_view = st.selectbox(
        "View leads by priority",
        ["High", "Medium", "Low"],
        key="dashboard_priority_filter",
    )
    priority_leads = frame[frame["priority"] == priority_to_view]
    if priority_leads.empty:
        st.info(f"No {priority_to_view.lower()} priority leads right now.")
    else:
        st.dataframe(
            _display_frame(priority_leads),
            width="stretch",
            height=260,
            hide_index=True,
        )

    _section_label("Pipeline insights")
    left, right = st.columns(2)
    status_counts = frame["status"].value_counts().rename_axis("status").reset_index(name="count")
    status_chart = px.bar(
        status_counts,
        x="status",
        y="count",
        title="Leads by status",
        color="status",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    with left.container(border=True):
        st.plotly_chart(_chart_layout(status_chart), width="stretch")

    source_counts = frame["source"].fillna("Unknown").value_counts().rename_axis("source").reset_index(name="count")
    source_chart = px.pie(
        source_counts,
        names="source",
        values="count",
        title="Leads by source",
        hole=0.45,
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    with right.container(border=True):
        st.plotly_chart(_chart_layout(source_chart), width="stretch")

    location_counts = (
        frame["location"].fillna("Unknown").value_counts().rename_axis("location").reset_index(name="count")
    )
    location_chart = px.bar(
        location_counts,
        x="location",
        y="count",
        title="Leads by location",
        color_discrete_sequence=["#1f4e79"],
    )
    with st.container(border=True):
        st.plotly_chart(_chart_layout(location_chart, height=300), width="stretch")

    _section_label("Action required")
    st.subheader("Follow-ups due today or overdue")
    if overdue:
        st.dataframe(
            _display_frame(pd.DataFrame(overdue)),
            width="stretch",
            height=260,
            hide_index=True,
        )
    else:
        st.success("No overdue follow-ups.")


def _lead_form(defaults: dict | None = None, *, submit_label: str) -> dict | None:
    defaults = defaults or {}
    with st.form("lead_form", clear_on_submit=defaults.get("id") is None):
        _section_label("Client details")
        col1, col2, col3 = st.columns(3)
        name = col1.text_input("Client name *", value=defaults.get("name") or "")
        phone = col2.text_input("Phone", value=defaults.get("phone") or "")
        email = col3.text_input("Email", value=defaults.get("email") or "")

        _section_label("Property requirements")
        col4, col5, col6 = st.columns(3)
        property_value = defaults.get("property") or PROPERTY_TYPES[0]
        property_index = (
            PROPERTY_TYPES.index(property_value) if property_value in PROPERTY_TYPES else 0
        )
        property_type = col4.selectbox("Property type", PROPERTY_TYPES, index=property_index)

        location_value = defaults.get("location") or LOCATIONS[0]
        location_index = LOCATIONS.index(location_value) if location_value in LOCATIONS else 0
        location = col5.selectbox("Location", LOCATIONS, index=location_index)

        budget_default = defaults.get("budget") or 0
        budget = col6.number_input(
            "Budget (PKR)",
            min_value=0,
            step=100_000,
            value=int(budget_default) if budget_default else 0,
        )

        _section_label("Sales tracking")
        col7, col8, col9 = st.columns(3)
        status_value = defaults.get("status") or "New"
        status_index = STATUSES.index(status_value) if status_value in STATUSES else 0
        status = col7.selectbox("Status", STATUSES, index=status_index)

        source_value = defaults.get("source") or SOURCES[0]
        source_index = SOURCES.index(source_value) if source_value in SOURCES else 0
        source = col8.selectbox("Source", SOURCES, index=source_index)

        last_contact = col9.date_input(
            "Last contact",
            value=_parse_date(defaults.get("last_contact")) or date.today(),
        )

        followup_col, schedule_col = st.columns([1, 1])
        next_default = _parse_date(defaults.get("next_followup"))
        next_followup = followup_col.date_input(
            "Next follow-up",
            value=next_default or date.today(),
        )
        set_followup = schedule_col.checkbox(
            "Schedule a follow-up",
            value=next_default is not None,
        )
        _section_label("Notes")
        notes = st.text_area("Notes", value=defaults.get("notes") or "", height=120)
        submitted = st.form_submit_button(submit_label, type="primary")

    if not submitted:
        return None
    if not name.strip():
        st.error("Client name is required.")
        return None
    if email.strip() and "@" not in email:
        st.error("Enter a valid email address, or leave it blank.")
        return None

    return {
        "name": name,
        "phone": phone,
        "email": email,
        "property": property_type,
        "budget": float(budget) if budget else None,
        "location": location,
        "status": status,
        "source": source,
        "last_contact": _date_to_str(last_contact),
        "next_followup": _date_to_str(next_followup) if set_followup else "",
        "notes": notes,
    }


def render_add_lead() -> None:
    _page_header(
        "Lead intake",
        "Add a new lead",
        "Capture the client’s requirements and create a clear next step for the team.",
    )
    payload = _lead_form(submit_label="Save lead")
    if payload:
        add_lead(**payload)
        st.success(f"Saved lead for {payload['name']}.")


def render_all_leads() -> None:
    _page_header(
        "Lead workspace",
        "All leads",
        "Search, filter, export, and maintain every Prime Properties Karachi inquiry.",
    )
    frame = _leads_frame()

    filters = st.columns(5)
    search = filters[0].text_input("Search name, phone, or notes")
    status_filter = filters[1].selectbox("Status", ["All"] + STATUSES)
    location_filter = filters[2].selectbox("Location", ["All"] + LOCATIONS)
    source_filter = filters[3].selectbox("Source", ["All"] + SOURCES)
    priority_filter = filters[4].selectbox("Priority", ["All", "High", "Medium", "Low"])

    filtered = frame.copy()
    if not filtered.empty:
        if search.strip():
            query = search.strip().lower()
            mask = (
                filtered["name"].fillna("").str.lower().str.contains(query, regex=False)
                | filtered["phone"].fillna("").str.lower().str.contains(query, regex=False)
                | filtered["notes"].fillna("").str.lower().str.contains(query, regex=False)
            )
            filtered = filtered[mask]
        if status_filter != "All":
            filtered = filtered[filtered["status"] == status_filter]
        if location_filter != "All":
            filtered = filtered[filtered["location"] == location_filter]
        if source_filter != "All":
            filtered = filtered[filtered["source"] == source_filter]
        if priority_filter != "All":
            filtered = filtered[filtered["priority"] == priority_filter]

    st.caption(f"Showing {len(filtered)} lead(s)")
    if filtered.empty:
        st.info("No leads match these filters.")
        return

    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv, "prime_properties_leads.csv", "text/csv")
    st.dataframe(_display_frame(filtered), width="stretch", height=420, hide_index=True)

    _section_label("Lead maintenance")
    st.subheader("Update a lead")
    options = {
        f"#{row.id} — {row.name} ({row.status})": int(row.id)
        for row in filtered.itertuples()
    }
    selected_label = st.selectbox("Select lead", list(options.keys()))
    selected_id = options[selected_label]
    current = get_lead(selected_id)
    if not current:
        st.warning("That lead could not be loaded.")
        return

    payload = _lead_form(current, submit_label="Update lead")
    if payload:
        update_lead(selected_id, **payload)
        st.success(f"Updated {payload['name']}.")
        st.rerun()

    with st.expander("Delete this lead"):
        if st.button("Delete permanently", type="secondary"):
            delete_lead(selected_id)
            st.success("Lead deleted.")
            st.rerun()


def render_followups() -> None:
    _page_header(
        "Client activity",
        "Follow-ups",
        "Keep scheduled conversations moving and make overdue work visible.",
    )
    rows = fetch_followups()
    today = date.today()

    if not rows:
        st.success("No follow-ups scheduled.")
        return

    frame = pd.DataFrame(rows)
    frame["due"] = frame["next_followup"].map(_parse_date)
    overdue = frame[frame["due"].notna() & (frame["due"] <= today)]
    upcoming = frame[frame["due"].notna() & (frame["due"] > today)]

    st.subheader("Due / overdue")
    if overdue.empty:
        st.success("Nothing overdue.")
    else:
        st.dataframe(
            _display_frame(overdue.drop(columns=["due"])),
            width="stretch",
            height=260,
            hide_index=True,
        )

    st.subheader("Upcoming")
    if upcoming.empty:
        st.info("No later follow-ups on the calendar.")
    else:
        st.dataframe(
            _display_frame(upcoming.drop(columns=["due"])),
            width="stretch",
            height=260,
            hide_index=True,
        )


with st.sidebar:
    st.markdown('<div class="brand-mark">Prime Properties</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-subtitle">Karachi · Lead workspace</div>', unsafe_allow_html=True)
    st.markdown("**Workspace**")
    page = st.radio(
        "Navigate",
        ["Dashboard", "Add Lead", "All Leads", "Follow-ups"],
        label_visibility="collapsed",
    )

if page == "Dashboard":
    render_dashboard()
elif page == "Add Lead":
    render_add_lead()
elif page == "All Leads":
    render_all_leads()
else:
    render_followups()
