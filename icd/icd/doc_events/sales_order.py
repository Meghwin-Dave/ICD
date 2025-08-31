import frappe
from frappe.utils import add_days, today

@frappe.whitelist()
def create_sales_order_from_bl(m_bl_no, h_bl_no=None):
    filters = {"m_bl_no": m_bl_no,"docstatus":1}
    if h_bl_no:
        filters["h_bl_no"] = h_bl_no
    

    service_orders = frappe.get_all(
        "Service Order",
        filters=filters,
        fields=[
            "name", "consignee", "company", "c_and_f_company",
            "manifest", "container_id", "m_bl_no"
        ]
    )

    created_orders = []
    for so in service_orders:
        # --- Consignee -> Customer ---
        if so.consignee:
            consignee_doc = frappe.get_doc("Consignee", so.consignee)
            customer = consignee_doc.customer  

        # --- Get Service Order full doc ---
        service_order_doc = frappe.get_doc("Service Order", so.name)

        # --- Fetch Container Details if exists ---
        container_doc = None
        if so.container_id:
            container_doc = frappe.get_doc("Container Details", so.container_id)

        # --- Create Sales Order ---
        sales_order = frappe.new_doc("Sales Order")
        sales_order.customer = customer
        sales_order.company = so.company

        # --- Custom Mappings ---
        sales_order.custom_m_bl_no = so.m_bl_no
        sales_order.custom_manifest = so.manifest
        sales_order.custom_container_id = so.container_id
        sales_order.custom_consignee = so.consignee or ""
        sales_order.custom_service_order = so.name
        sales_order.custom_c_and_f_company = so.c_and_f_company

        # --- Pull Container Details ---
        if container_doc:
            sales_order.custom_container_no = container_doc.container_no


        # --- Dates ---
        sales_order.transaction_date = today()
        sales_order.delivery_date = add_days(sales_order.transaction_date, 7)

        # --- Services -> Sales Order Items ---
        for srv in service_order_doc.service:
            item_code = srv.service
            if not frappe.db.exists("Item", item_code):
                frappe.throw("Item Not Exist")

            sales_order.append("items", {
                "item_code": item_code,
                "qty": srv.qtycbm or 1,
                "uom": "Nos",
                "description": srv.service,
                "delivery_date": sales_order.delivery_date
            })

        # --- Save & Submit ---
        sales_order.insert(ignore_permissions=True)
        doc = frappe.get_doc("Container Details",so.container_id)
        doc.db_set("status","At Gatepass")
        created_orders.append(sales_order.name)

    return {"created_orders": created_orders}
