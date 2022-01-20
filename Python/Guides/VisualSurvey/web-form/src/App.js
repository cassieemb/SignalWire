import React, { useState } from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  useParams,
} from "react-router-dom";
import './style.css';

export default function App() {

  return (
      <Router basename="/">
        <Routes>
          <Route path="/:callSID" element={<WebForm/>} />
        </Routes>
      </Router>
  );
}

// function to send post request using fetch()
async function postData(url = '', data = {}) {

  const response = await fetch(url, {
    method: 'POST',
    mode: 'cors',
    cache: 'no-cache',
    credentials: 'same-origin',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    },
    redirect: 'follow',
    referrerPolicy: 'no-referrer',
    body: JSON.stringify(data)
  });

  return response.json();
}

function WebForm() {

  const [trackingNumber, setTN] = useState('');
  const [arrivalDate, setArrivalDate] = useState('');
  const [typeResidence, setResidence] = useState('');
  const [callbackNumber, setNumber] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  let callSID = useParams()


  const submitHandler = (e) => {
    e.preventDefault()
    console.log('Submit', trackingNumber, arrivalDate, typeResidence, callbackNumber, firstName, lastName, callSID);

    // insert call to flask app with the above data along with callSID
    postData('https://cassiedev.ngrok.io/process_web_form', {"trackingNumber": trackingNumber, "arrivalDate":
      arrivalDate, "typeResidence": typeResidence, "callbackNumber": callbackNumber, "firstName": firstName,
      "lastName": lastName, "callSID": callSID}).then(data => {
        console.log(data)
    })
  };

  return (

      <div>
        <h1>FedUPS Lost Package Center</h1>
        <h3>Please submit the following information so that our team can help to locate your missing package.
          Your answers will be sent to our office.</h3>
        <form onSubmit={submitHandler}>
          <label>Please enter your 10 digit tracking number. </label>
          <input
              type="text"
              name="trackingNumber"
              value={trackingNumber}
              onChange={(e) => setTN(e.target.value)}
          />
          <br />

          <label>What was your expected arrival date? </label>
          <input
              type="date"
              name="arrivalDate"
              value={arrivalDate}
              onChange={(e) => setArrivalDate(e.target.value)}
          />
          <br />

          <label>What type of residence are we delivering to? </label>
          <select
              value={typeResidence}
              name={typeResidence}
              onChange={(e) => setResidence(e.target.value)}>
            <option defaultValue = "noneSelected">Choose a Residence Type</option>
            <option value = "house">House</option>
            <option value = "office">Office</option>
            <option value = "apartment">Apartment</option>
          </select>
          <br />

          <label>What is your callback number? </label>
          <input
              type="text"
              name="callbackNumber"
              value={callbackNumber}
              onChange={(e) => setNumber(e.target.value)}
          />
          <br />

          <label>What is your first name? </label>
          <input
              type="text"
              name="firstName"
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
          />
          <br />

          <label>What is your last name? </label>
          <input
              type="text"
              name="lastName"
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
          />
          <br />
          <br />

          <button type="submit">Send</button>
        </form>
      </div>
  );
}