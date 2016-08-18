# maptile
Yet another google-maps-style image splitter

To be used as google map tiles an image needs to be split into many different
256x256 tiles. This simple script should do so.

I make no promises this works, I'm writing this as an educational thing rather
than as a finished product =)

You can test the script on my _lovely_ hand-drawn images with
`./tile.py map overlay 0 4` Note how the colours of the overlay change as you
zoom in deeper.

I am using this with [Leaflet](https://github.com/Leaflet/Leaflet) but it should
work with any zoomable maps.
