import frappe
from frappe import _
from erpnext.stock.doctype.pick_list.pick_list import PickList

class CustomPickList(PickList):
	@frappe.whitelist()
	def set_item_locations(self, save=False):
		if self.fetch_item_locations:
			super(CustomPickList,self).set_item_locations(save=save)

	def before_submit(self):
		pass
		#if not self.fetch_item_locations:
		#	frappe.throw(_("Please make sure Auto Assign Item Location checked before submit"))
		#super(CustomPickList,self).before_submit()
