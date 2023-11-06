import frappe

# item
#更新子表：物料编号→[供应商]
@frappe.whitelist()
def mr_items_update_supply(name):
	company = frappe.defaults.get_user_default("company")
	doc = frappe.get_doc("Material Request", name)
	for row in doc.items:
		row.item_supplier = frappe.get_value("Item Default", {"parent": row.item_code, "company": company}, "default_supplier")
	doc.save()
	frappe.db.commit()
