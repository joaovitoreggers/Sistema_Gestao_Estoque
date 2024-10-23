from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404

class CompanyFilterMixin:
    company_model = None 

    def get_queryset(self):
        queryset = super().get_queryset()  # Chama o método da classe pai
        user_company = getattr(self.request.user.profile, 'company', None)

        if not user_company:
            raise PermissionDenied("Você não está associado a nenhuma empresa.")

        return queryset.filter(company=user_company)


class CompanyAssignMixin:

    def form_valid(self, form):
        user_company = getattr(self.request.user.profile, 'company', None)
        
        if user_company is None:
            raise Http404("Usuário não associado a nenhuma empresa.")
        
        form.instance.company = user_company
        return super().form_valid(form)
    

class PermissionsCreateMixin(LoginRequiredMixin, PermissionRequiredMixin, CompanyFilterMixin, CompanyAssignMixin):
    pass