<?php
	if (! isset($_POST['n']) || ! isset($_POST['c']))
		die("No se han enviado las variables necesarias");

	$name=$_POST['n'];
	$text=$_POST['c'];

	//some weird conversion of the data inputed
	//$name = str_replace("\'","'",$name);
	//$name = str_replace("'","\'",$name);
	//$text = str_replace("\'","'",$text);
	//$text = str_replace("'","\'",$text);
	$text = str_replace("---"," - - ",$text);
	$name = str_replace("---"," - - ",$name);
	$text = trim($text);
	$name = trim($name);

	//the message is cut of after 500 letters
	if (strlen($text) > 500)
		$text = substr($text,0,500);

	//to allow for linebreaks a space is inserted every 50 letters
	$text = preg_replace("/([^\s]{50})/","$1 ",$text);

	//the name is shortened to 30 letters
	if (strlen($name) > 30)
		$name = substr($name, 0,30);

	//only if a name and a message have been provides the information is added to the db
	if ($name != '' && $text != '') {
		//$handle = fopen("/var/run/apache2/fifo_chat", 'w');
		//fwrite($handle, $name.": ".$text);
		//fclose($handle);

		/* esto es para php5 */
		/*
		$client = new SoapClient(null, array('location' => "http://localhost:1212/",
						     'uri'      => "gulic.org"));
		$client->sendmessage($name.": ".$text);
		*/

		/* esto php4 */
		require 'SOAP/Client.php';
		$soapclient = new SOAP_Client('http://localhost:1212/');
		$options = array('namespace' => 'gulic.org');
		$ret = $soapclient->call('sendmessage',
			 $params = array('param0' => $name, 'param1' => $text),
			 $options);
	}
?>
