import React, { useState, useEffect } from 'react';
import socketIOClient from 'socket.io-client';

const ActivityForm = () => {
    const [activityName, setActivityName] = useState('');
    const [activityType, setActivityType] = useState('');
    const [numberOfPages, setNumberOfPages] = useState('');
    const [scrapedData, setScrapedData] = useState('');

    useEffect(() => {
        const socket = socketIOClient('http://localhost:5000');
        socket.on('response', (data) => {
            console.log('Response from server:', data);
            setScrapedData(data);
        });

        return () => socket.disconnect();
    }, []);

    const handleSubmit = async (event) => {
        event.preventDefault();
        
        const requestData = {
            activityName: activityName,
            activityType: activityType,
            numberOfPages: numberOfPages
        };

        try {
            const response = await fetch('http://localhost:5000/scrape', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData)
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            if (Object.keys(data).length === 0) {
                throw new Error('Empty response or invalid JSON format');
            }
            
            console.log('Response from server:', data);
            setScrapedData(data);
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <input type="text" placeholder="Activity Name" value={activityName} onChange={(e) => setActivityName(e.target.value)} />
                <input type="text" placeholder="Activity Type" value={activityType} onChange={(e) => setActivityType(e.target.value)} />
                <input type="number" placeholder="Number of Pages" value={numberOfPages} onChange={(e) => setNumberOfPages(e.target.value)} />
                <button type="submit">Submit</button>
            </form>
            <div>
                {scrapedData && <p>{JSON.stringify(scrapedData)}</p>}
            </div>
        </div>
    );
};

export default ActivityForm;
