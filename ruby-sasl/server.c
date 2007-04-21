#include "sasl.h"

VALUE cServer;

void sasl_init()
{
	VALUE appname = rb_iv_get(mSASL, "appname");
	int result;

	/* Initialize sasl server library */
	result = sasl_server_init(NULL, RSTRING(appname)->ptr);
	
	if(result != SASL_OK)
		sasl_raise(result);

	/* Mark as intialized to avoid appname attribute changes */
	sasl_initialized = 1;
}

/*
 * Server::initialize(service, fqdn, realm, laddr, raddr, flags)
 */
static VALUE server_new(int argc, VALUE *argv, VALUE self)
{
	sasl_conn_t *conn;
	sasl_callback_t *callbacks;
	VALUE rconn, rcallbacks;
	VALUE service, fqdn, realm, laddr, raddr, flags;
	const char *cservice, *cfqdn, *crealm, *claddr, *craddr;
	int cflags;
	int result;
	
	rb_scan_args(argc, argv, "06", &service,
			&fqdn, &realm, &laddr, &raddr, &flags);

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
	
	if(! NIL_P(realm)) {
		Check_Type(realm, T_STRING);
		crealm = RSTRING(realm)->ptr; 
	}
	else crealm = NULL;
	
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
	
	/* Initialize sasl library */
	sasl_init();
	
	callbacks = common_sasl_callbacks(self);

	/* Invoke sasl_server_new() */
	result = sasl_server_new(cservice, cfqdn, crealm, claddr, craddr,
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
 * Server::step(input)
 */
static VALUE server_step(VALUE self, VALUE input)
{
	sasl_conn_t *conn;
	int result;
	const char *out;
	unsigned len;
	
	Check_Type(input, T_STRING);

	Data_Get_Struct(rb_iv_get(self, "@conn"), sasl_conn_t, conn);
	
	/* Invoke sasl_server_step() */
	result = sasl_server_step(conn, RSTRING(input)->ptr,
			RSTRING(input)->len, &out, &len);
	
	if(result != SASL_OK && result != SASL_CONTINUE)
		sasl_raise(result);

	if(result == SASL_CONTINUE) {
		VALUE output = rb_str_new(out, len);
		
		if(rb_block_given_p()) {
			input = rb_yield(output);
		}
		else {
			return output;
		}
	}
	
	return Qnil;
}

/*
 * Server::start(mech, input)
 */
static VALUE server_start(int argc, VALUE *argv, VALUE self)
{
	sasl_conn_t *conn;
	int result;
	VALUE mech, input;
	const char *out, *cinput;
	unsigned inlen, outlen;

	rb_scan_args(argc, argv, "11", &mech, &input);
	cinput = NIL_P(input)	? NULL : RSTRING(input)->ptr;
	inlen	= NIL_P(input)	? 0 : RSTRING(input)->len;

	/* Invoke sasl_server_start() */
	Data_Get_Struct(rb_iv_get(self, "@conn"), sasl_conn_t, conn);
	result = sasl_server_start(conn, RSTRING(mech)->ptr,
			cinput, inlen, &out, &outlen);

	if(result != SASL_OK && result != SASL_CONTINUE)
		sasl_raise(result);

	if(result == SASL_CONTINUE) {
		VALUE output = rb_str_new(out, outlen);
		
		if(rb_block_given_p()) {
			input = rb_yield(output);
			rb_funcall(self, rb_intern("step"), 1, input);
		}
		else {
			return output;
		}
	}
	
	return Qnil;
}

/*
 * Server::listmech()
 */
static VALUE server_listmech(VALUE self)
{
	sasl_conn_t *conn;
	int result, count;
	const char *out;
	unsigned len;

	/* Invoke sasl_checkpass() */
	Data_Get_Struct(rb_iv_get(self, "@conn"), sasl_conn_t, conn);
	result = sasl_listmech(conn, NULL, "", ":", "", &out, &len, &count);

	if(result != SASL_OK)
		sasl_raise(result);

	return rb_str_split(rb_str_new(out, len), ":");
}

/*
 * Server::checkpass(user, pass)
 */
static VALUE server_checkpass(VALUE self, VALUE user, VALUE pass)
{
	sasl_conn_t *conn;
	int result;

	/* Invoke sasl_checkpass() */
	Data_Get_Struct(rb_iv_get(self, "@conn"), sasl_conn_t, conn);
	result = sasl_checkpass(conn, RSTRING(user)->ptr, RSTRING(user)->len,
			RSTRING(pass)->ptr, RSTRING(pass)->len);

	if(result == SASL_DISABLED)
		return Qfalse;
	else if(result == SASL_NOUSER)
		return Qfalse;
	else if(result != SASL_OK)
		sasl_raise(result);

	return Qtrue;
}

void init_server(void)
{
	VALUE cbmethods;
	
	/* Class Server */
	cServer = rb_define_class_under(mSASL, "Server", rb_cObject);

	rb_define_method(cServer, "initialize", server_new, -1);
	rb_define_method(cServer, "start", server_start, -1);
	rb_define_method(cServer, "step", server_step, 1);
	rb_define_method(cServer, "listmech", server_listmech, 0);
	rb_define_method(cServer, "checkpass", server_checkpass, 2);
	rb_define_method(cServer, "callback", common_callback, -1);

	rb_define_singleton_method(cClient, "register_callback",
			common_register_callback, -1);

	rb_define_attr(cServer, "mechusing", 1, 0);
	
	/* Make callback methods list */
	cbmethods = rb_hash_new();
	rb_define_class_variable(cServer, "@@cbmethods", cbmethods);
}

