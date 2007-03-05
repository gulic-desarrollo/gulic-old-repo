<?php
	/*
	XHTML live Chat
	author: alexander kohlhofer
	version: 1.0
	http://www.plasticshore.com
	http://www.plasticshore.com/projects/chat/
	please let the author know if you put any of this to use
	XHTML live Chat (including this code) is published under a creative commons license
	license: http://creativecommons.org/licenses/by-nc-sa/2.0/
	*/

	//Headers are sent to prevent browsers from caching.. IE is still resistent sometimes
	header( "Expires: Mon, 26 Jul 1997 05:00:00 GMT" );
	header( "Last-Modified: " . gmdate( "D, d M Y H:i:s" ) . "GMT" );
	header( "Cache-Control: no-cache, must-revalidate" );
	header( "Pragma: no-cache" );
	header("Content-Type: text/html; charset=utf-8");

	$history = 20;

	//if the request does not provide the id of the last know message the id is set to 0
	$lastID = isset($_GET['lastID']) ? $_GET['lastID'] : 0;

	// establishes a connection to a mySQL Database accroding to the details specified in db.php
	include("db.php"); //contains the given DB setup $db, $server, $user, $pass
	$conn = mysql_connect($server, $user, $pass);
	if (!$conn) die("Connection to DB was not possible!");

	if (!mysql_select_db($db, $conn)) 
		die ("No DB with that name seems to exist at the server!");

	if ($lastID == -1)  {
		$result = mysql_query("SELECT id FROM chatlog ORDER BY id DESC LIMIT 1", $conn);
		//$result = mysql_query("SELECT SQL_CACHE id FROM chatlog ORDER BY id DESC LIMIT 1;", $conn);
		$lastID = mysql_result($result, 0, 0);
		if ($lastID > $history) 
			$lastID -= $history;
		else
			$lastID = 0;
	}

	// retrieves all messages with an id greater than $lastID
	$sql = 	"SELECT * FROM chatlog WHERE id > $lastID ORDER BY id ASC LIMIT $history";
	$results = mysql_query($sql, $conn);

	if (!$results || empty($results)) 
		die('There was an error creating the entry');

	while ($row = mysql_fetch_array($results)) {
		list ($id, $date, $name, $text ) = $row;
		if ($name == '') $name = 'no name';
		if ($text == '') $name = 'no message';
		$name = mb_convert_encoding($name, 'utf-8', 'iso-8859-1');
		$text = mb_convert_encoding($text, 'utf-8', 'iso-8859-1');
		echo "$id---$date---$name---$text---"; // --- is being used to separete the fields in the output
	}

?>
