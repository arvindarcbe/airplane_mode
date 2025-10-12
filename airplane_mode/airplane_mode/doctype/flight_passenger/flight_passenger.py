import frappe
from frappe.model.document import Document


class FlightPassenger(Document):
    def before_save(self):
        # Safely handle missing last name
        first = (self.first_name or "").strip()
        last = (self.last_name or "").strip()

        if first and last:
            self.full_name = f"{first} {last}"
        else:
            self.full_name = first or last
