frappe.listview_settings['Sales Order'] = {
    onload: function(listview) {
        listview.page.add_inner_button(__('Create from M BL No'), function() {
            let d = new frappe.ui.Dialog({
                title: 'Fetch from M BL No',
                fields: [
                    {
                        label: 'M BL No',
                        fieldname: 'm_bl_no',
                        fieldtype: 'Data',
                        reqd: 1
                    },
                    {
                        label: 'H BL No',
                        fieldname: 'h_bl_no',
                        fieldtype: 'Data'
                    }
                ],
                primary_action_label: 'Create Sales Orders',
                primary_action(values) {
                    frappe.call({
                        method: 'icd.icd.doc_events.sales_order.create_sales_order_from_bl',
                        args: {
                            m_bl_no: values.m_bl_no,
                            h_bl_no: values.h_bl_no
                        },
                        callback: function(r) {
                            if(!r.exc) {
                                frappe.msgprint(__('Sales Orders Created Successfully'));
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
