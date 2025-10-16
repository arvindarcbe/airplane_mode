import frappe
from frappe.utils import getdate, nowdate


def _settings_enabled():
    return bool(frappe.db.get_single_value("Airport Shop Settings", "enable_reminder"))


def _current_ym():
    d = getdate(nowdate())
    return d.year, d.month


def _tenant_email(shop_name):
    tenent = frappe.db.get_value("Airport Shop", shop_name, "tenent")
    return frappe.db.get_value("Tenant", tenent, "email") if tenent else None


def _has_paid_this_month(shop_name, year, month):
    return bool(
        frappe.db.exists(
            "Rent Receipt",
            {"shop": shop_name, "status": "Paid", "year": year, "month": month},
        )
    )


def send_monthly_rent_reminders():
    if not _settings_enabled():
        return
    y, m = _current_ym()
    shops = frappe.get_all(
        "Airport Shop", filters={"status": "Occupied"}, fields=["name", "rent"]
    )
    for s in shops:
        if _has_paid_this_month(s["name"], y, m):
            continue
        email = _tenant_email(s["name"])
        if not email:
            continue
        frappe.sendmail(
            recipients=[email],
            subject="Monthly Rent Reminder",
            message=f"Dear Tenant,<br>Please pay <b>{s['rent']}</b> for shop <b>{s['name']}</b>.",
        )


def send_overdue_rent_reminders():
    if not _settings_enabled():
        return
    y, m = _current_ym()
    shops = frappe.get_all(
        "Airport Shop", filters={"status": "Occupied"}, fields=["name", "rent"]
    )
    for s in shops:
        if _has_paid_this_month(s["name"], y, m):
            continue
        email = _tenant_email(s["name"])
        if not email:
            continue
        frappe.sendmail(
            recipients=[email],
            subject="Overdue Rent Reminder",
            message=f"Dear Tenant,<br>Your rent <b>{s['rent']}</b> for shop <b>{s['name']}</b> is overdue.",
        )
