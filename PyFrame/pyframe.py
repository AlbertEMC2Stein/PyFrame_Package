"""
pyframe.py
~~~~~~~~~~

A simple animation framework for Python.

This module provides a simple framework for creating animations in Python. It
is designed to be simple to use and to be easily extended. It is not intended
to be a replacement for more powerful animation frameworks such as
matplotlib.animation or manim.

The framework is based on the concept of a Canvas object, which represents a
figure with axes. The Canvas can be populated with Artists, which are objects
that can draw themselves on the Canvas. The Canvas can then be shown or saved
to disk to produce an frame by frame animation.

The framework is designed to be easily extended. New types of Artists can be
created by subclassing the Artist class. The Artist class provides a simple
interface for drawing things on the Canvas, and for determining whether it
should be drawn on a given frame. The Artist class also provides a simple
interface for determining whether it is done drawing itself on the Canvas,
meaning it an be deleted from the list of current  artists.

Pre-Impemented Artists include:
    - Artist:
        A simple artist that draws itself on the Canvas on every frame.

    - TimedArtist:
        A simple artist that draws itself on the Canvas between a
        start and end frame.

    - ToggledArtist
        A simple artist that draws itself on the Canvas when it is
        toggled on.

    - OneTimeArtist:
        A simple artist that draws itself on the Canvas on a single
        (possibly future) frame and is then deactivated automatically.
"""


from string import ascii_lowercase
from ._decorator import doc_inherit
import numpy as np
import matplotlib.pyplot as plt


class Artist():
    """
    A simple artist that draws itself on the Canvas on every frame.
    Subclasses:
        - TimedArtist
        - ToggledArtist
        - OneTimeArtist

    Attributes
    ----------
    id : str
        A unique identifier for the artist.
    artist_factory : function
        A function that takes an axes object as an argument and draws
        something on it.
    layer : int, default = 0
        The layer on which the artist should be drawn. Artists with a
        lower layer number are drawn first.
    deactivated : bool
        A flag indicating whether the artist still needs to be drawn
        on the Canvas.

    Methods
    ----------
    draw(ax)
        Draws the artist on the Canvas.
    deactivate()
        Deactivates the artist.
    isActive(frame_counter)
        Returns True if the artist should be drawn on the given frame.
    isDone(frame_counter)
        Returns True if the artist is done drawing itself on the Canvas.
    """


    def __init__(self, artist_factory, layer=0):
        """
        Constructs all the necessary attributes for the Artist object.

        Parameters
        ----------
        artist_factory : function
            A function that takes an axes object as an argument and draws
            something on it.
        layer : int
            The layer on which the artist should be drawn. Artists with a
            lower layer number are drawn first.
        """

        self.id = ''.join(np.random.choice(list(ascii_lowercase), 10))
        self.artist_factory = artist_factory
        self.layer = layer
        self.deactivated = False


    def draw(self, ax):
        """
        Draws the artist on the Canvas.

        Parameters
        ----------
        ax : Axes
            The axes on which the artist should be drawn.
        """

        self.artist_factory(ax)
        plt.draw()


    def deactivate(self):
        """
        Deactivates the artist.
        """

        self.deactivated = True


    def isActive(self, frame_counter):
        """
        Returns True if the artist should be drawn on the given frame.

        Parameters
        ----------
        frame_counter : int
            The frame number for which activeness is checked.

        Returns
        -------
        bool
            True if the artist should be drawn on the given frame.
        """

        return not self.deactivated


    def isDone(self, frame_counter):
        """
        Returns True if the artist is done drawing itself on the Canvas.

        Parameters
        ----------
        frame_counter : int
            The frame number for which being done is checked.

        Returns
        -------
        bool
            True if the artist is done drawing itself on the Canvas.
        """

        return self.deactivated


    def __str__(self):
        return "Artist: %s" % self.id


    def __eq__(self, other):
        return self.id == other.id


