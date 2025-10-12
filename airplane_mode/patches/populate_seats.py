import random
import frappe

LETTERS = "ABCDE"


def execute():
    # For all tickets missing 'seat', set one like '21A'
    for row in frappe.get_all("Airplane Ticket", fields=["name", "seat"]):
        if not row.seat:
            seat = f"{random.randint(1,99)}{random.choice(LETTERS)}"
            frappe.db.set_value("Airplane Ticket", row.name, "seat", seat)
