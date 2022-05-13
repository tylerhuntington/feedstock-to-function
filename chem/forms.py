from chem.models import Chemical, ChemicalSubmission, BlendSubmission
from django import forms


class ChemicalSearchForm(forms.Form):


    search_type = forms.CharField(
        required=False,
        label='Option 1: Search by Identifier',
        widget=forms.Select(
            choices=[
                ('name', 'Molecular Name'),
                ('smiles', 'SMILES'),
                ('iupac', 'IUPAC'),
                ('formula', 'Molecular Formula'),
                ('inchi', 'InChIKey'),
            ],
            attrs={
                # 'class': 'form-control mx-1',
                'class': 'form-control col-lg-3',
            }
        )
    )

    search_term = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(
            attrs={
                # 'class': 'form-control col-lg-4 mr-5',
                'class': 'form-control mt-1 mb-3 col-lg-4',
            }

        )
    )

    prop = forms.CharField(
        required=False,
        label='Option 2: Search by Property',
        widget=forms.Select(
            choices=[
                ('mp', 'Melting Point (°C)'),
                ('bp', 'Boiling Point (°C)'),
                ('ysi', 'Yield Sooting Index'),
                ('cn', 'Cetane Number'),
                ('dcn', 'Derived Cetane Number'),
            ],
            attrs={
                'class': 'form-control mb-1 col-lg-3',
            }
        )
    )

    prop_min_val = forms.CharField(
        required=False,
        label='Minimum Value:',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control col-lg-1',
            }
        )
    )

    prop_max_val = forms.CharField(
        required=False,
        label='Maximum Value:',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control col-lg-1',
            }
        )
    )

    meta_search_type = forms.CharField(
        required=False,
        label='Search By:',
        widget=forms.RadioSelect(
            choices=[
                ('id', 'Identifier'),
                ('prop', 'Property'),
            ],
            attrs={
                # 'class': 'd-flex',
                # 'style': 'block',
                # 'class': 'div form-control div',
                'class': 'form-input',
            },
        )
    )


class ChemicalSubmissionForm(forms.ModelForm):
    smiles = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(
            attrs={
                # 'placeholder': 'CCO',
                'size': 30,
            }

        )
    )
    name = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(
            attrs={
                # 'placeholder': 'CCO',
                'size': 30,
            }

        )
    )
    iupac = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(
            attrs={
                # 'placeholder': 'CCO',
                'size': 30,
            }

        )
    )
    formula = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(
            attrs={
                # 'placeholder': 'CCO',
                'size': 30,
            }

        )
    )
    inchi = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(
            attrs={
                # 'placeholder': 'CCO',
                'size': 30,
            }

        )
    )
    cas = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(
            attrs={
                # 'placeholder': 'CCO',
                'size': 30,
            }

        )
    )

    comments = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'rows': 4,
                'cols': 80
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(ChemicalSubmissionForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if 'temp' in field:
                self.fields[field].widget.attrs.update(
                    {'class': 'form-control form-control-sm col-4'},
                )
                self.fields[field].widget.attrs.update(
                    {'style': 'display: inline'}
                )
            elif field == 'csv_submission':
                self.fields[field].widget.attrs.update(
                    {'class': 'form-control-file form-control-sm pl-0'}
                )
            else:
                self.fields[field].widget.attrs.update(
                    {'class': 'form-control form-control-sm'}
                )

    class Meta:
        model = ChemicalSubmission
        fields = '__all__'

class BlendSubmissionForm(forms.ModelForm):


    name = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(
            attrs={
                # 'placeholder': 'CCO',
                'size': 30,
            }

        )
    )
    cas = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(
            attrs={
                # 'placeholder': 'CCO',
                'size': 30,
            }

        )
    )

    comments = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'rows': 4,
                'cols': 80
            }
        )
    )

    # csv_submission = forms.FileField(
    #     required=False,
    #     widget=forms.FileField(
    #         attrs={
    #             'class': 'form-control-file'
    #         }
    #     )
    # )

    def __init__(self, *args, **kwargs):
        super(BlendSubmissionForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if 'temp' in field:
                self.fields[field].widget.attrs.update(
                    {'class': 'form-control form-control-sm col-4'},
                )
                self.fields[field].widget.attrs.update(
                    {'style': 'display: inline'}
                )
            elif field == 'csv_submission':
                self.fields[field].widget.attrs.update(
                    {'class': 'form-control-file form-control-sm pl-0'}
                )
            else:
                self.fields[field].widget.attrs.update(
                    {'class': 'form-control form-control-sm'}
                )

    class Meta:
        model = BlendSubmission
        fields = '__all__'

