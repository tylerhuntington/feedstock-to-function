from django.shortcuts import render
from django.views.generic import View, FormView, ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin




class TeaLcaToolView(LoginRequiredMixin, TemplateView):
    template_name = 'tea_lca_tool.html'



class TeaLcaAnalyzeView(LoginRequiredMixin, TemplateView):
    template_name = 'tea_lca_tool.html'

    def get_context_data(self, **kwargs):
        context = super(TeaLcaAnalyzeView, self).get_context_data(**kwargs)
        context['end_prod'] = self.kwargs.get('end_prod')
        return context

