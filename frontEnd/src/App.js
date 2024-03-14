import React, { useState } from 'react';

function MyForm() {
    const [activitesName, setActivitesName] = useState('');
    const [type, setType] = useState('');
    const [numberOfPages, setNumberOfPages] = useState('');

    const scrape = async (e) => {
      e.preventDefault();
      // Send the URLs to the server with fetch
      fetch("http://localhost:5000/setup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({"activites_name": activitesName, "type": type, "number_of_pages": numberOfPages}),
      })
        .then((response) => {
          // Start the EventSource connection
          const eventSource = new EventSource("http://localhost:5000/scrape");
  
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
      <input type="text" value={activitesName} onChange={e => setActivitesName(e.target.value)} placeholder="Activites Name" />
      <input type="text" value={type} onChange={e => setType(e.target.value)} placeholder="Type" />
      <input type="text" value={numberOfPages} onChange={e => setNumberOfPages(e.target.value)} placeholder="Number of Pages" />
      <button type="submit">Submit</button>
    </form>
  );
}

export default MyForm;