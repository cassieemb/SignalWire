import {RestClient} from "@signalwire/compatibility-api";
import fs from "fs";
import dotenv from 'dotenv';
dotenv.config({ path: '../../.env' })

const client = new RestClient(process.env.PROJECT_ID, process.env.AUTH_TOKEN, {signalwireSpaceUrl: process.env.SPACE_URL});

// create a file and open it, create array to hold rows
let writeStream = fs.createWriteStream("Calls.csv");
let csvData = [];

// set headers, make sure header order matches order of elements in row below
const header = [
    "Call Sid",
    "To",
    "From",
    "Date",
    "Status",
    "Direction",
    "Price",
];

// push headers into array
csvData.push(header);

// list calls filtered by optional parameters from docs
client.calls
    .list({
        status: "completed",
        from: process.env.PERSONAL_NUMBER,
        startTimeAfter: new Date(Date.UTC(2022, 4, 1, 0, 0, 0)), // js datetime objects start at 0
    })
    // iterate through results and push each call record into a row
    .then((calls) => {
        calls.forEach((c) => {
            const call_record = [
                c.sid,
                c.to,
                c.from,
                c.startTime,
                c.status,
                c.direction,
                c.price
            ]
            csvData.push(call_record);
        });

        writeStream.write(csvData.join("\n"), () => {
        });
        writeStream.end();
    });
