from django.db import models
from django.contrib import admin

class base_kana(models.Model):
    id = models.IntegerField(primary_key=True)
    kana = models.CharField(max_length=2)
    unicode = models.CharField(max_length=20, null=True, blank=True)
    pronunciation = models.CharField(max_length=10)
    pronunciation_tip = models.CharField(max_length=200, null=True, blank=True)
    mnemonic = models.CharField(max_length=200, null=True, blank=True)
    comment = models.CharField(max_length=200, null=True, blank=True)
    vowel_group = models.CharField(max_length=5, null=True, blank=True)
    consonant_group = models.CharField(max_length=5, null=True, blank=True)


class derived_kana(models.Model):
    kana = models.CharField(max_length=2)
    unicode = models.CharField(max_length=20, null=True, blank=True)
    base_kana_id = models.ForeignKey(base_kana)
    pronunciation = models.CharField(max_length=10)
    pronunciation_tip = models.CharField(max_length=200, null=True, blank=True)
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
                        {'start':1, 'end':15, 'section': 1, 'name':"Hiragana 1 - 15"},
                        {'start':16, 'end':30, 'section': 2, 'name':"Hiragana 16 - 30"},
                        {'start':31, 'end':47, 'section': 3, 'name':"Hiragana 31 - 47"},
                        {'start':48, 'end':68, 'section': 4, 'name':"Hiragana Combinations"},     
                     ]

katakana_sections = [
                        {'start':69, 'end':83, 'section': 1, 'name':"Katakana 1 - 15"},
                        {'start':84, 'end':98, 'section': 2, 'name':"Katakana 16 - 30"},
                        {'start':99, 'end':114, 'section': 3, 'name':"Katakana 31 - 45"},  
                     ]


admin.site.register(base_kana, base_kana_admin)
admin.site.register(derived_kana)
