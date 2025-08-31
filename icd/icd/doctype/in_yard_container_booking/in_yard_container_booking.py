# Copyright (c) 2025, Pal SHah and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class InYardContainerBooking(Document):
	pass


import frappe

@frappe.whitelist()
def get_container_details(m_bl_no):
    containers = frappe.get_all(
        "Container Details",
        filters={"m_bl_no": m_bl_no},
        fields=["name", "container_no", "cargo_type", "size_ft", "volume", "weight", "no_of_packages"]
    )
    return containers


@frappe.whitelist()
def create_booking_with_container(data):
    import json
    if isinstance(data, str):
        data = json.loads(data)

    # Check containers for this M B/L No
    containers = get_container_details(data.get("m_bl_no"))

    if not containers:
        frappe.throw(f"No containers found for M B/L No {data.get('m_bl_no')}")

    created_bookings = []
    for c in containers:
        booking = frappe.new_doc("In Yard Container Booking")
        booking.update({
            "m_bl_no": data.get("m_bl_no"),
            "h_bl_no": data.get("h_bl_no"),
            "company":data.get("company"),
            "c_and_f_company": data.get("c_and_f_company"),
            "inspection_date": data.get("inspection_date"),
            "inspection_location": data.get("inspection_location"),
            "container_no": c.container_no,
            "container_id":c.name,
            "cargo_type": c.cargo_type,
            "size_ft": c.size_ft,
            "volume": c.volume,
            "weight": c.weight,
            "no_of_packages": c.no_of_packages
        })
        booking.insert(ignore_permissions=True)
        created_bookings.append(booking.name)
        doc = frappe.get_doc("Container Details",c.name)
        doc.db_set("status","In Inspection")

    frappe.db.commit()
    return {"booking": created_bookings, "containers": [c.container_no for c in containers]}

@frappe.whitelist()
def get_booking_defaults(m_bl_no):
    # Assuming details stored in Container Detail or another DocType
    container = frappe.db.get_value(
        "Container Detail",
        {"m_bl_no": m_bl_no},
        ["c_and_f_company", "clearing_agent", "inspection_date", "inspection_location"],
        as_dict=True
    )
    return container or {}

@frappe.whitelist()
def create_container_inspection(booking_name):
    booking = frappe.get_doc("In Yard Container Booking", booking_name)

    inspection = frappe.new_doc("Container Inspection")
    inspection.in_yard_container_booking = booking.name
    inspection.company = booking.company
    inspection.c_and_f_company = booking.c_and_f_company
    inspection.clearing_agent = getattr(booking, "clearing_agent", None)
    inspection.consignee = getattr(booking, "consignee", None)
    inspection.container_id = booking.container_id
    inspection.m_bl_no = booking.m_bl_no
    inspection.container_no = booking.container_no
    inspection.inspection_date = booking.inspection_date
    inspection.inspection_location = booking.inspection_location
    inspection.additional_note = getattr(booking, "additional_note", None)

    inspection.insert(ignore_permissions=True)
    frappe.db.commit()

    return inspection.name

