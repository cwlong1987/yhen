from . import __version__ as app_version

app_name = "yhen"
app_title = "Yhen"
app_publisher = "hyaray"
app_description = "Yuehuan ERPNext"
app_email = "hyaray@vip.qq.com"
app_license = "MIT"

app_include_css = [
	"/assets/yhen/css/print.css",
	"/assets/yhen/css/form.css",
]
#app_include_js = ["public/js/app.bundle.js"]

doctype_js = {
	"BOM": "public/js/bom.js",
	"Item": "public/js/item.js",
	"Job Card": "public/js/job_card.js",
	"Pick List": "public/js/pick_list.js",
	"Production Plan": "public/js/production_plan.js.js",
	"Sales Order": "public/js/sales_order.js",
	"Stock Entry": "public/js/stock_entry.js",
	"Stock Reconciliation": "public/js/stock_reconciliation.js",
	"Purchase Order": "public/js/purchase_order.js",
	"Warehouse": "public/js/warehouse.js",
	#"Word Order": "public/js/work_order.js",
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}

jinja = {
	"methods": [
		"yhen.utils.qrcode_create",
		],
	"filters": [
		"yhen.utils.date_notime",
		],
}

permission_query_conditions = {
	"Item Price": "yhen.api.item_price.get_permission_query_conditions",
}

override_doctype_class = {
	"Production Plan": "yhen.override.production_plan.CustomProductionPlan",
	"Pick List": "yhen.override.pick_list.CustomPickList",
}

doc_events = {
	"Purchase Order": {
		"before_insert": "yhen.api.purchase_order.set_old_subcontracting_flow",
	},
	#"Pick List": {
	#	"after_insert": "yhen.api.pick_list.set_actual_qty",
	#},
}
