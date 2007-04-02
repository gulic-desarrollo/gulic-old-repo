# modelos de django

from django.db import models


class Charge(models.Model):
	"""
		Descr
	"""
	chargeType = models.ForeignKey('ChargeType', verbose_name = _('charge type'), blank = False, null = False)
	initOfPeriod = models.DateTimeField(verbose_name = _('init of period'))
	endOfPeriod = models.DateTimeField(verbose_name = _('end of period'))
	partner = models.ForeignKey('Partner', verbose_name = _('partner'), blank = False, null = False)
	class Meta:
		ordering = ['', '']
		verbose_name = _('')
		verbose_name_plural = _('')
		search_fields = ['', ]
	
	class Admin:
		list_display = ('', )

class ChargeType(models.Model):
	"""
		Descr
	"""
	description = models.CharField(verbose_name = _('description'), maxlength = 200, blank = True)
	duration = models.IntegerField(verbose_name = _('duration'), default=12,)
	warningTime = models.IntegerField(verbose_name = _('warning time'), default=1)
	class Meta:
		ordering = ['', '']
		verbose_name = _('')
		verbose_name_plural = _('')
		search_fields = ['', ]
	
	class Admin:
		list_display = ('', )

class FtpUsers(models.Model):
	"""
		Descr
	"""
	people = models.ForeignKey('People', verbose_name = _('people'), blank = False, null = False)
	nick = models.CharField(verbose_name = _('nick'), maxlength = 20, blank = False)
	pass = models.CharField(verbose_name = _('pass'), maxlength = 8, blank = False)
	initDate = models.DateTimeField(verbose_name = _('init date'))
	active = models.BooleanField(verbose_name = _('active'), blank = False, default = true)
	class Meta:
		ordering = ['', '']
		verbose_name = _('')
		verbose_name_plural = _('')
		search_fields = ['', ]
	
	class Admin:
		list_display = ('', )

class Im(models.Model):
	"""
		Descr
	"""
	people = models.ForeignKey('People', verbose_name = _('people'), blank = False, null = False)
	imType = models.ForeignKey('ImType', verbose_name = _('im type'), blank = False, null = False)
	data = models.CharField(verbose_name = _('data'), maxlength = 250, blank = False)
	isPreferred = models.BooleanField(verbose_name = _('is preferred'), blank = True, default = false)
	class Meta:
		ordering = ['', '']
		verbose_name = _('')
		verbose_name_plural = _('')
		search_fields = ['', ]
	
	class Admin:
		list_display = ('', )

class ImType(models.Model):
	"""
		Descr
	"""
	description = models.CharField(verbose_name = _('description'), maxlength = 250, blank = True)
	isPreferred = models.BooleanField(verbose_name = _('is preferred'), blank = True, default = false)
	class Meta:
		ordering = ['', '']
		verbose_name = _('')
		verbose_name_plural = _('')
		search_fields = ['', ]
	
	class Admin:
		list_display = ('', )

class JabberUsers(models.Model):
	"""
		Descr
	"""
	people = models.ForeignKey('People', verbose_name = _('people'), blank = False, null = False)
	nick = models.CharField(verbose_name = _('nick'), maxlength = 20, blank = False)
	pass = models.CharField(verbose_name = _('pass'), maxlength = 8, blank = False)
	initDate = models.DateTimeField(verbose_name = _('init date'))
	active = models.BooleanField(verbose_name = _('active'), blank = False, default = true)
	class Meta:
		ordering = ['', '']
		verbose_name = _('')
		verbose_name_plural = _('')
		search_fields = ['', ]
	
	class Admin:
		list_display = ('', )

