# Copyright (c) 2025, Aravind Rajendran and contributors
# For license information, please see license.txt

import random
import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe.model.document import Document


class AirplaneFlight(WebsiteGenerator):

    def before_validate(self):
        self.duplicates_not_allowed()
        self._require_pilot()

    def before_insert(self):
        if not (self.gate_number or "").strip():
            self.assign_gate_number()

    def on_submit(self):
        if not (self.gate_number or "").strip():
            self.assign_gate_number()
        self.status = "Completed"
        self.update_ticket_gate_numbers()

    def before_update_after_submit(self):
        if self.gate_number != self.get_doc_before_save().gate_number:
            frappe.throw("Gate number change is not allowed after Boarding Starts.")

    def _require_pilot(self):
        has_pilot = any(
            (row.role or "").strip().lower() == "pilot" for row in (self.crew or [])
        )
        if not has_pilot:
            frappe.throw("Each flight must have at least one Pilot assigned.")

    def duplicates_not_allowed(self):
        seen = set()
        dups = set()
        for row in self.crew or []:
            key = (row.crew_member or "").strip().lower()
            if not key:
                continue
            if key in seen:
                full_name = (
                    frappe.db.get_value("Flight Crew", row.crew_member, "full_name")
                    or row.crew_member
                )
                dups.add(full_name)
            else:
                seen.add(key)
        if dups:
            frappe.throw(
                f"Duplicate crew assignment detected for: {', '.join(sorted(dups))}"
            )

    def assign_gate_number(self):
        self.gate_number = f"G-{random.randint(1, 6)}"

    def update_ticket_gate_numbers(self):
        if not self.name:
            return
        ticket_names = frappe.get_all(
            "Airplane Ticket",
            filters={"flight": self.name},
            pluck="name",
        )
        if not ticket_names:
            return
        for tn in ticket_names:
            frappe.db.set_value(
                "Airplane Ticket",
                tn,
                "gate_number",
                self.gate_number or "",
                update_modified=False,
            )
