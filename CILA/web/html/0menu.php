<?php

$file = "html/0menu.xml";
$isatsection = 0;
$opensection = 0;
$opensubsection = 0;

function startElement($parser, $name, $attrs) {
	global $isatsection, $opensection, $isatsubsection, $opensubsection;
	switch ($name)
	{
		case "MENU":
			print "<table border=0 cellspacing=2 cellpadding=0 width=185>";
			break;
		case "TITLE":
			print "<tr><th>";
			break;
		case "SECTION":
			$isatsection = 1;
			if ($opensection)
				$opensection = 0;
			print "<tr><td><font size=3>";
			break;
		case "SUBSECTION":
			$isatsubsection = 1;
			if ($subopensection)
				$subopensection = 0;
			if ($opensection)
				print "<tr><td><font size=2>&nbsp;&nbsp;&nbsp;";
			break;
		case "SUBSUBSECTION":
			if ($opensection || $opensubsection)
				print "<tr><td><font size=1>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";
			break;
		case "LINK":
			if ($isatsection || $opensection)
				print "<a href='";
			break;
		case "TEXT":
			if ($isatsection || $opensection)
				print "onMouseOver=\"javascript:window.status='";
			break;
		case "NAME":
			if ($isatsection || $opensection)
				print "<b>:: ";
			break;
	}
}

function endElement($parser, $name) {
	global $isatsection, $opensection;
	switch ($name)
	{
		case "MENU":
			print "</table>";
			break;
		case "TITLE":
			print "</th></tr>";
			break;
		case "SECTION":
			print "</font></td></tr>";
			$isatsection = 0;
			break;
		case "SUBSECTION":
			if ($isatsection || $opensection)
				print "</font></td></tr>";
			break;
		case "SUBSUBSECTION":
			if ($isatsection || $opensection || $opensubsection)
				print "</font></td></tr>";
			break;
		case "LINK":
			if ($isatsection || $opensection || $opensubsection)
				print "' ";
			break;
		case "TEXT":
			if ($isatsection || $opensection || $opensubsection)
				print "';return true;\">";
			break;
		case "NAME":
			if ($isatsection || $opensection || $opensubsection)
				print "   </b></a>";
			break;
		default:
	}
}

function characterData($parser, $data) {
	global $isatsection, $opensection, $currentsection, $currentsubsection;
	if (($isatsection) && ($data == $currentsection))
		$opensection = 1;
	if (($isatsection) && ($data == $currentsubsection))
		$opensubsection = 1;
    if ($isatsection || $opensection || $opensubsection)
    		if ($data == "Evaluación")
			print "<big><big>$data</big></big>";
		else
			print $data;
}

$xml_parser = xml_parser_create();
// usa case-folding para que estemos seguros de encontrar la etiqueta
// en $map_array
xml_parser_set_option($xml_parser, XML_OPTION_CASE_FOLDING, true);
xml_set_element_handler($xml_parser, "startElement", "endElement");
xml_set_character_data_handler($xml_parser, "characterData");
if (!($fp = fopen($file, "r"))) {
    die("could not open XML input");
}

while ($data = fread($fp, 4096)) {
    if (!xml_parse($xml_parser, $data, feof($fp))) {
        die(sprintf("XML error: %s at line %d",
                    xml_error_string(xml_get_error_code($xml_parser)),
                    xml_get_current_line_number($xml_parser)));
    }
}
xml_parser_free($xml_parser);

?>
