class Messages():
    PodcastNotFound = "No podcast found"
    UserNotFound = "Your user wasn't found in the database plz start by adding a subscription"
    SubscriptionNotFound = "No subscription found for this podcast and user"
    FormatError = "The format for the timestamp is `hh:mm:ss`"
    NotConnected = "You are not connected to a voice channel"
    AudioSaved = "The audio stream was stopped and your current timestamp was saved"
    ErrorConnecting = "Error connecting to voice channel."
    Disconnected = "Disconnected"
    PodcastAdded = "Podcast added"
    PodcastNotAdded = "Podcast wasn't added"
    AlreadySubscribed = "You are already subscribed to this podcast"
    PlayMostRecentEpisode = "Do you want to play the last episode you were listening to?"
    TimeoutErrorMessage = "The interaction timed out."
    YesPlayLastEpisode = "Good i will play the last episode of the podcast you were listening to"
    NoPlayLastEpisode = "Ok i will play the most recent episode of the podcast"
    FastForwarded = "Track was fastforwarded 30 seconds"
    NotFastForwarded = "Track was not fastforwarded 30 seconds"
    Rewinded = "Track was rewinded"
    NotRewinded = "Track was not rewinded"
    def ConnectedTo(n): return f"I connected to {n}"
    def Playing(n, e): return f"Playing {n}  \nEpisode {e}"
