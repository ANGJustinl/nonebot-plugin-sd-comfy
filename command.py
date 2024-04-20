from arclet.alconna import Alconna, Arg, ArgFlag, Option, OptionResult


DrawCommand = Alconna(
    "aidraw",
    ["/", "!"],
    Arg("PositiveTags", str),
    Option("-n|--negative", Arg("NegativeTags", str, flags=ArgFlag.OPTIONAL)),
    Option(
        "-s|--steps",
        Arg("Steps", int, flags=ArgFlag.OPTIONAL),
        default=OptionResult(value=False, args={"Steps": 20}),
    ),
    Option(
        "-cfg|--scale",
        Arg("Scale", float, flags=ArgFlag.OPTIONAL),
        default=OptionResult(value=False, args={"Scale": 7.0}),
    ),
    Option(
        "--seed",
        Arg("Seed", int, flags=ArgFlag.OPTIONAL),
        default=OptionResult(value=False, args={"Seed": -1}),
    ),
)


def DrawCommandParse(message):
    Args_out = DrawCommand.parse(message)
    print(Args_out)
    if Args_out.matched:
        PositiveTags = Args_out.main_args
        Other_args = Args_out.other_args
        return PositiveTags, Other_args
    return Args_out.error_info
