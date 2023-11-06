frappe.ui.form.on("Warehouse", {

	onload: function(frm) {
		frm.fields_dict['currency_detail'].collapse();
	}

})
