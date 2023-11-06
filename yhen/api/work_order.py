import frappe
from frappe import _
from frappe.utils import flt

#来源 zelin_pp/api.py
@frappe.whitelist()
def work_order_split_qty(work_order_name, qty):
	qty = flt(qty)
	doc = frappe.get_doc("Work Order", work_order_name)
	if qty <= 0 or qty >= doc.qty:
		frappe.throw(_("(0 <= Qty <= {0}) error".format(doc.qty)))
	doc2 = frappe.copy_doc(doc)
	doc2.qty = doc.qty - qty
	doc1 = doc if doc.docstatus == 0 else frappe.copy_doc(doc)
	doc1.qty = qty
	if doc.docstatus == 1:
		doc.cancel()
		doc1.amended_from = doc.name
		doc1.submit()
	else:
		doc1.save()
	doc2.save()
	return doc1.name

# class Hy_WorkOrder:
#	 @staticmethod
