import {RestClient} from "@signalwire/compatibility-api";
import fs from "fs";
import "dotenv/config.js";

const client = new RestClient(process.env.PROJECT_ID, process.env.AUTH_TOKEN, {signalwireSpaceUrl: process.env.SPACE_URL});

// create a file and open it, create array to hold rows
let writeStream = fs.createWriteStream("Messages.csv");
let csvData = [];

// set headers, make sure header order matches order of elements in row below
const header = [
    "Message Sid",
    "To",
    "From",
    "Date Sent",
    "Status",
    "Direction",
    "Price",
];

// push headers into array
csvData.push(header);

// list messages filtered by optional parameters in docs
client.messages
    .list({
        from: process.env.PERSONAL_NUMBER,
        dateSentAfter: new Date(Date.UTC(2022, 4, 1, 0, 0, 0)), // js datetime objects start at 0
        status: "delivered",
    })
    // iterate through results and push each message record into a row
    .then((messages) => {
        messages.forEach((m) => {
            const message_record = [
                m.sid,
                m.to,
                m.from,
                m.dateSent,
                m.status,
                m.direction,
                m.price
            ]
            csvData.push(message_record);
        });

        writeStream.write(csvData.join("\n"), () => {
        });
        writeStream.end();
    });
