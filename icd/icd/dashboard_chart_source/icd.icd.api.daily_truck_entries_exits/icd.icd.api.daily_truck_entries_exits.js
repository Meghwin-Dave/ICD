frappe.provide("frappe.dashboards.chart_sources");

frappe.dashboards.chart_sources["icd.icd.api.daily_truck_entries_exits"] = {
	method: "icd.api.daily_truck_entries_exits",
	filters: [
		{ fieldname: "from_date", label: __("From Date"), fieldtype: "Date" },
		{ fieldname: "to_date", label: __("To Date"), fieldtype: "Date" },
	],
};


