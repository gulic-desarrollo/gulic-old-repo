<?php
// $Id: libdebug.php,v 1.1.4.3.2.3 2008/04/17 04:32:13 scafmac Exp $

function msg($string) {
  drupal_set_message("<pre style=\"border: 0; margin: 0; padding: 0;\">$string</pre>");
}

function msg_r($object) {
  msg(print_r($object, true));
}

?>
