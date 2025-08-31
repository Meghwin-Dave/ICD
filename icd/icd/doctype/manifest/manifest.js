frappe.ui.form.on("Manifest", {
    refresh: function(frm) {
        if (frm.doc.docstatus === 1) {
            frm.add_custom_button(__('Create Container Movement Order'), function() {
                // Open new CMO with manifest reference
                frappe.new_doc("Container Movement Order", {
                    manifest: frm.doc.name,
                    company: frm.doc.company,
                    ship: frm.doc.vessel_name,
                    port: frm.doc.port,
                    voyage_no: frm.doc.voyage
                });
            });
        }
    }
});
