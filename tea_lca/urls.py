from django.urls import path
from tea_lca import views

app_name = 'tea_lca'

urlpatterns = [
    path("", views.TeaLcaToolView.as_view(), name="tea_lca_tool"),
    path(
        "analyze/<str:chem>", views.TeaLcaAnalyzeView.as_view(), name="analyze"
    ),
]
