This was a project I started in my free time to parse Albion Online data and return 3D plots of the best locations to gather ore. Eventually I hope to expand this script more, but real life isn't allowing that right now :). Feel free to incorporate this into whatever project you may be working on. 

Some things I have been thinking about doing:

1. Set up script to grab resource tier data and match with each cluster.

2. Find a way to validate data. I feel like a lot of these templates include resrouce nodes that do not exist when you actually visit a cluster, so I would like to have this data be accurate as possible. I may need to look into methods to grab data from a running Albion application, but I would rather avoid this if possible.

3. A better system for switching which type of resource you want to gather information on (GUI? CLI? I haven't decided yet).

4. This currently spits out HTML, so maybe host a webpage if this proves useful?

5. ML algorithm to determine efficient gathering paths through each cluster.
