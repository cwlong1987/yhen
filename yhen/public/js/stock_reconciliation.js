//库存调账
frappe.ui.form.on("Stock Reconciliation Item", {
	//子表：物料→仓库+成本价
	item_code: function(frm, cdt, cdn) {
		let child = locals[cdt][cdn];
		if (child.item_code === undefined || child.item_code === null || child.item_code === "")
			return;
		console.log("old:"+child.item_code+" "+child.warehouse+" "+child.valuation_rate);
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
					frappe.model.set_value(cdt, cdn, "valuation_rate", r.message.valuation_rate);
					for (const row of r.message.item_defaults) { //用公司确定仓库
						if (row.company === frm.doc.company) {
							console.log(`成本价=${r.message.valuation_rate} 仓库=${row.default_warehouse}`);
							frappe.model.set_value(cdt, cdn, "warehouse", row.default_warehouse);
							return;
						}
					}
				}
			}
		});
	},

});
