from django.shortcuts import render
from django.views.generic import View, FormView, ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from chem.models import Chemical
from chem import PRED_PROP_CODES


class AboutPage(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):

        # init context accumulator
        c = {}
        for p in PRED_PROP_CODES:
            for s in ['_exp', '_pred', '_pred_perc_err']:
                field = f'{p}{s}'
                k = f'{field}__isnull'
                if s == '_pred_perc_err':
                    obj = Chemical.objects.first()
                    c[f'{p}{s}'] = getattr(obj, field)
                else:
                    c[f'{p}{s}'] = Chemical.objects.filter(**{k: False}).count()
        return c

