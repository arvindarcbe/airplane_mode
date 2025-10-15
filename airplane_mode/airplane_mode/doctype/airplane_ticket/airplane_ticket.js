// Copyright (c) 2025, Aravind Rajendran and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Airplane Ticket", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on("Airplane Ticket", {
	refresh(frm) {
		frm.add_custom_button(
			"Assign seat",
			function () {
				let dialog = new frappe.ui.Dialog({
					title: "Select seat",
					fields: [
						{
							label: "Seat Number",
							fieldname: "seat_number",
							fieldtype: "Data",
							reqd: true,
						},
					],
					primary_action_label: "Assign",
					primary_action(values) {
						frm.set_value("seat", values.seat_number);
						dialog.hide();
					},
				});

				dialog.show();
			},
			__("Actions")
		);
	},
});
