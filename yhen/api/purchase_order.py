import frappe

#委外自动使用旧版流程(hooks.py: doc_events: Before Insert)
def set_old_subcontracting_flow(doc, *args, **kwargs):
	if doc.is_subcontracted and [True for row in doc.items if row.production_plan]:
		doc.is_old_subcontracting_flow = 1
		#for row in doc.items:
		#	row.item_code = row.fg_item
		#	row.fg_item = ""
		#taxes = frappe.call(
		#	"erpnext.controllers.accounts_controller.get_taxes_and_charges",
		#	masterdoctype = "Purchase Taxes and Charges Template",
		#	master_name = doc.taxes_and_charges
		#	)
		#for tax in taxes or []:
		#	doc.append("taxes", tax)
		#doc.run_method("set_missing_values")
		#doc.run_method("calculate_taxes_and_totals")
