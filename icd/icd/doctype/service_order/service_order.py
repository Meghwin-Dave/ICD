# Copyright (c) 2025, Pal SHah and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ServiceOrder(Document):
	pass

@frappe.whitelist()
def create_bulk_service_order(m_bl_no, h_bl_no=None):
    # Fetch all related Container Inspections (or Bookings) by BL No
    inspections = frappe.get_all("Container Inspection", 
        filters={"m_bl_no": m_bl_no},
        fields=["name", "company", "c_and_f_company", "container_id", "container_no", "m_bl_no"]
    )

    service_orders = []
    for insp in inspections:
        so = frappe.new_doc("Service Order")
        so.company = insp.company
        so.c_and_f_company = insp.c_and_f_company
        so.container_id = insp.container_id
        so.container_no = insp.container_no
        so.m_bl_no = insp.m_bl_no
        if h_bl_no:
            so.h_bl_no = h_bl_no
        so.insert(ignore_permissions=True)
        service_orders.append(so.name)

    frappe.db.commit()
    return service_orders
