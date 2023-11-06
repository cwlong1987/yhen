# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
from __future__ import print_function, unicode_literals

import json
import frappe
import subprocess
from frappe import _

#####################################################################
## 安装触发函数
####################################################################
# install-app，安装前触发
def before_install():
	command = "source env/bin/activate && pip install qrcode"
	subprocess.run(command, shell=True)

# install-app，安装后触发
def after_install():
	insertWarehouseType()
	def insertWarehouseType():
		print("insertWarehouseType")
		doc = frappe.get_doc({"doctype":"Warehouse Type","name":"yhen"})
		doc.insert()
		doc.save()
