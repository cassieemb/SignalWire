require "signalwire/sdk"
require "csv"
require "dotenv"

Dotenv.load("./../.env")

@client = Signalwire::REST::Client.new ENV["PROJECT_ID"], ENV["AUTH_TOKEN"], signalwire_space_url: ENV["SPACE_URL"]

start_date = DateTime.now - 7

# Filter by optional parameters specified in docs
calls = @client.calls.list(status: "failed", start_time_after: start_date.to_time)

# Create headers
headers = %w[SID Date Direction From To Price Status]

calls.each do |record|
  # Create and open a CSV
  CSV.open("Calls.csv", "w+") do |csv|
    # Insert headers
    csv << headers
    # For each call record, insert a row.Make sure the order of parameters matches the order of the headers, or the data will be mismatched.
    calls.each do |record|
      csv << [record.sid, record.start_time, record.direction, record.from, record.to, record.price, record.status]
    end
  end
end
