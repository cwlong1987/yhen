frappe.ui.form.on("BOM", {

	onload: function(frm) {
		frm.fields_dict['transit_section'].collapse();
	}

	refresh(frm) {
		//删除子物料过滤条件：按工单发料=是
		frm.set_query("item_code", "items", function(doc) {
			console.log("app自定义refresh");
			return {
				query: "erpnext.manufacturing.doctype.bom.bom.item_query",
				filters: {
					//"include_item_in_manufacturing": 1,
					"is_fixed_asset": 0
				}
			};
		});
	},

})
