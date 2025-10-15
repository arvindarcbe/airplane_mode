// Copyright (c) 2025, Aravind Rajendran and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Airplane Ticket", {
// 	refresh(frm) {

// 	},
// });
// Custom client-side script for Airplane Ticket DocType
frappe.ui.form.on("Airplane Ticket", {
	refresh(frm) {
		frm.add_custom_button(
			"Assign seat",
			() => {
				const d = new frappe.ui.Dialog({
					title: "Select seat",
					fields: [
						{
							label: "Seat Number",
							fieldname: "seat_number",
							fieldtype: "Data",
							reqd: 1,
							default: frm.doc.seat || "",
						},
					],
					primary_action_label: "Assign",
					primary_action(values) {
						frm.set_value("seat", values.seat_number);
						d.hide();
						// Optional: save automatically
						// frm.save();
					},
				});
				d.show();
			},
			__("Actions")
		);
	},
});
