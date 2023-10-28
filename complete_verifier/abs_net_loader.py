import torch
import torch.nn as nn
import numpy as np

def model_from_file( fname ):
    """
    A custom loader for loading the abstract network as defined in semantic
    neuron merge. Refer to semantic neuron merge, network.py:Network.save for
    the spec for the npz file format
    """
    # Load data from file
    data = np.load( fname )

    # Get layer sizes
    layer_sizes = data['layer_sizes']

    # Collect linear and relu layers upto just before output layer
    layer_list = []
    linear_list = []
    for pre_size, post_size in zip( layer_sizes[:-2], layer_sizes[1:-1] ):
        linear_layer = nn.Linear( pre_size, post_size )
        linear_list.append( linear_layer )
        layer_list.append( linear_layer )
        layer_list.append( nn.ReLU() )

    # Add output layer
    linear_layer = nn.Linear( layer_sizes[-2], layer_sizes[-1] )
    linear_list.append( linear_layer )
    layer_list.append( linear_layer )
    if data['end_relu'][0]:
        layer_list.append( nn.ReLU() )

    # Create model
    model = nn.Sequential( *layer_list )

    # Copy weights and biases
    for i,l in enumerate( linear_list ):
        l.weight.data = torch.from_numpy( data[ 'weight_{}'.format(i) ]).T
        l.bias.data = torch.from_numpy( data[ 'bias_{}'.format(i) ])

    # DEBUG
    print( "Model :", model )
    print( "Model output on 0s: ", 
            model( torch.zeros( ( layer_sizes[0], ), dtype=torch.float32 )))

    return model

