<?php
require './vendor/autoload.php';
use SignalWire\Rest\Client;
$dotenv = Dotenv\Dotenv::createImmutable(__DIR__ . '/../../');
$dotenv->safeLoad();

$client = new Client($_ENV["PROJECT_ID"], $_ENV["AUTH_TOKEN"], array("signalwireSpaceUrl" => $_ENV["SPACE_URL"]));

// list messages filtered by optional parameters from docs
$messages = $client->messages->read([
    "dateSentAfter" => "2021-04-01",
    "dateSentBefore" => "2023-04-20",
    //'Status' => 'busy', // filter by Status
    //'From' => '+1xxxxxxxxxx', // filter by From
    //'To' => '+1xxxxxxxxxx', // filter by To
]);

// Write Headers
$fields = array('SID', 'From', 'To', 'Date', 'Status', 'Direction', 'Price');
echo '"'.implode('","', $fields).'"'."\n";

// Open File named TodaysDate_messageReport
$fp = fopen(date("Y-m-d").'_messageReport.csv', 'w');

// Insert headers
fputcsv($fp, $fields);

// Write rows
foreach ($messages as $message) {
    $row = array(
        $message->sid,
        $message->from,
        $message->to,
        $message->dateSent->format('Y-m-d H:i:s'),
        $message->status,
        $message->direction,
        $message->price,
    );

    // Insert rows into CSV
    fputcsv($fp, $row);
    echo '"'.implode('","', $row).'"'."\n";
}

// close file
fclose($fp);
