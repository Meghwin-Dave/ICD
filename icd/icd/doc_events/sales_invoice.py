# Trigger: After Submit on Sales Invoice

import frappe

def create_gatepass_from_invoice(doc, method):
    # fetch manifest
    manifest = None
    if doc.custom_manifest:
        manifest = frappe.get_doc("Manifest", doc.custom_manifest)

    # fetch container details
    container = None
    if doc.custom_container_id:
        container = frappe.get_doc("Container Details", doc.custom_container_id)

    # fetch service order
    service_order = None
    if getattr(doc, "custom_service_order", None):
        service_order = frappe.get_doc("Service Order", doc.custom_service_order)

    # create gatepass
    gatepass = frappe.new_doc("Gatepass")
    gatepass.company = doc.company
    gatepass.manifest = doc.custom_manifest
    gatepass.m_bl_no = doc.custom_m_bl_no
    gatepass.container_id = doc.custom_container_id

    if container:
        gatepass.container_no = container.container_no
        gatepass.size = container.size_ft
        gatepass.seal_no = container.seal_no1
        gatepass.good_decription = container.cargo_description

    # prefer Service Order → then Manifest
    if service_order:
        gatepass.c_and_f_company = service_order.c_and_f_company
        gatepass.clearing_agent = service_order.clearing_agent

    elif manifest:
        if not gatepass.c_and_f_company:
            gatepass.c_and_f_company = manifest.c_and_f_company
        if not gatepass.clearing_agent:
            gatepass.clearing_agent = manifest.clearing_agent

    gatepass.insert(ignore_permissions=True)
    frappe.msgprint(f"✅ Gatepass {gatepass.name} created from Sales Invoice {doc.name}")
