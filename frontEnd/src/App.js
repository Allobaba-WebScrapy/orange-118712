import React, { useState } from 'react';

function MyForm() {
  const [activitesName, setActivitesName] = useState('');
  const [type, setType] = useState('');
  const [numberOfPages, setNumberOfPages] = useState('');

  const scrape = async (e) => {
    e.preventDefault();
    // Send the URLs to the server with fetch
    fetch("http://localhost:5100/setup", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({"activites_name": activitesName, "type": type, "number_of_pages": numberOfPages}),
    })
    .then((response) => {
      // Start the EventSource connection
      const eventSource = new EventSource("http://localhost:5100/scrape");
  
      eventSource.addEventListener("done", function (event) {
      // Close the connection when the 'done' event is received
      console.log("Received done event, closing connection.");
      eventSource.close();
      });
  
      eventSource.onmessage = function (event) {
      const data = JSON.parse(event.data);
      console.log(data);
      };
      eventSource.onerror = function (error) {
      console.error("EventSource failed:", error);
      eventSource.close();
      };
    })
    .catch((error) => {
      console.error("Error:", error);
    });
  };
  

  return (
    <form onSubmit={(e)=>scrape(e)}>
      
      {/* ACTIVITIES NAME */}
      <select value={activitesName} onChange={e => setActivitesName(e.target.value)} className="border border-gray-300 rounded-md p-2 mb-2">
        <option value="">Select an option</option>
        <option value="Boulangeries">Boulangeries</option>
        <option value="Fleuristes">Fleuristes</option>
        <option value="Restaurants">Restaurants</option>
        <option value="Médecins">Médecins</option>
        <option value="Coiffeurs">Coiffeurs</option>
        <option value="Garages">Garages</option>
        <option value="Super marchés">Super marchés</option>
        <option value="Dentistes">Dentistes</option>
        <option value="Serruriers">Serruriers</option>
        <option value="Bricolage">Bricolage</option>
        <option value="Mairies">Mairies</option>
        <option value="Cafés">Cafés</option>
      </select>
      
      {/* TYPE(B2B/B2C/All) */}
      <div className="mb-2">
        <input type="radio" id="b2b" name="type" value="B2B" checked={type === 'B2B'} onChange={e => setType(e.target.value)} className="border border-gray-300 rounded-md p-2" />
        <label for="b2b">B2B</label>
        <input type="radio" id="b2c" name="type" value="B2C" checked={type === 'B2C'} onChange={e => setType(e.target.value)} className="border border-gray-300 rounded-md p-2" />
        <label for="b2c">B2C</label>
        <input type="radio" id="all" name="type" value="All" checked={type === 'All'} onChange={e => setType(e.target.value)} className="border border-gray-300 rounded-md p-2" />
        <label for="all">All</label>
      </div>
      
      {/* NUMBER OF PAGES */}
      <input type="text" value={numberOfPages} onChange={e => setNumberOfPages(e.target.value)} placeholder="Number of Pages" className="border border-gray-300 rounded-md p-2 mb-2" />
      
      {/* SUBMIT BUTTON */}
      <button type="submit" className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Submit</button>
    </form>
  );
}

export default MyForm;