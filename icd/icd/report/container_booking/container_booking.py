import frappe

def execute(filters=None):
    if not filters: filters = {}

    columns = [
        {"label": "Container No", "fieldname": "container_no", "fieldtype": "Data", "width": 120},
        {"label": "M B/L No", "fieldname": "m_bl_no", "fieldtype": "Data", "width": 150},
        {"label": "Seal", "fieldname": "container_seal", "fieldtype": "Data", "width": 100},
        {"label": "Size (ft)", "fieldname": "container_size", "fieldtype": "Data", "width": 100},
        {"label": "C & F Company", "fieldname": "c_and_f_company", "fieldtype": "Data", "width": 150},
        {"label": "Consignee", "fieldname": "consignee", "fieldtype": "Link", "options": "Consignee", "width": 150},
        {"label": "Location", "fieldname": "container_location", "fieldtype": "Data", "width": 120},
        {"label": "Date", "fieldname": "posting_date", "fieldtype": "Date", "width": 120},
        {"label": "Description", "fieldname": "description", "fieldtype": "Small Text", "width": 200},
    ]

    conditions = ""
    values = {}

    if filters.get("m_bl_no"):
        conditions += " AND so.m_bl_no = %(m_bl_no)s"
        values["m_bl_no"] = filters["m_bl_no"]

    if filters.get("from_date"):
        conditions += " AND so.posting_datetime >= %(from_date)s"
        values["from_date"] = filters["from_date"]

    if filters.get("to_date"):
        conditions += " AND so.posting_datetime <= %(to_date)s"
        values["to_date"] = filters["to_date"]

    data = frappe.db.sql(f"""
        SELECT 
            cd.container_no,
            so.m_bl_no,
            cd.seal_no1,
            cd.size_ft,
            so.c_and_f_company,
            so.consignee,
            cd.current_location,
            DATE(so.posting_datetime) as posting_date,
            cd.cargo_description
        FROM `tabContainer Details` cd
        LEFT JOIN `tabService Order` so ON so.container_id = cd.name
        WHERE 1=1 {conditions}
        ORDER BY so.posting_datetime DESC
    """, values, as_dict=True)

    return columns, data
