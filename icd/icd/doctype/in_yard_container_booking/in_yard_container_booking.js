// Copyright (c) 2025, Pal SHah and contributors
// For license information, please see license.txt

frappe.ui.form.on('In Yard Container Booking', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(__('Create Container Inspection'), function() {
                frappe.call({
                    method: "icd.icd.doctype.in_yard_container_booking.in_yard_container_booking.create_container_inspection",
                    args: {
                        booking_name: frm.doc.name
                    },
                    callback: function(r) {
                        if (r.message) {
                            frappe.set_route("form", "Container Inspection", r.message);
                        }
                    }
                });
            }, __("Create"));
        }
    }
});


