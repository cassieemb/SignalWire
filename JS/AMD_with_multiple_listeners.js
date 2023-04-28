import {Voice} from "@signalwire/realtime-api";
import "dotenv/config.js";

const client = new Voice.Client({
    project: process.env.PROJECT_ID,
    token: process.env.AUTH_TOKEN,
    contexts: ["office"],
    /* 
    Uncomment for Debugging
    debug: {
        logWsTraffic: true,
    },
    */
});

try {
    // create call
    const call = await client.dialPhone({
        from: process.env.FROM_NUMBER,
        to: process.env.PERSONAL_NUMBER,
        timeout: 30
    });
    console.log('The call has been answered!', call.id)
    const recording = await call.recordAudio({ direction: "both" });

    // Attach event listeners to handle different events
    call.on('detect.updated', async ({detect}) => {
        console.log('>>> detect.updated', detect)
        const determination = detect.params.event
        switch (determination) {
            case "HUMAN":
                console.log("Received human, carry on")
                break;
            case "MACHINE":
                console.log("Received machine, execute machine instructions")
                // stop currently playing tts or audio
                // pause to account for answering machine
                const playback = await call.playAudio({
                    url: "https://www2.cs.uic.edu/~i101/SoundFiles/preamble10.wav",
                });
                await playback.ended();
                await call.hangup()
                break;
            default:
                console.log("Unknown Result: ", determination)
        }
    })
    call.on('detect.ended', ({detect}) => {
        console.log('>>> detect.ended', detect)
    })
    call.on('detect.failed', (obj) => {
        console.log('>>> detect.failed', obj)
    })

    // Run AMD
    const detector = call.amd({
        timeout: 8,
        waitForBeep: true,
    })

    // start speaking to callee while AMD is processing, this call flow assumes the caller is human until proven otherwise
    const speech = await call.playTTS({
        text: "Hello Parent of Houston ISD. Please stay on the line to hear an important message about your student.",
    });
    await speech.ended()
    const playback = await call.playAudio({
        url: "https://www2.cs.uic.edu/~i101/SoundFiles/gettysburg10.wav",
    });
    await playback.ended();
    await call.hangup()

} catch (e) {
    console.error(e)
}

