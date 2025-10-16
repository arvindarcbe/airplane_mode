# Copyright (c) 2025, Aravind Rajendran and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    filters = filters or {}

    columns = [
        {
            "label": "Airport",
            "fieldname": "airport",
            "fieldtype": "Link",
            "options": "Airport",
            "width": 220,
        },
        {
            "label": "Total Shops",
            "fieldname": "total",
            "fieldtype": "Int",
            "width": 120,
        },
        {
            "label": "Available",
            "fieldname": "available",
            "fieldtype": "Int",
            "width": 120,
        },
        {
            "label": "Occupied",
            "fieldname": "occupied",
            "fieldtype": "Int",
            "width": 120,
        },
    ]

    where = []
    args = {}

    # Optional filter: Airport
    if filters.get("airport"):
        where.append("s.airport = %(airport)s")
        args["airport"] = filters["airport"]

    where_sql = (" WHERE " + " AND ".join(where)) if where else ""

    data = frappe.db.sql(
        f"""
        SELECT
            s.airport AS airport,
            COUNT(*) AS total,
            SUM(CASE WHEN s.status='Available' THEN 1 ELSE 0 END) AS available,
            SUM(CASE WHEN s.status='Occupied' THEN 1 ELSE 0 END) AS occupied
        FROM `tabAirport Shop` s
        {where_sql}
        GROUP BY s.airport
        ORDER BY s.airport
    """,
        args,
        as_dict=True,
    )

    return columns, data


def get_columns() -> list[dict]:
    """Return columns for the report.

    One field definition per column, just like a DocType field definition.
    """
    return [
        {
            "label": _("Column 1"),
            "fieldname": "column_1",
            "fieldtype": "Data",
        },
        {
            "label": _("Column 2"),
            "fieldname": "column_2",
            "fieldtype": "Int",
        },
    ]


def get_data() -> list[list]:
    """Return data for the report.

    The report data is a list of rows, with each row being a list of cell values.
    """
    return [
        ["Row 1", 1],
        ["Row 2", 2],
    ]
