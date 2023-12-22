from django.contrib.auth.models import Group
from django.views.generic import ListView, TemplateView, UpdateView, DeleteView, CreateView
from dashboard.views import UserAccessMixin
from django.db.models import Q

"""
Group
"""
class PermissionGroupsViewPage(UserAccessMixin, ListView):
    permission_required = 'auth.view_group'
    template_name = "tabs/permission_groups/permission_groups_list.html"
    model = Group

    def get_queryset(self):
        q = self.request.GET.get('q')
        if q:
            object_list = self.model.objects.filter(
                Q(name__icontains=q)
            )
        else:
            object_list = self.model.objects.all()
        return object_list