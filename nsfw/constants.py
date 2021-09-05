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


REDDIT_BASEURL = "https://api.reddit.com/r/{}/random"
IMGUR_LINKS = ("http://imgur.com", "https://m.imgur.com", "https://imgur.com")
GOOD_EXTENSIONS = (".png", ".jpg", ".jpeg", ".gif")

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
    "BestBooties",
    "ButtsAndBareFeet",
    "GodBooty",
    "HighResASS",
    "HungryButts",
    "ILikeLittleButts",
    "Mooning",
    "SnakeButt",
    "TheUnderbun",
    "Underbun",
    "Upshorts",
    "ass",
    "asshole",
    "assinthong",
    "asstastic",
    "beautifulbutt",
    "bigasses",
    "booty",
    "brunetteass",
    "datass",
    "datgap",
    "girlsinleggings",
    "girlsinyogapants",
    "hugeass",
    "paag",
    "pawg",
    "onherstomach",
    "facedownassup",
]
ASIANPORN = [
    "AmateurAsianGirls",
    "AsianAmericanHotties",
    "AsianCuties",
    "AsianHotties",
    "AsianNSFW",
    "AsianPorn",
    "AsianPussy",
    "AsiansGoneWild",
    "KoreanHotties",
    "NSFW_Japan",
    "NSFW_Korea",
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
    "sodomy",
]
BBW = ["BBW", "BBWVideos", "BBW_Chubby", "GoneWildPlus", "PerkyChubby", "chubby", "gonewildcurvy"]
BDSM = ["BDSMGW", "BDSM_NoSpam", "Bondage", "Spanking", "bdsm", "ropeart"]
BLACKCOCK = ["Blackdick", "ChurchOfTheBBC", "bigblackcocks", "blackcock"]
BLOWJOB = [
    "AsianBlowjobs",
    "BlowjobEyeContact",
    "BlowjobGifs",
    "Blowjobs",
    "OralCreampie",
    "SuckingItDry",
    "SwordSwallowers",
    "blowjobsandwich",
    "fellatio",
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
    "cleavage",
    "fortyfivefiftyfive",
    "ghostnipples",
    "homegrowntits",
    "hugeboobs",
    "naturaltitties",
    "piercedtits",
    "pokies",
    "smallboobs",
    "tits",
]
BOTTOMLESS = ["Bottomless", "nopanties", "upskirt"]
COSPLAY = [
    "CosplayBeauties",
    "CosplayBoobs",
    "CosplayLewd",
    "Cosplayheels",
    "cosplayonoff",
    "gwcosplay",
    "nsfwcosplay",
]
CUNNI = ["CunnilingusSelfie", "Hegoesdown", "cunnilingus"]
CUMSHOTS = [
    "ContainTheLoad",
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
DICK = ["DickPics4Freedom", "MassiveCock", "ThickDick", "bulges", "cock", "penis", "twinks"]
DILF = ["dilf", "dilfs"]
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
FACIALS = ["FacialFun", "facial", "facialcumshots"]
FEET = [
    "ButtsAndBareFeet",
    "Feet_NSFW",
    "Feetup",
    "FootFetish",
    "feetish",
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
    "Singlets",
    "broslikeus",
    "bulges",
    "gaybears",
    "gaynsfw",
    "gayotters",
    "jockstraps",
    "ladybonersgw",
    "lovegaymale",
    "malepornstars",
    "manass",
    "manlove",
    "MaleUnderwear",
]
GROUPS = ["GroupOfNudeGirls", "groupsex"]
LESBIANS = [
    "Ass_to_ssA",
    "HDLesbianGifs",
    "Lesbian_gifs",
    "StraightGirlsPlaying",
    "amateurlesbians",
    "dyke",
    "girlskissing",
    "lesbians",
    "mmgirls",
    "scissoring",
    "titstouchingtits",
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
    "BlowjobEyeContact",
    "BlowjobGifs",
    "Blowjobs",
    "CunnilingusSelfie",
    "DeepThroatTears",
    "Hegoesdown",
    "OralCreampie",
    "SuckingItDry",
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
    "RealPublicNudity",
    "Unashamed",
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
    "GirlsWithToys",
    "GodPussy",
    "HairyPussy",
    "Innies",
    "LabiaGW",
    "LipsThatGrip",
    "MoundofVenus",
    "PerfectPussies",
    "PussyFlashing",
    "PussyMound",
    "TheRearPussy",
    "grool",
    "legsup",
    "peachlips",
    "pelfie",
    "pussy",
    "rearpussy",
    "simps",
    "spreadeagle",
    "ButterflyWings",
    "DangleAndJingle",
    "Outies",
    "DarkBitsNPieces",
]
REAL_GIRLS = ["CellShots", "ChangingRooms", "Nude_Selfie", "RealGirls", "selfpix", "selfshots"]
REDHEADS = [
    "FireBush",
    "FireCrotch",
    "FreckledRedheads",
    "RedheadGifs",
    "RedheadsPorn",
    "ginger",
    "nsfw_redhead",
    "redhead",
    "redheads",
    "redheadxxx",
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
SQUIRTS = ["GushingGirls", "squirting", "squirting_gifs", "wetspot", "grool"]
THIGHS = [
    "ThickThighs",
    "Thigh",
    "Thighs",
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
    "Triplepenetration",
    "Xsome",
    "amateur_threesomes",
    "groupsex",
    "gangbang",
    "blowbang",
]
TRANS = [
    "DeliciousTraps",
    "GoneWildTrans",
    "SexyShemales",
    "ShemaleGalleries",
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
