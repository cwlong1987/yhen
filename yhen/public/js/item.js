frappe.ui.form.on("Item", {

	onload: function(frm) {
		frm.fields_dict['supplier_details'].collapse();
		frm.fields_dict['customer_details'].collapse();
	}

})
