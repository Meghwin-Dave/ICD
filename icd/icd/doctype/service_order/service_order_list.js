frappe.listview_settings['Service Order'] = {
    onload(listview) {
        listview.page.add_inner_button(__('Create Bulk Service Order'), function() {
            let d = new frappe.ui.Dialog({
                title: 'Bulk Service Order',
                fields: [
                    {
                        label: 'M B/L No',
                        fieldname: 'm_bl_no',
                        fieldtype: 'Data',
                        reqd: 1
                    },
                    {
                        label: 'H B/L No',
                        fieldname: 'h_bl_no',
                        fieldtype: 'Data'
                    }
                ],
                primary_action_label: 'Create Orders',
                primary_action(values) {
                    frappe.call({
                        method: "icd.icd.doctype.service_order.service_order.create_bulk_service_order",
                        args: values,
                        callback: function(r) {
                            if (!r.exc) {
                                frappe.msgprint(__('Created {0} Service Orders', [r.message.length]));
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
