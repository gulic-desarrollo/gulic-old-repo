#!/usr/bin/env ruby

require 'mkmf'

libpaths = %w(/lib /usr/lib /usr/local/lib).map {|s| s + '/sasl2' }
p libpaths

have_header('sasl/sasl.h')
have_library('sasl2', 'sasl_client_init')

create_makefile('sasl')

