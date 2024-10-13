#!/usr/bin/env python3
# ruff: noqa: S311

import subprocess
from functools import cache
from pathlib import Path
from random import Random

UNIQUE_ITEM_NAMES = [
    "%Cu+ie^_^ki||er",
    "/He4rtf;ull Spl0Dge..r",
    "12 Pounder",
    "1340 Shield",
    "3DD1.E",
    "88 Fragnum",
    "Absolute Zero",
    "Ack Ack",
    "Actualizer",
    "Aequitas",
    "Ahab",
    "Amigo Sincero",
    "Antagonist",
    "Antifection",
    "Asteroid Belt",
    "Avalanche",
    "Avenger",
    "Baby Boomer",
    "Baby Maker",
    "Bad Touch",
    "Badaboom",
    "Bane",
    "Bearcat",
    "Bekah",
    "Berrigan",
    "Big Boom Blaster",
    "Bigg Thumppr",
    "Bitch",
    "Black Hole",
    "Black Snake",
    "Blockade",
    "Blockhead",
    "Blood of Terramorphous",
    "Blood of the Ancients",
    "Blood of the Seraphs",
    "Blowfly",
    "Boganella",
    "Bone Shredder",
    "Bone of the Ancients",
    "Bonus Package",
    "Boom Puppy",
    "Boomacorn",
    "Boss Nova",
    "Bouncing Bazza",
    "Bouncing Bonny",
    "Boxxy Gunn",
    "Breath of Terramorphous",
    "Breath of the Seraphs",
    "Buffalo",
    "Bullpup",
    "Bunny",
    "Butcher",
    "CHOPPER",
    "Carnage",
    "Cat o' Nine Tails",
    "Cathartic Oz Kit",
    "Celestial Baroness",
    "Celestial Doppelganger",
    "Celestial Enforcer",
    "Celestial Fragtrap",
    "Celestial Gladiator",
    "Celestial Lawbringer",
    "Chain Lightning",
    "Cheat Code",
    "Chronicler Of Elpis",
    "Chulainn",
    "Chère-amie",
    "Cobra",
    "Commerce",
    "Company Man",
    "Conference Call",
    "Contraband Sky Rocket",
    "Cracked Sash",
    "Creamer",
    "Crit",
    "Crossfire",
    "Cry Baby",
    "Cryophobia",
    "Cyber Eagle",
    "Dahlminator",
    "Damned Cowboy",
    "Data Scrubber",
    "Deadly Bloom",
    "Deliverance",
    "Deputy's Badge",
    "Devastator",
    "Dog",
    "E-GUN",
    "Easy Mode",
    "Elephant Gun",
    "Emperor",
    "Eridian Vanquisher",
    "Evil Smasher",
    "Evolution",
    "Excalibastard",
    "Fabled Tortoise",
    "Fast Talker",
    "Fastball",
    "Fatale",
    "Fibber",
    "Fire Bee",
    "Fire Storm",
    "Fireball",
    "Firestarta",
    "Flakker",
    "Flame of the Firehawk",
    "Flayer",
    "Florentine",
    "Four Seasons",
    "Freedom Oz Kit",
    "Fremington's Edge",
    "Fridgia",
    "Frostfire",
    "Fusillade",
    "Fuster Cluck",
    "Globber",
    "Godfinger",
    "Good Touch",
    "Greed",
    "Grog Nozzle",
    "Gub",
    "Gunerang",
    "Gwen's Head",
    "Gwen's Other Head",
    "Hail",
    "Hammer Buster",
    "Hammer Buster II",
    "Hard Carry",
    "Hard Reboot",
    "Hawk Eye",
    "Haymaker",
    "Heart Breaker",
    "Heart of the Ancients",
    "Hector's Paradise",
    "Hellfire",
    "Hide of Terramorphous",
    "Hive",
    "Hoplite",
    "Hornet",
    "Hot Mama",
    "Hydra",
    "IVF",
    "Ice Scream",
    "Impaler",
    "Infection",
    "Infection Cleaner",
    "Infinity",
    "Interfacer",
    "Invader",
    "Invigoration Oz Kit",
    "Jack-o'-Cannon",
    "Jolly Roger",
    "Judge",
    "Kala",
    "Kaneda's Laser",
    "KerBlaster",
    "KerBoom",
    "Kiss of Death",
    "Kitten",
    "Lady Fist",
    "Landscaper",
    "Lascaux",
    "Laser Disker",
    "Law",
    "Lazlo's Freezeasy",
    "Lead Storm",
    "Leech",
    "Legendary Anarchist",
    "Legendary Berserker",
    "Legendary Binder",
    "Legendary Cat",
    "Legendary Catalyst",
    "Legendary Engineer",
    "Legendary Gunzerker",
    "Legendary Hoarder",
    "Legendary Hunter",
    "Legendary Killer",
    "Legendary Mechromancer",
    "Legendary Ninja",
    "Legendary Nurse",
    "Legendary Pointman",
    "Legendary Psycho",
    "Legendary Ranger",
    "Legendary Reaper",
    "Legendary Roboteer",
    "Legendary Sickle",
    "Legendary Siren",
    "Legendary Sniper",
    "Legendary Soldier",
    "Legendary Titan",
    "Legendary Torch",
    "Lightning Bolt",
    "Little Evie",
    "Logan's Gun",
    "Longbow",
    "Longest Yard",
    "Longnail",
    "Love Thumper",
    "Luck Cannon",
    "Lucrative Opportunity",
    "Lyuda",
    "M0RQ",
    "M2828 Thumpson",
    "MINAC's Atonement",
    "Madhous!",
    "Maggie",
    "Magic Missile",
    "Magma",
    "Major Tom",
    "Manly Man Shield",
    "Marek's Mouth",
    "Meat Grinder",
    "Meganade",
    "Meteor Shower",
    "Midnight Star",
    "Might of the Seraphs",
    "Min Min Lighter",
    "Mining Laser",
    "Mongol",
    "Monster Trap",
    "Moonface",
    "Moonlight Saga",
    "Moonscaper",
    "Morningstar",
    "Mouthwash",
    "Moxxi's Endowment",
    "Mysterious Amulet",
    "Nasty Surprise",
    "Naught",
    "Neogenator",
    "Nirvana",
    "Norfleet",
    "Nukem",
    "O-Negative",
    "Octo",
    "Ogre",
    "Ol' Painful",
    "Ol' Rosie",
    "Omen",
    "Omni-Cannon",
    "Orc",
    "Order",
    "Orphan Maker",
    "Otto Idol",
    "Overcompensator",
    "Oxidizer",
    "Pandemic",
    "Party Line",
    "Party Popper",
    "Patriot",
    "Peak Opener",
    "Pimpernel",
    "Pitchfork",
    "Plunkett",
    "Pocket Rocket",
    "Pot O' Gold",
    "Prismatic Bulwark",
    "Probe",
    "Proletarian Revolution",
    "Pun-chee",
    "Pyrophobia",
    "Quasar",
    "Rapid Release",
    "Rapier",
    "Razorback",
    "Reogenator",
    "Rerouter",
    "Retainer",
    "Retcher",
    "Rex",
    "Roaster",
    "RokSalt",
    "Rolling Thunder",
    "Rubi",
    "SWORDSPLOSION",
    "Sand Hawk",
    "Sawbar",
    "Scorpio",
    "Seeker",
    "Seraphim",
    "Shadow of the Seraphs",
    "Sheriff's Badge",
    "Shield of Ages",
    "Shooterang",
    "Shotgun 1340",
    "Shredifier",
    "Skin of the Ancients",
    "Skullmasher",
    "Slagga",
    "Slammer",
    "Slayer Of Terramorphous",
    # This is actually in vanilla, Kreig's COM is lowercase, deliberately ignoring it for clarity
    # "Slayer of Terramorphous",
    "Sledge's Shotgun",
    "Sledge's Shotty",
    "Sloth",
    "Slow Hand",
    "Smasher",
    "Snowball",
    "Sponge",
    "Stalker",
    "Stinger",
    "Stinkpot",
    "Stomper",
    "Storm",
    "Storm Front",
    "Striker",
    "Sunshine",
    "Supernova",
    "Support Relay",
    "Systems Purge",
    "T4s-R",
    "Tannis' Laser of Enlightenment",
    "Tattler",
    "Teapot",
    "Teeth of Terramorphous",
    "The Afterburner",
    "The Bee",
    "The Cradle",
    "The Electric Chair",
    "The Machine",
    "The Rough Rider",
    "The Sham",
    "The Shooting Star",
    "The Transformer",
    "The ZX-1",
    "Thingy",
    "Thunderball Fists",
    "Thunderfire",
    "Tidal Wave",
    "Tinderbox",
    "Toby's Bright Spadroon",
    "Too Scoops",
    "Toothpick",
    "Torguemada",
    "Torrent",
    "Trespasser",
    "Triquetra",
    "Tunguska",
    "Twister",
    "Unforgiven",
    "Unicornsplosion",
    "Unkempt Harold",
    "Vandergraffen",
    "Vault Hunter's Relic",
    "Veritas",
    "Veruc",
    "Vibra-Pulse",
    "Viral Marketer",
    "Volcano",
    "Volt Thrower",
    "Wallop",
    "Wanderlust",
    "Wet Week",
    "Whisky Tango Foxtrot",
    "Winter is Over",
    "Wombat",
    "World Burn",
    "Yellow Jacket",
    "Zappinator",
    "Zim",
]

