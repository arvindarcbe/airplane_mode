// Copyright (c) 2025, Aravind Rajendran and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Airplane Ticket", {
// 	refresh(frm) {

// 	},
// });
// Custom client-side script for Airplane Ticket DocType
frappe.ui.form.on("Airplane Ticket", {
	refresh(frm) {
		// Add a custom button "Assign seat" under the "Actions" group
		frm.add_custom_button(
			"Assign seat",
			function () {
				// Create a dialog (popup) to enter/select seat number
				let dialog = new frappe.ui.Dialog({
					title: "Select seat", // Title of the dialog
					fields: [
						{
							label: "Seat Number", // Label shown in dialog
							fieldname: "seat_number", // Internal name for field
							fieldtype: "Data", // Data type (simple text input)
							reqd: true, // Field is mandatory
						},
					],
					primary_action_label: "Assign", // Button label inside dialog

					// Function triggered when user clicks "Assign"
					primary_action(values) {
						// Set the selected seat number into the 'seat' field of the form
						frm.set_value("seat", values.seat_number);
						dialog.hide(); // Close the dialog after assigning
					},
				});

				// Show the dialog popup
				dialog.show();
			},
			__("Actions") // Group the button under "Actions" dropdown
		);
	},
});
