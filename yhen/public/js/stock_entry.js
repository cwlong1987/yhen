//翻译移动类型(stock_entry_type)
frappe.listview_settings["Stock Entry"] = {
	onload: function(frm) {
		frm.fields_dict['section_break_jwgn'].collapse();
	}

	formatters: {
		stock_entry_type: (value, df, doc) => __(value),
	},

};

frappe.ui.form.on("Stock Entry Detail", {
	//物料号→发料仓+收料仓
	//有工单的，一般都由工单带入，不需要手工输入
	item_code: function (frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		if (row.item_code) {
			frappe.call({
				method: "erpnext.stock.doctype.item.item.get_item_details",
				args: {
					item_code: row.item_code,
					company: frm.doc.company,
				},
				callback: function (r) {
					let default_warehouse = r.message.default_warehouse; //默认仓
					if (r.message) {
						console.log(frm.doc.purpose+" "+default_warehouse);
						switch (frm.doc.purpose) {
							case "Manufacture":
							case "Material Receipt":
								console.log("设置收料仓");
								frappe.model.set_value(cdt, cdn, "t_warehouse", default_warehouse);
								break;
							case "Material Transfer for Manufacture":
							case "Material Issue":
							case "Send to Subcontractor":
							default:
								console.log("设置发料仓");
								frappe.model.set_value(cdt, cdn, "s_warehouse", default_warehouse);
								break;
						}
						//frappe.model.set_value(cdt, cdn, {
						//	"s_warehouse": s_warehouse,
						//	"t_warehouse": r.message.default_in_transit_warehouse,
						//});
					}
				},
			});
		}
	}
});