PREVIOUS_RELEASE_NAMES = []


@cache
def get_git_commit_hash(identifier: str | None = None) -> str:
    """
    Gets the full commit hash of the current git repo.

    Args:
        identifier: The identifier of the commit to get, or None to get the latest.
    Returns:
        The commit hash.
    """
    args = ["git", "show", "-s", "--format=%H"]
    if identifier is not None:
        args.append(identifier)

    return subprocess.run(
        args,
        cwd=Path(__file__).parent,
        check=True,
        stdout=subprocess.PIPE,
        encoding="utf8",
    ).stdout.strip()


def pick_release_name(commit_hash: str, excludes: list[str] = PREVIOUS_RELEASE_NAMES) -> str:
    """
    Picks the name to use for a release.

    Args:
        commit_hash: The commit hash to pick the name of.
        excludes: The list of names to exclude.
    Returns:
        The release name.
    """
    # Think it's better to rely on an int than the string's hash method
    rng = Random(int(commit_hash, 16))
    while (name := rng.choice(UNIQUE_ITEM_NAMES)) in excludes:
        pass
    return name


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Picks the friendly name to use for the current release.",
    )
    parser.add_argument(
        "hash",
        nargs="?",
        default=None,
        help="The commit hash to base the name off of. If not given, retrieves from git.",
    )
    parser.add_argument(
        "--exclude",
        metavar="NAME",
        action="append",
        default=[],
        help="Excludes a name as if it were used in a previous release.",
    )
    parser.add_argument(
        "--ignore-previous-releases",
        action="store_true",
        help="Ignores all names which have been used in previous releases.",
    )
    args = parser.parse_args()

    commit_hash = get_git_commit_hash(args.hash)

    excludes = [] if args.ignore_previous_releases else PREVIOUS_RELEASE_NAMES
    excludes += args.exclude

    print(pick_release_name(commit_hash, excludes))