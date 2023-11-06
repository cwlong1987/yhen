import frappe

#物料号+仓库→库存
#warehouse
#	0 获取全部仓库的库存数量
#	1 仅获取物料默认仓库数量
#get_actual_qty("PTO-3611-4")
@frappe.whitelist()
def get_actual_qty(item_code, company=None, warehouse=1):
	company = company or frappe.defaults.get_user_default("company")
	if warehouse == 0:
		return frappe.db.get_values("Bin", {"item_code":item_code}, ["warehouse","actual_qty"])
	elif warehouse == 1 or isinstance(warehouse, str):
		if warehouse == 1:
			warehouse = frappe.db.get_value("Item Default", {"parent":item_code, "company":company}, ["default_warehouse"])
		if not warehouse is None:
			return frappe.db.get_values("Bin", {"item_code":item_code,"warehouse":warehouse}, ["warehouse","actual_qty"]) or 0
	elif isinstance(warehouse, list):
		if len(warehouse):
			return frappe.db.get_list("Bin", {"item_code":item_code,"warehouse":["in",warehouse]}, ["warehouse","actual_qty"])
	#获取全部
	return frappe.db.get_list("Bin", {"item_code":item_code}, ["warehouse","actual_qty"])