class TimedArtist(Artist):
    """
    A timed artist that draws itself on the Canvas in a given range of frames.
    Subclass of the Artist class.

    Attributes
    ----------
    id : str
        A unique identifier for the artist.
    artist_factory : function
        A function that takes an axes object as an argument and draws
        something on it.
    layer : int, default = 0
        The layer on which the artist should be drawn. Artists with a
        lower layer number are drawn first.
    deactivated : bool
        A flag indicating whether the artist still needs to be drawn
        on the Canvas.
    start : int
        The frame number on which the artist should start drawing itself.
    end : int
        The frame number on which the artist should stop drawing itself.

    Methods
    ----------
    draw(ax)
        Draws the artist on the Canvas.
    deactivate()
        Deactivates the artist.
    isActive(frame_counter)
        Returns True if the artist should be drawn on the given frame.
    isDone(frame_counter)
        Returns True if the artist is done drawing itself on the Canvas.
    """


    def __init__(self, artist_factory, start, end, layer=0):
        """
        Constructs all the necessary attributes for the TimedArtist object.

        Parameters
        ----------
        artist_factory : function
            A function that takes an axes object as an argument and draws
            something on it.
        start: int
            The frame number on which the artist should start drawing itself.
        end: int
            The frame number on which the artist should stop drawing itself.
        layer : int, default = 0
            The layer on which the artist should be drawn. Artists with a
            lower layer number are drawn first.
        """

        super().__init__(artist_factory, layer)
        self.start = start
        self.end = end


    @doc_inherit 
    def draw(self, ax):
        self.artist_factory(ax)
        plt.draw()


    @doc_inherit 
    def isActive(self, frame_counter):
        return frame_counter >= self.start and frame_counter <= self.end and not self.deactivated


    @doc_inherit 
    def isDone(self, frame_counter):
        return frame_counter > self.end or self.deactivated


    def __str__(self):
        return "TimedArtist: %s, start: %d, end: %d" % (self.id, self.start, self.end)


class ToggledArtist(Artist):
    """
    A toggleable artist that draws itself on the Canvas if it is toggled on.
    Subclass of the Artist class.

    Attributes
    ----------
    id : str
        A unique identifier for the artist.
    artist_factory : function
        A function that takes an axes object as an argument and draws
        something on it.
    layer : int, default = 0
        The layer on which the artist should be drawn. Artists with a
        lower layer number are drawn first.
    deactivated : bool
        A flag indicating whether the artist still needs to be drawn
        on the Canvas.
    state : str
        The state of the artist. Can be 'active' or 'inactive'.

    Methods
    ----------
    draw(ax)
        Draws the artist on the Canvas.
    deactivate()
        Deactivates the artist.
    toggle()
        Toggles the artist on or off.
    isActive(frame_counter)
        Returns True if the artist should be drawn on the given frame.
    isDone(frame_counter)
        Returns True if the artist is done drawing itself on the Canvas.
    """


    def __init__(self, artist_factory, state, layer=0):
        """
        Constructs all the necessary attributes for the ToggledArtist object.

        Parameters
        ----------
        artist_factory : function
            A function that takes an axes object as an argument and draws
            something on it.
        state : str
            The state of the artist. Can be 'active' or 'inactive'.
        layer : int, default = 0
            The layer on which the artist should be drawn. Artists with a
            lower layer number are drawn first.
        """

        super().__init__(artist_factory, layer)
        self.state = state


    @doc_inherit 
    def draw(self, ax):
        self.artist_factory(ax)
        plt.draw()


    def toggle(self):
        """
        Toggles the artist on or off.
        """

        self.state = 'active' if self.state == 'inactive' else 'inactive'


    @doc_inherit 
    def isActive(self, frame_counter):
        return self.state == 'active' and not self.deactivated


    @doc_inherit 
    def isDone(self, frame_counter):
        return self.deactivated
    

    def __str__(self):
        return "ToggledArtist: %s, state: %s" % (self.id, self.state)


