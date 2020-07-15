
The final goal of this is to have a multiple data pipelines that collect currency data
and then pass that data to a reinforcement learning bot. The bot's model will be capable 
of consuming ticket data aggregated to arbitrary time intervals as well as some sort of 
oc


List of things that needs to be done. 

 - [ ] get lots of historical bar data, maybe 5 minute
 - [ ] train time series neural net on currency data to predict price or prices
 - [ ] get lots of frequent tweet data or similar for the currency market
 - [ ] train models to predict sentiment 
   - [ ] create quick tool to label sentiment or use aws a2i
 - [ ] create robust live data streaming on aws docker image collecting and passing to agent
 - [ ] create reinforcement learning agent that uses transfer learning to give it a head start
 - [ ] use trading strategies alongside agent to use imitation learning to give it direction. 
 
 
 Do I need to create an actual play environment? Maybe use a months data to ramp it into a play account and see how it does. 
 


