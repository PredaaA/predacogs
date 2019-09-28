from random import choice

# Stuff for the cog
class Stuff:
    async def emoji(self):
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
IMGUR_LINKS = "http://imgur.com", "https://m.imgur.com", "https://imgur.com"
GOOD_EXTENSIONS = ".png", ".jpg", ".jpeg", ".gif"

# Subreddits
FOUR_K = ["HighResNSFW", "UHDnsfw", "nsfw4k", "nsfw_hd", "NSFW_Wallpapers", "HDnsfw", "closeup"]
AHEGAO = ["AhegaoGirls", "RealAhegao", "EyeRollOrgasm", "MouthWideOpen", "O_Faces"]
ASS = [
    "ass",
    "pawg",
    "AssholeBehindThong",
    "girlsinyogapants",
    "girlsinleggings",
    "bigasses",
    "asshole",
    "AssOnTheGlass",
    "TheUnderbun",
    "asstastic",
    "booty",
    "AssReveal",
    "beautifulbutt",
    "Mooning",
    "BestBooties",
    "brunetteass",
    "assinthong",
    "paag",
    "asstastic",
    "GodBooty",
    "Underbun",
    "datass",
    "ILikeLittleButts",
    "datgap",
    "HungryButts",
    "Upshorts",
]
ANAL = [
    "MasterOfAnal",
    "anal",
    "buttsex",
    "buttsthatgrip",
    "AnalGW",
    "analinsertions",
    "assholegonewild",
    "sodomy",
]
BDSM = ["BDSMGW", "bdsm", "ropeart", "shibari"]
BLACKCOCK = ["ChurchOfTheBBC", "blackcock", "Blackdick", "bigblackcocks"]
BLOWJOB = [
    "blowjobsandwich",
    "Blowjobs",
    "BlowjobGifs",
    "BlowjobEyeContact",
    "blowbang",
    "AsianBlowjobs",
    "SuckingItDry",
    "OralCreampie",
    "SwordSwallowers",
    "fellatio",
]
BOOBS = [
    "boobs",
    "TheHangingBoobs",
    "bigboobs",
    "BigBoobsGW",
    "hugeboobs",
    "pokies",
    "ghostnipples",
    "PiercedNSFW",
    "piercedtits",
    "PerfectTits",
    "BestTits",
    "Boobies",
    "JustOneBoob",
    "tits",
    "naturaltitties",
    "smallboobs",
    "Nipples",
    "homegrowntits",
    "TheUnderboob",
    "BiggerThanYouThought",
    "fortyfivefiftyfive",
    "Stacked",
    "BigBoobsGonewild",
    "AreolasGW",
    "TittyDrop",
    "Titties",
    "Boobies",
    "boobbounce",
    "TinyTits",
    "cleavage",
    "BoobsBetweenArms",
    "BustyNaturals",
    "burstingout",
    "boobgifs",
]
BOTTOMLESS = ["upskirt", "Bottomless", "Bottomless_Vixens", "nopanties", "Pantiesdown"]
COSPLAY = [
    "nsfwcosplay",
    "cosplayonoff",
    "Cosplayheels",
    "CosplayBoobs",
    "gwcosplay",
    "CosplayLewd",
    "CosplayBeauties",
]
CUNNI = ["cunnilingus", "eatpussy2015", "CunnilingusSelfie", "Hegoesdown"]
CUMSHOTS = [
    "cumfetish",
    "cumontongue",
    "cumshots",
    "CumshotSelfies",
    "facialcumshots",
    "pulsatingcumshots",
    "gwcumsluts",
    "ImpresssedByCum",
    "GirlsFinishingTheJob",
    "amateurcumsluts",
    "unexpectedcum",
    "bodyshots",
    "ContainTheLoad",
    "bodyshots",
]
DEEPTHROAT = [
    "deepthroat_gifs",
    "AmateurDeepthroat",
    "DeepThroatTears",
    "deepthroat",
    "SwordSwallowers",
]
DICK = ["DickPics4Freedom", "MassiveCock", "penis", "cock", "ThickDick", "bulges", "twinks"]
DOUBLE_P = ["doublepenetration", "dp_porn", "Technical_DP"]
FACIALS = ["facial", "EthnicGirlFacials", "facialcumshots", "FacialFun"]
FEET = ["ButtsAndBareFeet", "Feet_NSFW", "feetish", "Feetup", "rule34feet", "StomachDownFeetUp"]
FEMDOM = ["Femdom", "femdom", "FemdomHumiliation", "hentaifemdom"]
FUTA = [
    "FutanariHentai",
    "FutanariPegging",
    "HorsecockFuta",
    "Rule34_Futanari",
    "rule34futanari",
    "hugefutanari",
    "Futadomworld",
]
GAY_P = ["gayporn", "ladybonersgw", "bulges", "broslikeus", "gaygifs", "gayporn"]
GROUPS = ["GroupOfNudeGirls", "GroupOfNudeMILFs", "groupsex"]
# HENTAI = ["hentai", "thick_hentai", "HQHentai", "AnimeBooty", "thighdeology"]
# HENTAI_GIFS = ["ecchigifs", "nsfwanimegifs", "oppai_gif"]
LESBIANS = ["lesbians", "HDLesbianGifs", "amateurlesbians", "Lesbian_gifs"]
MILF = [
    "amateur_milfs",
    "GroupOfNudeMILFs",
    "ChocolateMilf",
    "milf",
    "Milfie",
    "hairymilfs",
    "HotAsianMilfs",
    "HotMILFs",
    "MILFs",
    "maturemilf",
    "puremilf",
    "amateur_milfs",
]
ORAL = [
    "blowjobsandwich",
    "Blowjobs",
    "BlowjobGifs",
    "BlowjobEyeContact",
    "blowbang",
    "AsianBlowjobs",
    "SuckingItDry",
    "OralCreampie",
    "cunnilingus",
    "eatpussy2015",
    "CunnilingusSelfie",
    "Hegoesdown",
    "DeepThroatTears",
    "deepthroat",
    "ballsucking",
    "SwordSwallowers",
]
PUBLIC = [
    "RealPublicNudity",
    "FlashingAndFlaunting",
    "FlashingGirls",
    "PublicFlashing",
    "Unashamed",
    "OutsideNude",
    "NudeInPublic",
    "publicplug",
    "casualnudity",
    "bitchinbubba",
    "FlashingTheGoods",
    "Flashing",
    "girlsflashing",
    "holdthemoan",
    "exposedinpublic",
]
PUSSY = [
    "pussy",
    "GodPussy",
    "AsianPussy",
    "rearpussy",
    "PussyFlashing",
    "Innies",
    "pelfie",
    "GirlsWithToys",
    "simps",
    "LabiaGW",
    "grool",
    "MoundofVenus",
]
REAL_GIRLS = ["RealGirls", "RealGirlsGoneWild", "Nude_Selfie"]
REDHEADS = [
    "redheadxxx",
    "redheads",
    "ginger",
    "FireBush",
    "FreckledRedheads",
    "redhead",
    "thesluttyginger",
    "RedheadGifs",
]
RULE_34 = [
    "rule34",
    "rule34cartoons",
    "Rule_34",
    "Rule34LoL",
    "AvatarPorn",
    "Overwatch_Porn",
    "Rule34Overwatch",
    "WesternHentai",
]
SQUIRTS = ["SquatSquirt", "GushingGirls", "squirting_gifs", "squirting"]
THIGHS = ["Thighs", "ThickThighs", "thighhighs", "Thigh", "leggingsgonewild", "legsup"]
TRAPS = [
    "Transex",
    "DeliciousTraps",
    "traps",
    "trapgifs",
    "GoneWildTrans",
    "SexyShemales",
    "Shemales",
    "shemale_gifs",
    "Shemales",
    "ShemalesParadise",
    "Shemale_Big_Cock",
    "ShemaleGalleries",
]
WILD = [
    "gonewild",
    "GWNerdy",
    "dirtysmall",
    "MyCalvins",
    "AsiansGoneWild",
    "GoneWildSmiles",
    "gonewildcurvy",
    "BigBoobsGonewild",
    "gonewildcouples",
    "gonewildcolor",
    "PetiteGoneWild",
    "GWCouples",
    "BigBoobsGW",
    "altgonewild",
    "LabiaGW",
    "UnderwearGW",
    "JustTheTop",
    "TallGoneWild",
    "LingerieGW",
    "Swingersgw",
    "workgonewild",
]
YIFF = ["Yiffbondage", "Hyiff", "femyiff", "yiff", "yiffgif"]

# Other APIs
NEKOBOT_HENTAI = choice(["hentai_anal", "hentai"])
NEKOBOT_URL = "https://nekobot.xyz/api/image?type={}"

NEKOS_LIFE_HOLO = choice(["holoero", "holo", "hololewd"])
NEKOS_LIFE_URL = "https://nekos.life/api/v2/img/{}"
