import frappe
from yhen.api.bin import get_actual_qty

#显示每行的库存数量
#仅限前端调用
@frappe.whitelist()
def set_actual_qty():
	locations = frappe.form_dict.get("locations")
	company = frappe.form_dict.get("company")
	res = {}
	for row in locations:
		res[row.name] = get_actual_qty(row.item_code, company=company, warehouse=row.warehouse or 1)
	frappe.response["message"] = res
