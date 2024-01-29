from random import choice

# Stuff for the cog


def emoji():
    """Randomize footer emojis."""
    EMOJIS = [
        "\N{AUBERGINE}",
        "\N{SMIRKING FACE}",
        "\N{PEACH}",
        "\N{SPLASHING SWEAT SYMBOL}",
        "\N{BANANA}",
        "\N{KISS MARK}",
    ]
    emoji = choice(EMOJIS)
    return emoji


REDDIT_BASEURL = "https://api.reddit.com/r/{sub}/random"
MARTINE_API_BASE_URL = "https://api.martinebot.com/v1/images/subreddit"
IMGUR_LINKS = ("http://imgur.com", "https://m.imgur.com", "https://imgur.com")
NOT_EMBED_DOMAINS = (
    "gfycat.com/",
    "gifdeliverynetwork.com/",
    "redgifs.com",
    "imgur.com/gallery/",
    "imgur.com/a/",
    ".gifv",
)
GOOD_EXTENSIONS = (".png", ".jpg", ".jpeg", ".gif", "gifv")

# Subreddits
FOUR_K = [
    "Hegre",
    "HighResNSFW",
    "NSFW_Wallpapers",
    "UHDnsfw",
    "closeup",
]
AHEGAO = ["AhegaoGirls", "EyeRollOrgasm", "O_Faces", "RealAhegao"]
ASS = [
    "AssOnTheGlass",
    "AssholeBehindThong",
    "ButtsAndBareFeet",
    "HungryButts",
    "Mooning",
    "SnakeButt",
    "TheUnderbun",
    "Upshorts",
    "ass",
    "asshole",
    "assinthong",
    "asstastic",
    "beautifulbutt",
    "bigasses",
    "booty",
    "datgap",
    "girlsinleggings",
    "girlsinyogapants",
    "hugeass",
    "paag",
    "pawg",
    "facedownassup",
]
ASIANPORN = [
    "AsianCuties",
    "AsianHotties",
    "AsianNSFW",
    "AsianPorn",
    "AsiansGoneWild",
    "KoreanHotties",
    "NSFW_Japan",
    "bustyasians",
    "juicyasians",
]
ANAL = [
    "AnalGW",
    "MasterOfAnal",
    "NotInThePussy",
    "anal",
    "analinsertions",
    "assholegonewild",
    "buttsthatgrip",
]
BBW = [
    "BBW",
    "BBW_Chubby",
    "GoneWildPlus",
    "PerkyChubby",
    "chubby",
    "gonewildcurvy",
]
BDSM = ["BDSMGW", "BDSM_NoSpam", "Bondage", "Spanking", "bdsm"]
BLACKCOCK = ["bigblackcocks", "blackcock"]
BLOWJOB = [
    "AsianBlowjobs",
    "Blowjobs",
    "OralCreampie",
    "SwordSwallowers",
    "blowjobsandwich",
]
BOOBS = [
    "AreolasGW",
    "BestTits",
    "BigBoobsGW",
    "BigBoobsGonewild",
    "BiggerThanYouThought",
    "Boobies",
    "BustyNaturals",
    "BustyPetite",
    "Nipples",
    "PerfectTits",
    "PiercedNSFW",
    "Stacked",
    "TheHangingBoobs",
    "TheUnderboob",
    "TinyTits",
    "Titties",
    "TittyDrop",
    "boobbounce",
    "boobgifs",
    "boobs",
    "burstingout",
    "fortyfivefiftyfive",
    "ghostnipples",
    "homegrowntits",
    "hugeboobs",
    "naturaltitties",
    "pokies",
    "smallboobs",
    "tits",
]
BOTTOMLESS = ["nopanties", "upskirt"]
COSPLAY = [
    "CosplayLewd",
    "Cosplayheels",
    "nsfwcosplay",
]
CUNNI = ["cunnilingus"]
CUMSHOTS = [
    "GirlsFinishingTheJob",
    "amateurcumsluts",
    "bodyshots",
    "cumfetish",
    "cumontongue",
    "cumshots",
    "facialcumshots",
    "pulsatingcumshots",
]
DEEPTHROAT = [
    "DeepThroatTears",
    "SwordSwallowers",
    "deepthroat",
]
DICK = [
    "MassiveCock",
    "ThickDick",
    "bulges",
    "cock",
    "penis",
    "twinks",
]
DOUBLE_P = ["Technical_DP", "doublepenetration"]
EBONY = [
    "DarkAngels",
    "Ebony",
    "EbonyGirls",
    "bigblackasses",
    "blackchickswhitedicks",
    "ebonyamateurs",
]
FACIALS = ["FacialFun", "facialcumshots"]
FEET = [
    "ButtsAndBareFeet",
    "Feet_NSFW",
    "Feetup",
    "FootFetish",
    "rule34feet",
]
FEMDOM = ["Femdom", "FemdomHumiliation", "femdom", "hentaifemdom"]
FUTA = [
    "FutanariHentai",
    "HorsecockFuta",
]
GAY_P = [
    "CuteGuyButts",
    "GayDaddiesPics",
    "GayGifs",
    "ManSex",
    "broslikeus",
    "bulges",
    "gaybears",
    "gaynsfw",
    "gayotters",
    "jockstraps",
    "ladybonersgw",
    "lovegaymale",
    "manass",
    "MaleUnderwear",
]
GROUPS = ["GroupOfNudeGirls", "groupsex"]
LESBIANS = [
    "HDLesbianGifs",
    "Lesbian_gifs",
    "StraightGirlsPlaying",
    "dyke",
    "girlskissing",
    "lesbians",
    "mmgirls",
    "scissoring",
]
MILF = [
    "AgedBeauty",
    "MILFs",
    "Milfie",
    "amateur_milfs",
    "cougars",
    "hairymilfs",
    "maturemilf",
    "milf",
]
ORAL = [
    "AsianBlowjobs",
    "Blowjobs",
    "DeepThroatTears",
    "OralCreampie",
    "SwordSwallowers",
    "blowjobsandwich",
    "cunnilingus",
    "deepthroat",
]
PUBLIC = [
    "ChangingRooms",
    "Flashing",
    "FlashingAndFlaunting",
    "FlashingGirls",
    "NSFW_Outdoors",
    "NotSafeForNature",
    "PublicFlashing",
    "WoodNymphs",
    "bitchinbubba",
    "casualnudity",
    "exposedinpublic",
    "gwpublic",
    "holdthemoan",
    "publicplug",
    "snowgirls",
]
PUSSY = [
    "GodPussy",
    "HairyPussy",
    "Innies",
    "LabiaGW",
    "LipsThatGrip",
    "MoundofVenus",
    "PussyFlashing",
    "PussyMound",
    "grool",
    "peachlips",
    "pelfie",
    "pussy",
    "rearpussy",
    "spreadeagle",
    "ButterflyWings",
    "DangleAndJingle",
]
REAL_GIRLS = [
    "CellShots",
    "ChangingRooms",
    "Nude_Selfie",
    "RealGirls",
    "selfpix",
]
REDHEADS = [
    "FreckledRedheads",
    "RedheadGifs",
    "RedheadsPorn",
    "ginger",
    "nsfw_redhead",
    "redheads",
]
RULE_34 = [
    "Overwatch_Porn",
    "Rule34LoL",
    "Rule_34",
    "rule34",
]
SQUIRTS = ["squirting", "squirting_gifs", "wetspot", "grool"]
THIGHS = [
    "ThickThighs",
    "Thigh",
    "datgap",
    "leggingsgonewild",
    "legs",
    "theratio",
    "thighhighs",
]
THREESOME = [
    "AirTight",
    "SpitRoasted",
    "Threesome",
    "Xsome",
    "amateur_threesomes",
    "groupsex",
    "gangbang",
    "blowbang",
]
TRANS = [
    "GoneWildTrans",
    "Shemale_Big_Cock",
    "Shemales",
    "ShemalesParadise",
    "trapgifs",
    "traps",
]
WILD = [
    "ArtGW",
    "AsiansGoneWild",
    "BigBoobsGW",
    "BigBoobsGonewild",
    "GWCouples",
    "GWNerdy",
    "GoneWildSmiles",
    "LabiaGW",
    "LingerieGW",
    "PetiteGoneWild",
    "Swingersgw",
    "TallGoneWild",
    "UnderwearGW",
    "altgonewild",
    "bigonewild",
    "dirtysmall",
    "gonewild",
    "gonewildcolor",
    "gonewildcouples",
    "gonewildcurvy",
    "gwpublic",
    "workgonewild",
]
YIFF = ["Hyiff", "Yiffbondage", "femyiff", "yiff", "yiffgif"]
# Other APIs
NEKOBOT_HENTAI = choice(["hentai_anal", "hentai"])
NEKOBOT_URL = "https://nekobot.xyz/api/image?type={}"
