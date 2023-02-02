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
    return choice(EMOJIS)


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
    "HighResASS",
    "HighResNSFW",
    "NSFW_Wallpapers",
    "UHDnsfw",
    "closeup",
]
AHEGAO = ["AhegaoGirls", "EyeRollOrgasm", "O_Faces", "RealAhegao", "ahegao"]
ASS = [
    "AssOnTheGlass",
    "AssReveal",
    "AssholeBehindThong",
    "ButtsAndBareFeet",
    "GodBooty",
    "HighResASS",
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
    "brunetteass",
    "datgap",
    "girlsinleggings",
    "girlsinyogapants",
    "hugeass",
    "paag",
    "pawg",
    "facedownassup",
]
ASIANPORN = [
    "AmateurAsianGirls",
    "AsianCuties",
    "AsianHotties",
    "AsianNSFW",
    "AsianPorn",
    "AsianPussy",
    "AsiansGoneWild",
    "KoreanHotties",
    "NSFW_Japan",
    "asian_gifs",
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
BDSM = ["BDSMGW", "BDSM_NoSpam", "Bondage", "Spanking", "bdsm", "ropeart"]
BLACKCOCK = ["Blackdick", "ChurchOfTheBBC", "bigblackcocks", "blackcock"]
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
    "BoobsBetweenArms",
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
    "bigboobs",
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
BOTTOMLESS = ["Bottomless", "nopanties", "upskirt"]
COSPLAY = [
    "CosplayBoobs",
    "CosplayLewd",
    "Cosplayheels",
    "gwcosplay",
    "nsfwcosplay",
]
CUNNI = ["CunnilingusSelfie", "cunnilingus"]
CUMSHOTS = [
    "GirlsFinishingTheJob",
    "amateurcumsluts",
    "bodyshots",
    "cumfetish",
    "cumontongue",
    "cumshots",
    "facialcumshots",
    "pulsatingcumshots",
    "unexpectedcum",
]
DEEPTHROAT = ["AmateurDeepthroat", "DeepThroatTears", "SwordSwallowers", "deepthroat"]
DICK = [
    "DickPics4Freedom",
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
    "blackporn",
    "ebonyamateurs",
]
FACIALS = ["FacialFun", "facialcumshots"]
FEET = [
    "ButtsAndBareFeet",
    "Feet_NSFW",
    "Feetup",
    "FootFetish",
    "legsup",
    "rule34feet",
]
FEMDOM = ["Femdom", "FemdomHumiliation", "femdom", "hentaifemdom"]
FUTA = [
    "FutanariHentai",
    "FutanariPegging",
    "HorsecockFuta",
    "Rule34_Futanari",
    "hugefutanari",
]
GAY_P = [
    "CuteGuyButts",
    "GayDaddiesPics",
    "GayGifs",
    "ManSex",
    "NSFW_GAY",
    "broslikeus",
    "bulges",
    "gaybears",
    "gaynsfw",
    "gayotters",
    "jockstraps",
    "ladybonersgw",
    "lovegaymale",
    "manass",
    "manlove",
    "MaleUnderwear",
]
GROUPS = ["GroupOfNudeGirls", "groupsex"]
LESBIANS = [
    "HDLesbianGifs",
    "Lesbian_gifs",
    "StraightGirlsPlaying",
    "amateurlesbians",
    "dyke",
    "girlskissing",
    "lesbians",
    "mmgirls",
    "scissoring",
]
MILF = [
    "AgedBeauty",
    "HotAsianMilfs",
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
    "CunnilingusSelfie",
    "DeepThroatTears",
    "OralCreampie",
    "SwordSwallowers",
    "ballsucking",
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
    "NudeInPublic",
    "PublicFlashing",
    "WoodNymphs",
    "bitchinbubba",
    "casualnudity",
    "exposedinpublic",
    "girlsflashing",
    "gwpublic",
    "holdthemoan",
    "publicplug",
    "snowgirls",
]
PUSSY = [
    "AsianPussy",
    "FireCrotch",
    "GodPussy",
    "HairyPussy",
    "Innies",
    "LabiaGW",
    "LipsThatGrip",
    "MoundofVenus",
    "PerfectPussies",
    "PussyFlashing",
    "PussyMound",
    "grool",
    "legsup",
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
    "selfshots",
]
REDHEADS = [
    "FireCrotch",
    "FreckledRedheads",
    "RedheadGifs",
    "RedheadsPorn",
    "ginger",
    "nsfw_redhead",
    "redhead",
    "redheads",
]
RULE_34 = [
    "Overwatch_Porn",
    "Rule34LoL",
    "Rule34Overwatch",
    "Rule_34",
    "WesternHentai",
    "rule34",
    "rule34cartoons",
    "rule34_ass",
]
SQUIRTS = ["squirting", "squirting_gifs", "wetspot", "grool"]
THIGHS = [
    "ThickThighs",
    "Thigh",
    "datgap",
    "leggingsgonewild",
    "legs",
    "legsup",
    "theratio",
    "thighhighs",
]
THREESOME = [
    "AirTight",
    "RealThreesomes",
    "SpitRoasted",
    "Threesome",
    "Xsome",
    "amateur_threesomes",
    "groupsex",
    "gangbang",
    "blowbang",
]
TRANS = [
    "DeliciousTraps",
    "GoneWildTrans",
    "Shemale_Big_Cock",
    "Shemales",
    "ShemalesParadise",
    "Transex",
    "shemale_gifs",
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
    "GirlsWithBikes",
    "GoneWildSmiles",
    "LabiaGW",
    "LingerieGW",
    "MyCalvins",
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
    "librarygirls",
    "workgonewild",
]
YIFF = ["Hyiff", "Yiffbondage", "femyiff", "yiff", "yiffgif"]

# Other APIs
NEKOBOT_HENTAI = choice(["hentai_anal", "hentai"])
NEKOBOT_URL = "https://nekobot.xyz/api/image?type={}"
