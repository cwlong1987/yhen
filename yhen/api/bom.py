import frappe

@frappe.whitelist()
def bom_update_bom_no():
	#获取所有最新可用BOM
	boms = frappe.get_list("BOM", {"is_default":1,"docstatus":1}, ["name","item"])
	#NOTE 记录母件料号 和 BOM号到dic
	dic = {bom.item: bom.name for bom in boms}
	res = [] #记录修改内容
	#遍历最新可用BOM
	for bom in boms:
		#根据单个BOM号获取所有子行的["name",料号]
		rs = frappe.get_all("BOM Item", filters={"parent": bom.name}, fields=["name","item_code"])
		for row in rs:
			#判断逻辑，赋值到 v1
			v0 = ""
			v1 = None
			if row.bom_no is None or row.bom_no == "": #当前行没有BOM号
				if row.item_code in dic: #当前行子物料有主BOM
					v1 = dic[row.item_code]
			else:
				v0 = row.bom_no
				if row.item_code in dic: #子物料有主BOM
					if dic[row.item_code] != row.bom_no:
						v1 = dic[row.item_code]
				else: #主BOM已失效(被引用的BOM默认是无法删除的，只能用代码删)，则清除
					v1 = ""
			#统一在这里修改
			if v1 is not None:
				res.append([bom.name, row.item_code, v0, v1]) #记录[BOM号，子件料号，原BOM号, 新BOM号]
				frappe.db.set_value("BOM Item", row.name, "bom_no", v1)
	frappe.db.commit()
	return res
