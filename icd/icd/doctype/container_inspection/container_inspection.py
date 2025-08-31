# Copyright (c) 2025, Pal SHah and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ContainerInspection(Document):
	pass

@frappe.whitelist()
def create_bulk_inspections(data):
    import json
    if isinstance(data, str):
        data = json.loads(data)

    inspections = []

    # Example: get matching In Yard Container Bookings by M BL No or H BL No
    filters = {}
    if data.get("m_bl_no"):
        filters["m_bl_no"] = data["m_bl_no"]
    if data.get("h_bl_no"):
        filters["h_bl_no"] = data["h_bl_no"]

    bookings = frappe.get_all("In Yard Container Booking", filters=filters, fields=["name"])

    for b in bookings:
        booking = frappe.get_doc("In Yard Container Booking", b.name)

        inspection = frappe.new_doc("Container Inspection")
        inspection.in_yard_container_booking = booking.name
        inspection.company = booking.company
        inspection.c_and_f_company = booking.c_and_f_company
        inspection.container_id = booking.container_id
        inspection.m_bl_no = booking.m_bl_no
        inspection.container_no = booking.container_no
        inspection.inspection_date = booking.inspection_date
        inspection.inspection_location = booking.inspection_location
        inspection.inspection_name = data.get("inspector_name")

        inspection.insert(ignore_permissions=True)
        inspections.append(inspection.name)

    frappe.db.commit()
    return inspections

@frappe.whitelist()
def create_service_order(inspection_name):
    inspection = frappe.get_doc("Container Inspection", inspection_name)

    # create new service order
    service_order = frappe.new_doc("Service Order")
    service_order.company = inspection.company
    service_order.c_and_f_company = inspection.c_and_f_company
    service_order.clearing_agent = inspection.clearing_agent
    service_order.consignee = inspection.consignee
    service_order.container_id = inspection.container_id
    service_order.container_no = inspection.container_no
    service_order.container_size = inspection.container_size
    # service_order.container_status = inspection.container_status
    service_order.container_location = inspection.new_container_location
    service_order.m_bl_no = inspection.m_bl_no
    service_order.port =  "TEAGTL"
    # service_order.country_of_destination = inspection.country_of_destination or "Saudi Arabia"
    # service_order.manifest = inspection.name   # link back to inspection

    # Optional extra fields (from inspection to service order)
    service_order.vessel_name = getattr(inspection, "vessel_name", None)
    service_order.posting_datetime = inspection.posting_datetime
    service_order.additional_note = inspection.additional_note

    # map child table: services
    for row in inspection.service:
        service_order.append("service", {
            "service": row.service
        })

    service_order.insert(ignore_permissions=True)
    frappe.db.commit()

    return service_order.name

