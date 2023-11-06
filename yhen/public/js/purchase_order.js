//✅委外自动使用旧版的委外流程
//frappe.ui.form.on('Purchase Order', {
	//is_subcontracted: (frm) => frm.set_value('is_old_subcontracting_flow', frm.doc.is_subcontracted)
//})

//提交时:有单价=0则再次确认
frappe.ui.form.on("Purchase Order", {
	before_submit: async function(frm) {
		for (const row of frm.doc.items) {
			if(row.rate <= 0) {
				let pm = new Promise((resolve, reject) => {
					frappe.confirm(
						`行${row.idx} 物料: <b>${row.item_code}</b> 单价为 0, 确认提交吗？`,
						() => resolve(),
						() => reject()
					);
				});
				await pm.then(
					() => frappe.show_alert("已提交", 3),
					() => {
						frappe.validated = false;
						frappe.show_alert("已取消提交", 3)
					}
				);
				return;
			}
		};
	},
})
