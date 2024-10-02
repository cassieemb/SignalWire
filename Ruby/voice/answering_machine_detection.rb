require "rubygems"
require "sinatra"
require "signalwire/sdk"
require "dotenv"

Dotenv.load("./../.env")

set :port, 3000

post "/start" do
  response = Signalwire::Sdk::VoiceResponse.new

  case params[:AnsweredBy]
  when "machine_end_other", "machine_end_silence", "machine_end_beep"
    puts "It's a machine!"
    response.pause(length: 1)

    # replace message with whatever voicemail you want to leave
    response.say(message: "Hello machine! This is the County Medical Center. We are calling you to confirm your doctor appointment. Please call us back as soon as possible.")
    response.hangup
  when "human"
    puts "We got ourselves a live human here!"
    response.say(message: "Hello human! This is the County Medical Center. We are calling you to confirm your doctor appointment. Please call us back as soon as possible.")
    response.hangup
  end

  # return as string
  response.to_s
end
