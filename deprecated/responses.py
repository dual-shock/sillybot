class Response:
    def __init__(self, 
                inputs: list[str], 
                anySubstring: bool, 
                startsWith: bool,
                responses: list[str]
                ):
        self.inputs = inputs
        self.anySubstring = anySubstring
        self.startsWith = startsWith
        self.responses = responses

responses = [
    Response(
        inputs=["shat"],
        anySubstring=True,
        startsWith=False,
        responses=[
            "shat is this real?",
            "shat.",
            "hi shatroom"
        ]
    ),
    Response(
        inputs=["chat"],
        anySubstring=True,
        startsWith=False,
        responses=[
            "chat is this real?",
            "chat.",
            "hi chatroom"
        ]
    ),
    Response(
        inputs=['itsyou','its you', "it's you","it'syou"],
        anySubstring=True,
        startsWith=False,
        responses=[
            "Despite everything, it's still you.",
            "Still just you, Frisk.",
            "It's me, Chara.",
        ]
    ),
    Response(
        inputs=["ban"],
        anySubstring=True,
        startsWith=False,
        responses=[
            "shat. ban.",
            "no ban.",
            "is this even bannable?"
        ]
    ),
    Response(
        inputs=["mpreg"],
        anySubstring=True,
        startsWith=False,
        responses=[
            "https://tenor.com/view/omori-hero-mpreg-mpreg-monday-hero-omori-gif-27440370",
            "https://tenor.com/view/mpreg-omori-mpreg-gif-22727222",
            "https://tenor.com/view/omori-omori-hero-hero-hero-omori-monday-gif-25055543",
            "https://tenor.com/view/mpreg-omori-basil-shayminthingz-bushfire-photobomb-gif-8174033405728295346"
        ]
    ),
    Response(
        inputs=["undertale"],
        anySubstring=True,
        startsWith=False,
        responses=[
            "https://tenor.com/view/lesser-dog-undertale-gif-4834820",
            "https://tenor.com/view/dancing-annoying-dog-deltarune-undertale-gif-23127679",
            "https://tenor.com/view/temmie-undertale-deltarune-text-box-gif-22453093",
            "https://tenor.com/view/frisk-undertale-gif-8147392428286254944"
        ]
    ),
    Response(
        inputs=["temmy", "temmie", "temy", "temie", "temi", "tem"],
        anySubstring=True,
        startsWith=False,
        responses=[
            "https://tenor.com/view/temmie-gif-19040913",
            "https://tenor.com/view/temmie-undertale-lick-icon-temmie-lick-deviantart-lick-gif-13689909709087974356",
            "https://tenor.com/view/temmie-tem-nyan-tem-nyan-temmie-gif-22559985",
            "https://tenor.com/view/t-emmie-gif-5723836"
        ]
    ),

]
