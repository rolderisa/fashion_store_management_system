from django import forms
from .models import Product, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'image', 'category', 'low_stock_threshold']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md', 'placeholder': 'Product Name', 'autocomplete': 'off'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md', 'rows': 4, 'placeholder': 'Product Description', 'autocomplete': 'off'}),
            'price': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md', 'placeholder': 'Price', 'autocomplete': 'off'}),
            'stock': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md', 'placeholder': 'Stock', 'autocomplete': 'off'}),
            'image': forms.FileInput(attrs={'class': 'hidden', 'accept': 'image/*', 'autocomplete': 'off'}),
            'category': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md', 'autocomplete': 'off'}),
            'low_stock_threshold': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md', 'placeholder': 'Low Stock Threshold', 'autocomplete': 'off'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        self.fields['category'].empty_label = "Select a category"

    # Mark the 'low_stock_threshold' as not required
    def clean(self):
        cleaned_data = super().clean()
        low_stock_threshold = cleaned_data.get('low_stock_threshold')
        
        # Ensure low_stock_threshold is optional by default
        if low_stock_threshold is None:
            cleaned_data['low_stock_threshold'] = 0  # or any other default value
        
        # Validation for category field
        if not cleaned_data.get('category'):
            self.add_error('category', 'Please select a category')

        return cleaned_data
