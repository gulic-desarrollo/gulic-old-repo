#include "sasl.h"

static VALUE default_callback();
static int unsupported_callback();
static int sasl_getsimple_callback(void*, int, const char**, unsigned*);
static int sasl_getsecret_callback(sasl_conn_t*, void*, int, sasl_secret_t**);

/*
 * SASL callback functions. See /usr/include/sasl/sasl.h
 * for a complete description of every callback.
 */
static const sasl_callback_t CALLBACKS[] = {
	/* Common callbacks */
	{ SASL_CB_GETOPT, unsupported_callback, NULL },
	{ SASL_CB_LOG, unsupported_callback, NULL },
	{ SASL_CB_GETPATH, unsupported_callback, NULL },
	{ SASL_CB_VERIFYFILE, unsupported_callback, NULL },
	{ SASL_CB_CANON_USER, unsupported_callback, NULL },
	/* Client-only callbacks */
	{ SASL_CB_USER, sasl_getsimple_callback, NULL},
	{ SASL_CB_AUTHNAME, sasl_getsimple_callback, NULL },
	{ SASL_CB_LANGUAGE, sasl_getsimple_callback, NULL },
	{ SASL_CB_CNONCE, sasl_getsimple_callback, NULL },
	{ SASL_CB_PASS, sasl_getsecret_callback, NULL },
	{ SASL_CB_ECHOPROMPT, unsupported_callback, NULL },
	{ SASL_CB_NOECHOPROMPT, unsupported_callback, NULL },
	{ SASL_CB_GETREALM, unsupported_callback, NULL },
	/* Server-only callbacks */
	{ SASL_CB_PROXY_POLICY, unsupported_callback, NULL },
	{ SASL_CB_SERVER_USERDB_CHECKPASS, unsupported_callback, NULL },
	{ SASL_CB_SERVER_USERDB_SETPASS, unsupported_callback, NULL },
	/* Callback list end */
	{ SASL_CB_LIST_END, NULL, NULL }
};

void common_dispose_conn(sasl_conn_t *ptr)
{
	sasl_dispose(&ptr);
}

void common_dispose_callbacks(sasl_callback_t *ptr)
{
	free((void*)ptr);
}

sasl_callback_t *common_sasl_callbacks(VALUE self)
{
	sasl_callback_t *callbacks, *cbd;
	const sasl_callback_t *cbs;
	VALUE cbmethods;
	unsigned len;
	
	cbmethods = rb_cv_get(CLASS_OF(self), "@@cbmethods");

	len = FIX2UINT(rb_funcall(cbmethods, rb_intern("length"), 0));
	len++;	/* for SASL_CB_LIST_END */
 
	callbacks = ALLOC_N(sasl_callback_t, len);

	for(cbs = CALLBACKS, cbd = callbacks; cbs->id != SASL_CB_LIST_END; cbs++)
	{
		if (! rb_funcall(cbmethods, rb_intern("include?"), 1, INT2FIX(cbs->id)))
			continue;
			
		VALUE method = rb_hash_aref(cbmethods,	INT2FIX(cbs->id));
		if (rb_funcall(method, rb_intern("interaction?"), 0)) {
			cbd->proc = NULL;
			cbd->context = NULL;
		}
		else {
			cbd->proc = cbd->proc;
			cbd->context = ROBJECT(self);
		}
		
		cbd->id = cbs->id;
		cbd++;
	}
	
	/* SASL_CB_LIST_END */
	cbd->id = SASL_CB_LIST_END;
	cbd->proc = NULL;
	cbd->context = NULL;

	return callbacks;
}

