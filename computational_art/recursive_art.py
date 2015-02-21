# Computational Art
# Jessica Sutantio
# SoftDes Spring 2015

import random
from PIL import Image
from math import *
from random import *

def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """

        # single input functions
    t = [['cos_pi'],['sin_pi']]

    # dual input functions
    s = [['X'],['Y'],['prod'],['avg'],['max']]

    if max_depth == 0:
        return choice([['a'],['b']])
    if min_depth <= 0:
        # randomly decide whether or not to continue with recursion
        contine_recurse = choice(['YES','NO'])
        if contine_recurse == 'NO':
            return choice([['a'],['b']])
        else:
            return build_random_function(min_depth-1,max_depth-1)

    else:
        function_type = choice(['one input','two input'])
        if function_type == 'one input':
            function = choice(t)
            function.append(build_random_function(min_depth-1,max_depth-1))
            return function
        else:
            function = choice(s)
            function.append(build_random_function(min_depth-1,max_depth-1))
            function.append(build_random_function(min_depth-1,max_depth-1))
            return function

def evaluate_random_function(f, x, y):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(['a'],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(['b'],0.1,0.02)
        0.02
    """

    for elem in f:
        # base case
        if elem == ['a']:
            return x
        if elem == ['b']:
            return y
        # evaluate the nested functions based on type
        else:
            if elem == 'X':
                result = f[1]
            if elem == 'Y':
                result = f[2]
            if elem == 'prod':
                result = f[1]*f[2]
            if elem == 'avg':
                result = 0.5*(f[1]+f[2])
            if elem == 'cos_pi':
                result = cos(pi*f[1])
            if elem == 'sin_pi':
                result = sin(pi*f[1])
            return evaluate_random_function(result,x,y)

        # for sub_elem in elem:

            # # base cases
            # if sub_elem == 'X':
            #     result = elem[1]
            # if sub_elem == 'Y':
            #     result = elem[1]
            # if sub_elem == 'prod':
            #     result = elem[1]*elem[2]
            # if sub_elem == 'avg':
            #     result = 0.5*(elem[1]+elem[2])
            # if sub_elem == 'cos_pi':
            #     result = cos(pi*elem[1])
            # if sub_elem == 'sin_pi':
            #     result = sin(pi*elem[1])

            # function *= result

def remap_interval(val, input_interval_start, input_interval_end, output_interval_start, output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """

    # check to see if val is in the interval
    if (val > input_interval_start) and (val < input_interval_end):
        input_offset = 0 - input_interval_start
        scale = float(val+input_offset)/(input_interval_end+input_offset)
        output_offset = 0 - output_interval_start
        val = scale*(output_interval_end+output_offset)
        return val - output_offset
    if val == input_interval_start:
        return output_interval_start
    if val == input_interval_end:
        return output_interval_end


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = [build_random_function(7,9)]
    green_function = [build_random_function(7,9)]
    blue_function = [build_random_function(7,9)]

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)),
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y))
                    )

    im.save(filename)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    # generate_art("myart.png")
    print build_random_function(2,3)

    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    # test_image("noise.png")
