#include <ruby.h>
#include <st.h>
#include <sasl/sasl.h>
#include "sasl.h"

#define DEF_CONST_BASE(obj, prefix, x) \
	rb_define_const(obj, #x, INT2FIX(prefix##x))
#define DEF_CONST(x)		 DEF_CONST_BASE(mSASL, SASL_, x)
#define DEF_CONST_SEC(x) DEF_CONST_BASE(mSecurity, SASL_SEC_, x)
#define DEF_CONST_LOG(x) DEF_CONST_BASE(mLog, SASL_LOG_, x)
#define DEF_CONST_CB(x)	DEF_CONST_BASE(mCallback, SASL_CB_, x)
#define DEF_CONST_CU(x)	DEF_CONST_BASE(mCanonical, SASL_CU_, x)
#define DEF_CONST_SET(x) DEF_CONST_BASE(mSetPass, SASL_SET_, x)
#define DEF_CONST_AUX(x) \
	rb_define_const(mAuxiliary, #x, rb_str_new2(SASL_AUX_##x))

VALUE mSASL;
int sasl_initialized = 0;

/*
 * SASL::appname?
 */
VALUE sasl_get_appname(VALUE self)
{
	return rb_iv_get(mSASL, "appname");
}

/*
 * SASL::appname= value
 */
VALUE sasl_set_appname(VALUE self, VALUE value)
{
	if (sasl_initialized) {
		return sasl_get_appname(self);
	}

	value = NIL_P(value) ? rb_gv_get("$0") : value;
	Check_Type(value, T_STRING);
	return rb_iv_set(mSASL, "appname", value);
}

void Init_sasl(void)
{
	VALUE mSecurity, mLog, mCallback, mCanonical, mSetPass, mAuxiliary;

	/* Module SASL */
	mSASL		= rb_define_module("SASL");
	mSecurity	= rb_define_module_under(mSASL, "Security");
	mLog		= rb_define_module_under(mSASL, "Log");
	mCallback	= rb_define_module_under(mSASL, "Callback");
	mCanonical	= rb_define_module_under(mSASL, "Canonical");
	mSetPass	= rb_define_module_under(mSASL, "SetPass");
	mAuxiliary	= rb_define_module_under(mSASL, "Auxiliary");

	/* Version numbers */
	DEF_CONST(VERSION_MAJOR);
	DEF_CONST(VERSION_MINOR);
	DEF_CONST(VERSION_STEP);

	/* Result codes */
	DEF_CONST(CONTINUE);
	DEF_CONST(OK);
	DEF_CONST(FAIL);
	DEF_CONST(NOMEM);
	DEF_CONST(BUFOVER);
	DEF_CONST(NOMECH);
	DEF_CONST(BADPROT);
	DEF_CONST(NOTDONE);
	DEF_CONST(BADPARAM);
	DEF_CONST(TRYAGAIN);
	DEF_CONST(NOTINIT);

	DEF_CONST(INTERACT);
	DEF_CONST(BADSERV);
	DEF_CONST(WRONGMECH);

	DEF_CONST(BADAUTH);
	DEF_CONST(NOAUTHZ);
	DEF_CONST(TOOWEAK);
	DEF_CONST(ENCRYPT);
	DEF_CONST(TRANS);
	DEF_CONST(EXPIRED);
	DEF_CONST(DISABLED);
	DEF_CONST(NOUSER);
	DEF_CONST(UNAVAIL);
	DEF_CONST(NOVERIFY);
	DEF_CONST(PWLOCK);
	DEF_CONST(NOCHANGE);
	DEF_CONST(WEAKPASS);
	DEF_CONST(NOUSERPASS);

	/* Usage flags for sasl_server_new() and sasl_client_new() */
	DEF_CONST(SUCCESS_DATA);
	DEF_CONST(NEED_PROXY);

	/* Security property types */
	DEF_CONST_SEC(NOPLAINTEXT);
	DEF_CONST_SEC(NOACTIVE);
	DEF_CONST_SEC(NODICTIONARY);
	DEF_CONST_SEC(FORWARD_SECRECY);
	DEF_CONST_SEC(NOANONYMOUS);
	DEF_CONST_SEC(PASS_CREDENTIALS);
	DEF_CONST_SEC(MUTUAL_AUTH);
	DEF_CONST_SEC(MAXIMUM);

	/* Log */
	DEF_CONST_LOG(NONE);
	DEF_CONST_LOG(ERR);
	DEF_CONST_LOG(FAIL);
	DEF_CONST_LOG(WARN);
	DEF_CONST_LOG(NOTE);
	DEF_CONST_LOG(DEBUG);
	DEF_CONST_LOG(TRACE);
	DEF_CONST_LOG(PASS);

	/* Canonicalization function flags */
	DEF_CONST_CU(NONE);
	DEF_CONST_CU(AUTHID);
	DEF_CONST_CU(AUTHZID);

	/* Callbacks */
	DEF_CONST_CB(GETOPT);
	DEF_CONST_CB(LOG);
	DEF_CONST_CB(GETPATH);
	DEF_CONST_CB(VERIFYFILE);
	DEF_CONST_CB(USER);
	DEF_CONST_CB(AUTHNAME);
	DEF_CONST_CB(LANGUAGE);
	DEF_CONST_CB(CNONCE);
	DEF_CONST_CB(PASS);
	DEF_CONST_CB(ECHOPROMPT);
	DEF_CONST_CB(NOECHOPROMPT);
	DEF_CONST_CB(GETREALM);
	DEF_CONST_CB(PROXY_POLICY);
	DEF_CONST_CB(SERVER_USERDB_CHECKPASS);
	DEF_CONST_CB(SERVER_USERDB_SETPASS);
	DEF_CONST_CB(CANON_USER);

	DEF_CONST(NOLOG);
	DEF_CONST(USERNAME);
	DEF_CONST(SSF);
	DEF_CONST(MAXOUTBUF);
	DEF_CONST(DEFUSERREALM);
	DEF_CONST(GETOPTCTX);
	DEF_CONST(CALLBACK);
	DEF_CONST(IPLOCALPORT);
	DEF_CONST(IPREMOTEPORT);
	DEF_CONST(PLUGERR);
	DEF_CONST(DELEGATEDCREDS);
	DEF_CONST(SERVICE);
	DEF_CONST(SERVERFQDN);
	DEF_CONST(AUTHSOURCE);
	DEF_CONST(MECHNAME);
	DEF_CONST(AUTHUSER);
	DEF_CONST(APPNAME);
	DEF_CONST(SSF_EXTERNAL);
	DEF_CONST(SEC_PROPS);
	DEF_CONST(AUTH_EXTERNAL);

	/* For sasl_user_exists */
	DEF_CONST_SET(CREATE);
	DEF_CONST_SET(DISABLE);
	DEF_CONST_SET(NOPLAIN);
	DEF_CONST_SET(CURMECH_ONLY);

	/* Auxiliary property support */
	DEF_CONST_AUX(PASSWORD_PROP);
	DEF_CONST_AUX(PASSWORD);
	DEF_CONST_AUX(UIDNUM);
	DEF_CONST_AUX(GIDNUM);
	DEF_CONST_AUX(FULLNAME);
	DEF_CONST_AUX(HOMEDIR);
	DEF_CONST_AUX(SHELL);
	DEF_CONST_AUX(MAILADDR);
	DEF_CONST_AUX(UNIXMBX);
	DEF_CONST_AUX(MAILCHAN);

	/* Create accessor methods for settable application name */
	rb_define_module_function(mSASL, "appname?", sasl_get_appname, 0);
	rb_define_module_function(mSASL, "appname=", sasl_set_appname, 1);
	sasl_set_appname(mSASL, rb_gv_get("$0"));

	/* Classes */
	init_error();
	init_cbmethod();
	init_client();
	init_server();
}
