//待生产物料：物料→生产类型(委外|采购件=采购，工单入库=自制)
frappe.ui.form.on("Production Plan Item", {
	item_code: function(frm, cdt, cdn) {
		let child = locals[cdt][cdn];
		if (child.item_code === undefined || child.item_code === null || child.item_code === "")
			return;
		console.log(child.item_code);
		frappe.call({
			method: "frappe.client.get",
			args: {
				doctype: "Item",
				filters: {
					name: child.item_code
				},
			},
			callback: function(r) {
				if (r.message) {
					for (const row of r.message.item_defaults) { //用公司确定仓库
						if (row.company === frm.doc.company) {
							//console.log(row.default_warehouse);
							frappe.model.set_value(cdt, cdn, "warehouse", row.default_warehouse);
							return;
						}
					}
				}
			}
		});
	},
});
