# Seismic Modeling and Reverse Time Migration  

This code was made to do the migration of seismic session, but before this, we need to make the modeling to do the seismogram, that will used to migration.  
In this case, the model is Marmousi, but you can do the process with any model. You just have to change the dimensions and the parameters in parameters.py archive.  

To run the script, if you've Windows, just execute the run.bat. If you've Linux, execute the run.sh.   

Add: You'll need the Python and its librarys installed in your computer, they are: math, time, numba, numpy, matplotlib, mpl_toolkits.axes_grid1, scipy.  

The results of process are:  

The modeling:  

![Seismogram Marmousi](https://user-images.githubusercontent.com/54816858/101291302-877c2d00-37e6-11eb-807d-6de5b7f3e687.png)  

The migration:  

![Laplacian 2](https://user-images.githubusercontent.com/54816858/101295897-12692180-37ff-11eb-8fef-d520823cd33e.png)
