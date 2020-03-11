from users import models


class AccessPermission():

    def __init__(self, roles):
        self.role = roles

    def has_prod_perm(self):
        return self.role.module.__contains__('Product')

    def has_batch_perm(self):
        return self.role.module.__contains__('Batch')

    def has_admin_perm(self):
        return self.role.module.__contains__('Admin')

    def has_billing_perm(self):
        return self.role.module.__contains__('Billing')

    def has_support_perm(self):
        return self.role.module.__contains__('Support')

    def is_create(self):
        return self.role.create

    def is_view(self):
        return self.role.view

    def is_update(self):
        return self.role.update

    def is_delete(self):
        return self.role.delete