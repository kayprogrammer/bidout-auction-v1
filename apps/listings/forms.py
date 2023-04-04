from django import forms
from django.utils import timezone
from .models import Category, Listing
from apps.accounts.models import User
from zoneinfo import ZoneInfo

try:
    category_choices = list(Category.objects.values_list("name", "name"))
    category_choices.insert(0, ("", "Choose a Category"))
    category_choices.append(("Other", "Other"))
except:
    category_choices = []

class CreateListingForm(forms.ModelForm):
    name = forms.CharField(
        max_length=70,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Input The Product Name",
            }
        ),
    )
    desc = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": "6"})
    )
    category = forms.ChoiceField(
        choices=category_choices,
        widget=forms.Select(
            attrs={"class": "form-select form-select-md"},
        ),
    )
    price = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control ps-5",
                "placeholder": "Enter a starting price",
                "step": ".01",
                "width": "100",
            }
        )
    )
    image = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
                "placeholder": "Input The Product Image",
            }
        )
    )
    closing_date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
                "class": "form-control",
                "placeholder": "Enter a closing date",
                "step": "any",
            }
        )
    )

    def clean_category(self):
        category_name = self.cleaned_data.get("category")

        category = Category.objects.filter(name=category_name)
        if not category.exists():
            if not category_name == "Other":
                raise forms.ValidationError("Please select a valid category.")
            self.fields["category"].required = False
            category = None
        else:
            category = category.get()
        return category

    def clean_closing_date(self):
        closing_date = self.cleaned_data["closing_date"]
        closing_date = closing_date.replace(
            tzinfo=ZoneInfo(str(closing_date.tzinfo))
        ).astimezone(timezone.utc)
        if closing_date < timezone.now():
            raise forms.ValidationError(
                "Enter a datetime farther than the current datetime."
            )
        return closing_date

    class Meta:
        model = Listing
        exclude = ["auctioneer", "slug", "active"]


class UpdateProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=25, widget=forms.TextInput({"class": "form-control"})
    )
    last_name = forms.CharField(
        max_length=25, widget=forms.TextInput({"class": "form-control"})
    )
    avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
                "placeholder": "Change your avatar",
            }
        ),
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "avatar"]
