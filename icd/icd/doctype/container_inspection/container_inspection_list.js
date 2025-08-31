frappe.listview_settings['Container Inspection'] = {
    onload: function(listview) {
        // Add Inner Button
        listview.page.add_inner_button(__('Bulk Inspections'), function() {
            let d = new frappe.ui.Dialog({
                title: "Bulk Inspections",
                fields: [
                    {fieldname:"m_bl_no", label:"M BL No", fieldtype:"Data"},
                    {fieldname:"h_bl_no", label:"H BL No", fieldtype:"Data"},
                    {fieldname:"inspector_name", label:"Inspector Name", fieldtype:"Data", reqd:1}
                ],
                primary_action_label: "Create Inspections",
                primary_action(values) {
                    frappe.call({
                        method: "icd.icd.doctype.container_inspection.container_inspection.create_bulk_inspections",
                        args: { data: values },
                        callback: function(r) {
                            if (r.message) {
                                frappe.msgprint(`✅ Created ${r.message.length} Inspections`);
                                d.hide();
                                listview.refresh();
                            }
                        }
                    });
                }
            });
            d.show();
        });
    }
};
