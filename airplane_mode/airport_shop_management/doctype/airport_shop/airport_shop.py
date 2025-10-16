# Copyright (c) 2025, Aravind Rajendran and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AirportShop(Document):
    def validate(self):
        # If shop_number is empty, mirror the docname for display
        if not (self.shop_number or "").strip():
            self.shop_number = self.name

        # Default rent from Settings if missing
        if not self.rent:
            self.rent = (
                frappe.db.get_single_value(
                    "Airport Shop Settings", "default_rent_amount"
                )
                or 0
            )
