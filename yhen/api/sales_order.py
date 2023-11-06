import frappe
import json

#从前台传入items，客户料号→料号
@frappe.whitelist()
def so_refcode_to_itemcode():
	#提取js传入参数
	ao_items = json.loads(frappe.form_dict.get("items"))
	customer_name = frappe.form_dict.get("customer")
	#获取js传入的全部客户料号(非重复)
	s_ref_code = {r.get("customer_item_code") for r in ao_items}
	#从xx表获取所有客户料号对应的【料号】
	item_code_map = dict(
		frappe.get_all("Item Customer Detail",
			filters = {"customer_name":customer_name,
						"ref_code":("in", s_ref_code)
					},
			fields = ["ref_code", "parent"],
			as_list = 1
	))
	# frappe.msgprint(customer_name+"--"+str(s_ref_code)+"--"+str(items))
	#返回行id：料号键值对（字典)
	result = {r.get("name"):item_code_map.get(r.get("customer_item_code")) for r in ao_items}
	frappe.response["message"] = result
