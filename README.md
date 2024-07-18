# EVC-visualizer
<p>
This is a tool to visualize how an eternal vertex cover guards move when an edge is attacked over grid graphs, particularly hexagonal, triangular, octagonal, and squared grids.
</p> 
<p> 
What is an <b>Eternal Vertex Cover</b>? </br>
An eternal vertex cover is a set of vertices in a graph such that,
as edges are attacked over time, it is always possible to move
guards within the graph in response to these attacks such that
at least one guard covers every edge at all times.
</p> 

## Usage
The application is reachable at the following [link](http://evc-visualizer.di.uniroma1.it/) </br>
If you want to run it locally, install the dependencies and run the code as follows:
#### Installing Dependencies
Install all the dependencies in your environment
``` 
pip -r install requirements.txt
```

#### Run the code
Run the application using python
``` 
python app.py
```

## Credits and Resources
The movement strategies are based on [(Eternal) Vertex Cover Number of Infinite and Finite Grid Graphs](https://doi.org/10.48550/arXiv.2209.05102) </br>
Hamiltonian path algorithm [source](https://gist.github.com/mikkelam/ab7966e7ab1c441f947b)
