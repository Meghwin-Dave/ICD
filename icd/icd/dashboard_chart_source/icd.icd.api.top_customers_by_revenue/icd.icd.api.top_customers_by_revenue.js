frappe.provide("frappe.dashboards.chart_sources");

frappe.dashboards.chart_sources["icd.icd.api.top_customers_by_revenue"] = {
	method: "icd.api.top_customers_by_revenue",
	filters: [
		{ fieldname: "from_date", label: __("From Date"), fieldtype: "Date" },
		{ fieldname: "to_date", label: __("To Date"), fieldtype: "Date" },
		{ fieldname: "limit", label: __("Limit"), fieldtype: "Int", default: 10 },
	],
};


