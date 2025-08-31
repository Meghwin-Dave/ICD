frappe.listview_settings['In Yard Container Booking'] = {
    onload: function(listview) {
        listview.page.add_inner_button(__('Create Bulk Container'), function() {
            let d = new frappe.ui.Dialog({
                title: "Bulk Container Booking",
                fields: [
                    {fieldname:"m_bl_no", label:"M B/L No", fieldtype:"Data", reqd:1},
                    {fieldname:"h_bl_no", label:"H B/L No", fieldtype:"Data"},
                    {fieldname:"company", label:"Company", fieldtype:"Link", options:"Company", reqd:1},
                    {fieldname:"c_and_f_company", label:"C and F Company", fieldtype:"Link", options:"Cleaning and Forward Company", reqd:1},
                    {fieldname:"clearing_agent", label:"Clearing Agent", fieldtype:"Link",reqd:1,options:"Clearing Agent"},
                    {fieldname:"inspection_date", label:"Inspection Date", fieldtype:"Date", reqd:1},
                    {fieldname:"inspection_location", label:"Inspection Location", fieldtype:"Link", reqd:1,options:"Container Location"}
                ],
                primary_action_label: "Create Bookings",
                primary_action(values) {
                    frappe.call({
                        method: "icd.icd.doctype.in_yard_container_booking.in_yard_container_booking.create_booking_with_container",
                        args: { data: values },
                        callback: function(r) {
                            if(r.message) {
                                frappe.msgprint(
                                    __("Created {0} booking(s) for M B/L No {1}", [r.message.booking.length, values.m_bl_no])
                                );
                                d.hide();
                                listview.refresh();
                            }
                        }
                    });
                }
            });

            // Fetch data when M B/L No is entered
            d.fields_dict.m_bl_no.$input.on("change", function() {
                let m_bl_no = d.get_value("m_bl_no");
                if(m_bl_no) {
                    frappe.call({
                        method: "icd.icd.doctype.in_yard_container_booking.in_yard_container_booking.get_booking_defaults",
                        args: { m_bl_no: m_bl_no },
                        callback: function(r) {
                            if(r.message) {
                                // Autofill dialog fields
                                d.set_value("c_and_f_company", r.message.c_and_f_company);
                                d.set_value("clearing_agent", r.message.clearing_agent);
                                d.set_value("inspection_date", r.message.inspection_date);
                                d.set_value("inspection_location", r.message.inspection_location);
                            }
                        }
                    });
                }
            });

            d.show();
        });
        listview.page.add_inner_button(__('Container Booking Report'), function() {
            frappe.set_route("query-report", "Container Booking");
        });
    }
};