class OneTimeArtist(Artist):
    """
    A one time artist that draws itself on the Canvas once on a given frame.
    Subclass of the Artist class.

    Attributes
    ----------
    id : str
        A unique identifier for the artist.
    artist_factory : function
        A function that takes an axes object as an argument and draws
        something on it.
    layer : int, default = 0
        The layer on which the artist should be drawn. Artists with a
        lower layer number are drawn first.
    deactivated : bool
        A flag indicating whether the artist still needs to be drawn
        on the Canvas.
    drawn : bool
        A flag indicating whether the artist has already been drawn on the Canvas.
    when : int
        The frame number on which the artist should draw itself.

    Methods
    ----------
    draw(ax)
        Draws the artist on the Canvas.
    deactivate()
        Deactivates the artist.
    toggle()
        Toggles the artist on or off.
    isActive(frame_counter)
        Returns True if the artist should be drawn on the given frame.
    isDone(frame_counter)
        Returns True if the artist is done drawing itself on the Canvas.
    """


    def __init__(self, artist_factory, when=0, layer=0):
        """
        Constructs all the necessary attributes for the OneTimeArtist object.

        Parameters
        ----------
        artist_factory : function
            A function that takes an axes object as an argument and draws
            something on it.
        when : int, default = 0
            The frame number on which the artist should draw itself.
        layer : int, default = 0
            The layer on which the artist should be drawn. Artists with a
            lower layer number are drawn first.
        """

        super().__init__(artist_factory, layer)
        self.drawn = False
        self.when = when


    @doc_inherit 
    def draw(self, ax):
        self.artist_factory(ax)
        self.drawn = True
        plt.draw()


    @doc_inherit 
    def isActive(self, frame_counter):
        return frame_counter == self.when and not self.deactivated


    @doc_inherit 
    def isDone(self, frame_counter):
        return self.drawn or self.deactivated
    

    def __str__(self):
        return "OneTimeArtist: %s, drawn: %s" % (self.id, self.drawn)