class MailUsers(models.Model):
	"""
		Descr
	"""
	people = models.ForeignKey('People', verbose_name = _('people'), blank = False, null = False)
	nick = models.CharField(verbose_name = _('nick'), maxlength = 20, blank = False)
	pass = models.CharField(verbose_name = _('pass'), maxlength = 8, blank = False)
	initDate = models.DateTimeField(verbose_name = _('init date'))
	active = models.BooleanField(verbose_name = _('active'), blank = False, default = true)
	class Meta:
		ordering = ['', '']
		verbose_name = _('')
		verbose_name_plural = _('')
		search_fields = ['', ]
	
	class Admin:
		list_display = ('', )

class Partner(models.Model):
	"""
		Descr
	"""
	users = models.ForeignKey('Users', verbose_name = _('users'), blank = False, null = False)
	people = models.ForeignKey('People', verbose_name = _('people'), blank = False, null = False)
	partner = models.BooleanField(verbose_name = _('partner'), blank = False, default = false)
	class Meta:
		ordering = ['', '']
		verbose_name = _('')
		verbose_name_plural = _('')
		search_fields = ['', ]
	
	class Admin:
		list_display = ('', )

class PartnerType(models.Model):
	"""
		Descr
	"""
	description = models.CharField(verbose_name = _('description'), maxlength = 50, blank = False)
	class Meta:
		ordering = ['', '']
		verbose_name = _('')
		verbose_name_plural = _('')
		search_fields = ['', ]
	
	class Admin:
		list_display = ('', )

class People(models.Model):
	"""
		Descr
	"""
	firstName = models.CharField(verbose_name = _('first name'), maxlength = 40, blank = False)
	lastName = models.CharField(verbose_name = _('last name'), maxlength = 40, blank = True, default = ''))
	surname = models.CharField(verbose_name = _('surname'), maxlength = 200, blank = False)
	nif = models.CharField(verbose_name = _('nif'), maxlength = 9, blank = True, default= 'xxxxxxxxx'))
	dateofbirth = models.DateTimeField(verbose_name = _('date of birth'))
	class Meta:
		ordering = ['', '']
		verbose_name = _('')
		verbose_name_plural = _('')
		search_fields = ['', ]
	
	class Admin:
		list_display = ('', )

class Quota(models.Model):
	"""
		Descr
	"""
	partner = models.ForeignKey('Partner', verbose_name = _('partner'), blank = False, null = False)
	partnerType = models.ForeignKey('PartnerType', verbose_name = _('partner type'), blank = False, null = False) #, default = 1
	paymentDate = models.DateTimeField(verbose_name = _('payment date'))
	endOfPeriod = models.DateTimeField(verbose_name = _('end of period'))
	quotaType = models.ForeignKey('QuotaType', verbose_name = _('quota type'), blank = False, null = False) # DEFAULT 1
	class Meta:
		ordering = ['', '']
		verbose_name = _('')
		verbose_name_plural = _('')
		search_fields = ['', ]
	
	class Admin:
		list_display = ('', )

class QuotaType(models.Model):
	"""
		Descr
	"""
	description = models.CharField(verbose_name = _('description'), maxlength = 200, blank = True)
	duration = models.IntegerField(verbose_name = _('duration'), default=12,)
	warningTime = models.IntegerField(verbose_name = _('warning time'), default=1)
	class Meta:
		ordering = ['', '']
		verbose_name = _('')
		verbose_name_plural = _('')
		search_fields = ['', ]
	
	class Admin:
		list_display = ('', )

class WebUsers(models.Model):
	"""
		Descr
	"""
	people = models.ForeignKey('People', verbose_name = _('people'), blank = False, null = False)
	nick = models.CharField(verbose_name = _('nick'), maxlength = 20, blank = False)
	password = models.CharField(verbose_name = _('password'), maxlength = 8, blank = False)
	initDate = models.DateTimeField(verbose_name = _('init date'))
	active = models.BooleanField(verbose_name = _('active'), blank = False, default = true)
	class Meta:
		ordering = ['', '']
		verbose_name = _('')
		verbose_name_plural = _('')
		search_fields = ['', ]
	
	class Admin:
		list_display = ('', )

