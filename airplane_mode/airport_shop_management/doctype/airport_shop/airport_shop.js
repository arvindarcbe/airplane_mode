// Copyright (c) 2025, Aravind Rajendran and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airport Shop", {
	refresh(frm) {
		if (!frm.doc.name) return;
		frm.add_custom_button(
			"Create Rent Receipt",
			() => {
				frappe.new_doc("Rent Receipt", {
					shop: frm.doc.name,
					tenent: frm.doc.tenent,
					amount: frm.doc.rent,
				});
			},
			__("Actions")
		);
	},
});
