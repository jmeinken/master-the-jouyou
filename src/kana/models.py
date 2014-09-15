from django.db import models
from django.contrib import admin

class kana(models.Model):
    kana_order = models.IntegerField(null=True, blank=True)
    kana = models.CharField(max_length=2)
    unicode = models.CharField(max_length=20, null=True, blank=True)
    pronunciation = models.CharField(max_length=10, null=True, blank=True)
    pronunciation_tip = models.CharField(max_length=200, null=True, blank=True)
    mnemonic = models.CharField(max_length=200, null=True, blank=True)
    comment = models.CharField(max_length=1000, null=True, blank=True)
    vowel_group = models.CharField(max_length=5, null=True, blank=True)
    consonant_group = models.CharField(max_length=5, null=True, blank=True)
    parent = models.CharField(max_length=2, null=True, blank=True)
    hiragana_equivalent = models.CharField(max_length=2, null=True, blank=True)


class combinations(models.Model):
    kana = models.CharField(max_length=10)
    pronunciation = models.CharField(max_length=10)
    pronunciation_tip = models.CharField(max_length=200, null=True, blank=True)
    vowel_group = models.CharField(max_length=5, null=True, blank=True)
    consonant_group = models.CharField(max_length=5, null=True, blank=True)
    
class word(models.Model):
    word = models.CharField(max_length=50)
    pronunciation = models.CharField(max_length=100, null=True, blank=True)
    translation = models.CharField(max_length=500)
    module = models.IntegerField(null=True, blank=True)
    section = models.IntegerField(null=True, blank=True)
    
#class derived_kana_inline(admin.StackedInline):
#    model = derived_kana
#    extra = 4
#
class kana_admin(admin.ModelAdmin):
    #    inlines = [derived_kana_inline]
    list_display = ('kana_order', 'kana', 'pronunciation')
    
hiragana_sections = [
                        {'start':1, 'end':15, 'section': 1, 'name':"Hiragana 1 - 15"},
                        {'start':16, 'end':30, 'section': 2, 'name':"Hiragana 16 - 30"},
                        {'start':31, 'end':46, 'section': 3, 'name':"Hiragana 31 - 47"},    
                     ]

katakana_sections = [
                        {'start':47, 'end':61, 'section': 1, 'name':"Katakana 1 - 15"},
                        {'start':62, 'end':76, 'section': 2, 'name':"Katakana 16 - 30"},
                        {'start':77, 'end':94, 'section': 3, 'name':"Katakana 31 - 45"},  
                     ]


admin.site.register(kana, kana_admin)
admin.site.register(combinations)
admin.site.register(word)
