import overpass


api = overpass.API()
map_query = overpass.MapQuery(-122.490128,37.722134,-122.416657,37.789994)
response = api.Get(map_query)
print_r(response)


        