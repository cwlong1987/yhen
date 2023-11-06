import frappe
from frappe import _, msgprint
from frappe.utils import (
	add_days,
	ceil,
	cint,
	comma_and,
	flt,
	get_link_to_form,
	getdate,
	now_datetime,
	nowdate,
)

from erpnext.manufacturing.doctype.work_order.work_order import get_item_details
from erpnext.setup.doctype.item_group.item_group import get_item_group_defaults
from erpnext.stock.get_item_details import get_conversion_factor

from erpnext.manufacturing.doctype.production_plan.production_plan import ProductionPlan

class CustomProductionPlan(ProductionPlan):
#按钮1: 推单采购订单: 增加了料号
#目前是在zelin_pp的override.py里调用原函数
	def make_subcontracted_purchase_order(self, subcontracted_po, purchase_orders):
		if not subcontracted_po:
			return

		#以供应商分组，每个供应商一张委外采购订单
		for supplier, po_list in subcontracted_po.items():
			#委外采购订单
			#   主表
			po = frappe.new_doc("Purchase Order")
			po.company = self.company
			po.supplier = supplier
			po.schedule_date = getdate(po_list[0].schedule_date) if po_list[0].schedule_date else nowdate()
			po.is_subcontracted = 1
			#   子表
			for row in po_list:
				po_data = {
					"item_code": row.production_item, #hyaray
					"fg_item": row.production_item,
					"warehouse": row.fg_warehouse,
					"production_plan_sub_assembly_item": row.name,
					"bom": row.bom_no,
					"production_plan": self.name,
					"fg_item_qty": row.qty,
				}

				#添加以下字段(若有值)
				for field in [
					"schedule_date",
					"qty",
					"description",
					"production_plan_item",
				]:
					po_data[field] = row.get(field)
				po.append("items", po_data)

			po.is_old_subcontracting_flow = 1 #hyaray 否则 set_missing_values 报错
			po.set_missing_values()
			po.flags.ignore_mandatory = True
			po.flags.ignore_validate = True
			po.insert()
			purchase_orders.append(po.name)

#按钮2: 添加物料需求-增加供应商
	@frappe.whitelist()
	def make_material_request(self):
		"""Create Material Requests grouped by Sales Order and Material Request Type"""
		material_request_list = []
		material_request_map = {}

		for item in self.mr_items:
			item_doc = frappe.get_cached_doc("Item", item.item_code)

			#需求类型
			material_request_type = item.material_request_type or item_doc.default_material_request_type

			# key for Sales Order:Material Request Type:Customer
			key = "{}:{}:{}".format(item.sales_order, material_request_type, item_doc.customer or "")
			schedule_date = item.schedule_date or add_days(nowdate(), cint(item_doc.lead_time_days))

			#material_request_map 添加键值对，值=新建的物料需求单
			if not key in material_request_map:
				# make a new MR for the combination
				material_request_map[key] = frappe.new_doc("Material Request")
				material_request = material_request_map[key]
				material_request.update(
					{
						"transaction_date": nowdate(),
						"status": "Draft",
						"company": self.company,
						"material_request_type": material_request_type,
						"customer": item_doc.customer or "",
					}
				)
				material_request_list.append(material_request)
			else:
				material_request = material_request_map[key]

			# add item
			supplier = frappe.get_value("Item Default", {"parent":item.item_code, "company":self.company}, "default_supplier") #hyaray
			material_request.append(
				"items",
				{
					"item_code": item.item_code,
					"item_supplier": supplier, #hyaray
					"from_warehouse": item.from_warehouse
					if material_request_type == "Material Transfer"
					else None,
					"qty": item.quantity,
					"schedule_date": schedule_date,
					"warehouse": item.warehouse,
					"sales_order": item.sales_order,
					"production_plan": self.name,
					"material_request_plan_item": item.name,
					"project": frappe.db.get_value("Sales Order", item.sales_order, "project")
					if item.sales_order
					else None,
				},
			)

		for material_request in material_request_list:
			# submit
			material_request.flags.ignore_permissions = 1
			material_request.run_method("set_missing_values")

			material_request.save()
			if self.get("submit_material_request"):
				material_request.submit()

		frappe.flags.mute_messages = False

		if material_request_list:
			material_request_list = [
				"""<a href="/app/Form/Material Request/{0}">{1}</a>""".format(m.name, m.name)
				for m in material_request_list
			]
			msgprint(_("{0} created").format(comma_and(material_request_list)))
		else:
			msgprint(_("No material request created"))

#子表3: 采购件: 仓库修改为物料默认仓库
	def get_material_request_items(
		row, sales_order, company, ignore_existing_ordered_qty, include_safety_stock, warehouse, bin_dict
	):
		total_qty = row["qty"]

		required_qty = 0
		if ignore_existing_ordered_qty or bin_dict.get("projected_qty", 0) < 0:
			required_qty = total_qty
		elif total_qty > bin_dict.get("projected_qty", 0):
			required_qty = total_qty - bin_dict.get("projected_qty", 0)
		if required_qty > 0 and required_qty < row["min_order_qty"]:
			required_qty = row["min_order_qty"]
		item_group_defaults = get_item_group_defaults(row.item_code, company)

		if not row["purchase_uom"]:
			row["purchase_uom"] = row["stock_uom"]

		if row["purchase_uom"] != row["stock_uom"]:
			if not (row["conversion_factor"] or frappe.flags.show_qty_in_stock_uom):
				frappe.throw(
					_("UOM Conversion factor ({0} -> {1}) not found for item: {2}").format(
						row["purchase_uom"], row["stock_uom"], row.item_code
					)
				)

				required_qty = required_qty / row["conversion_factor"]

		if frappe.db.get_value("UOM", row["purchase_uom"], "must_be_whole_number"):
			required_qty = ceil(required_qty)

		if include_safety_stock:
			required_qty += flt(row["safety_stock"])

		item_details = frappe.get_cached_value(
			"Item", row.item_code, ["purchase_uom", "stock_uom"], as_dict=1
		)

		conversion_factor = 1.0
		if (
			row.get("default_material_request_type") == "Purchase"
			and item_details.purchase_uom
			and item_details.purchase_uom != item_details.stock_uom
		):
			conversion_factor = (
				get_conversion_factor(row.item_code, item_details.purchase_uom).get("conversion_factor") or 1.0
			)

		if required_qty > 0:
			return {
				"item_code": row.item_code,
				"item_name": row.item_name,
				"quantity": required_qty / conversion_factor,
				"conversion_factor": conversion_factor,
				"required_bom_qty": total_qty,
				"stock_uom": row.get("stock_uom"),
				"warehouse": frappe.get_value("Item Default", {"parent":row.item_code, "company":company}, "default_warehouse"), #hyaray
				#hyaray "warehouse": warehouse
				#hyaray or row.get("source_warehouse")
				#hyaray or row.get("default_warehouse")
				#hyaray or item_group_defaults.get("default_warehouse"),
				"safety_stock": row.safety_stock,
				"actual_qty": bin_dict.get("actual_qty", 0),
				"projected_qty": bin_dict.get("projected_qty", 0),
				"ordered_qty": bin_dict.get("ordered_qty", 0),
				"reserved_qty_for_production": bin_dict.get("reserved_qty_for_production", 0),
				"min_order_qty": row["min_order_qty"],
				"material_request_type": row.get("default_material_request_type"),
				"sales_order": sales_order,
				"description": row.get("description"),
				"uom": row.get("purchase_uom") or row.get("stock_uom"),
			}
