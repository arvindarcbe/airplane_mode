# Copyright (c) 2025, Aravind Rajendran and contributors
# For license information, please see license.txt

import random
import frappe
from frappe.model.document import Document


class AirplaneTicket(Document):
    def before_insert(self):
        seat_number = random.randint(1, 99)
        seat_letter = random.choice(["A", "B", "C", "D", "E"])
        self.seat = f"{seat_number}{seat_letter}"
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

    def before_submit(self):
        if self.status != "Boarded":
            frappe.throw("Only tickets with Status 'Boarded' can be submitted.")
