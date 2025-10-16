# Copyright (c) 2025, Aravind Rajendran and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate


class ShopLeaseContract(Document):
    def before_insert(self):
        # Fill monthly_rent from shop, else from settings
        if not self.monthly_rent:
            self.monthly_rent = (
                frappe.db.get_value("Airport Shop", self.shop, "rent")
                or frappe.db.get_single_value(
                    "Airport Shop Settings", "default_rent_amount"
                )
                or 0
            )

    def validate(self):
        if getdate(self.end_date) < getdate(self.start_date):
            frappe.throw("End Date must be after Start Date.")

    def on_submit(self):
        # Occupy the shop and stamp contract details on shop
        frappe.db.set_value(
            "Airport Shop",
            self.shop,
            {
                "status": "Occupied",
                "tenent": self.tenent,
                "lease_contract": self.name,
                "contract_start_date": self.start_date,
                "contract_end_date": self.end_date,
            },
            update_modified=False,
        )

    def on_cancel(self):
        # Free the shop
        frappe.db.set_value(
            "Airport Shop",
            self.shop,
            {
                "status": "Available",
                "tenent": None,
                "lease_contract": None,
                "contract_start_date": None,
                "contract_end_date": None,
            },
            update_modified=False,
        )
