<?php
if (getenv("PGPASSFILE")!="")
  putenv("PGPASSFILE=".getenv("PGPASSFILE"));
$email = htmlspecialchars($_POST['email']);
if(!empty($_POST['nums'])) {

  $numArray = explode("\n", str_replace("\r", "", $_POST['nums']));
  //$numArray = array_filter(explode("\n", $_POST['nums']));
};

//get db credentials
$file = ''; //insert path to .pgpass file here
$pgpass = file_get_contents($file);

list($first_line) = explode("\n",$pgpass);
list($host, $port, $database, $user, $password) = explode(":",$first_line);

//connect to db
  	$conn = pg_connect("host=$host dbname=$database port=$port user=$user password=$password");
  	if (!$conn) {
	  echo "An error occurred.\n";
	  exit;
	}

//for each value in the nums array
$x = 0;
$output = array();
foreach ($numArray as $iter) {
	$value = pg_escape_string($iter);
	//insert the value into a query and get the result 
	$query = "SELECT record_num FROM sierra_view.varfield_view v WHERE v.field_content = '{$value}'  AND v.varfield_type_code = 'k' AND v.record_type_code = 'b';";
	$row = array();
	$results= pg_query($query)
		or die(pg_last_error());;
	while($row = pg_fetch_array($results)){
	$bibNum = "b".$row[0];
	$output[$x][0] = $iter;
	$output[$x][1] = $bibNum;
	$x++;
	};
};

$startHTML="<html><head><title>Other number to Bib no</title></head><body>";
$headers="<table><thead><tr><th>Input num</th><th>Bib num</th></tr></thead>";
$tableEnd="</table>";
$endHTML="</body></html>";
$message = "";

echo $startHTML;
echo $headers;
foreach($output as $rowOut){
	echo "<tr><td>".$rowOut[0]."</td><td>".$rowOut[1]."</td></tr>";
	$message = $message.$rowOut[1]."\n";
};
echo $tableEnd;

if(mail($email, "Other number to bib number conversion", $message)){
	echo "<p>mail sent to ".$email."</p>";
}
else{
	echo "mail not sent";
};
echo $endHTML;

?>

