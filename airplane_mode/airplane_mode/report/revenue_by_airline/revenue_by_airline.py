# Copyright (c) 2025, Aravind Rajendran and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.query_builder import Field
from frappe.query_builder.functions import Sum


def execute(filters: dict | None = None):
    """Main entry point for the report.
    Called every time the report is loaded or refreshed.
    """

    columns = get_columns()
    data = get_data()

    # Create donut chart and summary if data exists
    chart = get_chart(data) if data else None
    report_summary = get_report_summary(data)

    # Return in correct order: columns, data, message, chart, summary
    return columns, data, None, chart, report_summary


# -------------------------------------------------------------
# Define columns shown in the report table
# -------------------------------------------------------------
def get_columns() -> list[dict]:
    """Return column definitions."""
    return [
        {
            "label": _("Airline"),
            "fieldname": "airline",
            "fieldtype": "Link",
            "options": "Airline",
            "width": 200,
        },
        {
            "label": _("Revenue"),
            "fieldname": "revenue",
            "fieldtype": "Currency",
            "width": 200,
        },
    ]


# -------------------------------------------------------------
# Fetch and calculate report data
# -------------------------------------------------------------
def get_data() -> list[dict]:
    """Return data for the report."""
    # Fetch all airlines
    airlines = frappe.get_all("Airline", fields=["name"])
    data = []

    # Define DocTypes for query builder
    AirplaneTicket = frappe.qb.DocType("Airplane Ticket")
    AirplaneFlight = frappe.qb.DocType("Airplane Flight")
    Airplane = frappe.qb.DocType("Airplane")

    # For each airline, calculate total ticket revenue
    for airline in airlines:
        # Build revenue query using frappe.query_builder
        revenue_query = (
            frappe.qb.from_(AirplaneTicket)
            .join(AirplaneFlight)
            .on(AirplaneTicket.flight == AirplaneFlight.name)
            .join(Airplane)
            .on(AirplaneFlight.airplane == Airplane.name)
            .where(Airplane.airline == airline["name"])
            .select(Sum(AirplaneTicket.total_amount).as_("total_revenue"))
        )

        # Execute query
        revenue_result = frappe.db.sql(revenue_query.get_sql(), as_dict=True)
        revenue = (
            revenue_result[0].total_revenue
            if revenue_result and revenue_result[0].total_revenue
            else 0
        )

        # Append row for this airline
        data.append(
            {
                "airline": airline["name"],
                "revenue": revenue,
            }
        )

    return data


# -------------------------------------------------------------
# Create donut chart data
# -------------------------------------------------------------
def get_chart(data):
    """Return donut chart configuration."""
    chart = {
        "data": {
            "labels": [row["airline"] for row in data],
            "datasets": [{"values": [row["revenue"] for row in data]}],
        },
        "type": "donut",
        "height": 300,
    }
    return chart


# -------------------------------------------------------------
# Report summary (Total Revenue)
# -------------------------------------------------------------
def get_report_summary(data):
    """Return total revenue summary."""
    total_revenue = sum(row["revenue"] for row in data)
    return [
        {
            "value": total_revenue,
            "indicator": "Green",
            "label": _("Total Revenue"),
            "datatype": "Currency",
        }
    ]
