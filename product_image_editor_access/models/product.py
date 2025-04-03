from odoo import models, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def fields_get(self, allfields=None, attributes=None):
        # Call the super method to get the standard fields properties
        res = super().fields_get(allfields, attributes)

        # Fetch the Product Image Editor group ID
        image_editor_group = self.env.ref('product_image_editor_access.group_product_image_editor', raise_if_not_found=False)

        # Check if the current user is in the group
        if image_editor_group and image_editor_group.id in self.env.user.groups_id.ids:
            # Loop through each field and make them readonly except 'image_1920'
            for field_name in res:
                if field_name != 'image_1920':
                    res[field_name]['readonly'] = True

        return res
