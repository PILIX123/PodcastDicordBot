class Description():
    Play = """## How to Use the Play Command

To use the command, follow this format:

</play:1169005927714787430> `name:<podcast_name> episode_number:[episode_number] timestamp:[timestamp]`

Here's what each part of the command means:  
    - `<podcast_name>` (Required): Specify the name of the podcast you want to play.  
    - `[episode_number]` (Optional): You can provide an episode number if you want to listen to a specific episode. If not, the latest episode will be selected.  
    - `[timestamp]` (Optional): If you want to start listening from a specific timestamp in the episode, provide it in HH:MM:SS format.  

### Examples

    - `/play name: Awesome Podcast` : Starts playing the latest episode of the "Awesome Podcast."  
    - `/play name: Tech Talk episode_number:5` : Plays the 5th episode of "Tech Talk."  
    - `/play name: Science Hour episode_number:7 timestamp:00:15:30` : Initiates playback of the 7th episode of "Science Hour" from the 15-minute and 30-second mark."""

    Unsubscribe = """
## Unsubscribe from a Podcast

### How to Use the Command

To unsubscribe from a podcast, use the following command:
</unsubscribe:1168995344412057673> `name:<podcast_name>`

Here's what this means:

- `<podcast_name>` (Required): Specify the name of the podcast you want to unsubscribe from.

### Example

- `/unsubscribe name:Awesome Podcast` : Unsubscribes you from the "Awesome Podcast."
"""

    Subscribe = """
## Subscribe to a Podcast

### How to Use the Command

To subscribe to a podcast, use the following command:
</subscribe:1168995344412057672> `url: <podcast_url>`

Here's what this means:

- `<podcast_url>` (Required): Specify the URL of the podcast you want to subscribe to. The url does not need to start with "http://" or "https://"  
The url needs to point to an [RSS feed](https://rss.com/blog/how-do-rss-feeds-work/) is.  
On your favorite podcast page there should be a logo similar to this <:rss:1169062226448093194> copy the link that is given and paste it.
### Example

- `/subscribe url: https://example-podcast.com` : Subscribes you to the podcast hosted at "https://example-podcast.com."
"""

    Connect = """
## Connect to Voice Channel

### How to Use the Command

To connect to a voice channel, use the following command:
</connect:1158674334777344050>

### Example

- `/connect`: Initiates a connection to a voice channel.
"""

    Disconnect = """
## Disconnect from Voice Channel

### How to Use the Command

To disconnect from the voice channel, use the following command:
</disconnect:1158677824106938399>

### Example

- `/disconnect`: Disconnects from the current voice channel if connected.
"""

    Stop = """
## Stop Audio Playback

### How to Use the Command

To stop audio playback and save the audio file, use the following command:
</stop:1168136268132130917>

### Example

- `/stop`: Stops audio playback, saves the audio file, and notifies the user.
"""
