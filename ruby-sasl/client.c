#include "sasl.h"

VALUE cClient;

/*
 * Client::initialize(service, fqdn, laddr, raddr, flags)
 */
static VALUE client_new(int argc, VALUE *argv, VALUE self)
{
	sasl_conn_t *conn;
	sasl_callback_t *callbacks;
	VALUE rconn, rcallbacks;
	VALUE service, fqdn, laddr, raddr, flags;
	const char *cservice, *cfqdn, *claddr, *craddr;
	int cflags;
	int result;

	rb_scan_args(argc, argv, "05", &service, &fqdn, &laddr, &raddr, &flags);
	
	if(! NIL_P(service)) {
		Check_Type(service, T_STRING);
		cservice = RSTRING(service)->ptr; 
	}
	else cservice = DEFAULT_SERVICE_NAME;
	
	if(! NIL_P(fqdn)) {
		Check_Type(fqdn, T_STRING);
		cfqdn = RSTRING(fqdn)->ptr; 
	}
	else cfqdn = NULL;
	
	if(! NIL_P(laddr)) {
		Check_Type(laddr, T_STRING);
		claddr = RSTRING(laddr)->ptr; 
	}
	else claddr = NULL;
	
	if(! NIL_P(raddr)) {
		Check_Type(raddr, T_STRING);
		craddr = RSTRING(raddr)->ptr; 
	}
	else craddr = NULL;
	
	if(! NIL_P(flags)) {
		Check_Type(flags, T_FIXNUM);
		cflags = FIX2INT(flags); 
	}
	else cflags = 0;
	
	callbacks = common_sasl_callbacks(self);

	/* Invoke sasl_client_new() */
	result = sasl_client_new(cservice, cfqdn, claddr, craddr,
			callbacks, cflags, &conn); 
	if(result != SASL_OK)
		sasl_raise(result);

	/* @conn = conn */
	rconn = Data_Wrap_Struct(rb_cData, 0, common_dispose_conn, conn);
	rb_iv_set(self, "@conn", rconn);

	/* @callbacks = callbacks */
	rcallbacks = Data_Wrap_Struct(rb_cData, 0,
			common_dispose_callbacks, callbacks);
	rb_iv_set(self, "@callbacks", rcallbacks);
	
	/* @cbmethods = @@cbmethods */
	VALUE cbmethods = rb_cv_get(CLASS_OF(self), "@@cbmethods");
	rb_iv_set(self, "@cbmethods", cbmethods);
	
	/* @mechusing = nil */
	rb_iv_set(self, "@mechusing", Qnil);

	return self;
}

/*
 * Client::step(input)
 */
static VALUE client_step(VALUE self, VALUE input)
{
	int result;
	sasl_conn_t *conn;
	sasl_interact_t *interact;

	Check_Type(input, T_STRING);
	
	Data_Get_Struct(rb_iv_get(self, "@conn"), sasl_conn_t, conn);
	do {
		const char *out;
		unsigned len;

		/* Invoke sasl_client_step() */
		result = sasl_client_step(conn, RSTRING(input)->ptr,
				RSTRING(input)->len, &interact, &out, &len);
		
		if(result == SASL_INTERACT) {
			common_process_interaction(self, interact);
		}
		else if(result == SASL_CONTINUE) {						
			VALUE output = rb_str_new(out, len);
			
			if(rb_block_given_p()) {
				input = rb_yield(output);
			}
			else {
				return output;
			}			
		}
		
	} while(result == SASL_INTERACT || result == SASL_CONTINUE);

	if(result != SASL_OK)
		sasl_raise(result);

	return Qnil;
}

/*
 * Client::start(mechlist)
 */
static VALUE client_start(VALUE self, VALUE mechlist)
{
	sasl_conn_t *conn;
	int result;
	const char *out, *cmechlist, *mechusing;
	unsigned len;
	VALUE input, output;
	sasl_interact_t *interact = NULL;

	/* Get mechlist */
	if(TYPE(mechlist) == T_ARRAY) {
		int i;
		VALUE mlbuf = rb_str_new2("");

		for(i = 0; i < RARRAY(mechlist)->len; ++i) {
			if(i > 0)
				rb_str_concat(mlbuf, INT2FIX(' '));
			rb_str_concat(mlbuf, RARRAY(mechlist)->ptr[i]);
		}

		rb_p(mlbuf);
		cmechlist = RSTRING(mlbuf)->ptr;
	}
	else if(TYPE(mechlist) == T_STRING) {
		cmechlist = RSTRING(mechlist)->ptr;
	}
	else {
		rb_raise(rb_eTypeError, "cannot understand mechlist");
	}

	/* Invoke sasl_client_start() */
	Data_Get_Struct(rb_iv_get(self, "@conn"), sasl_conn_t, conn);
	do {
		result = sasl_client_start(conn, cmechlist, &interact,
				&out, &len, &mechusing);

		if(result == SASL_INTERACT) {
			common_process_interaction(self, interact);
		}
	} while(result == SASL_INTERACT);

	if(result != SASL_OK && result != SASL_CONTINUE) {
		sasl_raise(result);
	}

	rb_iv_set(self, "@mechusing", rb_str_new2(mechusing));
	output = rb_str_new(out, len);

	/* Invoke block for next step if was given */
	if(result == SASL_CONTINUE && rb_block_given_p()) {
		input = rb_yield(output);
		rb_funcall(self, rb_intern("step"), 1, input);

		return Qnil;
	}
	/* or return output in otherwise */
	else {
		return output;
	}
}

void init_client(void)
{
	VALUE cbmethods;

	/* Class Client */
	cClient = rb_define_class_under(mSASL, "Client", rb_cObject);

	rb_define_method(cClient, "initialize", client_new, -1);
	rb_define_method(cClient, "start", client_start, 1);
	rb_define_method(cClient, "step", client_step, 1);
	rb_define_method(cClient, "callback", common_callback, -1);
	rb_define_method(cClient, "interaction", common_interaction, -1);
	
	rb_define_singleton_method(cClient, "register_callback",
			common_register_callback, -1);
	rb_define_singleton_method(cClient, "register_interaction",
			common_register_interaction, -1);

	rb_define_attr(cClient, "mechusing", 1, 0);

	/* Make callback methods list */
	cbmethods = rb_hash_new();
	rb_define_class_variable(cClient, "@@cbmethods", cbmethods);

	rb_funcall(cClient, rb_intern("register_interaction"),
			2, INT2FIX(SASL_CB_PASS), ID2SYM(rb_intern("pass")));

	/* Initialize sasl client library */
	sasl_client_init(NULL);
}

