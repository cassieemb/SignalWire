require "sinatra"
require "uri"
require "net/https"
require "dotenv"

Dotenv.load("./../.env")

set :bind, "0.0.0.0"

# Utility method to perform HTTP requests against the SW Video API
def api_request(payload, endpoint)
  url = URI("https://#{ENV["SPACE_URL"]}/api/video/#{endpoint}")

  http = Net::HTTP.new(url.host, url.port)
  http.use_ssl = true

  request = Net::HTTP::Post.new(url)
  request["Accept"] = "application/json"
  request["Content-Type"] = "application/json"
  request.body = payload.to_json
  request.basic_auth ENV["PROJECT_ID"], ENV["AUTH_TOKEN"]

  response = http.request(request)
  puts response.read_body
end

# Request a token with simple capabilities
def request_token(room, user = nil)
  payload = {
    room_name: room,
    user_name: user.nil? ? "user#{rand(1000)}" : user,
    permissions: %w[room.self.audio_mute room.self.audio_unmute room.self.video_mute room.self.video_unmute],
  }
  result = api_request(payload, "room_tokens")
  puts result
end

# Create a room to join
def create_room(room)
  payload = {
    name: room,
    display_name: room,
    max_participants: 5,
    delete_on_end: false,
  }
  api_request(payload, "rooms")
end

get "/" do
  @room = params[:room] || "room_#{rand(1000)}"
  @user = params[:user] || "user_#{rand(1000)}"

  @room_url = "#{request.base_url}?room=#{@room}"
  create_room(@room)
  @token = request_token(@room, @user)
end