class Canvas():
    """
    A Canvas object that manages the drawing of Artists on a figure.

    Attributes
    ----------
    frame_counter : int
        The current frame number.
    xlims : tuple
        The x-axis limits of the figure.
    ylims : tuple
        The y-axis limits of the figure.
    fig : matplotlib.figure.Figure
        The figure on which the artists are drawn.
    ax : matplotlib.axes.Axes
        The axes on which the artists are drawn.
    artists : list
        A list of Artist objects.
    
    Methods
    ----------
    addArtistFactory(artist_factory, type, **kwargs)
        Adds an artist to the Canvas by providing a function taking an axes 
        object as an argument and drawing something on it.
    addArtist(artist)
        Adds an artist to the Canvas.
    getAllArtists(asString=False)
        Returns a list of all the artists on the Canvas. If asString
        is True, the list contains the string representation of the
        artists.
    getActiveArtists(asString=False)
        Returns a list of all the currently active artists on the Canvas. 
        If asString is True, the list contains the string representation 
        of the artists.
    draw()
        Draws all the artists on the Canvas and removes all done 
        or deactivated artists.
    resetAxes()
        Clears the axes.
    show()
        Shows the figure.
    save(folder, filename)
        Saves the figure to a file.
    """


    def __init__(self, width, height, xlims=(0, 1), ylims=(0, 1), dpi=100):
        """
        Constructs all the necessary attributes for the Canvas object.
        
        Parameters
        ----------
        width : int
            The width of the figure.
        height : int
            The height of the figure.
        xlims : tuple, default = (0, 1)
            The x-axis limits of the figure.
        ylims : tuple, default = (0, 1)
            The y-axis limits of the figure.
        dpi : int, default = 100
            The resolution of the figure.
        """

        self.frame_counter = 1
        self.xlims = xlims
        self.ylims = ylims
        self.fig = plt.figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        self.artists = []

        self.ax.set_xlim(xlims)
        self.ax.set_ylim(ylims)


    def addArtistFactory(self, artist_factory, type, **kwargs):
        """
        Adds an artist to the Canvas by providing an function
        returning an artist given an axes object.

        Parameters
        ----------
        artist_factory : function
            A function that takes an axes object as an argument and draws
            something on it.
        type : class
            The class of the artist to be added.
        **kwargs
            Additional keyword arguments to be passed to the artist.
        """

        self.artists += [type(artist_factory, **kwargs)]
        self.artists.sort(key=lambda artist: artist.layer)


    def addArtist(self, artist):
        """
        Adds an artist to the Canvas.

        Parameters
        ----------
        artist : Artist
            The artist to be added.
        """

        self.artists += [artist]
        self.artists.sort(key=lambda artist: artist.layer)


    def getAllArtists(self, asString=False):
        """
        Returns a list of all the artists on the Canvas. If asString
        is True, the list contains the string representation of the
        artists.

        Parameters
        ----------
        asString : bool, default = False
            If True, the list contains the string representation of the
            artists.

        Returns
        ----------
        list
            A list of all the artists on the Canvas.
        """
        if asString:
            return [str(artist) for artist in self.artists]
        else:
            return self.artists


    def getActiveArtists(self, asString=False):
        """
        Returns a list of all the currently active artists on the Canvas. 
        If asString is True, the list contains the string representation 
        of the artists.

        Parameters
        ----------
        asString : bool, default = False
            If True, the list contains the string representation of the
            artists.

        Returns
        ----------
        list
            A list of all the currently active artists on the Canvas.
        """

        if asString:
            return [str(artist) for artist in self.artists if artist.isActive(self.frame_counter)]
        else:
            return [artist for artist in self.artists if artist.isActive(self.frame_counter)]


    def draw(self):
        """
        Draws all the artists on the Canvas and removes all done
        or deactivated artists.
        """

        up_for_ramoval = []
        for artist in self.artists:
            if artist.isActive(self.frame_counter):
                artist.draw(self.ax)

            if artist.isDone(self.frame_counter):
                up_for_ramoval += [artist]

        for artist in up_for_ramoval:
            self.artists.remove(artist)


    def resetAxes(self):    
        """
        Resets the axes.
        """

        self.ax.clear()
        self.ax.set_xlim(self.xlims)
        self.ax.set_ylim(self.ylims)


    def show(self):
        """
        Shows the drawn figure.
        """

        self.draw()
        plt.show()


    def save(self, folder, fname):
        """
        Saves the drawn figure to a file.

        Parameters
        ----------
        folder : str
            The folder to save the figure to.
        fname : str
            The name of the file to save the figure to.
        """

        self.draw()
        self.fig.savefig(f"{folder}/{fname}_{self.frame_counter}")
        self.resetAxes()
        self.frame_counter += 1


    def __str__(self):
        return f"The Canvas has {len(self.artists)} (possibly idle) artists:\n\t- " + "\n\t- ".join(self.getAllArtists(asString=True))


if __name__ == "__main__":
    import os

    if not os.path.exists('out/'):
        os.makedirs('out/')

    permanent_artist = Artist(lambda ax: ax.plot([0, 10], [0, 10]))
    toggled_artist = ToggledArtist(lambda ax: ax.scatter([2.5, 7.5], [2.5, 7.5]), 'inactive')

    canvas = Canvas(5, 5, (0, 10), (0, 10))
    
    canvas.addArtist(permanent_artist)
    canvas.addArtistFactory(lambda ax: ax.plot([0, 10], [10, 0]), Artist)
    canvas.addArtistFactory(lambda ax: ax.plot([0, 10], [5, 5]), TimedArtist, start=10, end=20)
    canvas.addArtistFactory(lambda ax: ax.plot([5, 5], [0, 10]), TimedArtist, start=30, end=40)
    canvas.addArtist(toggled_artist)
    canvas.addArtistFactory(lambda ax: ax.scatter([5], [5], s=50), OneTimeArtist, when=25)

    print(canvas, '\n')
    for i in range(50):
        if canvas.frame_counter in [25, 30]:
            toggled_artist.toggle()

        if canvas.frame_counter == 45:
            permanent_artist.deactivate()

        print(f"Frame {canvas.frame_counter}:\n\t- " + "\n\t- ".join(canvas.getActiveArtists(asString=True)) + "\n")
        canvas.save('out', 'test')