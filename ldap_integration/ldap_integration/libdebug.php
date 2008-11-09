<?php
// $Id: libdebug.php,v 1.2 2007/01/28 20:38:03 kreaper Exp $

function msg($string) {
  drupal_set_message("<pre style=\"border: 0; margin: 0; padding: 0;\">$string</pre>");
}

function msg_r($object) {
  msg(print_r($object, true));
}

?>
