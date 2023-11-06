import frappe

#返回权限where表达式字符串
def get_permission_query_conditions(user):
	roles = frappe.get_roles(user)
	if "Sales User" in roles and "Purchase User" in roles:
		return "1=1"
	if "Sales User" in roles:
		return "`tabItem Price`.selling=1"
	elif "Purchase User" in roles:
		return "`tabItem Price`.buying=1"
	else:
		return "0=1"