void common_process_interaction(VALUE self, sasl_interact_t *interact)
{
	VALUE cbmethods = rb_iv_get(self, "@cbmethods");
	sasl_interact_t *it;

	/* Iterate among interactions */
	for(it = interact; it->id != SASL_CB_LIST_END; ++it) {
		VALUE itid = INT2FIX(it->id);
		VALUE output;
		VALUE challenge = rb_str_new2(it->challenge);
		VALUE prompt = rb_str_new2(it->prompt);
		VALUE defout = Qnil;

		if(it->defresult) {
			defout = rb_str_new2(it->defresult);
		}
		
		/* Invoke callback for the interaction */
		if(rb_funcall(cbmethods, rb_intern("include?"), 1, itid)) {
			/* Registered interaction */
			VALUE method = rb_hash_aref(cbmethods, itid);
			output = rb_funcall(method, rb_intern("call"),
					4, self, challenge, prompt, defout);
			
			if(TYPE(output) == T_STRING){
				it->result = RSTRING(output)->ptr;
				it->len	= RSTRING(output)->len;
			}
		}
		else {
			/* Unregistered interaction */
			default_callback();
		}
	}
}

void _register_callback(VALUE cbmethods, VALUE it, int argc, VALUE *argv)
{
	VALUE cbid, method, block;

	rb_scan_args(argc, argv, "11&", &cbid, &method, &block);

	method = NIL_P(method) ? block : method;
	method = NIL_P(method) ? rb_proc_new(default_callback, -1) : method;

	/* Register callback */
	rb_hash_aset(cbmethods, cbid, rb_funcall(cCbMethod,
				rb_intern("new"), 3, cbid, it, method));
}

/*
 * Object::callback(id, :method){block}
 */
VALUE common_callback(int argc, VALUE *argv, VALUE self)
{
	VALUE cbmethods = rb_iv_get(self, "@cbmethods");

	_register_callback(cbmethods, Qfalse, argc, argv);

	return self;
}

/*
 * Object::interaction(id, :method){block}
 */
VALUE common_interaction(int argc, VALUE *argv, VALUE self)
{
	VALUE cbmethods = rb_iv_get(self, "@cbmethods");

	_register_callback(cbmethods, Qtrue, argc, argv);
	
	return self;
}

/*
 * Class::register_callback(id, :method){block}
 */
VALUE common_register_callback(int argc, VALUE *argv, VALUE self)
{
	VALUE cbmethods = rb_cv_get(self, "@@cbmethods");

	_register_callback(cbmethods, Qfalse, argc, argv);

	return self;
}

/*
 * Class::register_interaction(id, :method){block}
 */
VALUE common_register_interaction(int argc, VALUE *argv, VALUE self)
{
	VALUE cbmethods = rb_cv_get(self, "@@cbmethods");

	_register_callback(cbmethods, Qtrue, argc, argv);
	
	return self;
}

static VALUE default_callback()
{
	rb_raise(rb_eNameError, "undefined callback method");
}

static int unsupported_callback()
{
	rb_raise(rb_eNameError, "unsupported callback");
}

static int sasl_getsimple_callback(void *context, int id, const char **result, unsigned *len)
{
	VALUE self = (VALUE)context;
	VALUE cbmethods = rb_iv_get(self, "@cbmethods");

	/* Invoke callback */
//	if(rb_funcall(cbmethods, rb_intern("include?"), 1, id)) {
//		/* Registered interaction */
//		VALUE method = rb_hash_aref(cbmethods, itid);
//		VALUE output = rb_funcall(method, rb_intern("call"), 0);
//			
//		if(TYPE(output) == T_STRING){
//			*result = RSTRING(output)->ptr;
//			*len = RSTRING(output)->len;
//		}
//	}
//	else {
//		/* Unregistered interaction */
//		default_callback();
//	}
//
//	return SASL_OK;

	rb_raise(rb_eNameError, "unsupported callback");
}

static int sasl_getsecret_callback(sasl_conn_t *conn, void *context, int id, sasl_secret_t **psecret)
{
	VALUE self = (VALUE)context;
	VALUE cbmethods = rb_iv_get(self, "@cbmethods");
	
	rb_raise(rb_eNameError, "unsupported callback");
}
