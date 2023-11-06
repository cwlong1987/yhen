frappe.ui.form.on("Pick List", {
	//每次进入表单时根据(料号+仓库)生成库存数
	onload: function(frm) {
		if (frm.is_new() || !frm.doc.locations.length)
			return;
		let ao_locations = frm.doc.locations.map((row) => ({
			'name': row.name,
			'item_code': row.item_code,
			'warehouse': row.warehouse,
		}));
		console.log(ao_locations);
		frappe.call({
			method: "yhen.api.pick_list.set_actual_qty",
			args:{
				"locations": ao_locations,
				"company": frm.doc.company,
			},
			freeze: true,
			freeze_message: __("正在从后台获取库存数量..."),
			callback: function(r) {
				console.log(r.message);
				if (!r.exc && r.message){
					//message是行名：物料号键值对，{'name':'item_code'}
					frm.doc.locations.forEach((row) => {
						console.log(row.name+" "+r.message[row.name]);
						frappe.model.set_value(row.doctype, row.name, 'custom_actual_qty', r.message[row.name]);
					})
					refresh_field('locations');
				}
			}
		})
	},
});

frappe.ui.form.on("Pick List Item", {

	//物料号→库存数量(custom_actual_qty)
	item_code: function(frm, cdt, cdn) {
		let child = locals[cdt][cdn];
		if (child.item_code === undefined || child.item_code === null || child.item_code === "")
			return;
		console.log(child);
		frappe.call({
			method: "yhen.api.bin.get_actual_qty",
			args: {
				item_code: child.item_code,
			},
			callback: function(r) {
				console.log(r.message);
				if (r.message) {
					actual_qty = 0;
					for (const arr of r.message) {
						actual_qty += arr[1];
					}
					frappe.model.set_value(cdt, cdn, "custom_actual_qty", actual_qty);
				}
			}
		});
	},

});

