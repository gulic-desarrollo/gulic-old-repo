#include "sasl.h"

VALUE eSASLError;

void sasl_raise(int errcode)
{
	VALUE exc;
	const char *errmsg;

	errmsg = sasl_errstring(errcode, NULL, NULL);
	
	exc = rb_exc_new2(eSASLError, errmsg);
	rb_iv_set(exc, "@errcode", INT2FIX(errcode));
	rb_exc_raise(exc);
}

void init_error()
{
	/* Class SASLError */
	eSASLError = rb_define_class_under(mSASL, "SASLError", rb_eException);
	
	rb_define_attr(eSASLError, "errcode", 1, 0);
}
