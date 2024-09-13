in milestone one, i created this iotair function with a http trigger to send mock air quality data to event hub

in milestone 2, i have made another function to trigger when an event is arrives at the event hub for parsing, enriching the data.
I was not able to connect with the SQL db i had made in azure, python sdk for azure sql is a bit tricky, I'm still working on it.

in milestone 3, i made a service bus queue and connected it to the event hub via logic apps to send the data, i have attached the workflow code for the same, event hub to queue is working fine but another function to consume those messages is still in progress, 

For milestone 4 and 5, i'm still working on the present challenges regarding consumption of the queue messages and connnection to sql db.