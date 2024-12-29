Top Trackify

With the release of Spotify Wrapped 2024, I heard rumors that Spotify wasn't displaying our real top tracks and artists.
So, I decided to create an app that would use the data straight from the source, the Spotify API. 
In this project I used OAuth 2.0 to receive tokens and codes from Spotify and then used those tokens to access my personal data, straight from the Spotify database.
I originally was going to use Spotipy, which is a library for handling with Spotify OAuth, but decided to do everything without it, as it would further my understanding of API's and OAuth.


The rumors appear to be true; my top artists and tracks for the past year were different than the ones Spotify displayed in my 2024 Spotify Wrapped.

According to Spotify:
Top artists                 Top Tracks
1. Kanye West               1. BURN
2. Drake                    2. DO IT
3. Travis Scott             3. KING
4. Beabadoobee              4. BACK TO ME
5. Tyler, The Creator       5. Los Pollos Hermanos


According to Top Trackify:
Top artists                     Top Tracks
1. Kanye West                   1. Good Life
2. Jay-Z                        2. Heard 'Em Say
3. Drake                        3. I Wonder
4. J. Cole                      4. Black Skinhead
5. Younboy Never Broke Again    5. All Falls Down


Sources:
Spotify Web API Documentation: https://developer.spotify.com/documentation/web-api