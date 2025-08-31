// Copyright (c) 2025, Pal SHah and contributors
// For license information, please see license.txt

frappe.query_reports["Container Booking"] = {
    "filters": [
        {
            "fieldname": "m_bl_no",
            "label": "M B/L No",
            "fieldtype": "Data",
            "reqd": 0
        },
        {
            "fieldname": "from_date",
            "label": "From Date",
            "fieldtype": "Date"
        },
        {
            "fieldname": "to_date",
            "label": "To Date",
            "fieldtype": "Date"
        }
    ]
};
