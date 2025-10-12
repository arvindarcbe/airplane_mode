// frappe.ready(function() {
// 	// bind events here
// })

frappe.web_form.on("load", () => {
	const qp = frappe.utils.get_query_params();
	if (qp.flight) {
		frappe.web_form.set_value("flight", qp.flight);
	}
	// set any price you want here (or compute via server call if you prefer)
	frappe.web_form.set_value("flight_price", 4500);
});
