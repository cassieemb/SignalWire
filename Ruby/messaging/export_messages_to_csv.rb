require 'signalwire/sdk'
require 'csv'
require 'dotenv'

Dotenv.load("./../.env")

@client = Signalwire::REST::Client.new ENV['PROJECT_ID'], ENV['AUTH_TOKEN'], signalwire_space_url: ENV['SPACE_URL']

# Filter by optional parameters specified in docs
messages = @client.messages.list(from: ENV['PERSONAL_NUMBER'])

# Create headers
headers = %w[SID Date Direction From To Price Status]

messages.each do |record|
  # Create and open a CSV
  CSV.open('Messages.csv', 'w+') do |csv|
    # Insert headers
    csv << headers
    # For each message record, insert a row.Make sure the order of parameters matches the order of the headers, or the data will be mismatched.
    messages.each do |record|
      csv << [record.sid, record.date_sent, record.direction, record.from, record.to, record.price, record.status]
    end
  end
end