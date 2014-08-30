from django.db import models
from django.contrib import admin

class base_kana(models.Model):
    id = models.IntegerField(primary_key=True)
    kana = models.CharField(max_length=2)
    unicode = models.CharField(max_length=20, null=True, blank=True)
    pronunciation = models.CharField(max_length=5)
    pronunciation_tip = models.CharField(max_length=50, null=True, blank=True)
    mnemonic = models.CharField(max_length=200, null=True, blank=True)
    comment = models.CharField(max_length=200, null=True, blank=True)
    vowel_group = models.CharField(max_length=5, null=True, blank=True)
    consonant_group = models.CharField(max_length=5, null=True, blank=True)


class derived_kana(models.Model):
    kana = models.CharField(max_length=2)
    unicode = models.CharField(max_length=20, null=True, blank=True)
    base_kana_id = models.ForeignKey(base_kana)
    pronunciation = models.CharField(max_length=5)
    pronunciation_tip = models.CharField(max_length=50, null=True, blank=True)
    comment = models.CharField(max_length=200, null=True, blank=True)
    vowel_group = models.CharField(max_length=5, null=True, blank=True)
    consonant_group = models.CharField(max_length=5, null=True, blank=True)
    
class derived_kana_inline(admin.StackedInline):
    model = derived_kana
    extra = 4

class base_kana_admin(admin.ModelAdmin):
    inlines = [derived_kana_inline]
    list_display = ('id', 'kana', 'pronunciation')
    
hiragana_sections = [
                        {'start':1, 'end':15, 'section': 1},
                        {'start':16, 'end':30, 'section': 2},
                        {'start':31, 'end':45, 'section': 3},
                        {'start':46, 'end':56, 'section': 4},
                        {'start':57, 'end':60, 'section': 5, 'name':"Hiragana Combinations"},     
                     ]


admin.site.register(base_kana, base_kana_admin)
admin.site.register(derived_kana)
