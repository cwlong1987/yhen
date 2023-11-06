import frappe
import os
import importlib
###############################################################################
__version__ = "231104A"

patches_loaded = False
###############################################################################
# 猴子补丁，加载函数
###############################################################################
def load_monkey_patches():
	global patches_loaded

	if (
		patches_loaded
		or not getattr(frappe, "conf", None)
		or not "yhen" in frappe.get_installed_apps()
	):
		return

	for app in frappe.get_installed_apps():
		if app in ['frappe', 'erpnext']: continue

		folder = frappe.get_app_path(app, "monkey_patches")
		if not os.path.exists(folder): continue

		for module_name in os.listdir(folder):
			if not module_name.endswith(".py") or module_name == "__init__.py":
				continue

			importlib.import_module(f"{app}.monkey_patches.{module_name[:-3]}")

	patches_loaded = True


##############################################################################################
# 猴子补丁，加载处理
##############################################################################################
connect = frappe.connect

def custom_connect(*args, **kwargs):
	out = connect(*args, **kwargs)

	if frappe.conf.auto_commit_on_many_writes:
		frappe.db.auto_commit_on_many_writes = 1

	load_monkey_patches()
	return out


frappe.connect = custom_connect
