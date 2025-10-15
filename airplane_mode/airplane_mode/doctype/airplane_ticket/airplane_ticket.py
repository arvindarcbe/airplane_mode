# Copyright (c) 2025, Aravind Rajendran and contributors
# For license information, please see license.txt

import random
import frappe
from frappe.model.document import Document


class AirplaneTicket(Document):
    def before_insert(self):
        # Assign a random seat when creating a ticket
        seat_number = random.randint(1, 99)
        seat_letter = random.choice(["A", "B", "C", "D", "E"])
        self.seat = f"{seat_number}{seat_letter}"
        if not (self.gate_number or "").strip() and self.flight:
            self.gate_number = frappe.db.get_value(
                "Airplane Flight", self.flight, "gate_number"
            )

    def validate(self):
        add_on_list = []
        total_item_amount = 0

        # --- Check for duplicate add-ons ---
        for add_on in self.add_ons:
            if add_on.item not in add_on_list:
                add_on_list.append(add_on.item)
            else:
                frappe.throw("Duplicate items are not allowed in Add-ons.")

        # --- Calculate total amount ---
        for item in self.add_ons:
            total_item_amount += item.amount

        self.total_amount = self.flight_price + total_item_amount

        # --- Capacity check (added) ---
        if self.flight:
            # Get the linked flight doc
            flight_doc = frappe.get_doc("Airplane Flight", self.flight)
            airplane = flight_doc.airplane

            if airplane:
                airplane_doc = frappe.get_doc("Airplane", airplane)
                airplane_capacity = airplane_doc.capacity or 0

                # Count tickets already booked for this flight
                ticket_count = frappe.db.count(
                    "Airplane Ticket", {"flight": self.flight}
                )

                # Prevent booking beyond capacity
                if ticket_count >= airplane_capacity:
                    frappe.throw("Airplane is full. Please select another flight.")

    def before_submit(self):
        if self.status != "Checked In":
            frappe.throw("Only tickets with Status 'Checked In' can be submitted.")
        self.status = "Boarded"

    def before_update_after_submit(self):
        original = self.get_doc_before_save()
        if original.seat != self.seat:
            frappe.throw("Seat change is not allowed after Boarding.")
