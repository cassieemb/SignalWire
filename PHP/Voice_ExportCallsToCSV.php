<?php
require './vendor/autoload.php';
use SignalWire\Rest\Client;
$dotenv = Dotenv\Dotenv::createImmutable(__DIR__);
$dotenv->safeLoad();

$client = new Client($_ENV["PROJECT_ID"], $_ENV["AUTH_TOKEN"], array("signalwireSpaceUrl" => $_ENV["SPACE_URL"]));

// list calls filtered by optional parameters from docs
$calls = $client->calls->read([
    "startTimeAfter" => "2021-04-01",
    "startTimeBefore" => "2023-04-20",
    //'Status' => 'busy', // filter by Status
    //'From' => '+1xxxxxxxxxx', // filter by From
    //'To' => '+1xxxxxxxxxx', // filter by To
]);

// Write Headers
$fields = array('SID', 'From', 'To', 'Date', 'Status', 'Direction', 'Price');
echo '"'.implode('","', $fields).'"'."\n";

// Open File named TodaysDate_messageReport
$fp = fopen(date("Y-m-d").'_callReport.csv', 'w');

// Insert headers
fputcsv($fp, $fields);

// Write rows
foreach ($calls as $call) {
    $row = array(
        $call->sid,
        $call->from,
        $call->to,
        $call->startTime->format('Y-m-d H:i:s'),
        $call->status,
        $call->direction,
        $call->price,
    );

    // Insert rows into CSV
    fputcsv($fp, $row);
    echo '"'.implode('","', $row).'"'."\n";
}

// close file
fclose($fp);
