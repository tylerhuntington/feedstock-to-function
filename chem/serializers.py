from rest_framework import serializers
from chem.models import Chemical, Source
from drf_queryfields import QueryFieldsMixin


# class SourceSerializer(serializers.ModelSerializer):
#     src_name = serializers.CharField(source="name")
#
#     class Meta:
#         model = Source
#         fields = ['name', 'src_name']
#         # exclude = (
#         #     "_struct_img",
#         #     "mp_estimator",
#         #     "bp_estimator",
#         #     "cn_estimator",
#         #     "dcn_estimator",
#         #     "ysi_estimator",
#         # )

class ChemicalSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    # TODO: figure out a sensible ordering for CSV columns

    bp_exp_srcs = serializers.StringRelatedField(many=True, read_only=True)
    mp_exp_srcs = serializers.StringRelatedField(many=True, read_only=True)
    fp_exp_srcs = serializers.StringRelatedField(many=True, read_only=True)
    cn_exp_srcs = serializers.StringRelatedField(many=True, read_only=True)
    dcn_exp_srcs = serializers.StringRelatedField(many=True, read_only=True)
    ysi_exp_srcs = serializers.StringRelatedField(many=True, read_only=True)

    synonyms = serializers.SerializerMethodField()

    bp_unit = serializers.ReadOnlyField()
    mp_unit = serializers.ReadOnlyField()
    fp_unit = serializers.ReadOnlyField()
    cn_unit = serializers.ReadOnlyField()
    dcn_unit = serializers.ReadOnlyField()
    ysi_unit = serializers.ReadOnlyField()

    bp_pred_abs_err = serializers.ReadOnlyField()
    mp_pred_abs_err = serializers.ReadOnlyField()
    fp_pred_abs_err = serializers.ReadOnlyField()
    cn_pred_abs_err = serializers.ReadOnlyField()
    dcn_pred_abs_err = serializers.ReadOnlyField()
    ysi_pred_abs_err = serializers.ReadOnlyField()



    def get_synonyms(self, obj):
        return [syn.name for syn in obj.synonyms.all()]

    class Meta:
        model = Chemical
        # fields = (
        #     'name',
        #     'smiles',
        #     'iupac',
        #     'inchi',
        #     'synonyms'
        # )
        exclude = (
            "_struct_img",
            "mp_estimator",
            "bp_estimator",
            "fp_estimator",
            "cn_estimator",
            "dcn_estimator",
            "ysi_estimator",
            "pubchem_cid",
            "tea_lca_tool_alias"
        )

# class TagSerializer:
#     class Meta:
#         model = Source
