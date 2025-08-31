// Copyright (c) 2025, Pal SHah and contributors
// For license information, please see license.txt

frappe.ui.form.on('Container Inspection', {
    refresh: function(frm) {
        if (!frm.is_new() && frm.doc.docstatus == 1) {
            frm.add_custom_button(__('Create Service Order'), function() {
                frappe.call({
                    method: "icd.icd.doctype.container_inspection.container_inspection.create_service_order",
                    args: { inspection_name: frm.doc.name },
                    callback: function(r) {
                        if (r.message) {
                            frappe.set_route("Form", "Service Order", r.message);
                        }
                    }
                });
            });
        }
    }
});

