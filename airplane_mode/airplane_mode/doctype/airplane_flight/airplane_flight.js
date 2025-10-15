// Copyright (c) 2025, Aravind Rajendran and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Airplane Flight", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on("Airplane Flight", {
	refresh(frm) {
		frm.add_custom_button(
			"Assign gate",
			() => {
				const d = new frappe.ui.Dialog({
					title: "Set Gate Number",
					fields: [
						{
							label: "Gate Number",
							fieldname: "gate_number",
							fieldtype: "Data",
							reqd: 1,
							default: frm.doc.gate_number || "",
						},
					],
					primary_action_label: "Assign",
					primary_action(values) {
						frm.set_value("gate_number", values.gate_number);
						d.hide();
						// uncomment if you want to auto-save:
						// frm.save();
					},
				});
				d.show();
			},
			__("Actions")
		);
	},
});
