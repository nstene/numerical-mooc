
import numpy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

def L2_rel_error(p, pn):
    ''' Compute the relative L2 norm of the difference
    Parameters:
    ----------
    p : array of float
        array 1
    pn: array of float
        array 2
    Returns:
    -------
    Relative L2 norm of the difference
    '''
    return numpy.sqrt(numpy.sum((p - pn)**2)/numpy.sum(pn**2))

def plot2D(x, y, p):
    '''Creates 3D projection plot with appropriate limits and viewing angle
    
    Parameters:
    ----------
    x: array of float
        nodal coordinates in x
    y: array of float
        nodal coordinates in y
    p: 2D array of float
        calculated potential field
    
    '''
    fig = plt.figure(figsize=(11,7), dpi=100)
    ax = fig.gca(projection='3d')
    X,Y = numpy.meshgrid(x,y)
    surf = ax.plot_surface(X,Y,p[:], rstride=1, cstride=1, cmap=cm.coolwarm,
            linewidth=0, antialiased=False)

    ax.set_xlim(0,x[-1])
    ax.set_ylim(0,y[-1])
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    ax.set_zlabel('$z$')
    ax.view_init(30,45)
    
def laplace2d_jacobi(p, y, dx, dy, l2_target):
    '''Solves the diffusion equation with forward-time, centered scheme
    
    Parameters:
    ----------
    p: 2D array of float
        Initial potential distribution
    y: array of float
        Nodal coordinates in y
    dx: float
        Mesh size
    dy: float
        Mesh size
    l2_target: float
        Error target
        
    Returns:
    -------
    p: 2D array of float
        Potential distribution after relaxation

    iteration_count: int
        Number of iterations required to meet tolerance
    '''
    
    l2norm = 1
    pn = numpy.empty_like(p)
    iteration_count = 0

    while l2norm > l2_target:
        pn = p.copy()
        p[1:-1,1:-1] = .25 * (pn[1:-1,2:]+pn[1:-1,:-2]+pn[2:,1:-1]+pn[:-2,1:-1])
            
        p[:,-1] = p[:,-2]
        
        l2norm = numpy.sum(numpy.abs(p[1:-1,1:-1] - pn[1:-1,1:-1]))
        
        iteration_count += 1
     
    return p, iteration_count

def p_analytical(x, y):
    '''Returns the analytical solution for the given Laplace Problem on a grid
    with coordinates x and y
    
    Parameters:
    ----------
    xL array of float
        Nodal coordinates in x
    y: array of float
        Nodal coordinates in y
        
    Returns:
    -------
    pxy: 2D array of float
        Potential distribution analytical solution
    
    '''
    X, Y = numpy.meshgrid(x,y)
    pxy = numpy.sinh(1.5*numpy.pi*Y / x[-1]) /\
    (numpy.sinh(1.5*numpy.pi*y[-1]/x[-1]))*numpy.sin(1.5*numpy.pi*X/x[-1])
    
    return pxy