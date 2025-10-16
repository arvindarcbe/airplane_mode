# Copyright (c) 2025, Aravind Rajendran and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, getdate


class RentReceipt(Document):
    def before_insert(self):
        if not self.amount and self.shop:
            self.amount = frappe.db.get_value("Airport Shop", self.shop, "rent") or 0
        if not self.payment_date:
            self.payment_date = nowdate()
        # Set month/year if missing based on payment_date
        d = getdate(self.payment_date)
        if not self.month:
            self.month = d.month
        if not self.year:
            self.year = d.year
        if not self.status:
            self.status = "Pending"

    def before_submit(self):
        self.status = "Paid"
        tenent = frappe.db.get_value("Airport Shop", self.shop, "tenent")
        email = frappe.db.get_value("Tenant", tenent, "email") if tenent else None
        if email:
            try:
                frappe.sendmail(
                    recipients=[email],
                    subject=f"Rent Receipt {self.name}",
                    message=f"Dear {tenent},<br>Thanks for the payment of <b>{self.amount}</b> for shop <b>{self.shop}</b>.",
                    reference_doctype=self.doctype,
                    reference_name=self.name,
                )
            except Exception:
                frappe.log_error(
                    "Failed sending rent receipt email", "RentReceiptEmail"
                )
