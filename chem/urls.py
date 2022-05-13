# noinspection PyInterpreter,PyPackageRequirements,PyPackageRequirements,PyInterpreter
from django.urls import path
from . import views

app_name = 'chem'

urlpatterns = [
    path(
        "search/",
        views.ChemicalSearchView.as_view(),
        name="search"
    ),
    path(
        "search/results/",
        views.ChemicalSearchResultsAJAXView.as_view(),
        name="search_results"
    ),
    path(
        "blend/",
        views.ChemicalBlendView.as_view(),
        name="blend"
    ),
    path("detail/<int:pk>/", views.ChemicalDetail.as_view(), name='detail'),
    path("download/<int:pk>/", views.DownloadChemCSVToClient.as_view(),
         name='download'
    ),
    path(
        "download_chem_subm_tmpl",
         views.DownloadChemSubmissionTemplate.as_view(),
         name='download_chem_subm_tmpl'
    ),
    path(
        "download_blend_subm_tmpl",
         views.DownloadBlendSubmissionTemplate.as_view(),
         name='download_blend_subm_tmpl'
    ),
    path(
        "submit_chem",
        views.ChemicalSubmissionFormView.as_view(),
        name='submit_chem'
    ),
    path(
        "submit_blend", views.BlendSubmissionFormView.as_view(),
        name='submit_blend'
    ),
    path(
        "submit_data_success",
        views.SubmitDataSuccessView.as_view(),
        name='submit_data_success'
    ),
]
