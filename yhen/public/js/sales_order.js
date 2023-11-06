//客户料号→料号
frappe.ui.form.on("Sales Order", {
	custom_get_item_code: function(frm){
		//获取所有子表 name, 客户料号
		let ao_items = frm.doc.items.map((item) => ({"name": item.name, "customer_item_code": item.customer_item_code}));
		console.log(ao_items);
		frappe.call({
			method: "yhen.api.sales_order.so_refcode_to_itemcode",
			args:{
				items: ao_items,
				"customer": frm.doc.customer,
			},
			freeze: true,
			freeze_message: __("正在获取客户料号..."),
			callback: function(r) {
				console.log(r.message);
				if (!r.exc && r.message) {
					//message是行名：物料号键值对，{"name":"item_code"}
					frm.doc.items.forEach((item) => {
						let item_code = r.message[item.name];
						if (item_code)
							frappe.model.set_value(item.doctype, item.name, "item_code", item_code);
					})
					refresh_field("items");
				}
			}
	})
}
})
