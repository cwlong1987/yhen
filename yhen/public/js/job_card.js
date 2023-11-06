frappe.ui.form.on("Job Card", {

	onload: function(frm) {
		frm.fields_dict['timing_detail'].collapse();
	}

})
