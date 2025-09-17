// Copyright (c) 2025, Pal SHah and contributors
// For license information, please see license.txt

frappe.ui.form.on("Container Movement Order", {
    refresh: function(frm) {
        // Transporter → no extra filter, free choice

        // Driver → filter by transporter + disable = 0
        frm.set_query("driver", function() {
            return {
                filters: {
                    custom_transporter_name: frm.doc.transporter,
                    status: "Active"
                }
            };
        });

        // Truck → filter by transporter, not disabled, is_truck = 1
        frm.set_query("truck", function() {
            return {
                filters: {
                    Custom_vehicle_owner: frm.doc.tranporter,
                    custom_disable: 0,
                    custom_is_truck: 1
                }
            };
        });

        // Trailer → filter by transporter, not disabled, is_trailer = 1
        frm.set_query("trailer", function() {
            return {
                filters: {
                    Custom_vehicle_owner: frm.doc.tranporter,
                    custom_disable: 0,
                    custom_trailer: "Yes"
                }
            };
        });
        frm.set_query("tranporter", function() {
            return {
                filters: {
                    disable: 0,
                }
            };
        });
        if (!frm.is_new() && frm.doc.docstatus == 1) {
            frm.add_custom_button(__('Create Container Reception'), function () {
                frappe.call({
                    method: "icd.icd.doctype.container_movement_order.container_movement_order.make_container_reception",
                    args: {
                        source_name: frm.doc.name
                    },
                    callback: function (r) {
                        if (r.message) {
                            frappe.model.sync(r.message);
                            frappe.set_route("Form", r.message.doctype, r.message.name);
                        }
                    }
                });
            });
        }
    
    },
    onload_post_render: function(frm) {
        // ✅ Only auto-open when new doc AND manifest is set
        if (frm.is_new() && frm.doc.manifest) {
            frm.trigger("open_select_container_dialog");
        }
    },

    select_container: function(frm) {
        // ✅ Manual button click
        frm.trigger("open_select_container_dialog");
    },

    open_select_container_dialog: function(frm) {
        if (!frm.doc.manifest) {
            frappe.msgprint("Please link a Manifest first.");
            return;
        }

        let dialog = new frappe.ui.Dialog({
            title: "Select Container",
            size: "large",
            fields: [
                {
                    fieldtype: "Data",
                    fieldname: "m_bl_no_filter",
                    label: "M BL No",
                    description: "Enter M BL No to filter"
                },
                {
                    fieldtype: "Button",
                    fieldname: "apply_filter",
                    label: "Apply Filter"
                },
                {
                    fieldtype: "Table",
                    fieldname: "container_selection",
                    label: "Containers",
                    cannot_add_rows: true,
                    in_place_edit: true,
                    fields: [
                        { fieldtype: "Check", fieldname: "select", label: "✔", in_list_view: 1, width: "5%" },
                        { fieldtype: "Data", fieldname: "container_no", label: "Container NO", in_list_view: 1, read_only: 1 },
                        { fieldtype: "Data", fieldname: "m_bl_no", label: "M BL No", in_list_view: 1, read_only: 1 },
                        { fieldtype: "Data", fieldname: "type_of_container", label: "Cargo Type", in_list_view: 1, read_only: 1 },
                        { fieldtype: "Data", fieldname: "container_size", label: "Size", in_list_view: 1, read_only: 1 },
                        { fieldtype: "Data", fieldname: "freight_indicator", label: "Freight Indicator", in_list_view: 1, read_only: 1 },
                        { fieldtype: "Int", fieldname: "no_of_packages", label: "No of Packages", in_list_view: 1, read_only: 1 },
                        { fieldtype: "Data", fieldname: "weight", label: "Weight", in_list_view: 1, read_only: 1 },
                        { fieldtype: "Data", fieldname: "weight_unit", label: "Weight Unit", in_list_view: 1, read_only: 1 },
                    ],
                    data: []
                }
            ],
            primary_action_label: "Select",
            primary_action(values) {
                let selected = (values.container_selection || []).filter(r => r.select);
                if (!selected.length) {
                    frappe.msgprint("Please select a container.");
                    return;
                }
                let c = selected[0];
                frm.set_value("container_no", c.container_no);
                frm.set_value("m_bl_no", c.m_bl_no);
                frm.set_value("size_ft", c.container_size);
                frm.set_value("freight_indicator", c.freight_indicator);
                frm.set_value("cargo_type", c.type_of_container);
                dialog.hide();
            }
        });

        const load_rows = (filter_value) => {
            frappe.call({
                method: "icd.icd.doctype.container_movement_order.container_movement_order.get_containers_for_manifest",
                args: {
                    manifest: frm.doc.manifest,
                    m_bl_no_filter: filter_value || ""
                },
                callback: function(r) {
                    const data = r.message || [];
                    dialog.fields_dict.container_selection.grid.df.data = data.map(d => ({
                        select: 0,
                        container_no: d.container_no,
                        m_bl_no: d.m_bl_no,
                        container_size: d.container_size,
                        freight_indicator: d.freight_indicator,
                        type_of_container: d.type_of_container,
                        no_of_packages: d.no_of_packages,
                        weight: d.weight,
                        weight_unit: d.weight_unit
                    }));
                    dialog.fields_dict.container_selection.grid.refresh();
                }
            });
        };

        // hook filter button
        dialog.fields_dict.apply_filter.input.onclick = () => {
            load_rows(dialog.get_value("m_bl_no_filter"));
        };

        // initial load
        load_rows("");
        dialog.show();
    }
});

