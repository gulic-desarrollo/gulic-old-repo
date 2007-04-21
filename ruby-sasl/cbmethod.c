#include "sasl.h"

VALUE cCbMethod;

/*
 * CbMethod::initialize(id, interaction, method)
 */
static VALUE cbmethod_new(VALUE self, VALUE id, VALUE it, VALUE method)
{
	Check_Type(id, T_FIXNUM);
	rb_iv_set(self, "@id", id);
	
	if(TYPE(it) != T_TRUE && TYPE(it) != T_FALSE){
		rb_raise(rb_eTypeError, "wrong argument type");
	}
	
	rb_iv_set(self, "@it", it);
	
	if(TYPE(method) != T_SYMBOL && TYPE(method) != T_DATA){
		rb_raise(rb_eTypeError, "wrong argument type");
	}
	
	rb_iv_set(self, "@method", method);

	return self;
}

/*
 * CbMethod::interaction?
 */
static VALUE cbmethod_getinteraction(VALUE self)
{
	return rb_iv_get(self, "@it");
}

/*
 * CbMethod::call(recv, ...)
 */
static VALUE cbmethod_call(int argc, VALUE *argv, VALUE self)
{
	VALUE recv, rest;
	VALUE method = rb_iv_get(self, "@method");

	rb_scan_args(argc, argv, "1*", &recv, &rest); 
	
	if (TYPE(method) == T_SYMBOL) {
		return rb_funcall2(recv, SYM2ID(method), --argc, ++argv);
	}
	else {
		return rb_funcall2(method, rb_intern("call"), --argc, ++argv);
	}
}

void init_cbmethod(void)
{
	/* Class CbMethod */
	cCbMethod = rb_define_class_under(mSASL, "CbMethod", rb_cObject);

	rb_define_method(cCbMethod, "initialize", cbmethod_new, 3);
	rb_define_method(cCbMethod, "interaction?", cbmethod_getinteraction, 0);
	rb_define_method(cCbMethod, "call", cbmethod_call, -1);
	
	rb_define_attr(cCbMethod, "id", 1, 0);
	rb_define_attr(cCbMethod, "method", 1, 0);
}

