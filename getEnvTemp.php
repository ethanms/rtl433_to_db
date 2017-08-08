<?php
$interval = $_REQUEST["interval"];
$sensor = $_REQUEST["sensor"];

if (!$sensor)
	$sensor = "15108"; // This is the ID of the default sensor I want

if ((!$interval) || ($interval < 1) || ($interval > 8760))
	$interval = 48;

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

$sql = "SELECT UNIX_TIMESTAMP(timestamp) AS timestamp, temperatureC
		FROM env 
		WHERE timestamp >= (NOW() - INTERVAL " . $interval . " HOUR)
                AND id = '" . $sensor . "' 
		ORDER BY timestamp";

if (!$result = mysql_query($sql)){
	die('There was an error running the query [' . mysql_error() . ']');
}	

$big_data = array();

while ($row = mysql_fetch_assoc($result)){
    $data = array();
    $data[] = ($row[timestamp]*1000);
    $data[] = floatval(($row[temperatureC]*1.8)+32);

    $big_data[] = $data;
}

echo json_encode($big_data);
?>
