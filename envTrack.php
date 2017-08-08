<?php

function isValidJSON($str) {
   json_decode($str);
   return json_last_error() == JSON_ERROR_NONE;
}

$json_params = file_get_contents("php://input");

$success = false;

if (strlen($json_params) > 0 && isValidJSON($json_params)){
    $success=true;
    $decoded_params = json_decode($json_params, true);

    $servername = "<YOUR_SERVER>";
    $username = "<YOUR_DB_USERNAME>";
    $password = "<YOUR_DB_PASSWORD>";
    $dB = "<YOUR_DB_NAME>";

    // Create connection
    $conn = mysql_connect($servername, $username, $password);

    // Check connection
    if ($conn->connect_error) {
        die("Connection failed: " . mysql_error());
    } 
    mysql_select_db($dB);

	$sql = "INSERT INTO env (id, temperatureC, humidity) VALUES ('" . $decoded_params['id'] . "','" . $decoded_params['temperature_C'] . "','" . $decoded_params['humidity'] . "')";
	
	if (!$result = mysql_query($sql))
	{
		die('There was an error running the query [' . mysql_error() . ']');
        $success=false;
	}
}

if (success)
{
    echo "OK";
}

?>