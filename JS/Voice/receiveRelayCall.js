import { Voice } from "@signalwire/realtime-api";
import dotenv from 'dotenv';
dotenv.config({ path: './../.env' })

const client = new Voice.Client({
    project: process.env.PROJECT_ID,
    token: process.env.AUTH_TOKEN,
    contexts: ["office"],
    // host: process.env.HOST // not required in production environments
});

console.log("Started successfully - waiting for a call to be received")

client.on("call.received", async (call) => {
    console.log("Got call", call.from, call.to);

    try {
        await call.answer();
        console.log("Inbound call answered");
        
        await call.playTTS({
          text: "Hello! This script tests several Relay SDK Events. Please enter 4 digits to test collect.",
        });

        const collect = await call.collect({
            digits: {
              max: 5,
              digitTimeout: 4,
              terminators: "#*",
            },
          });
          
          const { digits } = await collect.ended();
          
          console.log("PIN collected:", digits);

          await call.playTTS({
            text: "Thank you! Please listen to the following audio.",
          });

          const playback = await call.playAudio({
            url: "https://cdn.signalwire.com/default-music/welcome.mp3",
          });

          await playback.ended();

          await call.playTTS({
            text: "Thank you! Goodbye now.",
          });
        
          call.hangup();


    } catch (error) {
        console.error("Error answering inbound call", error);
    }
});