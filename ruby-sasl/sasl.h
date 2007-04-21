#ifndef ___SASL_SASL_H_
#define ___SASL_SASL_H_

#include <ruby.h>
#include <sasl/sasl.h>

#define DEFAULT_SERVICE_NAME	"none"

extern VALUE mSASL;
extern VALUE cClient;
extern VALUE cServer;
extern VALUE cCbMethod;
extern VALUE eSASLError;

extern int sasl_initialized;

void sasl_raise(int);

void common_dispose_conn(sasl_conn_t *);
void common_dispose_callbacks(sasl_callback_t *);

sasl_callback_t *common_sasl_callbacks(VALUE);
void common_process_interaction(VALUE, sasl_interact_t *);
VALUE common_callback(int, VALUE *, VALUE);
VALUE common_interaction(int, VALUE *, VALUE);
VALUE common_register_callback(int, VALUE *, VALUE);
VALUE common_register_interaction(int, VALUE *, VALUE);

void init_error(void);
void init_cbmethod(void);
void init_client(void);
void init_server(void);

#endif   /* ___SASL_SASL_H_ */

